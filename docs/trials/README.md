# Palette trials

Four copies of the same 15-slide deck, differing **only** in colour. Everything
else is identical: pure white slides, black text, two font sizes (36/20), one
3pt black border per box, and a single subtle vinyl on slides 1 and 15.

Open all four in PowerPoint and compare slide 1 (title), slide 6 (stats) and
slide 15 (Q&A) — those show the palette most clearly.

| File | Based on | Box colours | Feel |
|---|---|---|---|
| `yellow_coral.pptx` | `802977808620021241.jpg` | `#FEF200` yellow, `#F2D21C` gold, `#F7A6A6` coral | Closest to the current deck; warm and bright |
| `dandadan.pptx` | `Dandadan Color Palette _ Seiko Ayase.jpg` | `#E3F21C` lime, `#ADFB70` green, `#13A3B5` teal | Liveliest; brings green back |
| `crimson_gold.pptx` | `tri.jpg` | `#E5D561` gold, `#F2B8C6` pink, `#E56595` rose | Dramatic, warm-cool contrast |
| `teal_red.pptx` | Russian colour-combination pin | `#EDE6E0` cream, `#8FC3C9` teal, `#E8A0A0` red | Calmest and most muted |

The dark colours in the reference images (e.g. `#0F3F49` teal, `#800407` red,
`#D11544` crimson) were **lightened** for the box fills so black text stays
readable. The original dark hue is kept for the "limit" role (slide 11 and
highlights).

## Regenerating

```bash
python3 docs/build_presentation.py --palette yellow_coral --out docs/trials/yellow_coral.pptx
python3 docs/build_presentation.py --palette dandadan     --out docs/trials/dandadan.pptx
python3 docs/build_presentation.py --palette crimson_gold --out docs/trials/crimson_gold.pptx
python3 docs/build_presentation.py --palette teal_red     --out docs/trials/teal_red.pptx
```

With no arguments, `docs/build_presentation.py` still rebuilds the original
`docs/Presentation.pptx` unchanged.
