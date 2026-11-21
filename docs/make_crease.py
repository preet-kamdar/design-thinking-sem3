#!/usr/bin/env python3
"""Generate a realistic folded-paper crease texture for the crease trial.

A real crease is NOT a straight line: it is a soft band of shadow with a
companion highlight, it bends slightly, and it fades in and out along its
length. This script paints several such bands over the official pale-lime
background and saves an opaque PNG sized for a 16:9 slide.
"""
from pathlib import Path

import numpy as np
from PIL import Image

W, H = 1600, 900
BG = np.array([0xF2, 0xF7, 0xEA], dtype=float)   # official pale-lime background

yy, xx = np.mgrid[0:H, 0:W].astype(float)


def crease_band(x0, y0, angle_deg, length, seed,
                dark_w=10, dark_a=0.20, light_w=16, light_a=0.30,
                core_w=1.6, core_a=0.28):
    """Return an RGB-adjustment array for one wavy, fading crease band."""
    ang = np.deg2rad(angle_deg)
    ux, uy = np.cos(ang), np.sin(ang)          # along the crease
    vx, vy = -uy, ux                            # perpendicular to it

    dx, dy = xx - x0, yy - y0
    t = dx * ux + dy * uy                       # distance along
    n = dx * vx + dy * vy                       # signed distance across

    # Gentle bend: a low-frequency sine plus a slow drift.
    bend = np.sin(t / 230.0 + seed) * 11 + np.sin(t / 90.0 + seed * 2) * 3
    wob = np.sin(t / 37.0 + seed * 3) * 1.4     # slight local wobble
    n = n - bend - wob

    # Fade the band in/out along its length so it breaks, not a ruler line.
    fade = np.clip(1 - (np.abs(t) / (length / 2)) ** 3, 0, 1)
    for gap_t in (-length * 0.22, length * 0.18):
        fade *= np.clip(np.abs(t - gap_t) / 70.0, 0.18, 1)

    shadow = np.where(n < 0, np.exp(-((n) / dark_w) ** 2), 0) * dark_a
    highlight = np.where(n > 0, np.exp(-((n) / light_w) ** 2), 0) * light_a
    core = np.exp(-((n) / core_w) ** 2) * core_a

    adj = np.zeros((H, W, 3), dtype=float)
    adj += np.array([-26.0, -22.0, -18.0])[None, None, :] * (shadow / dark_a)[..., None]
    adj += np.array([10.0, 9.0, 6.0])[None, None, :] * (highlight / light_a)[..., None]
    adj += np.array([-20.0, -17.0, -14.0])[None, None, :] * (core / core_a)[..., None]
    adj *= fade[..., None]
    return adj


# A handful of folds at different angles, like a poster folded into thirds and
# opened again. Overlapping wavy bands give the "shades of lines" look.
bands = [
    crease_band(W * 0.32, H * 0.50, 73, H * 1.5, 1, dark_a=0.22, light_a=0.34),
    crease_band(W * 0.67, H * 0.46, 108, H * 1.5, 2, dark_a=0.20, light_a=0.30),
    crease_band(W * 0.50, H * 0.52, 4, W * 1.4, 3, dark_a=0.16, light_a=0.24),
    crease_band(W * 0.18, H * 0.30, 96, H * 1.2, 4, dark_a=0.13, light_a=0.20),
    crease_band(W * 0.80, H * 0.75, 84, H * 1.2, 5, dark_a=0.13, light_a=0.20),
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
