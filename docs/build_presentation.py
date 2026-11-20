#!/usr/bin/env python3
"""Generate the designed 15-slide presentation deck.

Design system
-------------
* Exactly THREE font sizes: 32 (hero), 16 (body), 11 (meta).
  Every text helper passes requested sizes through ``fs()`` which snaps to
  the nearest allowed size, so adding new slides cannot break the rule.
* Each slide gets a two-stop gradient background plus subtle music motifs
  (vinyl rings, waveform bars, note glyph) at low opacity.
* Charts are generated with gridlines by webapp/analysis/analysis.py.

Extending
---------
1. Add a builder function ``sN(prs)`` that calls ``decorate(prs.slides[-1], N)``.
2. Append it to ``SLIDE_BUILDERS``. Speaker notes come from slide_notes.json.
3. Change palette / gradient angles in THEME at the top of this file.
"""

import json
from pathlib import Path

from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import MSO_ANCHOR, PP_ALIGN
from pptx.oxml.xmlchemy import OxmlElement
from pptx.util import Inches, Pt

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
OUT = HERE / "Presentation.pptx"
NOTES_FILE = HERE / "slide_notes.json"
CHARTS = ROOT / "data" / "charts"

# --------------------------------------------------------------------------- #
# Theme — edit here to restyle the whole deck
# --------------------------------------------------------------------------- #
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

# (gradient start, gradient end, accent, angle)
THEME = [
    (RGBColor(9, 26, 17), RGBColor(14, 14, 16), GREEN, 45),
    (RGBColor(9, 28, 32), RGBColor(14, 14, 16), CYAN, 135),
    (RGBColor(12, 24, 18), RGBColor(16, 14, 18), GREEN, 45),
    (RGBColor(24, 14, 34), RGBColor(14, 14, 16), PURPLE, 135),
    (RGBColor(30, 20, 10), RGBColor(14, 14, 16), ORANGE, 45),
    (RGBColor(9, 28, 32), RGBColor(16, 14, 20), CYAN, 135),
    (RGBColor(12, 26, 18), RGBColor(14, 14, 16), GREEN, 45),
    (RGBColor(24, 14, 34), RGBColor(14, 16, 20), PURPLE, 135),
    (RGBColor(30, 20, 10), RGBColor(14, 14, 16), ORANGE, 45),
    (RGBColor(12, 24, 18), RGBColor(14, 14, 18), GREEN, 135),
    (RGBColor(30, 14, 18), RGBColor(14, 14, 16), RED, 45),
    (RGBColor(9, 28, 32), RGBColor(14, 16, 20), CYAN, 135),
    (RGBColor(30, 20, 10), RGBColor(18, 14, 16), ORANGE, 45),
    (RGBColor(12, 26, 18), RGBColor(14, 14, 16), GREEN, 135),
    (RGBColor(9, 26, 17), RGBColor(14, 14, 16), GREEN, 45),
]

FONT_HERO, FONT_BODY, FONT_META = 32, 16, 11
FONTS = (FONT_HERO, FONT_BODY, FONT_META)   # the ONLY font sizes allowed

# Uniform TEXT palette. Accent colours are for SHAPES only — every piece of
# text resolves to white (body), muted grey (captions) or green (headings).
T_HEAD, T_BODY, T_MUTED = GREEN, WHITE, MUTED
ACCENTS = (GREEN, CYAN, ORANGE, PURPLE, RED)


def text_color(color):
    """Collapse any per-slide accent colour to the single heading colour."""
    return T_HEAD if color in ACCENTS else color

W, H = 13.333, 7.5


def fs(size: int) -> int:
    """Snap any requested size to the nearest of the three allowed sizes."""
    return min(FONTS, key=lambda f: abs(f - size))


def _alpha(color_format, opacity_percent: int) -> bool:
    """Attach DrawingML alpha to a colour format. 100 = solid, 8 = very subtle."""
    try:
        srgb = color_format._xFill.srgbClr
        if srgb is None:
            return False
        for child in list(srgb):
            if child.tag.endswith("alpha"):
                srgb.remove(child)
        alpha = OxmlElement("a:alpha")
        alpha.set("val", str(int(opacity_percent * 1000)))
        srgb.append(alpha)
        return True
    except Exception:
        return False


def set_opacity(shape, opacity_percent: int) -> None:
    """Set opacity on BOTH fill and line (line-only shapes need the latter)."""
    for getter in (lambda: shape.fill.fore_color, lambda: shape.line.color):
        try:
            _alpha(getter(), opacity_percent)
        except Exception:
            pass  # e.g. _NoFill has no foreground colour — that is fine


