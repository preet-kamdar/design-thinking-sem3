#!/usr/bin/env python3
"""Generate a folded-paper crease texture matching the reference photo.

The reference (crease.jpg) is a poster folded into thirds: creases run at
roughly 1/3 and 2/3 in BOTH directions. Each crease is not a hard line but a
soft band — a dark shadow gradient on one side, a lighter highlight on the
other — that bends slightly and breaks/fades along its length. This script
recreates that exact structure over the official pale-lime slide background.
"""
from pathlib import Path

import numpy as np
from PIL import Image

W, H = 1600, 900
BG = np.array([0xF2, 0xF7, 0xEA], dtype=float)   # official pale-lime background

yy, xx = np.mgrid[0:H, 0:W].astype(float)


def fold_band(centre, span, axis, seed, w_shadow=24, w_light=32,
              a_dark=0.85, a_light=0.80, bend_amp=8, gaps=True):
    """One soft, wavy, breaking fold band perpendicular to ``axis``.

    Returns an RGB adjustment array. ``axis`` is 'x' for a vertical crease
    (varying across x, running down y) or 'y' for a horizontal crease.
    """
    along, across = (yy, xx) if axis == "x" else (xx, yy)
    a0 = centre

    # Gentle bend + slow wobble so the crease is never ruler-straight.
    bend = (np.sin(along / 260.0 + seed) * bend_amp +
            np.sin(along / 95.0 + seed * 2) * (bend_amp * 0.35))
    n = (across - a0) - bend

    # Fade at the ends; optionally add 2 gaps where the fold pressure eased.
    fade = np.clip(1 - (np.abs(along - span / 2) / (span / 2)) ** 4, 0, 1)
    if gaps:
        for g in (span * 0.31, span * 0.70):
            fade *= np.clip(np.abs(along - g) / 55.0, 0.12, 1)

    shadow = np.where(n < 0, np.exp(-((n) / w_shadow) ** 2), 0)
    highlight = np.where(n > 0, np.exp(-((n) / w_light) ** 2), 0)
    core = np.exp(-((n) / 2.2) ** 2)

    adj = np.zeros((H, W, 3), dtype=float)
    adj += np.array([-46.0, -40.0, -34.0])[None, None, :] * (shadow * a_dark)[..., None]
    adj += np.array([20.0, 18.0, 13.0])[None, None, :] * (highlight * a_light)[..., None]
    adj += np.array([-30.0, -26.0, -22.0])[None, None, :] * (core * 0.7)[..., None]
    return adj * fade[..., None]


# Tri-fold layout: creases at 1/3 and 2/3 of each dimension, matching the
# reference poster. Vertical folds are a touch stronger (they read clearly in
# a photo); horizontal folds are softer. Positions deviate slightly from exact
# thirds, as real folds do.
bands = [
    fold_band(W / 3 - 8, H, "x", 1, a_dark=0.34, a_light=0.46, bend_amp=8),
    fold_band(2 * W / 3 + 11, H, "x", 2, a_dark=0.30, a_light=0.42, bend_amp=7),
    fold_band(H / 3 + 6, W, "y", 3, a_dark=0.26, a_light=0.36, bend_amp=6),
    fold_band(2 * H / 3 - 9, W, "y", 4, a_dark=0.24, a_light=0.34, bend_amp=6),
]

img = np.broadcast_to(BG, (H, W, 3)).copy()
for b in bands:
    img = img + b
img = np.clip(img, 0, 255).astype(np.uint8)
out = Image.fromarray(img, "RGB")
path = Path(__file__).parent / "crease_background.png"
out.save(path)
g = np.array(out.convert("L"))
print(f"Wrote {path} ({W}x{H}) luma std={g.std():.2f} range {g.min()}..{g.max()}")
