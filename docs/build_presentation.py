#!/usr/bin/env python3
"""Generate a visually designed 15-slide presentation deck.

Every slide has its own layout: stat cards, charts, diagrams, grids, timelines,
two-column comparisons. Speaker notes are loaded from docs/slide_notes.json.
"""

import json
from pathlib import Path

from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import MSO_ANCHOR, PP_ALIGN
from pptx.util import Inches, Pt

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
OUT = HERE / "Presentation.pptx"
NOTES_FILE = HERE / "slide_notes.json"
CHARTS = ROOT / "data" / "charts"

# Palette
BLACK = RGBColor(14, 14, 16)
PANEL = RGBColor(26, 26, 30)
PANEL2 = RGBColor(36, 36, 42)
GREEN = RGBColor(29, 185, 84)
CYAN = RGBColor(0, 188, 212)
ORANGE = RGBColor(255, 152, 0)
PURPLE = RGBColor(156, 39, 176)
RED = RGBColor(241, 94, 108)
WHITE = RGBColor(245, 245, 245)
MUTED = RGBColor(163, 163, 170)
DARK = RGBColor(10, 10, 12)

W, H = 13.333, 7.5


# --------------------------------------------------------------------------- #
# Helpers
# --------------------------------------------------------------------------- #
def set_bg(slide, color=BLACK):
    fill = slide.background.fill
    fill.solid()
    fill.fore_color.rgb = color


def shape(slide, kind, x, y, w, h, fill, line=None, radius=None):
    s = slide.shapes.add_shape(kind, Inches(x), Inches(y), Inches(w), Inches(h))
    s.fill.solid()
    s.fill.fore_color.rgb = fill
    if line is None:
        s.line.fill.background()
    else:
        s.line.color.rgb = line
        s.line.width = Pt(1)
    if radius is not None and hasattr(s, "adjustments") and len(s.adjustments):
        s.adjustments[0] = radius
    return s


def box(slide, x, y, w, h, fill=PANEL, line=None, round_=True):
    kind = MSO_SHAPE.ROUNDED_RECTANGLE if round_ else MSO_SHAPE.RECTANGLE
    return shape(slide, kind, x, y, w, h, fill, line)


def circle(slide, x, y, d, fill, line=None):
    return shape(slide, MSO_SHAPE.OVAL, x, y, d, d, fill, line)


def text(slide, x, y, w, h, value, size=18, color=WHITE, bold=False,
         align=PP_ALIGN.LEFT, valign=MSO_ANCHOR.TOP, italic=False):
    tb = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    tf = tb.text_frame
    tf.word_wrap = True
    tf.vertical_anchor = valign
    tf.margin_left = tf.margin_right = Inches(0.04)
    tf.margin_top = tf.margin_bottom = Inches(0.02)
    parts = value.split("\n")
    for i, part in enumerate(parts):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.text = part
        p.font.size = Pt(size)
        p.font.bold = bold
        p.font.italic = italic
        p.font.color.rgb = color
        p.font.name = "Calibri"
        p.alignment = align
        p.space_after = Pt(4)
    return tb


def bullet_list(slide, x, y, w, h, items, size=16, color=WHITE, gap=10, bullet_color=GREEN):
    tb = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    tf = tb.text_frame
    tf.word_wrap = True
    for i, item in enumerate(items):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        bullet = p.add_run()
        bullet.text = "●  "
        bullet.font.size = Pt(size)
        bullet.font.color.rgb = bullet_color or color
        bullet.font.name = "Calibri"
        body = p.add_run()
        body.text = item
        body.font.size = Pt(size)
        body.font.color.rgb = color
        body.font.name = "Calibri"
        p.space_after = Pt(gap)
    return tb


def kicker(slide, label, color=GREEN):
    text(slide, 0.7, 0.35, 8, 0.3, label.upper(), size=11, color=color, bold=True)