# --------------------------------------------------------------------------- #
# Shape / text helpers
# --------------------------------------------------------------------------- #
def shape(slide, kind, x, y, w, h, fill, line=None):
    s = slide.shapes.add_shape(kind, Inches(x), Inches(y), Inches(w), Inches(h))
    s.fill.solid()
    s.fill.fore_color.rgb = fill
    if line is None:
        s.line.fill.background()
    else:
        s.line.color.rgb = line
        s.line.width = Pt(0.75)
    return s


def box(slide, x, y, w, h, fill=PANEL, line=None):
    panel = shape(slide, MSO_SHAPE.ROUNDED_RECTANGLE, x, y, w, h, fill, line)
    if w >= 2.4 and h >= 0.8:
        # Faint tinted wash stops large panels reading as flat blocks.
        wash = shape(slide, MSO_SHAPE.ROUNDED_RECTANGLE,
                     x + 0.02, y + 0.02, w - 0.04, h - 0.04, T_HEAD)
        set_opacity(wash, 3)
        # Tiny equaliser motif: 6% opacity keeps text fully readable.
        for i, extra in enumerate((0.12, 0.30, 0.16, 0.36, 0.22)):
            bar = shape(slide, MSO_SHAPE.RECTANGLE,
                        x + w - 1.2 + i * 0.2, y + h - 0.55,
                        0.07, 0.18 + extra, T_HEAD)
            set_opacity(bar, 6)
    return panel


def circle(slide, x, y, d, fill):
    return shape(slide, MSO_SHAPE.OVAL, x, y, d, d, fill)


def text(slide, x, y, w, h, value, size=FONT_BODY, color=WHITE, bold=False,
         align=PP_ALIGN.LEFT, valign=MSO_ANCHOR.TOP, italic=False):
    tb = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    tf = tb.text_frame
    tf.word_wrap = True
    tf.vertical_anchor = valign
    tf.margin_left = tf.margin_right = Inches(0.03)
    tf.margin_top = tf.margin_bottom = Inches(0.01)
    for i, part in enumerate(str(value).split("\n")):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.alignment = align
        p.space_after = Pt(3)
        r = p.add_run()
        r.text = part
        r.font.size = Pt(fs(size))
        r.font.bold = bold
        r.font.italic = italic
        r.font.color.rgb = text_color(color)
        r.font.name = "Calibri"
    return tb


def bullets(slide, x, y, w, h, items, color=WHITE, accent=GREEN, gap=9):
    tb = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    tf = tb.text_frame
    tf.word_wrap = True
    for i, item in enumerate(items):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        b = p.add_run(); b.text = "●  "
        b.font.size = Pt(FONT_META if len(item) > 48 else FONT_BODY)
        b.font.color.rgb = text_color(accent or color); b.font.name = "Calibri"
        r = p.add_run(); r.text = item
        r.font.size = Pt(FONT_META if len(item) > 48 else FONT_BODY)
        r.font.color.rgb = text_color(color); r.font.name = "Calibri"
        p.space_after = Pt(gap)
    return tb


def kicker(slide, label, accent):
    text(slide, 0.7, 0.33, 8, 0.28, label.upper(), size=FONT_META, color=accent, bold=True)


def header(slide, index, title, subtitle, accent):
    kicker(slide, f"{index:02d} / 15", accent)
    text(slide, 0.7, 0.62, 12, 0.65, title, size=FONT_HERO, color=WHITE, bold=True)
    if subtitle:
        text(slide, 0.72, 1.3, 11.8, 0.35, subtitle, size=FONT_META, color=MUTED)
    shape(slide, MSO_SHAPE.RECTANGLE, 0.7, 1.72, 1.0, 0.05, accent)


def footer(slide, index, accent):
    text(slide, 0.7, 6.95, 9, 0.35, "Reimagining the Personal Music Experience",
         size=FONT_META, color=MUTED)
    text(slide, 11.85, 6.95, 0.8, 0.35, f"{index:02d}", size=FONT_META,
         color=accent, align=PP_ALIGN.RIGHT)


def stat_card(slide, x, y, w, h, big, label, accent):
    box(slide, x, y, w, h, PANEL)
    shape(slide, MSO_SHAPE.RECTANGLE, x, y, 0.05, h, accent)
    text(slide, x + 0.22, y + 0.16, w - 0.4, 0.7, big, size=FONT_HERO, color=accent, bold=True)
    text(slide, x + 0.22, y + 0.95, w - 0.4, h - 1.0, label, size=FONT_META, color=MUTED)


