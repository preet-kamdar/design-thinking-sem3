# Palette trials

Copies of the same 15-slide deck, differing **only** in colour. Everything
else is identical: two font sizes (36/20), one 3pt dark border per box, and a
single subtle vinyl on slides 1 and 15.

The two shortlisted palettes now have **tinted-background versions** to compare
against the original white-background ones. Text uses two matching dark inks:
one on the bright boxes, one on the slide background. Both exceed 5:1 contrast.

| File | Based on | Background / text ink | Box colours |
|---|---|---|---|
| `dandadan.pptx` | Dandadan / Seiko Ayase | white / black | `#E3F21C` lime, `#ADFB70` green, `#13A3B5` teal |
| **`dandadan_tinted.pptx`** | same | pale lime `#F2F7EA` / deep green `#1B2C24` + `#14201A` | same |
| `crimson_gold.pptx` | `tri.jpg` | white / black | `#E5D561` gold, `#F2B8C6` pink, `#E56595` rose |
| **`crimson_gold_tinted.pptx`** | same | warm cream `#FBF3E9` / deep wine `#3A1F2B` + `#2A1820` | same |
| `yellow_coral.pptx` | `802977808620021241.jpg` | white / black | `#FEF200` yellow, `#F2D21C` gold, `#F7A6A6` coral |
| `teal_red.pptx` | Russian colour-combination pin | white / black | `#EDE6E0` cream, `#8FC3C9` teal, `#E8A0A0` red |

Open the two tinted decks and compare **slide 1** (title), **slide 6** (stats)
and **slide 15** (Q&A) — those show each theme most clearly.

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
python3 docs/build_presentation.py --palette dandadan_tinted      --out docs/trials/dandadan_tinted.pptx
python3 docs/build_presentation.py --palette crimson_gold_tinted  --out docs/trials/crimson_gold_tinted.pptx
```

With no arguments, `docs/build_presentation.py` still rebuilds the original
`docs/Presentation.pptx` unchanged.
