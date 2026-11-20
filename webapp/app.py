#!/usr/bin/env python3
"""Flask backend + SQLite for the Personal Music Experience web dashboard.

The companion dashboard gives the Chrome extension's saved songs and preferences
a responsive web home, and records usage data for Stage 5 testing.

Run:
    python3 webapp/app.py
Then open http://127.0.0.1:5000
"""

from __future__ import annotations

import csv
import json
import sqlite3
import time
import uuid
from pathlib import Path

from flask import (Flask, g, jsonify, render_template, request, redirect,
                   url_for, send_from_directory)

from recommendations import LEVELS, VIBE_TAGS, get_recommendations, get_vibe_recommendations

BASE = Path(__file__).resolve().parent
ROOT = BASE.parent
DB_PATH = BASE / "pme.db"
SURVEY_CSV = ROOT / "data" / "survey_responses_anonymised.csv"

app = Flask(__name__)
app.config["SECRET_KEY"] = "design-thinking-prototype-only"


# --------------------------------------------------------------------------- #
# Database
# --------------------------------------------------------------------------- #
def get_db() -> sqlite3.Connection:
    if "db" not in g:
        g.db = sqlite3.connect(DB_PATH)
        g.db.row_factory = sqlite3.Row
        g.db.execute("PRAGMA foreign_keys = ON")
    return g.db


@app.teardown_appcontext
def close_db(_exc=None) -> None:
    db = g.pop("db", None)
    if db is not None:
        db.close()


def init_db() -> None:
    with sqlite3.connect(DB_PATH) as db:
        db.executescript(
            """
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id TEXT UNIQUE NOT NULL,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            );
            CREATE TABLE IF NOT EXISTS saved_songs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                title TEXT NOT NULL,
                artist TEXT NOT NULL,
                genre TEXT,
                reason TEXT,
                source TEXT,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                UNIQUE(user_id, title, artist),
                FOREIGN KEY(user_id) REFERENCES users(id)
            );
            CREATE TABLE IF NOT EXISTS preferences (
                user_id INTEGER PRIMARY KEY,
                discovery_level TEXT DEFAULT 'balanced',
                preferred_vibe TEXT DEFAULT 'chill',
                tracking_enabled INTEGER DEFAULT 1,
                updated_at TEXT DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY(user_id) REFERENCES users(id)
            );
            CREATE TABLE IF NOT EXISTS usage_events (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                session_id TEXT,
                event_type TEXT NOT NULL,
                detail TEXT,
                duration_ms INTEGER,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY(user_id) REFERENCES users(id)
            );
            CREATE TABLE IF NOT EXISTS test_tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                task_name TEXT NOT NULL,
                started_at TEXT,
                ended_at TEXT,
                duration_ms INTEGER,
                clicks INTEGER DEFAULT 0,
                errors INTEGER DEFAULT 0,
                completed INTEGER DEFAULT 0,
                FOREIGN KEY(user_id) REFERENCES users(id)
            );
            CREATE INDEX IF NOT EXISTS idx_events_user ON usage_events(user_id);
            CREATE INDEX IF NOT EXISTS idx_saved_user ON saved_songs(user_id);
            """
        )


def current_user() -> sqlite3.Row:
    """Identify the browser via a cookie, creating a user row on first visit."""
    db = get_db()
    sid = request.cookies.get("pme_session")
    if sid:
        row = db.execute("SELECT * FROM users WHERE session_id = ?", (sid,)).fetchone()
        if row:
            return row
    sid = uuid.uuid4().hex
    db.execute("INSERT INTO users (session_id) VALUES (?)", (sid,))
    db.commit()
    g.new_session = sid
    return db.execute("SELECT * FROM users WHERE session_id = ?", (sid,)).fetchone()


@app.after_request
def set_session_cookie(response):
    sid = getattr(g, "new_session", None)
    if sid:
        response.set_cookie("pme_session", sid, max_age=60 * 60 * 24 * 30,
                            httponly=True, samesite="Lax")
    return response


def log_event(event_type: str, detail: str = "", duration_ms: int | None = None) -> None:
    user = current_user()
    get_db().execute(
        "INSERT INTO usage_events (user_id, session_id, event_type, detail, duration_ms) VALUES (?,?,?,?,?)",
        (user["id"], request.cookies.get("pme_session"), event_type, detail, duration_ms),
    )
    get_db().commit()