def feature_card(slide, x, y, w, h, tag, title, body, accent):
    box(slide, x, y, w, h, PANEL)
    circle(slide, x + 0.22, y + 0.22, 0.42, accent)
    text(slide, x + 0.22, y + 0.28, 0.42, 0.3, tag, size=FONT_META, color=DARK,
         bold=True, align=PP_ALIGN.CENTER)
    text(slide, x + 0.78, y + 0.22, w - 0.95, 0.4, title, size=FONT_BODY, color=WHITE, bold=True)
    text(slide, x + 0.28, y + 0.8, w - 0.55, h - 0.9, body, size=FONT_META, color=MUTED)


def arrow(slide, x, y, w=0.5, h=0.3, color=GREEN):
    return shape(slide, MSO_SHAPE.RIGHT_ARROW, x, y, w, h, color)


# --------------------------------------------------------------------------- #
# Decoration — gradient + subtle music motifs on every slide
# --------------------------------------------------------------------------- #
def decorate(slide, index: int) -> RGBColor:
    c1, c2, accent, angle = THEME[(index - 1) % len(THEME)]

    # Gradient background
    bg = shape(slide, MSO_SHAPE.RECTANGLE, 0, 0, W, H, c1)
    bg.fill.gradient()
    stops = bg.fill.gradient_stops
    stops[0].color.rgb = c1
    stops[0].position = 0.0
    stops[1].color.rgb = c2
    stops[1].position = 1.0
    bg.fill.gradient_angle = angle
    bg.line.fill.background()

    # Subtle vinyl record rings bleeding off the top-right corner
    for d, op in [(3.4, 8), (2.5, 10), (1.6, 12), (0.7, 16)]:
        ring = slide.shapes.add_shape(MSO_SHAPE.OVAL, Inches(W - d / 2 - 0.4),
                                      Inches(-d / 2 - 0.3), Inches(d), Inches(d))
        ring.fill.background()
        ring.line.color.rgb = accent
        ring.line.width = Pt(1.2)
        set_opacity(ring, op)

    # Subtle waveform bars along the bottom edge
    for i, height in enumerate([0.32, 0.55, 0.24, 0.7, 0.4, 0.62, 0.3, 0.48]):
        bar = shape(slide, MSO_SHAPE.RECTANGLE, 0.7 + i * 0.28, H - height - 0.18,
                    0.1, height, accent)
        set_opacity(bar, 10)

    # Faint music note glyph (alpha applied to the run's colour)
    note = text(slide, 11.9, 5.95, 0.7, 0.6, "♫", size=FONT_HERO, color=accent)
    for p in note.text_frame.paragraphs:
        for r in p.runs:
            _alpha(r.font.color, 14)
    return accent


# --------------------------------------------------------------------------- #
# Slides — each builder adds its slide then decorates it
# --------------------------------------------------------------------------- #
def new(prs, index):
    s = prs.slides.add_slide(prs.slide_layouts[6])
    return s, decorate(s, index)


def s1(prs):
    s, a = new(prs, 1)
    shape(s, MSO_SHAPE.RECTANGLE, 0, 0, 0.18, H, GREEN)
    circle(s, 0.85, 0.8, 0.72, GREEN)
    text(s, 0.85, 0.95, 0.72, 0.35, "♫", size=FONT_BODY, color=DARK,
         bold=True, align=PP_ALIGN.CENTER)
    text(s, 1.72, 0.9, 9, 0.3, "DESIGN THINKING  ·  INTEGRATED PROJECT",
         size=FONT_META, color=GREEN, bold=True)
    text(s, 0.9, 1.95, 11, 1.7, "Reimagining the\nPersonal Music Experience",
         size=FONT_HERO, color=WHITE, bold=True)
    shape(s, MSO_SHAPE.RECTANGLE, 0.95, 4.05, 3.0, 0.05, GREEN)
    text(s, 0.95, 4.35, 9.5, 0.5,
         "A privacy-first personalisation layer with statistical validation",
         size=FONT_BODY, color=MUTED)
    box(s, 0.95, 5.35, 7.8, 0.95, PANEL)
    text(s, 1.2, 5.52, 7.3, 0.65,
         "[Name] · [Roll Number]\n[Department] · [Institution] · Mentor: [Name]",
         size=FONT_META, color=MUTED)
    footer(s, 1, a)


