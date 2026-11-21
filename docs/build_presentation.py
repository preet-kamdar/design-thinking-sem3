#!/usr/bin/env python3
"""Generate the official 20-slide presentation deck.

Design system
-------------
* Exactly TWO font sizes: 36 (hero) and 20 (everything else). Bold is used
  only on hero text. ``fs()`` snaps requests to these two; ``fit_height()``
  grows text boxes using the same measurement as check_layout.py, so overflow
  is 0.
* OFFICIAL "Dandadan tinted" theme: pale lime background `#F2F7EA`, two dark
  green text inks, soft cream-yellow / green / teal boxes, dark red only for
  limitations. ONE 3pt dark border per box. The five real survey charts are
  placed full-width on their own evidence slides, never squeezed into a corner.
* Subtle vinyl records appear on a curated set of slides, each placed by hand
  in empty space or behind an opaque box so they never cover text. Only the
  bottom-right slide number is shown. Text is vertically centred in its box.
* Charts are generated with grids and large labels by
  webapp/analysis/analysis.py.
* ``--crease`` builds a trial copy with folded-paper background creases; the
  official deck is unchanged by that flag.

Extending
---------
1. Add a builder function ``sN(prs)`` that calls ``new(prs, N)``.
2. Append it to ``SLIDE_BUILDERS`` and add a note to slide_notes.json.
3. Update the numbered builder calls if you insert a slide mid-deck.
"""

import argparse
import json
from pathlib import Path

from PIL import Image, ImageFont
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
WHITE = RGBColor(255, 255, 255)
CREASE = False                       # --crease adds trial folded-paper folds
CREASE_DARK = RGBColor(214, 227, 205)
BG = WHITE                           # slide background (palette-dependent)
INK = RGBColor(0, 0, 0)              # ink on the bright boxes
BG_INK = RGBColor(0, 0, 0)           # ink on the slide background
BLACK = INK
DARK = INK

# A deliberately TINY palette: three bright colours, used consistently.
# Green and purple are gone; yellow and blue are brighter; coral owns the
# "caution / limitation" role. Fewer colours reads as more professional.
SUN = RGBColor(255, 226, 46)        # FFE22E — bright, popping yellow
AQUA = RGBColor(94, 214, 200)       # 5ED6C8 — bridge between yellow and blue
BLUE = RGBColor(69, 196, 248)       # 45C4F8 — bright sky blue
CORAL = RGBColor(255, 118, 118)     # FF7676 — bright coral

SUN_SOFT = RGBColor(255, 247, 205)
AQUA_SOFT = RGBColor(218, 246, 241)
BLUE_SOFT = RGBColor(214, 241, 252)
CORAL_SOFT = RGBColor(255, 226, 226)

# Legacy names map onto the 3-colour palette so existing slide code keeps
# working without a rewrite. Text is black regardless of what is passed in.
GREEN = SUN
CYAN = BLUE
ORANGE = CORAL
PURPLE = AQUA
RED = CORAL
AMBER = SUN
LILAC = AQUA_SOFT
SKY = BLUE_SOFT
MINT = SUN_SOFT
PEACH = SUN_SOFT
ROSE = CORAL_SOFT

PANEL = WHITE
PANEL2 = WHITE
MUTED = INK
T_HEAD = INK
T_BODY = INK
T_MUTED = INK
T_GREEN = INK
T_AMBER = INK
T_PURPLE = INK
T_RED = INK

# (box colour, decorative colour, accent) — one box colour per slide.
# Slides step gently through yellow → aqua → blue so the change between
# consecutive slides is soft rather than a jarring jump. Coral marks limits.
THEME = [
    (SUN, SUN_SOFT, SUN),
    (AQUA, AQUA_SOFT, AQUA),
    (BLUE, BLUE_SOFT, BLUE),
    (BLUE, BLUE_SOFT, BLUE),
    (AQUA, AQUA_SOFT, AQUA),
    (SUN, SUN_SOFT, SUN),
    (SUN, SUN_SOFT, SUN),
    (AQUA, AQUA_SOFT, AQUA),
    (BLUE, BLUE_SOFT, BLUE),
    (BLUE, BLUE_SOFT, BLUE),
    (CORAL, CORAL_SOFT, CORAL),
    (AQUA, AQUA_SOFT, AQUA),
    (SUN, SUN_SOFT, SUN),
    (SUN, SUN_SOFT, SUN),
    (AQUA, AQUA_SOFT, AQUA),
]

# --- Trial palettes -------------------------------------------------------- #
# Each entry maps to the four roles used by the slide code. The "soft" colours
# are auto-derived for the faint decorative shapes. Dark reference hues are
# lightened here so black text stays readable on every box.
# OFFICIAL THEME — Dandadan tinted. No trials remain; this is the deck.
PALETTES = {
    "official": dict(primary="F5E3A0", bridge="ADFB70", secondary="2FB4C2",
                     limit="B73B36", limit_box="E89A8A",
                     bg="F2F7EA", ink="0E3B2A", bg_ink="1B5E3F"),
}
THEME_ORDER = ("primary", "bridge", "secondary", "secondary", "bridge",
               "primary", "primary", "bridge", "secondary", "secondary",
               "limit", "bridge", "primary", "primary", "bridge")


def _rgb(h):
    return RGBColor(int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16))