def get_preferences(user_id: int) -> dict:
    db = get_db()
    row = db.execute("SELECT * FROM preferences WHERE user_id = ?", (user_id,)).fetchone()
    if not row:
        db.execute("INSERT INTO preferences (user_id) VALUES (?)", (user_id,))
        db.commit()
        row = db.execute("SELECT * FROM preferences WHERE user_id = ?", (user_id,)).fetchone()
    return dict(row)


# --------------------------------------------------------------------------- #
# Context helpers
# --------------------------------------------------------------------------- #
@app.context_processor
def inject_common():
    return {"levels": LEVELS, "vibe_tags": VIBE_TAGS, "current_year": 2026}


# --------------------------------------------------------------------------- #
# Pages
# --------------------------------------------------------------------------- #
@app.route("/")
def index():
    user = current_user()
    db = get_db()
    saved = db.execute(
        "SELECT * FROM saved_songs WHERE user_id = ? ORDER BY created_at DESC", (user["id"],)
    ).fetchall()
    prefs = get_preferences(user["id"])
    stats = {
        "saved": len(saved),
        "events": db.execute("SELECT COUNT(*) FROM usage_events WHERE user_id = ?", (user["id"],)).fetchone()[0],
        "platforms": db.execute("SELECT COUNT(DISTINCT source) FROM saved_songs WHERE user_id = ?", (user["id"],)).fetchone()[0],
    }
    return render_template("index.html", saved=saved, prefs=prefs, stats=stats, active="home")


@app.route("/discover")
def discover():
    user = current_user()
    prefs = get_preferences(user["id"])
    level = request.args.get("level", prefs["discovery_level"])
    artist = request.args.get("artist", "")
    platform = request.args.get("platform", "Spotify")
    items = get_recommendations(platform, level, artist)
    saved_ids = {r["title"] for r in get_db().execute(
        "SELECT title FROM saved_songs WHERE user_id = ?", (user["id"],))}
    log_event("discover_view", f"platform={platform}; level={level}; artist={artist}")
    return render_template("discover.html", items=items, level=level, platform=platform,
                           artist=artist, saved_titles=saved_ids, active="discover")


@app.route("/vibe")
def vibe():
    user = current_user()
    prefs = get_preferences(user["id"])
    selected = request.args.get("vibe", "").lower()
    platform = request.args.get("platform", "Spotify")
    items = get_vibe_recommendations(platform, selected) if selected else []
    saved_ids = {r["title"] for r in get_db().execute(
        "SELECT title FROM saved_songs WHERE user_id = ?", (user["id"],))}
    if selected:
        log_event("vibe_view", f"platform={platform}; vibe={selected}")
    return render_template("vibe.html", items=items, selected=selected, platform=platform,
                           saved_titles=saved_ids, active="vibe")


@app.route("/preferences", methods=["GET", "POST"])
def preferences():
    user = current_user()
    db = get_db()
    if request.method == "POST":
        level = request.form.get("level", "balanced")
        vibe = request.form.get("vibe", "chill")
        tracking = 1 if request.form.get("tracking") else 0
        if level not in LEVELS:
            level = "balanced"
        if vibe not in VIBE_TAGS:
            vibe = "chill"
        db.execute(
            """INSERT INTO preferences (user_id, discovery_level, preferred_vibe, tracking_enabled, updated_at)
               VALUES (?,?,?,?,CURRENT_TIMESTAMP)
               ON CONFLICT(user_id) DO UPDATE SET
                 discovery_level=excluded.discovery_level,
                 preferred_vibe=excluded.preferred_vibe,
                 tracking_enabled=excluded.tracking_enabled,
                 updated_at=CURRENT_TIMESTAMP""",
            (user["id"], level, vibe, tracking),
        )
        db.commit()
        log_event("preferences_saved", f"level={level}; vibe={vibe}; tracking={tracking}")
        return redirect(url_for("preferences", saved=1))
    prefs = get_preferences(user["id"])
    return render_template("preferences.html", prefs=prefs, active="preferences",
                           saved=request.args.get("saved"))