def header(slide, index, title, subtitle=None, accent=GREEN):
    kicker(slide, f"{index:02d} / 15", accent)
    text(slide, 0.7, 0.68, 12, 0.7, title, size=30, color=WHITE, bold=True)
    if subtitle:
        text(slide, 0.72, 1.36, 11.8, 0.4, subtitle, size=13, color=MUTED)
    shape(slide, MSO_SHAPE.RECTANGLE, 0.7, 1.78, 1.1, 0.055, accent)


def footer(slide, index, accent=GREEN):
    text(slide, 0.7, 7.05, 9, 0.25, "Reimagining the Personal Music Experience", size=9, color=MUTED)
    text(slide, 11.8, 7.05, 0.9, 0.25, f"{index:02d}", size=9, color=accent, align=PP_ALIGN.RIGHT)


def stat_card(slide, x, y, w, h, big, label, accent):
    box(slide, x, y, w, h, PANEL)
    shape(slide, MSO_SHAPE.RECTANGLE, x, y, 0.06, h, accent)
    text(slide, x + 0.25, y + 0.18, w - 0.4, 0.8, big, size=34, color=accent, bold=True)
    text(slide, x + 0.25, y + 1.0, w - 0.4, h - 1.1, label, size=12, color=MUTED)


def feature_card(slide, x, y, w, h, tag, title, body, accent):
    box(slide, x, y, w, h, PANEL)
    circle(slide, x + 0.25, y + 0.25, 0.42, accent)
    text(slide, x + 0.25, y + 0.29, 0.42, 0.3, tag, size=11, color=DARK, bold=True, align=PP_ALIGN.CENTER)
    text(slide, x + 0.8, y + 0.25, w - 1.0, 0.4, title, size=16, color=WHITE, bold=True)
    text(slide, x + 0.3, y + 0.85, w - 0.6, h - 1.0, body, size=12, color=MUTED)


def arrow(slide, x, y, w=0.5, h=0.35, color=GREEN):
    return shape(slide, MSO_SHAPE.RIGHT_ARROW, x, y, w, h, color)


def notes(slide, idx, notes_list):
    if idx < len(notes_list):
        slide.notes_slide.notes_text_frame.text = notes_list[idx]


# --------------------------------------------------------------------------- #
# Slides
# --------------------------------------------------------------------------- #
def s1(prs):
    s = prs.slides.add_slide(prs.slide_layouts[6]); set_bg(s)
    # Decorative shapes
    circle(s, 10.3, -1.5, 4.2, PANEL)
    circle(s, 11.6, 4.9, 3.0, PANEL2)
    shape(s, MSO_SHAPE.RECTANGLE, 0, 0, 0.22, H, GREEN)
    circle(s, 0.85, 0.8, 0.75, GREEN)
    text(s, 0.85, 0.95, 0.75, 0.4, "♫", size=22, color=DARK, bold=True, align=PP_ALIGN.CENTER)
    text(s, 1.75, 0.92, 8, 0.35, "DESIGN THINKING  ·  INTEGRATED PROJECT", size=12, color=GREEN, bold=True)
    text(s, 0.9, 2.0, 11.2, 1.9, "Reimagining the\nPersonal Music Experience",
         size=42, color=WHITE, bold=True)
    shape(s, MSO_SHAPE.RECTANGLE, 0.95, 4.15, 3.2, 0.06, GREEN)
    text(s, 0.95, 4.45, 9.5, 0.5, "A privacy-first personalisation layer with statistical validation",
         size=18, color=MUTED)
    box(s, 0.95, 5.45, 7.6, 1.0, PANEL)
    text(s, 1.2, 5.62, 7.1, 0.7, "[Name]  ·  [Roll Number]\n[Department]  ·  [Institution]  ·  Mentor: [Name]",
         size=12, color=MUTED)
    footer(s, 1)