def _soft(c, mix=0.78):
    return RGBColor(*[int(v + (255 - v) * mix) for v in tuple(c)])


def apply_palette(name):
    """Swap every colour role, then rebuild THEME in the same soft order."""
    global SUN, AQUA, BLUE, CORAL, SUN_SOFT, AQUA_SOFT, BLUE_SOFT, CORAL_SOFT
    global THEME, GREEN, CYAN, ORANGE, PURPLE, RED, AMBER, LILAC, SKY, MINT, PEACH, ROSE
    global BG, INK, BG_INK, LIMIT_BOX
    p = PALETTES[name]
    BG, INK, BG_INK = _rgb(p["bg"]), _rgb(p["ink"]), _rgb(p["bg_ink"])
    LIMIT_BOX = _rgb(p.get("limit_box", p["limit"]))
    SUN, AQUA, BLUE, CORAL = (_rgb(p[k]) for k in
                              ("primary", "bridge", "secondary", "limit"))
    SUN_SOFT, AQUA_SOFT, BLUE_SOFT, CORAL_SOFT = (
        _soft(c) for c in (SUN, AQUA, BLUE, CORAL))
    GREEN = AMBER = SUN
    CYAN = BLUE
    PURPLE = AQUA
    ORANGE = RED = CORAL
    LILAC = AQUA_SOFT
    SKY = BLUE_SOFT
    MINT = PEACH = SUN_SOFT
    ROSE = CORAL_SOFT
    # The limitations slide gets a LIGHTER box fill so dark box-ink stays
    # readable, while the stripe/accent keeps the true dark red of the source
    # palette. Palettes without limit_box use the limit colour for both.
    limit_box = _rgb(p.get("limit_box", p["limit"]))
    colors = dict(primary=SUN, bridge=AQUA, secondary=BLUE, limit=limit_box)
    softs = dict(primary=SUN_SOFT, bridge=AQUA_SOFT,
                 secondary=BLUE_SOFT, limit=_soft(limit_box))
    accents = dict(primary=SUN, bridge=AQUA, secondary=BLUE, limit=CORAL)
    THEME = [(colors[r], softs[r], accents[r]) for r in THEME_ORDER]


# Only TWO type sizes: a hero for titles/big numbers, one size for everything
# else. Bold is reserved for hero text, so a slide no longer reads as a mess
# of competing sizes and weights.
FONT_HERO, FONT_BODY, FONT_META = 36, 20, 20
FONTS = (FONT_HERO, FONT_BODY)              # the ONLY font sizes allowed


def text_color(color, on_panel=True):
    """Dark ink in two matching shades: one for boxes, one for the background."""
    return INK if on_panel else BG_INK


def _on_panel(slide, x, y):
    """True when a text box sits inside an already-drawn coloured shape.

    Circles count too (e.g. numbered step badges): their numbers need the same
    dark box-ink as text on rounded rectangles, not the lighter background ink.
    Tiny decorative ovals are excluded.
    """
    for sh in slide.shapes:
        if sh.shape_type == 1 and sh.auto_shape_type in (
                MSO_SHAPE.ROUNDED_RECTANGLE, MSO_SHAPE.OVAL):
            l, t = sh.left / 914400, sh.top / 914400
            w, h = sh.width / 914400, sh.height / 914400
            if w >= 0.3 and h >= 0.3 and l <= x <= l + w and t <= y <= t + h:
                return True
    return False

W, H = 13.333, 7.5


def fs(size: int) -> int:
    """Snap any requested size to the nearest of the three allowed sizes."""
    return min(FONTS, key=lambda f: abs(f - size))


# --- Conservative text measurement (mirrors docs/check_layout.py) ----------- #
_FONT_PATH = "/usr/share/fonts/TTF/DejaVuSans.ttf"
_FONT_CACHE = {}


def _pil_font(pt):
    key = max(1, int(round(pt * 96 / 72)))
    if key not in _FONT_CACHE:
        try:
            _FONT_CACHE[key] = ImageFont.truetype(_FONT_PATH, key)
        except Exception:
            _FONT_CACHE[key] = None
    return _FONT_CACHE[key]


def _wrap_lines(part, pt, width_in):
    font = _pil_font(pt)
    avail_w = max(1, width_in * 96 - 6)          # 0.06" of text-box margins
    lines, cur = 0, ""
    for word in str(part).split():
        trial = (cur + " " + word).strip()
        if font and (font.getlength(trial) <= avail_w or not cur):
            cur = trial
        else:
            lines += 1
            cur = word
    return max(1, lines + 1 if cur else lines)


def fit_height(height_in, width_in, paras):
    """Grow a text box so larger fonts never overflow its own box.

    ``paras`` is a list of ``(text, pt, space_after_pt)``. Uses DejaVuSans,
    the same deliberately-wide stand-in the layout checker uses, plus a small
    safety margin.
    """
    needed = 0.0
    for part, pt, gap in paras:
        needed += _wrap_lines(part, pt, width_in) * (pt * 96 / 72 * 1.2)
        needed += gap * 96 / 72
    return max(height_in, (needed + 4) / 96)


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


