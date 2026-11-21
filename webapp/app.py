#!/usr/bin/env python3
"""Flask backend + SQLite for the Personal Music Experience web dashboard.

HOW THE WEBSITE WORKS (the whole story in five lines):
  1. You type a URL, e.g. /discover.
  2. Flask matches it to a function below with the same @app.route(...) label.
  3. That function reads or writes the SQLite database (pme.db).
  4. It hands the results to a template in templates/, which becomes HTML.
  5. The browser displays that HTML; static/app.js adds the clickable behaviour.

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
# One database connection per request. Flask's "g" is a safe place to keep it.
def get_db() -> sqlite3.Connection:
    if "db" not in g:
        g.db = sqlite3.connect(DB_PATH)
        g.db.row_factory = sqlite3.Row
        g.db.execute("PRAGMA foreign_keys = ON")
    return g.db


# Close that connection when the request is finished.
@app.teardown_appcontext
def close_db(_exc=None) -> None:
    db = g.pop("db", None)
    if db is not None:
        db.close()


# Run once at startup: create the five tables if they do not exist yet.
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


# Identify the browser with a cookie, creating a user row on the first visit.
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


# Give the browser its cookie back with the very first response.
@app.after_request
def set_session_cookie(response):
    sid = getattr(g, "new_session", None)
    if sid:
        response.set_cookie("pme_session", sid, max_age=60 * 60 * 24 * 30,
                            httponly=True, samesite="Lax")
    return response


# Write one row into usage_events — this is the built-in measurement.
def log_event(event_type: str, detail: str = "", duration_ms: int | None = None) -> None:
    user = current_user()
    get_db().execute(
        "INSERT INTO usage_events (user_id, session_id, event_type, detail, duration_ms) VALUES (?,?,?,?,?)",
        (user["id"], request.cookies.get("pme_session"), event_type, detail, duration_ms),
    )
    get_db().commit()


# Every new user gets a preferences row, with defaults, on first use.
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
# Make these values available in every template, so we never repeat them.
@app.context_processor
def inject_common():
    return {"levels": LEVELS, "vibe_tags": VIBE_TAGS, "current_year": 2026}


# --------------------------------------------------------------------------- #
# Findings page helper
# --------------------------------------------------------------------------- #
def survey_summary(rows: list[dict]) -> dict:
    """Count a few headline percentages from the anonymised CSV.

    It is ordinary arithmetic: (rows that match / all rows) x 100. The full
    statistical work lives in analysis.py; this only powers the top of the
    Findings page, so the numbers can never drift away from the survey.
    """
    total = len(rows)
    if total == 0:
        return {"total": 0, "spotify": 0, "save": 0, "difficulty": 0, "taste": 0, "ads": 0}

    def percent(count: int) -> int:
        return round(100 * count / total)

    platform_col = "Which music-streaming platform do you use most often?"
    saving_col = "When you find a song you like, what do you usually do with it?"
    retrieval_col = "How easy is it to find songs you saved a long time ago?"
    taste_col = "How well does your music app understand your taste?"
    open_cols = [
        "What is the biggest problem you face while using your music-streaming app?",
        "What do you wish your music app could do better?",
        "If you could change one thing about your music-streaming experience, what would it be?",
    ]
    # Same keywords as THEMES["Ads / paywall"] in analysis.py, so both agree.
    ad_words = ("ad", "premium", "subscribe", "free music", "ad free", "advertisement")

    spotify = save = difficulty = unclear_taste = ads = 0
    for row in rows:
        if row[platform_col] == "Spotify":
            spotify += 1
        if row[saving_col] in ("Add it to a playlist", "Save/Like it"):
            save += 1
        if row[retrieval_col] == "Sometimes difficult":
            difficulty += 1
        if row[taste_col] in ("Somewhat", "Poorly"):
            unclear_taste += 1
        written = " ".join(row[col].lower() for col in open_cols)
        if any(word in written for word in ad_words):
            ads += 1

    return {
        "total": total,
        "spotify": percent(spotify),
        "save": percent(save),
        "difficulty": percent(difficulty),
        "taste": percent(unclear_taste),
        "ads": percent(ads),
    }


# --------------------------------------------------------------------------- #
# Pages
# --------------------------------------------------------------------------- #
# Page 1 — My Music: list saved songs and show three counts.
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


# Page 2 — Discover: picks chosen by platform + familiarity level.
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


# Page 3 — Find by Vibe: picks chosen by mood.
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


# Page 4 — Preferences: GET shows the form, POST saves it.
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
        # Save in two plain steps: first try to UPDATE the existing row.
        # If that changed nothing, INSERT a new one. This is called an "upsert".
        changed = db.execute(
            """UPDATE preferences
               SET discovery_level=?, preferred_vibe=?, tracking_enabled=?,
                   updated_at=CURRENT_TIMESTAMP
               WHERE user_id=?""",
            (level, vibe, tracking, user["id"]),
        ).rowcount
        if changed == 0:
            db.execute(
                """INSERT INTO preferences
                   (user_id, discovery_level, preferred_vibe, tracking_enabled)
                   VALUES (?,?,?,?)""",
                (user["id"], level, vibe, tracking),
            )
        db.commit()
        log_event("preferences_saved", f"level={level}; vibe={vibe}; tracking={tracking}")
        return redirect(url_for("preferences", saved=1))
    prefs = get_preferences(user["id"])
    return render_template("preferences.html", prefs=prefs, active="preferences",
                           saved=request.args.get("saved"))


# Page 5 — Study: past tasks and the 10-item SUS form.
@app.route("/study")
def study():
    """Stage 5: short timed tasks that log clicks, errors, completion and duration."""
    user = current_user()
    tasks = get_db().execute(
        "SELECT * FROM test_tasks WHERE user_id = ? ORDER BY id DESC LIMIT 10", (user["id"],)
    ).fetchall()
    return render_template("study.html", tasks=tasks, active="study")


# Page 6 — Findings: read the anonymised CSV and show the charts.
@app.route("/results")
def results():
    """Survey findings and charts for the presentation."""
    user = current_user()
    rows = []
    if SURVEY_CSV.exists():
        with SURVEY_CSV.open(encoding="utf-8-sig", newline="") as f:
            rows = list(csv.DictReader(f))
    summary = survey_summary(rows)
    return render_template("results.html", rows=rows, summary=summary, active="results")


# --------------------------------------------------------------------------- #
# API
# --------------------------------------------------------------------------- #
# API — the Save buttons call this; it adds a row to saved_songs.
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


# API — the Remove buttons call this; it deletes one row.
@app.route("/api/unsave/<int:song_id>", methods=["POST"])
def api_unsave(song_id: int):
    user = current_user()
    db = get_db()
    cur = db.execute("DELETE FROM saved_songs WHERE id = ? AND user_id = ?", (song_id, user["id"]))
    db.commit()
    log_event("unsave_song", str(song_id))
    return jsonify({"ok": cur.rowcount > 0})


# API — JavaScript calls this to log a click, a task start or a SUS score.
@app.route("/api/event", methods=["POST"])
def api_event():
    data = request.get_json(force=True) or {}
    event_type = str(data.get("type", "interaction"))[:80]
    log_event(event_type, str(data.get("detail", ""))[:200], data.get("duration_ms"))
    return jsonify({"ok": True})


# API — called when a timed study task is stopped.
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


# API — raw counts from the database, handy for a quick check.
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


# Serve the PNG charts that analysis.py generated.
@app.route("/charts/<path:filename>")
def charts(filename: str):
    """Serve analysis PNGs from data/charts."""
    return send_from_directory(ROOT / "data" / "charts", filename)


# Simple check: is the server alive, and is the survey CSV present?
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