def s2(prs):
    s = prs.slides.add_slide(prs.slide_layouts[6]); set_bg(s)
    header(s, 2, "Introduction", "Everyday routine, uneven personalisation", CYAN)
    stat_card(s, 0.7, 2.1, 3.7, 2.1, "78%", "use their music app daily or\nseveral times a week", CYAN)
    stat_card(s, 4.8, 2.1, 3.7, 2.1, "61%", "say the app only 'somewhat' or\n'poorly' understands their taste", ORANGE)
    stat_card(s, 8.9, 2.1, 3.7, 2.1, "39%", "say their taste is understood\n'very well'", GREEN)
    box(s, 0.7, 4.7, 11.9, 1.7, PANEL)
    shape(s, MSO_SHAPE.RECTANGLE, 0.7, 4.7, 0.06, 1.7, CYAN)
    text(s, 1.0, 4.95, 11.2, 0.5, "THE QUESTION", size=11, color=CYAN, bold=True)
    text(s, 1.0, 5.35, 11.2, 0.8,
         "Can a lightweight utility improve discovery and rediscovery\nwithout access to private streaming APIs?",
         size=19, color=WHITE, bold=True)
    footer(s, 2, CYAN)


def s3(prs):
    s = prs.slides.add_slide(prs.slide_layouts[6]); set_bg(s)
    header(s, 3, "Project overview", "Three objectives, four outcomes", GREEN)
    feature_card(s, 0.7, 2.0, 3.8, 2.3, "1", "Control familiarity",
                 "Let users choose Familiar, Balanced or Exploratory recommendations.", GREEN)
    feature_card(s, 4.75, 2.0, 3.8, 2.3, "2", "Rediscover music",
                 "Make saved songs easy to find with a personal library.", CYAN)
    feature_card(s, 8.8, 2.0, 3.8, 2.3, "3", "Prove with data",
                 "Use statistics to show which pain points the design addresses.", ORANGE)
    text(s, 0.7, 4.7, 6, 0.35, "OUTCOMES", size=11, color=GREEN, bold=True)
    chips = [("Chrome extension", GREEN), ("Flask + SQLite", CYAN),
             ("Responsive dashboard", ORANGE), ("Re-runnable analysis", PURPLE)]
    x = 0.7
    for label, c in chips:
        w = 2.85
        box(s, x, 5.2, w, 0.85, PANEL2)
        shape(s, MSO_SHAPE.RECTANGLE, x, 5.2, w, 0.06, c)
        text(s, x + 0.15, 5.4, w - 0.3, 0.5, label, size=13, color=WHITE, bold=True, align=PP_ALIGN.CENTER)
        x += w + 0.15
    footer(s, 3)


def s4(prs):
    s = prs.slides.add_slide(prs.slide_layouts[6]); set_bg(s)
    header(s, 4, "User research", "Convenience sample · n = 18 · ages 18–30 (median 19)", PURPLE)
    text(s, 0.7, 2.05, 5.5, 0.35, "PRIMARY PLATFORM", size=11, color=PURPLE, bold=True)
    bars = [("Spotify", 78, GREEN), ("YouTube Music", 17, CYAN), ("Other", 5, ORANGE)]
    y = 2.5
    for label, pct, c in bars:
        text(s, 0.7, y, 2.2, 0.35, label, size=13, color=WHITE)
        shape(s, MSO_SHAPE.RECTANGLE, 2.9, y + 0.05, 4.0, 0.28, PANEL2)
        shape(s, MSO_SHAPE.RECTANGLE, 2.9, y + 0.05, 4.0 * pct / 100, 0.28, c)
        text(s, 7.05, y - 0.02, 0.9, 0.35, f"{pct}%", size=13, color=c, bold=True)
        y += 0.7
    box(s, 8.4, 2.05, 4.2, 2.9, PANEL)
    text(s, 8.7, 2.3, 3.7, 0.35, "METHOD", size=11, color=PURPLE, bold=True)
    bullet_list(s, 8.7, 2.75, 3.6, 2.0,
                ["Multiple choice + ordinal ratings", "Numeric age + open-ended items",
                 "78% Spotify — platform imbalance", "Below target of 30 — declared"],
                size=12, gap=8, bullet_color=PURPLE)
    box(s, 0.7, 5.3, 11.9, 1.1, PANEL)
    shape(s, MSO_SHAPE.RECTANGLE, 0.7, 5.3, 0.06, 1.1, PURPLE)
    text(s, 1.0, 5.5, 11.2, 0.7,
         "33% discover new music OUTSIDE the app  ·  78% save or like tracks  ·  44% struggle to find old saves",
         size=15, color=WHITE, bold=True)
    footer(s, 4, PURPLE)