def box(slide, x, y, w, h, fill=None, line=None):
    # Full bright fill + one bold black border. No per-box vinyl/dot motifs —
    # the record now lives at slide level (see vinyl_record) so it is spread
    # around the slide instead of repeated in every box corner.
    accent = getattr(slide, "_pme_accent", GREEN)
    panel = shape(slide, MSO_SHAPE.ROUNDED_RECTANGLE, x, y, w, h,
                  accent, line or INK)
    panel.line.width = Pt(3.0)
    return panel


def tinted_box(slide, x, y, w, h, fill, line=None):
    """A rounded panel with an explicit fill colour, for one-off accent boxes."""
    panel = shape(slide, MSO_SHAPE.ROUNDED_RECTANGLE, x, y, w, h,
                  fill, line or INK)
    panel.line.width = Pt(3.0)
    return panel


def circle(slide, x, y, d, fill):
    return shape(slide, MSO_SHAPE.OVAL, x, y, d, d, fill)


def text(slide, x, y, w, h, value, size=FONT_BODY, color=T_BODY, bold=False,
         align=PP_ALIGN.LEFT, valign=MSO_ANCHOR.MIDDLE, italic=False):
    on_panel = _on_panel(slide, x, y)
    tb = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    tf = tb.text_frame
    tf.word_wrap = True
    tf.vertical_anchor = valign
    tf.margin_left = tf.margin_right = Inches(0.03)
    tf.margin_top = tf.margin_bottom = Inches(0.01)
    for i, part in enumerate(str(value).split("\n")):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.alignment = align
        p.space_after = Pt(1)
        r = p.add_run()
        r.text = part
        r.font.size = Pt(fs(size))
        r.font.bold = bool(bold and fs(size) == FONT_HERO)
        r.font.italic = italic
        r.font.color.rgb = text_color(color, on_panel)
        r.font.name = "Calibri"
    pt = fs(size)
    fitted = fit_height(h, w, [(p, pt, 0) for p in str(value).split("\n")])
    tb.height = Inches(fitted)
    # With vertical_anchor=MIDDLE, growing the box would slide the visible
    # text DOWN by half the growth. Compensate so the centre stays put.
    if fitted > h:
        tb.top = Inches(y - (fitted - h) / 2)
    return tb


def centered_text(slide, x, y, w, h, value, size=FONT_BODY, color=T_BODY,
                  bold=False):
    """Pin text to the exact centre of a rectangle (no height auto-growth)."""
    on_panel = _on_panel(slide, x, y)
    tb = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    tf = tb.text_frame
    tf.word_wrap = True
    tf.vertical_anchor = MSO_ANCHOR.MIDDLE
    tf.margin_left = tf.margin_right = Inches(0.02)
    tf.margin_top = tf.margin_bottom = 0
    for i, part in enumerate(str(value).split("\n")):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.alignment = PP_ALIGN.CENTER
        p.space_after = Pt(0)
        r = p.add_run()
        r.text = part
        r.font.size = Pt(fs(size))
        r.font.bold = bool(bold and fs(size) == FONT_HERO)
        r.font.color.rgb = text_color(color, on_panel)
        r.font.name = "Calibri"
    return tb


def bullets(slide, x, y, w, h, items, color=T_BODY, accent=T_AMBER, gap=6):
    on_panel = _on_panel(slide, x, y)
    tb = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    tf = tb.text_frame
    tf.word_wrap = True
    tf.vertical_anchor = MSO_ANCHOR.MIDDLE
    tf.margin_top = tf.margin_bottom = 0
    for i, item in enumerate(items):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        b = p.add_run(); b.text = "●  "
        b.font.size = Pt(FONT_META if len(item) > 48 else FONT_BODY)
        b.font.color.rgb = text_color(accent or color, on_panel); b.font.name = "Calibri"
        r = p.add_run(); r.text = item
        r.font.size = Pt(FONT_META if len(item) > 48 else FONT_BODY)
        r.font.color.rgb = text_color(color, on_panel); r.font.name = "Calibri"
        p.space_after = Pt(gap if i < len(items) - 1 else 0)
    paras = [("●  " + item, FONT_META if len(item) > 48 else FONT_BODY, gap)
             for item in items]
    fitted = fit_height(h, w, paras)
    tb.height = Inches(fitted)
    if fitted > h:
        tb.top = Inches(y - (fitted - h) / 2)
    return tb


def header(slide, index, title, subtitle, accent):
    # Only ONE slide number (the bottom-right footer). The old top-left
    # "NN / 15" kicker was a duplicate and is removed.
    text(slide, 0.7, 0.55, 12, 0.65, title, size=FONT_HERO, color=WHITE, bold=True)
    if subtitle:
        text(slide, 0.72, 1.23, 11.8, 0.35, subtitle, size=FONT_META, color=MUTED)
    shape(slide, MSO_SHAPE.RECTANGLE, 0.7, 1.65, 1.0, 0.05, accent)


def footer(slide, index, accent):
    text(slide, 0.7, 6.95, 9, 0.35, "Reimagining the Personal Music Experience",
         size=FONT_META, color=MUTED)
    text(slide, 11.85, 6.95, 0.8, 0.35, f"{index:02d}", size=FONT_META,
         color=T_AMBER, align=PP_ALIGN.RIGHT)


def stat_card(slide, x, y, w, h, big, label, accent):
    box(slide, x, y, w, h, PANEL)
    text(slide, x + 0.22, y + 0.16, w - 0.4, 0.7, big, size=FONT_HERO, color=T_GREEN, bold=True)
    text(slide, x + 0.22, y + 0.95, w - 0.4, h - 1.0, label, size=FONT_META, color=MUTED)