def s2(prs):
    s, a = new(prs, 2)
    header(s, 2, "Introduction", "Everyday routine, uneven personalisation", a)
    stat_card(s, 0.7, 2.0, 3.7, 1.9, "78%", "use their app daily or\nseveral times a week", a)
    stat_card(s, 4.8, 2.0, 3.7, 1.9, "61%", "say taste is only 'somewhat'\nor 'poorly' understood", ORANGE)
    stat_card(s, 8.9, 2.0, 3.7, 1.9, "39%", "say taste is understood\n'very well'", GREEN)
    box(s, 0.7, 4.35, 11.9, 1.9, PANEL)
    shape(s, MSO_SHAPE.RECTANGLE, 0.7, 4.35, 0.05, 1.9, a)
    text(s, 1.0, 4.6, 11.2, 0.3, "THE QUESTION", size=FONT_META, color=a, bold=True)
    text(s, 1.0, 5.0, 11.2, 1.0,
         "Can a lightweight utility improve discovery and rediscovery\nwithout private streaming APIs?",
         size=FONT_BODY, color=WHITE, bold=True)
    footer(s, 2, a)


def s3(prs):
    s, a = new(prs, 3)
    header(s, 3, "Project overview", "Three objectives, four outcomes", a)
    feature_card(s, 0.7, 1.95, 3.8, 2.2, "1", "Control familiarity",
                 "Choose Familiar, Balanced or Exploratory recommendations.", GREEN)
    feature_card(s, 4.75, 1.95, 3.8, 2.2, "2", "Rediscover music",
                 "A personal library makes saved songs easy to find.", a)
    feature_card(s, 8.8, 1.95, 3.8, 2.2, "3", "Prove with data",
                 "Statistics show which pain points the design addresses.", ORANGE)
    text(s, 0.7, 4.5, 6, 0.28, "OUTCOMES", size=FONT_META, color=a, bold=True)
    chips = [("Chrome extension", GREEN), ("Flask + SQLite", CYAN),
             ("Responsive dashboard", ORANGE), ("Re-runnable analysis", PURPLE)]
    x = 0.7
    for label, c in chips:
        box(s, x, 4.9, 2.85, 0.8, PANEL2)
        shape(s, MSO_SHAPE.RECTANGLE, x, 4.9, 2.85, 0.05, c)
        text(s, x + 0.1, 5.12, 2.65, 0.45, label, size=FONT_META,
             color=WHITE, bold=True, align=PP_ALIGN.CENTER)
        x += 3.0
    footer(s, 3, a)


def s4(prs):
    s, a = new(prs, 4)
    header(s, 4, "User research", "Convenience sample · n = 18 · ages 18–30 (median 19)", a)
    text(s, 0.7, 1.98, 5.5, 0.28, "PRIMARY PLATFORM", size=FONT_META, color=a, bold=True)
    y = 2.4
    for label, pct, c in [("Spotify", 78, GREEN), ("YouTube Music", 17, CYAN), ("Other", 5, ORANGE)]:
        text(s, 0.7, y, 2.1, 0.3, label, size=FONT_META, color=WHITE)
        shape(s, MSO_SHAPE.RECTANGLE, 2.8, y + 0.05, 3.9, 0.24, PANEL2)
        shape(s, MSO_SHAPE.RECTANGLE, 2.8, y + 0.05, 3.9 * pct / 100, 0.24, c)
        text(s, 6.85, y - 0.02, 0.8, 0.3, f"{pct}%", size=FONT_META, color=c, bold=True)
        y += 0.65
    box(s, 8.1, 1.98, 4.5, 2.9, PANEL)
    text(s, 8.4, 2.2, 4.0, 0.28, "METHOD", size=FONT_META, color=a, bold=True)
    bullets(s, 8.4, 2.6, 3.9, 2.1,
            ["MCQ + ordinal + numeric + open", "78% Spotify — platform imbalance",
             "Below target of 30 — declared"], accent=a, gap=8)
    box(s, 0.7, 5.1, 11.9, 1.1, PANEL)
    shape(s, MSO_SHAPE.RECTANGLE, 0.7, 5.1, 0.05, 1.1, a)
    text(s, 1.0, 5.35, 11.2, 0.7,
         "33% discover OUTSIDE the app  ·  78% save or like tracks  ·  44% struggle to find old saves",
         size=FONT_BODY, color=WHITE, bold=True)
    footer(s, 4, a)