def s5(prs):
    s = prs.slides.add_slide(prs.slide_layouts[6]); set_bg(s)
    header(s, 5, "Empathise", "Four-quadrant empathy map from real responses", ORANGE)
    quads = [
        (0.7, 2.0, "SAYS", GREEN, ["'Remove ads'", "'Better recommendations'", "'Organise music by vibe'"]),
        (6.8, 2.0, "THINKS", CYAN, ["'Why the same songs?'", "'Will I find that saved track?'"]),
        (0.7, 4.35, "DOES", ORANGE, ["78% save or like tracks", "33% discover outside the app"]),
        (6.8, 4.35, "FEELS", RED, ["Annoyed by ads (50%)", "Mildly satisfied, not delighted"]),
    ]
    for x, y, label, c, items in quads:
        box(s, x, y, 5.8, 2.1, PANEL)
        shape(s, MSO_SHAPE.RECTANGLE, x, y, 5.8, 0.05, c)
        text(s, x + 0.25, y + 0.2, 5.3, 0.3, label, size=11, color=c, bold=True)
        bullet_list(s, x + 0.25, y + 0.6, 5.3, 1.3, items, size=13, gap=5, bullet_color=c)
    footer(s, 5, ORANGE)


def s6(prs):
    s = prs.slides.add_slide(prs.slide_layouts[6]); set_bg(s)
    header(s, 6, "Statistical findings", "Ordinal coding 1–3 · neutral = 2 · one-sample t-tests", CYAN)
    stat_card(s, 0.7, 2.0, 3.7, 1.85, "2.50", "Vibe ease · p = 0.003\nCI [2.19, 2.81]", GREEN)
    stat_card(s, 4.8, 2.0, 3.7, 1.85, "2.33", "Taste understanding · p = 0.029\nCI [2.04, 2.63]", CYAN)
    stat_card(s, 8.9, 2.0, 3.7, 1.85, "2.11", "Saved retrieval · p = 0.651\nnot significant", ORANGE)
    chart = CHARTS / "ordinal_distributions.png"
    if chart.exists():
        box(s, 0.7, 4.05, 7.4, 2.8, PANEL)
        s.shapes.add_picture(str(chart), Inches(0.9), Inches(4.2), width=Inches(7.0))
    box(s, 8.4, 4.05, 4.2, 2.8, PANEL)
    shape(s, MSO_SHAPE.RECTANGLE, 8.4, 4.05, 0.06, 2.8, CYAN)
    text(s, 8.7, 4.3, 3.7, 0.35, "HONEST READING", size=11, color=CYAN, bold=True)
    text(s, 8.7, 4.75, 3.7, 1.9,
         "Above neutral ≠ unhappy.\n\nGood-but-not-great baseline.\n\nWe claim refinement,\nnot rescue.",
         size=14, color=WHITE)
    footer(s, 6, CYAN)