@app.route("/study")
def study():
    """Stage 5: short timed tasks that log clicks, errors, completion and duration."""
    user = current_user()
    tasks = get_db().execute(
        "SELECT * FROM test_tasks WHERE user_id = ? ORDER BY id DESC LIMIT 10", (user["id"],)
    ).fetchall()
    return render_template("study.html", tasks=tasks, active="study")


@app.route("/results")
def results():
    """Survey findings and charts for the presentation."""
    user = current_user()
    rows = []
    if SURVEY_CSV.exists():
        with SURVEY_CSV.open(encoding="utf-8-sig", newline="") as f:
            rows = list(csv.DictReader(f))
    return render_template("results.html", rows=rows, active="results")


# --------------------------------------------------------------------------- #
# API
# --------------------------------------------------------------------------- #
@app.route("/api/save", methods=["POST"])
def api_save():
    user = current_user()
    data = request.get_json(force=True) or {}
    title = str(data.get("title", "")).strip()
    artist = str(data.get("artist", "")).strip()
    if not title or not artist:
        return jsonify({"ok": False, "error": "title and artist required"}), 400
    db = get_db()
    try:
        db.execute(
            """INSERT OR IGNORE INTO saved_songs
               (user_id, title, artist, genre, reason, source) VALUES (?,?,?,?,?,?)""",
            (user["id"], title, artist, data.get("genre", ""), data.get("reason", ""),
             data.get("source", "web")),
        )
        db.commit()
    except sqlite3.Error as exc:
        app.logger.error("Save failed: %s", exc)
        return jsonify({"ok": False, "error": "database error"}), 500
    log_event("save_song", f"{title} - {artist}")
    return jsonify({"ok": True})


@app.route("/api/unsave/<int:song_id>", methods=["POST"])
def api_unsave(song_id: int):
    user = current_user()
    db = get_db()
    cur = db.execute("DELETE FROM saved_songs WHERE id = ? AND user_id = ?", (song_id, user["id"]))
    db.commit()
    log_event("unsave_song", str(song_id))
    return jsonify({"ok": cur.rowcount > 0})


@app.route("/api/event", methods=["POST"])
def api_event():
    data = request.get_json(force=True) or {}
    event_type = str(data.get("type", "interaction"))[:80]
    log_event(event_type, str(data.get("detail", ""))[:200], data.get("duration_ms"))
    return jsonify({"ok": True})


@app.route("/api/task", methods=["POST"])
def api_task():
    """Record a completed Stage 5 task."""
    user = current_user()
    data = request.get_json(force=True) or {}
    db = get_db()
    db.execute(
        """INSERT INTO test_tasks
           (user_id, task_name, started_at, ended_at, duration_ms, clicks, errors, completed)
           VALUES (?,?,?,?,?,?,?,?)""",
        (user["id"], str(data.get("task", "untitled"))[:80], data.get("started_at"),
         data.get("ended_at"), int(data.get("duration_ms", 0)),
         int(data.get("clicks", 0)), int(data.get("errors", 0)),
         1 if data.get("completed") else 0),
    )
    db.commit()
    return jsonify({"ok": True})


@app.route("/api/summary")
def api_summary():
    db = get_db()
    return jsonify({
        "users": db.execute("SELECT COUNT(*) FROM users").fetchone()[0],
        "saved_songs": db.execute("SELECT COUNT(*) FROM saved_songs").fetchone()[0],
        "events": db.execute("SELECT COUNT(*) FROM usage_events").fetchone()[0],
        "tasks": db.execute("SELECT COUNT(*) FROM test_tasks").fetchone()[0],
        "task_rows": [dict(r) for r in db.execute("SELECT * FROM test_tasks")],
    })


@app.route("/charts/<path:filename>")
def charts(filename: str):
    """Serve analysis PNGs from data/charts."""
    return send_from_directory(ROOT / "data" / "charts", filename)


@app.route("/health")
def health():
    return jsonify({
        "status": "ok",
        "db": str(DB_PATH),
        "survey_csv": "present" if SURVEY_CSV.exists() else "missing",
    })


if __name__ == "__main__":
    init_db()
    app.run(debug=True, host="127.0.0.1", port=5000)