def s5(prs):
    s, a = new(prs, 5)
    header(s, 5, "Empathise", "Four-quadrant empathy map from real responses", a)
    quads = [
        (0.7, 1.95, "SAYS", GREEN, ["'Remove ads'", "'Better recommendations'", "'Organise music by vibe'"]),
        (6.8, 1.95, "THINKS", CYAN, ["'Why the same songs?'", "'Will I find that saved track?'"]),
        (0.7, 4.2, "DOES", ORANGE, ["78% save or like tracks", "33% discover outside apps"]),
        (6.8, 4.2, "FEELS", RED, ["Annoyed by ads (50%)", "Mildly satisfied, not delighted"]),
    ]
    for x, y, label, c, items in quads:
        box(s, x, y, 5.8, 2.0, PANEL)
        shape(s, MSO_SHAPE.RECTANGLE, x, y, 5.8, 0.05, c)
        text(s, x + 0.25, y + 0.18, 5.3, 0.28, label, size=FONT_META, color=c, bold=True)
        bullets(s, x + 0.25, y + 0.58, 5.3, 1.3, items, accent=c, gap=4)
    footer(s, 5, a)


def s6(prs):
    s, a = new(prs, 6)
    header(s, 6, "Statistical findings", "Ordinal 1–3 · neutral = 2 · one-sample t-tests", a)
    stat_card(s, 0.7, 1.95, 3.7, 1.8, "2.50", "Vibe ease · p = 0.003", GREEN)
    stat_card(s, 4.8, 1.95, 3.7, 1.8, "2.33", "Taste · p = 0.029", a)
    stat_card(s, 8.9, 1.95, 3.7, 1.8, "2.11", "Retrieval · p = 0.651", ORANGE)
    chart = CHARTS / "ordinal_distributions.png"
    if chart.exists():
        box(s, 0.7, 3.95, 7.4, 2.75, PANEL)
        s.shapes.add_picture(str(chart), Inches(0.85), Inches(4.15), width=Inches(7.1))
    box(s, 8.4, 3.95, 4.2, 2.75, PANEL)
    shape(s, MSO_SHAPE.RECTANGLE, 8.4, 3.95, 0.05, 2.75, a)
    text(s, 8.7, 4.2, 3.6, 0.28, "HONEST READING", size=FONT_META, color=a, bold=True)
    text(s, 8.7, 4.65, 3.6, 1.8,
         "Above neutral ≠ unhappy.\nGood-but-not-great baseline.\nWe claim refinement, not rescue.",
         size=FONT_BODY, color=WHITE)
    footer(s, 6, a)


def s7(prs):
    s, a = new(prs, 7)
    header(s, 7, "Define", "Persona · POV · HMW · MoSCoW", a)
    box(s, 0.7, 1.95, 3.9, 4.65, PANEL)
    circle(s, 1.85, 2.2, 1.1, GREEN)
    text(s, 1.85, 2.42, 1.1, 0.62, "A", size=FONT_HERO, color=DARK,
         bold=True, align=PP_ALIGN.CENTER)
    text(s, 0.95, 3.38, 3.4, 0.72, "Aarav, 19", size=FONT_HERO, color=WHITE,
         bold=True, align=PP_ALIGN.CENTER)
    text(s, 0.95, 4.25, 3.4, 2.1,
         "B.Tech student\nDaily Spotify listener\nDiscovers music outside apps\nSaves tracks, rarely revisits\nWants mood-based choice",
         size=FONT_META, color=MUTED, align=PP_ALIGN.CENTER)
    box(s, 4.85, 1.95, 7.75, 2.1, PANEL2)
    shape(s, MSO_SHAPE.RECTANGLE, 4.85, 1.95, 0.05, 2.1, a)
    text(s, 5.15, 2.15, 7.1, 0.28, "POINT OF VIEW", size=FONT_META, color=a, bold=True)
    text(s, 5.15, 2.55, 7.1, 1.3,
         "A listener who saves but cannot rediscover, and feels recommendations only 'somewhat' match their taste, needs familiarity control and mood-based retrieval.",
         size=FONT_BODY, color=WHITE)
    box(s, 4.85, 4.2, 7.75, 0.95, PANEL)
    shape(s, MSO_SHAPE.RECTANGLE, 4.85, 4.2, 0.05, 0.95, CYAN)
    text(s, 5.15, 4.4, 7.1, 0.6,
         "HMW: give that control without a paid subscription?",
         size=FONT_BODY, color=CYAN, bold=True)
    box(s, 4.85, 5.3, 7.75, 1.3, PANEL)
    text(s, 5.15, 5.5, 7.1, 0.28, "MOSCOW", size=FONT_META, color=ORANGE, bold=True)
    text(s, 5.15, 5.85, 7.1, 0.6,
         "Must: Discover, My Music, backend   |   Won't: ads, offline downloads",
         size=FONT_META, color=WHITE)
    footer(s, 7, a)