def s7(prs):
    s = prs.slides.add_slide(prs.slide_layouts[6]); set_bg(s)
    header(s, 7, "Define", "Persona · POV · HMW · MoSCoW", GREEN)
    box(s, 0.7, 2.0, 3.9, 4.7, PANEL)
    circle(s, 1.8, 2.25, 1.2, GREEN)
    text(s, 1.8, 2.55, 1.2, 0.5, "A", size=28, color=DARK, bold=True, align=PP_ALIGN.CENTER)
    text(s, 0.95, 3.6, 3.4, 0.5, "Aarav, 19", size=20, color=WHITE, bold=True, align=PP_ALIGN.CENTER)
    text(s, 0.95, 4.15, 3.4, 2.2,
         "B.Tech student\nDaily Spotify listener\nDiscovers music outside apps\nSaves tracks, rarely revisits\nWants mood-based choice",
         size=12, color=MUTED, align=PP_ALIGN.CENTER)
    box(s, 4.85, 2.0, 7.75, 2.15, PANEL2)
    shape(s, MSO_SHAPE.RECTANGLE, 4.85, 2.0, 0.06, 2.15, GREEN)
    text(s, 5.15, 2.2, 7.1, 0.3, "POINT OF VIEW", size=11, color=GREEN, bold=True)
    text(s, 5.15, 2.6, 7.1, 1.35,
         "A listener who saves but cannot rediscover, and feels recommendations only 'somewhat' match their taste, needs familiarity control and mood-based retrieval.",
         size=14, color=WHITE)
    box(s, 4.85, 4.35, 7.75, 1.0, PANEL)
    shape(s, MSO_SHAPE.RECTANGLE, 4.85, 4.35, 0.06, 1.0, CYAN)
    text(s, 5.15, 4.5, 7.1, 0.7,
         "HMW: give that control without a paid subscription or new account?",
         size=15, color=CYAN, bold=True)
    box(s, 4.85, 5.55, 7.75, 1.15, PANEL)
    text(s, 5.15, 5.7, 7.1, 0.3, "MOSCOW", size=11, color=ORANGE, bold=True)
    text(s, 5.15, 6.05, 7.1, 0.5,
         "Must: Discover, My Music, backend   |   Won't: ads, offline downloads",
         size=12, color=WHITE)
    footer(s, 7)


def s8(prs):
    s = prs.slides.add_slide(prs.slide_layouts[6]); set_bg(s)
    header(s, 8, "Ideation", "10 ideas · mind map · SWOT", PURPLE)
    box(s, 5.1, 3.35, 3.1, 0.9, GREEN)
    text(s, 5.1, 3.6, 3.1, 0.4, "PERSONAL MUSIC", size=14, color=DARK, bold=True, align=PP_ALIGN.CENTER)
    branches = [
        (0.7, 2.0, "Discovery", GREEN), (0.7, 3.35, "Mood", CYAN),
        (0.7, 4.7, "Library", ORANGE), (9.6, 2.0, "Understanding", PURPLE),
        (9.6, 3.35, "Preferences", RED),
    ]
    for x, y, label, c in branches:
        box(s, x, y, 2.9, 0.85, PANEL)
        shape(s, MSO_SHAPE.RECTANGLE, x, y, 0.06, 0.85, c)
        text(s, x + 0.2, y + 0.25, 2.5, 0.4, label, size=14, color=WHITE, bold=True)
        if x < 5:
            arrow(s, x + 2.95, y + 0.25, 1.4, 0.3, c)
        else:
            shape(s, MSO_SHAPE.LEFT_ARROW, x - 1.45, y + 0.25, 1.35, 0.3, c)
    box(s, 8.6, 4.7, 3.9, 1.85, PANEL)
    text(s, 8.9, 4.9, 3.3, 0.3, "10 IDEAS INCLUDED", size=11, color=PURPLE, bold=True)
    text(s, 8.9, 5.3, 3.3, 1.1,
         "Discovery slider · Vibe tags\nSave + library · Preferences\nUnderstand · AI chatbot · Ad blocker",
         size=12, color=MUTED)
    footer(s, 8, PURPLE)