def feature_card(slide, x, y, w, h, tag, title, body, accent):
    box(slide, x, y, w, h, PANEL)
    circle(slide, x + 0.22, y + 0.22, 0.42, accent)
    centered_text(slide, x + 0.22, y + 0.22, 0.42, 0.42, tag,
                  size=FONT_META, color=DARK, bold=True)
    text(slide, x + 0.78, y + 0.22, w - 0.95, 0.4, title, size=FONT_BODY, color=WHITE, bold=True)
    text(slide, x + 0.28, y + 0.8, w - 0.55, h - 0.9, body, size=FONT_META, color=MUTED)


def arrow(slide, x, y, w=0.5, h=0.3, color=GREEN):
    return shape(slide, MSO_SHAPE.RIGHT_ARROW, x, y, w, h, color)


def chart_frame(slide, x, y, w, h, filename, pad=0.05):
    """White framed panel with the generated chart fitted inside, full size."""
    frame = shape(slide, MSO_SHAPE.ROUNDED_RECTANGLE, x, y, w, h, WHITE, INK)
    frame.line.width = Pt(2.5)
    chart = CHARTS / filename
    if not chart.exists():
        text(slide, x, y + h / 2, w, 0.4,
             "Chart missing — re-run webapp/analysis/analysis.py",
             size=FONT_META, color=T_RED, align=PP_ALIGN.CENTER)
        return
    with Image.open(chart) as im:
        iw, ih = im.size
    scale = min((w - 2 * pad) / iw, (h - 2 * pad) / ih)
    pw, ph = iw * scale, ih * scale
    slide.shapes.add_picture(str(chart), Inches(x + (w - pw) / 2),
                             Inches(y + (h - ph) / 2),
                             width=Inches(pw), height=Inches(ph))


def takeaway(slide, index, message):
    """One honest reading line under a chart, above the footer."""
    box(slide, 0.7, 6.35, 11.9, 0.5, PANEL)
    text(slide, 0.95, 6.47, 11.4, 0.3, message, size=FONT_META, color=MUTED)
    footer(slide, index, getattr(slide, "_pme_accent", GREEN))


# --------------------------------------------------------------------------- #
# Decoration — pale tinted background, occasional subtle vinyl disc
# --------------------------------------------------------------------------- #
def vinyl_record(slide, cx, cy, d, label_color):
    """One readable vinyl disc: dark disc, grooves, coloured label + spindle."""
    disc = shape(slide, MSO_SHAPE.OVAL, cx - d / 2, cy - d / 2, d, d, INK)
    set_opacity(disc, 18)
    for frac, op in ((0.84, 24), (0.68, 30), (0.52, 38), (0.38, 46)):
        r = d * frac
        ring = slide.shapes.add_shape(MSO_SHAPE.OVAL, Inches(cx - r / 2),
                                      Inches(cy - r / 2), Inches(r), Inches(r))
        ring.fill.background()
        ring.line.color.rgb = INK
        ring.line.width = Pt(1.3)
        set_opacity(ring, op)
    lr = d * 0.30
    label = shape(slide, MSO_SHAPE.OVAL, cx - lr / 2, cy - lr / 2, lr, lr,
                  label_color)
    set_opacity(label, 72)
    hole = shape(slide, MSO_SHAPE.OVAL, cx - 0.04, cy - 0.04, 0.08, 0.08, WHITE)
    set_opacity(hole, 85)


def paper_creases(slide):
    """Trial-only folded-paper texture covering the whole slide background.

    The texture is generated by make_crease.py: overlapping wavy bands with
    soft shadow + highlight gradients, so the creases bend, break and read as
    folds rather than hard straight lines.
    """
    tex = HERE / "crease_background.png"
    if tex.exists():
        slide.shapes.add_picture(str(tex), 0, 0, width=Inches(W), height=Inches(H))


# Records are an occasional motif, never wallpaper. Each sits at a slide
# corner with its centre just outside the canvas, so a clean quarter-disc
# shows — visible, but never over text. Drawn before content as a safeguard.
# (slide -> centre x, centre y, diameter)
VINYL_SPOTS = {
    1:  (11.00, 2.80, 3.0),   # large disc in the empty right of the title slide
    4:  (13.55, 6.35, 2.0),   # bottom-right corner sliver
    6:  (-0.45, 6.40, 2.0),   # bottom-left corner sliver
    12: (13.55, 6.35, 2.0),   # bottom-right corner sliver
    15: (-0.40, 1.55, 2.0),   # top-left corner sliver
    18: (13.55, 1.55, 2.0),   # top-right corner sliver
    20: (11.10, 3.90, 3.2),   # large disc in the empty right of the Q&A slide
}