def s8(prs):
    s, a = new(prs, 8)
    header(s, 8, "Ideation", "10 ideas · mind map · SWOT", a)
    box(s, 5.1, 3.25, 3.1, 0.85, GREEN)
    text(s, 5.1, 3.48, 3.1, 0.4, "PERSONAL MUSIC", size=FONT_META,
         color=DARK, bold=True, align=PP_ALIGN.CENTER)
    for x, y, label, c in [(0.7, 1.95, "Discovery", GREEN), (0.7, 3.25, "Mood", CYAN),
                           (0.7, 4.55, "Library", ORANGE), (9.6, 1.95, "Understanding", PURPLE),
                           (9.6, 3.25, "Preferences", RED)]:
        box(s, x, y, 2.9, 0.8, PANEL)
        shape(s, MSO_SHAPE.RECTANGLE, x, y, 0.05, 0.8, c)
        text(s, x + 0.2, y + 0.22, 2.5, 0.4, label, size=FONT_BODY, color=WHITE, bold=True)
        if x < 5:
            arrow(s, x + 2.95, y + 0.25, 1.4, 0.28, c)
        else:
            shape(s, MSO_SHAPE.LEFT_ARROW, x - 1.45, y + 0.25, 1.35, 0.28, c)
    box(s, 8.6, 4.55, 3.9, 1.9, PANEL)
    text(s, 8.9, 4.75, 3.3, 0.28, "10 IDEAS", size=FONT_META, color=a, bold=True)
    text(s, 8.9, 5.15, 3.3, 1.1,
         "Slider · Vibe tags · Library\nPreferences · Understand\nAI chatbot · Ad blocker",
         size=FONT_META, color=MUTED)
    footer(s, 8, a)


def s9(prs):
    s, a = new(prs, 9)
    header(s, 9, "Idea selection", "Weighted: desirability 40% · feasibility 35% · viability 25%", a)
    text(s, 0.7, 1.95, 7.5, 0.28, "WEIGHTED SCORE", size=FONT_META, color=a, bold=True)
    y = 2.35
    for label, score, c in [("Discovery slider", 5.0, GREEN), ("Vibe tags", 5.0, GREEN),
                            ("Save + library", 5.0, GREEN), ("Preferences", 4.65, CYAN),
                            ("Usage logging", 4.2, CYAN), ("AI chatbot", 2.45, RED),
                            ("Ad blocker", 2.8, RED)]:
        text(s, 0.7, y, 2.2, 0.28, label, size=FONT_META, color=WHITE)
        shape(s, MSO_SHAPE.RECTANGLE, 2.9, y + 0.03, 3.7, 0.2, PANEL2)
        shape(s, MSO_SHAPE.RECTANGLE, 2.9, y + 0.03, 3.7 * score / 5, 0.2, c)
        text(s, 6.75, y - 0.02, 0.8, 0.28, f"{score:.2f}", size=FONT_META, color=c, bold=True)
        y += 0.55
    box(s, 7.9, 1.95, 4.7, 4.6, PANEL)
    shape(s, MSO_SHAPE.RECTANGLE, 7.9, 1.95, 0.05, 4.6, a)
    text(s, 8.2, 2.18, 4.1, 0.28, "HYPOTHESES (FIXED EARLY)", size=FONT_META, color=a, bold=True)
    bullets(s, 8.2, 2.6, 4.0, 3.6,
            ["Retrieval time lower", "Taste rating above 2.33", "SUS above 68",
             "α = 0.05 · paired design", "Ad blocker rejected"], accent=a, gap=11)
    footer(s, 9, a)