def s9(prs):
    s = prs.slides.add_slide(prs.slide_layouts[6]); set_bg(s)
    header(s, 9, "Idea selection", "Weighted: desirability 40% · feasibility 35% · viability 25%", ORANGE)
    text(s, 0.7, 2.0, 7.5, 0.3, "WEIGHTED SCORE", size=11, color=ORANGE, bold=True)
    rows = [("Discovery slider", 5.0, GREEN), ("Vibe tags", 5.0, GREEN),
            ("Save + library", 5.0, GREEN), ("Preferences", 4.65, CYAN),
            ("Usage logging", 4.2, CYAN), ("AI chatbot", 2.45, RED), ("Ad blocker", 2.8, RED)]
    y = 2.4
    for label, score, c in rows:
        text(s, 0.7, y, 2.2, 0.3, label, size=12, color=WHITE)
        shape(s, MSO_SHAPE.RECTANGLE, 2.95, y + 0.04, 3.8, 0.22, PANEL2)
        shape(s, MSO_SHAPE.RECTANGLE, 2.95, y + 0.04, 3.8 * score / 5, 0.22, c)
        text(s, 6.9, y - 0.02, 0.8, 0.3, f"{score:.2f}", size=12, color=c, bold=True)
        y += 0.58
    box(s, 8.0, 2.0, 4.6, 4.6, PANEL)
    shape(s, MSO_SHAPE.RECTANGLE, 8.0, 2.0, 0.06, 4.6, ORANGE)
    text(s, 8.3, 2.25, 4.0, 0.3, "HYPOTHESES (FIXED EARLY)", size=11, color=ORANGE, bold=True)
    bullet_list(s, 8.3, 2.7, 4.0, 3.6,
                ["Retrieval time lower with prototype",
                 "Taste rating above 2.33 baseline",
                 "SUS above 68 benchmark",
                 "α = 0.05 · paired design",
                 "Ad blocker rejected: infeasible"],
                size=13, gap=12, bullet_color=ORANGE)
    footer(s, 9, ORANGE)


def s10(prs):
    s = prs.slides.add_slide(prs.slide_layouts[6]); set_bg(s)
    header(s, 10, "Prototype", "Extension → Flask → SQLite · all data local", GREEN)
    nodes = [(0.7, "CHROME\nEXTENSION", GREEN), (4.9, "FLASK\nBACKEND", CYAN),
             (9.1, "SQLITE\nDATABASE", ORANGE)]
    for x, label, c in nodes:
        box(s, x, 2.2, 3.5, 1.6, PANEL)
        shape(s, MSO_SHAPE.RECTANGLE, x, 2.2, 3.5, 0.07, c)
        text(s, x + 0.1, 2.65, 3.3, 0.8, label, size=17, color=WHITE, bold=True, align=PP_ALIGN.CENTER)
    arrow(s, 4.3, 2.8, 0.5, 0.4, GREEN)
    arrow(s, 8.5, 2.8, 0.5, 0.4, CYAN)
    text(s, 0.7, 4.15, 11.9, 0.3, "KEY FEATURES", size=11, color=GREEN, bold=True)
    chips = [("Discover · 3 levels", GREEN), ("Find by Vibe · 8 tags", CYAN),
             ("My Music · saved list", ORANGE), ("Preferences · consent", PURPLE),
             ("Usage logging", RED)]
    x = 0.7
    for label, c in chips:
        w = 2.28
        box(s, x, 4.55, w, 0.9, PANEL2)
        shape(s, MSO_SHAPE.RECTANGLE, x, 4.55, w, 0.05, c)
        text(s, x + 0.1, 4.78, w - 0.2, 0.5, label, size=11, color=WHITE, bold=True, align=PP_ALIGN.CENTER)
        x += w + 0.14
    box(s, 0.7, 5.75, 11.9, 0.95, PANEL)
    text(s, 1.0, 5.95, 11.3, 0.6,
         "Per-platform track adapters  ·  2-second polling  ·  No login  ·  No external API  ·  Responsive dashboard",
         size=14, color=WHITE, align=PP_ALIGN.CENTER)
    footer(s, 10)


