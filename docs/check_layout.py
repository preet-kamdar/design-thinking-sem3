#!/usr/bin/env python3
"""Estimate text-overflow in docs/Presentation.pptx.

Uses DejaVuSans as a deliberately conservative stand-in for Calibri (it is
wider), so anything that passes here will comfortably fit in PowerPoint.
Run after rebuilding the deck:  python3 docs/check_layout.py
"""

from pathlib import Path

from PIL import ImageFont
from pptx import Presentation

PPTX = Path(__file__).with_name("Presentation.pptx")
FONT_PATH = "/usr/share/fonts/TTF/DejaVuSans.ttf"
DPI = 96
EMU_PER_IN = 914400


def px(emu):
    return emu / EMU_PER_IN * DPI


def font_for(pt):
    return ImageFont.truetype(FONT_PATH, max(1, int(round(pt * DPI / 72))))


def wrapped_lines(text, draw_font, max_width):
    if not text.strip():
        return 1
    lines, current = 0, ""
    for word in text.split():
        trial = (current + " " + word).strip()
        if draw_font.getlength(trial) <= max_width or not current:
            current = trial
        else:
            lines += 1
            current = word
    return lines + 1 if current else lines


def check():
    prs = Presentation(PPTX)
    problems = []
    for idx, slide in enumerate(prs.slides, 1):
        for shp in slide.shapes:
            if not shp.has_text_frame or not shp.text_frame.text.strip():
                continue
            tf = shp.text_frame
            # available box interior, minus the small margins used by the builder
            avail_w = px(shp.width) - px(Inches := int(0.06 * EMU_PER_IN))
            avail_h = px(shp.height) - 2
            needed = 0.0
            for par in tf.paragraphs:
                text = "".join(r.text for r in par.runs) or par.text
                sizes = [r.font.size.pt for r in par.runs if r.font.size]
                if not sizes and par.font.size:
                    sizes = [par.font.size.pt]
                pt = max(sizes) if sizes else 16
                fnt = font_for(pt)
                lines = wrapped_lines(text, fnt, max(1, avail_w))
                line_h = pt * DPI / 72 * 1.2
                gap = (par.space_after.pt if par.space_after else 0) * DPI / 72
                needed += lines * line_h + gap
            if needed > avail_h + 1:
                problems.append((idx, round(needed), round(avail_h),
                                 shp.text_frame.text.strip().replace("\n", " / ")[:70]))
    return problems


if __name__ == "__main__":
    probs = check()
    print(f"Estimated overflowing text boxes: {len(probs)}")
    for slide, needed, avail, snippet in probs:
        print(f"  slide {slide:02d}: needs {needed}px, has {avail}px — {snippet}")