def s10(prs):
    s, a = new(prs, 10)
    header(s, 10, "Prototype", "Extension → Flask → SQLite · all data local", a)
    for x, label, c in [(0.7, "CHROME\nEXTENSION", GREEN), (4.9, "FLASK\nBACKEND", CYAN),
                        (9.1, "SQLITE\nDATABASE", ORANGE)]:
        box(s, x, 2.1, 3.5, 1.5, PANEL)
        shape(s, MSO_SHAPE.RECTANGLE, x, 2.1, 3.5, 0.06, c)
        text(s, x + 0.1, 2.5, 3.3, 0.8, label, size=FONT_BODY, color=WHITE,
             bold=True, align=PP_ALIGN.CENTER)
    arrow(s, 4.3, 2.65, 0.5, 0.35, GREEN)
    arrow(s, 8.5, 2.65, 0.5, 0.35, CYAN)
    text(s, 0.7, 3.95, 6, 0.28, "KEY FEATURES", size=FONT_META, color=a, bold=True)
    x = 0.7
    for label, c in [("Discover · 3 levels", GREEN), ("Vibe · 8 tags", CYAN),
                     ("My Music · saved list", ORANGE), ("Preferences", PURPLE),
                     ("Usage logging", RED)]:
        box(s, x, 4.35, 2.28, 0.85, PANEL2)
        shape(s, MSO_SHAPE.RECTANGLE, x, 4.35, 2.28, 0.05, c)
        text(s, x + 0.1, 4.6, 2.08, 0.45, label, size=FONT_META, color=WHITE,
             bold=True, align=PP_ALIGN.CENTER)
        x += 2.42
    box(s, 0.7, 5.5, 11.9, 0.9, PANEL)
    text(s, 1.0, 5.75, 11.3, 0.5,
         "Per-platform adapters · 2-second polling · No login · No external API · Responsive dashboard",
         size=FONT_META, color=WHITE, align=PP_ALIGN.CENTER)
    footer(s, 10, a)


def s11(prs):
    s, a = new(prs, 11)
    header(s, 11, "Testing and validation", "Paired design · timed tasks · SUS", a)
    x = 0.7
    for i, (n, label, c) in enumerate([("1", "Recruit", RED), ("2", "3 tasks", ORANGE),
                                       ("3", "SUS form", CYAN), ("4", "Analyse", GREEN)]):
        circle(s, x + 0.42, 2.0, 0.75, c)
        text(s, x + 0.42, 2.16, 0.75, 0.4, n, size=FONT_BODY, color=DARK,
             bold=True, align=PP_ALIGN.CENTER)
        text(s, x, 2.9, 1.6, 0.4, label, size=FONT_META, color=WHITE,
             bold=True, align=PP_ALIGN.CENTER)
        if i < 3:
            arrow(s, x + 1.72, 2.23, 0.55, 0.28, c)
        x += 2.4
    box(s, 0.7, 3.7, 5.7, 2.8, PANEL)
    shape(s, MSO_SHAPE.RECTANGLE, 0.7, 3.7, 0.05, 2.8, a)
    text(s, 1.0, 3.95, 5.1, 0.28, "MEASURES", size=FONT_META, color=a, bold=True)
    bullets(s, 1.0, 4.35, 5.0, 2.0,
            ["Duration per task (ms)", "Clicks and errors counted",
             "SUS 0–100, benchmark 68", "Wilcoxon / paired t-test"], accent=a, gap=9)
    box(s, 6.7, 3.7, 5.9, 2.8, PANEL2)
    text(s, 7.0, 3.95, 5.3, 0.28, "RESULTS STATUS", size=FONT_META, color=GREEN, bold=True)
    text(s, 7.0, 4.4, 5.3, 1.8,
         "Instrument and logging are built.\n\nParticipant runs still being collected — add real SUS and task numbers.",
         size=FONT_BODY, color=WHITE)
    footer(s, 11, a)


def s12(prs):
    s, a = new(prs, 12)
    header(s, 12, "Results and iterations", "Three changes driven by testing and reflection", a)
    y = 1.95
    for n, title, body, c in [
        ("1", "Per-platform adapters", "Single selector broke on YouTube Music; split into one adapter per site.", GREEN),
        ("2", "Companion dashboard", "Saved songs had no view; added a SQLite-backed library.", CYAN),
        ("3", "Usage logging + consent", "Testing needed real measurement; added events and a tracking toggle.", ORANGE),
    ]:
        box(s, 0.7, y, 11.9, 1.4, PANEL)
        circle(s, 0.95, y + 0.32, 0.72, c)
        text(s, 0.95, y + 0.46, 0.72, 0.35, n, size=FONT_BODY, color=DARK,
             bold=True, align=PP_ALIGN.CENTER)
        text(s, 1.9, y + 0.2, 10.2, 0.4, title, size=FONT_BODY, color=WHITE, bold=True)
        text(s, 1.9, y + 0.68, 10.2, 0.55, body, size=FONT_META, color=MUTED)
        y += 1.53
    text(s, 0.7, 6.7, 11.9, 0.25,
         "Add measured SUS and task-time changes once real runs are complete.",
         size=FONT_META, color=MUTED, italic=True)
    footer(s, 12, a)