def s11(prs):
    s = prs.slides.add_slide(prs.slide_layouts[6]); set_bg(s)
    header(s, 11, "Testing and validation", "Paired design · timed tasks · SUS", RED)
    steps = [("1", "Recruit", RED), ("2", "3 timed tasks", ORANGE),
             ("3", "SUS form", CYAN), ("4", "Analyse", GREEN)]
    x = 0.7
    for i, (n, label, c) in enumerate(steps):
        circle(s, x + 0.45, 2.1, 0.8, c)
        text(s, x + 0.45, 2.28, 0.8, 0.4, n, size=18, color=DARK, bold=True, align=PP_ALIGN.CENTER)
        text(s, x, 3.05, 1.7, 0.5, label, size=12, color=WHITE, bold=True, align=PP_ALIGN.CENTER)
        if i < 3:
            arrow(s, x + 1.75, 2.35, 0.6, 0.3, c)
        x += 2.4
    box(s, 0.7, 3.85, 5.7, 2.8, PANEL)
    shape(s, MSO_SHAPE.RECTANGLE, 0.7, 3.85, 0.06, 2.8, RED)
    text(s, 1.0, 4.1, 5.1, 0.3, "MEASURES", size=11, color=RED, bold=True)
    bullet_list(s, 1.0, 4.5, 5.0, 2.0,
                ["Duration per task (ms)", "Clicks and errors counted",
                 "SUS 0–100, benchmark 68", "Wilcoxon / paired t-test"],
                size=13, gap=10, bullet_color=RED)
    box(s, 6.7, 3.85, 5.9, 2.8, PANEL2)
    text(s, 7.0, 4.1, 5.3, 0.3, "RESULTS STATUS", size=11, color=GREEN, bold=True)
    text(s, 7.0, 4.55, 5.3, 1.8,
         "Instrument and logging are built.\n\nParticipant runs still being collected — fill in real SUS and task numbers before presenting.",
         size=14, color=WHITE)
    footer(s, 11, RED)


def s12(prs):
    s = prs.slides.add_slide(prs.slide_layouts[6]); set_bg(s)
    header(s, 12, "Results and iterations", "Three changes driven by testing and reflection", CYAN)
    items = [
        ("1", "Per-platform adapters", "Single-file selector broke on YouTube Music's DOM; split into one adapter per site.", GREEN),
        ("2", "Companion dashboard", "Saved songs existed in extension storage but had no view; added a SQLite-backed library.", CYAN),
        ("3", "Usage logging + consent", "Testing needed real measurement; added event logging and a tracking toggle.", ORANGE),
    ]
    y = 2.0
    for n, title, body, c in items:
        box(s, 0.7, y, 11.9, 1.45, PANEL)
        circle(s, 0.95, y + 0.35, 0.75, c)
        text(s, 0.95, y + 0.5, 0.75, 0.4, n, size=18, color=DARK, bold=True, align=PP_ALIGN.CENTER)
        text(s, 1.95, y + 0.22, 10.2, 0.4, title, size=16, color=WHITE, bold=True)
        text(s, 1.95, y + 0.7, 10.2, 0.6, body, size=12, color=MUTED)
        y += 1.6
    text(s, 0.7, 6.85, 11.9, 0.25, "Add measured SUS and task-time changes here once real runs are complete.",
         size=10, color=MUTED, italic=True)
    footer(s, 12, CYAN)