def decorate(slide, index: int) -> RGBColor:
    box_color, deco_color, accent = THEME[(index - 1) % len(THEME)]

    # Background fill comes from the chosen palette.
    bg = shape(slide, MSO_SHAPE.RECTANGLE, 0, 0, W, H, BG)
    bg.line.fill.background()
    if CREASE:
        paper_creases(slide)

    # Bold accent stripe down the left edge.
    shape(slide, MSO_SHAPE.RECTANGLE, 0, 0, 0.20, H, accent)

    # One subtle record per curated slide, placed by hand so it never covers
    # text. Drawn before content, so boxes always sit above it.
    if index in VINYL_SPOTS:
        cx, cy, d = VINYL_SPOTS[index]
        vinyl_record(slide, cx, cy, d, box_color)

    # Small confetti dots in the top-right corner.
    for i in range(4):
        dot = shape(slide, MSO_SHAPE.OVAL, 12.1 + (i % 2) * 0.35,
                    0.5 + (i // 2) * 0.35, 0.12, 0.12, accent)
        set_opacity(dot, 55)

    return box_color


# --------------------------------------------------------------------------- #
# Slides — each builder adds its slide then decorates it
# --------------------------------------------------------------------------- #
def new(prs, index):
    s = prs.slides.add_slide(prs.slide_layouts[6])
    a = decorate(s, index)
    s._pme_accent = a          # box() reads this to tint every panel consistently
    return s, a


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
    stat_card(s, 0.7, 2.0, 3.7, 2.2, "78%", "use their app daily or\nseveral times a week", a)
    stat_card(s, 4.8, 2.0, 3.7, 2.2, "61%", "say taste is only 'somewhat'\nor 'poorly' understood", ORANGE)
    stat_card(s, 8.9, 2.0, 3.7, 2.2, "39%", "say taste is understood\n'very well'", GREEN)
    box(s, 0.7, 4.35, 11.9, 1.9, PANEL)
    text(s, 1.0, 4.6, 11.2, 0.3, "THE QUESTION", size=FONT_META, color=T_AMBER, bold=True)
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
                 "A personal library makes saved songs easy to find.", GREEN)
    feature_card(s, 8.8, 1.95, 3.8, 2.2, "3", "Prove with data",
                 "Statistics show which pain points the design addresses.", GREEN)
    text(s, 0.7, 4.5, 6, 0.28, "OUTCOMES", size=FONT_META, color=T_AMBER, bold=True)
    chips = ["Chrome extension", "Flask + SQLite",
             "Responsive dashboard", "Re-runnable analysis"]
    x = 0.7
    for label in chips:
        box(s, x, 4.9, 2.85, 1.0, PANEL2)
        centered_text(s, x, 4.9, 2.85, 1.0, label, size=FONT_META,
                      color=WHITE, bold=True)
        x += 3.0
    footer(s, 3, a)


def s4(prs):
    s, a = new(prs, 4)
    header(s, 4, "User research", "Convenience sample · n = 18 · ages 18–30 (median 19)", a)
    text(s, 0.7, 1.98, 5.5, 0.28, "PRIMARY PLATFORM", size=FONT_META, color=T_AMBER, bold=True)
    y = 2.4
    for label, pct, c in [("Spotify", 78, GREEN), ("YouTube Music", 17, CYAN), ("Other", 5, ORANGE)]:
        text(s, 0.7, y, 2.1, 0.3, label, size=FONT_META, color=WHITE)
        shape(s, MSO_SHAPE.RECTANGLE, 2.8, y + 0.05, 3.9, 0.24, PANEL2)
        shape(s, MSO_SHAPE.RECTANGLE, 2.8, y + 0.05, 3.9 * pct / 100, 0.24, c)
        text(s, 6.85, y - 0.02, 0.8, 0.3, f"{pct}%", size=FONT_META, color=c, bold=True)
        y += 0.65
    box(s, 8.1, 1.98, 4.5, 3.3, PANEL)
    text(s, 8.4, 2.2, 4.0, 0.28, "METHOD", size=FONT_META, color=T_AMBER, bold=True)
    bullets(s, 8.4, 2.6, 3.9, 2.3,
            ["MCQ + ordinal + numeric + open", "78% Spotify — platform imbalance",
             "Below target of 30 — declared"], accent=T_AMBER, gap=8)
    box(s, 0.7, 5.4, 11.9, 1.1, PANEL)
    text(s, 1.0, 5.62, 11.2, 0.6,
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
        text(s, x + 0.25, y + 0.18, 5.3, 0.28, label, size=FONT_META, color=c, bold=True)
        bullets(s, x + 0.25, y + 0.58, 5.3, 1.3, items, accent=c, gap=4)
    footer(s, 5, a)


def s6(prs):
    s, a = new(prs, 6)
    header(s, 6, "Statistical findings", "Ordinal 1–3 · neutral = 2 · one-sample t-tests", a)
    stat_card(s, 0.7, 2.0, 3.7, 1.8, "2.50", "Vibe ease · p = 0.003", GREEN)
    stat_card(s, 4.8, 2.0, 3.7, 1.8, "2.33", "Taste · p = 0.029", a)
    stat_card(s, 8.9, 2.0, 3.7, 1.8, "2.11", "Retrieval · p = 0.651", ORANGE)
    box(s, 0.7, 4.0, 11.9, 2.25, PANEL)
    text(s, 1.0, 4.25, 11.2, 0.3, "HONEST READING", size=FONT_META, color=T_AMBER, bold=True)
    text(s, 1.0, 4.72, 11.2, 1.3,
         "Above neutral ≠ unhappy. This is a good-but-not-great baseline.\n"
         "We claim refinement, not rescue — every distribution follows on the next five slides.",
         size=FONT_BODY, color=MUTED)
    footer(s, 6, a)


# --- Five full-size evidence slides: every real chart gets its own slide ---- #
def s7(prs):
    s, a = new(prs, 7)
    header(s, 7, "Evidence 1 · platform and usage", "Who answered, and how often they listen", a)
    chart_frame(s, 0.7, 1.95, 11.9, 4.3, "platform_and_frequency.png")
    takeaway(s, 7, "Spotify 78%; 9 listen daily. The platform imbalance is a stated limitation.")


def s8(prs):
    s, a = new(prs, 8)
    header(s, 8, "Evidence 2 · discovery and saving", "How tracks are found and kept", a)
    chart_frame(s, 0.7, 1.95, 11.9, 4.3, "discovery_and_saving.png")
    takeaway(s, 8, "33% discover outside apps; 78% save tracks. That gap is our design target.")


def s9(prs):
    s, a = new(prs, 9)
    header(s, 9, "Evidence 3 · ordinal distributions", "Counts behind the three baseline tests", a)
    chart_frame(s, 0.7, 1.95, 11.9, 4.3, "ordinal_distributions.png")
    takeaway(s, 9, "Vibe 2.50 (p .003) and taste 2.33 (p .029) beat neutral; retrieval does not.")


def s10(prs):
    s, a = new(prs, 10)
    header(s, 10, "Evidence 4 · age and score spread", "Sample profile and ordinal spread", a)
    chart_frame(s, 0.7, 1.95, 11.9, 4.3, "age_and_boxplots.png")
    takeaway(s, 10, "17 numeric ages, mean 19.7. Retrieval spread is widest — directional only.")


def s11(prs):
    s, a = new(prs, 11)
    header(s, 11, "Evidence 5 · correlations", "Spearman rho · n = 18 · critical |r| ≈ 0.468", a)
    # A wide heatmap plus a compact reading panel with the three key pairs,
    # so the slide carries real detail instead of a sea of empty space.
    chart_frame(s, 0.7, 1.95, 8.1, 4.15, "correlation_heatmap.png")
    box(s, 9.0, 1.95, 3.6, 4.15, PANEL)
    text(s, 9.25, 2.15, 3.1, 0.3, "KEY PAIRS (rho)", size=FONT_META,
         color=T_AMBER, bold=True)
    text(s, 9.25, 2.85, 3.1, 2.1,
         "Usage–Vibe   −0.45\n"
         "Vibe–Save    +0.36\n"
         "Save–Taste   +0.31",
         size=FONT_META, color=MUTED)
    text(s, 9.25, 5.15, 3.1, 0.8,
         "None reach critical.\nWeak, non-signal.",
         size=FONT_META, color=T_AMBER, bold=True)
    box(s, 0.7, 6.25, 11.9, 0.5, PANEL2)
    text(s, 0.95, 6.35, 11.4, 0.3,
         "No coefficient is significant — we describe associations, never causation.",
         size=FONT_META, color=MUTED)
    footer(s, 11, a)


def s12(prs):
    s, a = new(prs, 12)
    header(s, 12, "Define", "Persona · POV · HMW · MoSCoW", a)
    box(s, 0.7, 1.95, 3.9, 4.65, PANEL)
    circle(s, 1.85, 2.2, 1.1, GREEN)
    text(s, 1.85, 2.42, 1.1, 0.7, "A", size=FONT_HERO, color=DARK,
         bold=True, align=PP_ALIGN.CENTER)
    text(s, 0.95, 3.38, 3.4, 0.72, "Aarav, 19", size=FONT_HERO, color=WHITE,
         bold=True, align=PP_ALIGN.CENTER)
    text(s, 0.95, 4.25, 3.4, 2.1,
         "B.Tech student · 19\nDaily Spotify listener\nSaves but rarely revisits\nWants mood-based choice",
         size=FONT_META, color=MUTED, align=PP_ALIGN.CENTER)
    box(s, 4.85, 1.95, 7.75, 2.2, PANEL2)
    text(s, 5.15, 2.15, 7.1, 0.28, "POINT OF VIEW", size=FONT_META, color=T_AMBER, bold=True)
    text(s, 5.15, 2.55, 7.1, 1.3,
         "A listener who saves but cannot rediscover, and feels recommendations only 'somewhat' match their taste, needs familiarity control and mood-based retrieval.",
         size=FONT_BODY, color=WHITE)
    box(s, 4.85, 4.2, 7.75, 1.05, PANEL)
    text(s, 5.15, 4.4, 7.1, 0.6,
         "HMW: give that control without a paid subscription?",
         size=FONT_BODY, color=CYAN, bold=True)
    box(s, 4.85, 5.3, 7.75, 1.3, PANEL)
    text(s, 5.15, 5.5, 7.1, 0.28, "MOSCOW", size=FONT_META, color=ORANGE, bold=True)
    text(s, 5.15, 5.85, 7.1, 0.6,
         "Must: Discover, My Music, backend   |   Won't: ads, offline downloads",
         size=FONT_META, color=WHITE)
    footer(s, 12, a)


def s13(prs):
    s, a = new(prs, 13)
    header(s, 13, "Ideation", "10 generated ideas · one mind map", a)
    # One central topic, five branches in an even row, and a full-width idea
    # list below — the old scattered layout left most of the slide empty.
    box(s, 4.85, 1.95, 3.6, 0.85, GREEN)
    centered_text(s, 4.85, 1.95, 3.6, 0.85, "PERSONAL MUSIC EXPERIENCE",
                  size=FONT_META, color=DARK, bold=True)
    branches = ["Discovery", "Mood", "Library", "Understanding", "Preferences"]
    x = 0.7
    for label in branches:
        box(s, x, 3.35, 2.2, 0.8, PANEL)
        centered_text(s, x, 3.35, 2.2, 0.8, label,
                      size=FONT_BODY, color=WHITE, bold=True)
        shape(s, MSO_SHAPE.DOWN_ARROW, x + 1.0, 2.82, 0.2, 0.5, GREEN)
        x += 2.42
    box(s, 0.7, 4.65, 11.9, 2.05, PANEL)
    text(s, 1.0, 4.82, 11.2, 0.3, "10 IDEAS", size=FONT_META,
         color=T_AMBER, bold=True)
    # Both columns use an identical, generously sized fixed box so their
    # contents sit on the same line instead of drifting apart via auto-grow.
    text(s, 1.0, 5.18, 5.4, 1.5,
         "1  Familiar/Balanced/Exploratory slider\n"
         "2  Vibe-tag browser  ·  3  Save button\n"
         "4  Library page  ·  5  Track context",
         size=FONT_META, color=MUTED)
    text(s, 6.8, 5.18, 5.4, 1.5,
         "6  Preference panel  ·  7  Usage logging\n"
         "8  Understand panel  ·  9  AI chatbot\n"
         "10  In-app ad blocker",
         size=FONT_META, color=MUTED)
    footer(s, 13, a)


def s14(prs):
    s, a = new(prs, 14)
    header(s, 14, "Idea selection", "Weighted: desirability 40% · feasibility 35% · viability 25%", a)
    text(s, 0.7, 1.95, 7.5, 0.28, "WEIGHTED SCORE", size=FONT_META, color=T_AMBER, bold=True)
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
    tinted_box(s, 7.9, 1.95, 4.7, 3.25, LIMIT_BOX)
    text(s, 8.2, 2.18, 4.1, 0.28, "HYPOTHESES (FIXED EARLY)", size=FONT_META, color=T_AMBER, bold=True)
    bullets(s, 8.2, 2.55, 4.0, 2.35,
            ["Retrieval time lower", "Taste rating above 2.33", "SUS above 68",
             "α = 0.05 · paired design", "Ad blocker rejected"], accent=T_AMBER, gap=11)
    footer(s, 14, a)


def s15(prs):
    s, a = new(prs, 15)
    header(s, 15, "Prototype", "Extension → Flask → SQLite · all data local", a)
    for x, label, c in [(0.7, "CHROME\nEXTENSION", GREEN), (4.9, "FLASK\nBACKEND", CYAN),
                        (9.1, "SQLITE\nDATABASE", ORANGE)]:
        box(s, x, 2.1, 3.5, 1.5, PANEL)
        text(s, x + 0.1, 2.5, 3.3, 0.8, label, size=FONT_BODY, color=WHITE,
             bold=True, align=PP_ALIGN.CENTER)
    arrow(s, 4.3, 2.65, 0.5, 0.35, GREEN)
    arrow(s, 8.5, 2.65, 0.5, 0.35, CYAN)
    text(s, 0.7, 3.95, 6, 0.28, "KEY FEATURES", size=FONT_META, color=T_AMBER, bold=True)
    x = 0.7
    for label, c in [("Discover · 3 levels", GREEN), ("Vibe · 8 tags", CYAN),
                     ("My Music · saved list", ORANGE), ("Preferences", PURPLE),
                     ("Usage logging", RED)]:
        box(s, x, 4.35, 2.28, 1.05, PANEL2)
        text(s, x + 0.1, 4.6, 2.08, 0.45, label, size=FONT_META, color=WHITE,
             bold=True, align=PP_ALIGN.CENTER)
        x += 2.42
    box(s, 0.7, 5.5, 11.9, 1.05, PANEL)
    text(s, 1.0, 5.75, 11.3, 0.5,
         "Per-platform adapters · 2-second polling · No login · No external API · Responsive dashboard",
         size=FONT_META, color=WHITE, align=PP_ALIGN.CENTER)
    footer(s, 15, a)


def s16(prs):
    s, a = new(prs, 16)
    header(s, 16, "Testing and validation", "Paired design · timed tasks · SUS", a)
    x = 0.7
    # All four step badges share the bridge green; the arrows match so the
    # sequence reads as one flow. (Slide 17 uses the blue instead.)
    for i, (n, label) in enumerate([("1", "Recruit"), ("2", "3 tasks"),
                                    ("3", "SUS form"), ("4", "Analyse")]):
        circle(s, x + 0.42, 2.0, 0.75, AQUA)
        centered_text(s, x + 0.42, 2.0, 0.75, 0.75, n,
                      size=FONT_BODY, color=DARK, bold=True)
        centered_text(s, x, 2.9, 1.6, 0.4, label,
                      size=FONT_META, color=WHITE, bold=True)
        if i < 3:
            arrow(s, x + 1.72, 2.23, 0.55, 0.28, AQUA)
        x += 2.4
    box(s, 0.7, 3.7, 5.7, 2.8, PANEL)
    text(s, 1.0, 3.95, 5.1, 0.28, "MEASURES", size=FONT_META, color=T_AMBER, bold=True)
    bullets(s, 1.0, 4.35, 5.0, 2.0,
            ["Duration per task (ms)", "Clicks and errors counted",
             "SUS 0–100, benchmark 68", "Wilcoxon / paired t-test"], accent=T_AMBER, gap=9)
    box(s, 6.7, 3.7, 5.9, 2.8, PANEL2)
    text(s, 7.0, 3.95, 5.3, 0.28, "RESULTS STATUS", size=FONT_META, color=GREEN, bold=True)
    text(s, 7.0, 4.4, 5.3, 1.8,
         "Instrument and logging are built.\n\nParticipant runs still being collected — add real SUS and task numbers.",
         size=FONT_BODY, color=WHITE)
    footer(s, 16, a)


def s17(prs):
    s, a = new(prs, 17)
    header(s, 17, "Results and iterations", "Three changes driven by testing and reflection", a)
    y = 1.95
    for n, title, body, c in [
        ("1", "Per-platform adapters", "Single selector broke on YouTube Music; split into one adapter per site.", CYAN),
        ("2", "Companion dashboard", "Saved songs had no view; added a SQLite-backed library.", CYAN),
        ("3", "Usage logging + consent", "Testing needed real measurement; added events and a tracking toggle.", CYAN),
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
    footer(s, 17, a)


def s18(prs):
    s, a = new(prs, 18)
    header(s, 18, "Impact and limitations", "Benefits weighed against threats to validity", a)
    box(s, 0.7, 1.95, 5.8, 4.6, PANEL)
    text(s, 1.0, 2.2, 5.2, 0.28, "BENEFITS", size=FONT_META, color=GREEN, bold=True)
    bullets(s, 1.0, 2.65, 5.1, 3.6,
            ["No account or login required", "Data never leaves the machine",
             "Works across three platforms", "Addresses the retrieval gap",
             "Built-in measurement", "Three-part working prototype",
             "Hypotheses fixed before testing"], accent=GREEN, gap=12)
    box(s, 6.8, 1.95, 5.8, 4.6, PANEL)
    text(s, 7.1, 2.2, 5.2, 0.28, "LIMITATIONS", size=FONT_META, color=RED, bold=True)
    bullets(s, 7.1, 2.65, 5.1, 3.6,
            ["n = 18, below target of 30", "78% Spotify; no Apple Music users",
             "Ads (50%) out of scope", "Demo recommendation database",
             "Single-contributor scope", "Junk / joke rows flagged",
             "Underpowered at n = 18"], accent=RED, gap=12)
    footer(s, 18, a)


def s19(prs):
    s, a = new(prs, 19)
    header(s, 19, "Conclusion and future scope", "A small utility addressing a measured gap", a)
    box(s, 0.7, 1.95, 11.9, 1.65, PANEL)
    text(s, 1.0, 2.25, 11.2, 1.1,
         "78% save music. 44% struggle to find old saves.\nA private utility closes that loop — without claiming to fix ads.",
         size=FONT_BODY, color=WHITE, bold=True)
    text(s, 0.7, 3.95, 6, 0.28, "FUTURE WORK", size=FONT_META, color=T_AMBER, bold=True)
    x = 0.7
    for title, body, c in [("Real recommender", "Replace demo data with a learned model, then re-test.", GREEN),
                           ("Understand section", "Lyrics and song context, opened from the vibe view.", CYAN),
                           ("Larger sample", "30+ responses and a full SUS study; re-test at α=0.05.", ORANGE)]:
        box(s, x, 4.35, 3.8, 1.85, PANEL)
        text(s, x + 0.25, 4.65, 3.3, 0.4, title, size=FONT_BODY, color=WHITE, bold=True)
        text(s, x + 0.25, 5.2, 3.3, 0.9, body, size=FONT_META, color=MUTED)
        x += 3.95
    footer(s, 19, a)


def s20(prs):
    s, a = new(prs, 20)
    shape(s, MSO_SHAPE.RECTANGLE, 0, 0, 0.18, H, GREEN)
    text(s, 0.9, 1.2, 8, 0.3, "REFERENCES & Q&A", size=FONT_META, color=GREEN, bold=True)
    text(s, 0.9, 1.85, 11, 1.1, "Thank you.", size=FONT_HERO, color=WHITE, bold=True)
    text(s, 0.95, 3.0, 8, 0.6, "Questions?", size=FONT_BODY, color=GREEN, bold=True)
    bullets(s, 0.95, 4.1, 8.5, 2.0,
            ["Anonymised survey dataset (R01–R18)", "Integrated assignment brief",
             "Libraries: Flask, pandas, SciPy, matplotlib", "AI tooling disclosed per brief"],
            accent=GREEN, gap=9)
    footer(s, 20, a)


SLIDE_BUILDERS = [s1, s2, s3, s4, s5, s6, s7, s8, s9, s10,
                  s11, s12, s13, s14, s15, s16, s17, s18, s19, s20]


def main():
    global OUT, CREASE
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=None, help="output .pptx path")
    ap.add_argument("--crease", action="store_true",
                    help="trial: add a folded-paper crease background")
    args = ap.parse_args()
    CREASE = args.crease
    apply_palette("official")
    if args.out:
        OUT = Path(args.out)

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