def s13(prs):
    s, a = new(prs, 13)
    header(s, 13, "Impact and limitations", "Benefits weighed against threats to validity", a)
    box(s, 0.7, 1.95, 5.8, 4.6, PANEL)
    shape(s, MSO_SHAPE.RECTANGLE, 0.7, 1.95, 5.8, 0.06, GREEN)
    text(s, 1.0, 2.2, 5.2, 0.28, "BENEFITS", size=FONT_META, color=GREEN, bold=True)
    bullets(s, 1.0, 2.65, 5.1, 3.6,
            ["No account or login required", "Data never leaves the machine",
             "Works across three platforms", "Addresses the retrieval gap",
             "Built-in measurement"], accent=GREEN, gap=12)
    box(s, 6.8, 1.95, 5.8, 4.6, PANEL)
    shape(s, MSO_SHAPE.RECTANGLE, 6.8, 1.95, 5.8, 0.06, RED)
    text(s, 7.1, 2.2, 5.2, 0.28, "LIMITATIONS", size=FONT_META, color=RED, bold=True)
    bullets(s, 7.1, 2.65, 5.1, 3.6,
            ["n = 18, below target of 30", "78% Spotify; no Apple Music users",
             "Ads (50%) out of scope", "Demo recommendation database",
             "Single-contributor scope"], accent=RED, gap=12)
    footer(s, 13, a)


def s14(prs):
    s, a = new(prs, 14)
    header(s, 14, "Conclusion and future scope", "A small utility addressing a measured gap", a)
    box(s, 0.7, 1.95, 11.9, 1.65, PANEL)
    shape(s, MSO_SHAPE.RECTANGLE, 0.7, 1.95, 0.05, 1.65, a)
    text(s, 1.0, 2.25, 11.2, 1.1,
         "78% save music. 44% struggle to find old saves.\nA private utility closes that loop — without claiming to fix ads.",
         size=FONT_BODY, color=WHITE, bold=True)
    text(s, 0.7, 3.95, 6, 0.28, "FUTURE WORK", size=FONT_META, color=a, bold=True)
    x = 0.7
    for title, body, c in [("Real recommender", "Replace demo data with a learned model", GREEN),
                           ("Understand section", "Lyrics and song meaning", CYAN),
                           ("Larger sample", "30+ responses and a full SUS study", ORANGE)]:
        box(s, x, 4.35, 3.8, 1.85, PANEL)
        shape(s, MSO_SHAPE.RECTANGLE, x, 4.35, 3.8, 0.06, c)
        text(s, x + 0.25, 4.65, 3.3, 0.4, title, size=FONT_BODY, color=WHITE, bold=True)
        text(s, x + 0.25, 5.2, 3.3, 0.9, body, size=FONT_META, color=MUTED)
        x += 3.95
    footer(s, 14, a)


def s15(prs):
    s, a = new(prs, 15)
    shape(s, MSO_SHAPE.RECTANGLE, 0, 0, 0.18, H, GREEN)
    text(s, 0.9, 1.2, 8, 0.3, "REFERENCES & Q&A", size=FONT_META, color=GREEN, bold=True)
    text(s, 0.9, 1.85, 11, 1.1, "Thank you.", size=FONT_HERO, color=WHITE, bold=True)
    text(s, 0.95, 3.0, 8, 0.6, "Questions?", size=FONT_BODY, color=GREEN, bold=True)
    bullets(s, 0.95, 4.1, 8.5, 2.0,
            ["Anonymised survey dataset (R01–R18)", "Integrated assignment brief",
             "Libraries: Flask, pandas, SciPy, matplotlib", "AI tooling disclosed per brief"],
            accent=GREEN, gap=9)
    footer(s, 15, a)


SLIDE_BUILDERS = [s1, s2, s3, s4, s5, s6, s7, s8, s9, s10, s11, s12, s13, s14, s15]


def main():
    notes_list = json.loads(NOTES_FILE.read_text()) if NOTES_FILE.exists() else []
    prs = Presentation()
    prs.slide_width = Inches(W)
    prs.slide_height = Inches(H)
    for i, builder in enumerate(SLIDE_BUILDERS):
        builder(prs)
        if i < len(notes_list):
            prs.slides[i].notes_slide.notes_text_frame.text = notes_list[i]
    prs.save(OUT)

    sizes = set()
    for slide in prs.slides:
        for shp in slide.shapes:
            if shp.has_text_frame:
                for par in shp.text_frame.paragraphs:
                    for run in par.runs:
                        if run.font.size:
                            sizes.add(round(run.font.size.pt))
    print(f"Wrote {OUT} — {len(SLIDE_BUILDERS)} slides")
    print("Font sizes used:", sorted(sizes), "(allowed:", FONTS, ")")


if __name__ == "__main__":
    main()