def s13(prs):
    s = prs.slides.add_slide(prs.slide_layouts[6]); set_bg(s)
    header(s, 13, "Impact and limitations", "Benefits weighed honestly against threats to validity", ORANGE)
    box(s, 0.7, 2.0, 5.8, 4.6, PANEL)
    shape(s, MSO_SHAPE.RECTANGLE, 0.7, 2.0, 5.8, 0.07, GREEN)
    text(s, 1.0, 2.25, 5.2, 0.35, "BENEFITS", size=12, color=GREEN, bold=True)
    bullet_list(s, 1.0, 2.75, 5.1, 3.6,
                ["No account or login required", "Data never leaves the machine",
                 "Works across three platforms", "Directly addresses the retrieval gap",
                 "Built-in measurement for testing"],
                size=14, gap=14, bullet_color=GREEN)
    box(s, 6.8, 2.0, 5.8, 4.6, PANEL)
    shape(s, MSO_SHAPE.RECTANGLE, 6.8, 2.0, 5.8, 0.07, RED)
    text(s, 7.1, 2.25, 5.2, 0.35, "LIMITATIONS", size=12, color=RED, bold=True)
    bullet_list(s, 7.1, 2.75, 5.1, 3.6,
                ["n = 18, below the target of 30", "78% Spotify; zero Apple Music users",
                 "Ads (50%) out of scope", "Demo recommendation database",
                 "Single-contributor scope"],
                size=14, gap=14, bullet_color=RED)
    footer(s, 13, ORANGE)


def s14(prs):
    s = prs.slides.add_slide(prs.slide_layouts[6]); set_bg(s)
    header(s, 14, "Conclusion and future scope", "A small utility addressing a measured gap", GREEN)
    box(s, 0.7, 2.0, 11.9, 1.7, PANEL)
    shape(s, MSO_SHAPE.RECTANGLE, 0.7, 2.0, 0.06, 1.7, GREEN)
    text(s, 1.0, 2.3, 11.2, 1.1,
         "78% save music. 44% struggle to find old saves.\nA focused, private utility closes that loop — without claiming to fix ads.",
         size=20, color=WHITE, bold=True)
    text(s, 0.7, 4.1, 6, 0.3, "FUTURE WORK", size=11, color=GREEN, bold=True)
    cards = [("Real recommender", "Replace demo data with a learned model", GREEN),
             ("Understand section", "Lyrics and song meaning", CYAN),
             ("Larger sample", "30+ stratified responses and full SUS study", ORANGE)]
    x = 0.7
    for title, body, c in cards:
        box(s, x, 4.5, 3.8, 1.9, PANEL)
        shape(s, MSO_SHAPE.RECTANGLE, x, 4.5, 3.8, 0.06, c)
        text(s, x + 0.25, 4.8, 3.3, 0.4, title, size=15, color=WHITE, bold=True)
        text(s, x + 0.25, 5.3, 3.3, 1.0, body, size=12, color=MUTED)
        x += 3.95
    footer(s, 14)


def s15(prs):
    s = prs.slides.add_slide(prs.slide_layouts[6]); set_bg(s)
    circle(s, 10.0, -1.0, 4.5, PANEL)
    shape(s, MSO_SHAPE.RECTANGLE, 0, 0, 0.22, H, GREEN)
    text(s, 0.9, 1.3, 8, 0.4, "REFERENCES & Q&A", size=12, color=GREEN, bold=True)
    text(s, 0.9, 2.0, 11, 1.3, "Thank you.", size=52, color=WHITE, bold=True)
    text(s, 0.95, 3.35, 8, 0.6, "Questions?", size=28, color=GREEN, bold=True)
    bullet_list(s, 0.95, 4.35, 8.5, 2.1,
                ["Anonymised survey dataset (R01–R18)", "Integrated assignment brief",
                 "Open-source libraries: Flask, pandas, SciPy, matplotlib",
                 "AI tooling disclosed per brief"],
                size=13, gap=10, bullet_color=GREEN)
    footer(s, 15)


BUILDERS = [s1, s2, s3, s4, s5, s6, s7, s8, s9, s10, s11, s12, s13, s14, s15]


def main():
    notes_list = json.loads(NOTES_FILE.read_text()) if NOTES_FILE.exists() else []
    prs = Presentation()
    prs.slide_width = Inches(W)
    prs.slide_height = Inches(H)
    for i, builder in enumerate(BUILDERS):
        builder(prs)
        notes(prs.slides[i], i, notes_list)
    prs.save(OUT)
    print(f"Wrote {OUT} — {len(BUILDERS)} designed slides, {len(notes_list)} speaker notes")


if __name__ == "__main__":
    main()
