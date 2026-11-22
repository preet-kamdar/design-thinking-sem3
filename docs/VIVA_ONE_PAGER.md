# Viva One-Pager — Project Facts Only

**Preet Kamdar · 256019 · B.Tech CSE (AI & ML), JG University**
Combined project: Python · Web Tech · Design Thinking · Probability & Statistics
Mentors: Suryansh Rajput · Tanya Verma · Harsh Bhojak · Neelu Verma

No definitions here. For anything on this page, the source files are listed at the bottom.

---

## 1. What was built

A **Chrome extension** that injects a side panel into Spotify, YouTube Music and Apple Music:

- **Discover** — Familiar / Balanced / Exploratory familiarity slider
- **Find by Vibe** — 8 mood tags
- **My Music** — saved-song library
- Preferences panel with tracking toggle

Plus a **Flask + SQLite dashboard**: 6 pages (`/`, `/discover`, `/vibe`, `/preferences`, `/study`, `/results`), 5 JSON APIs, 5 database tables (`users`, `saved_songs`, `preferences`, `usage_events`, `test_tasks`), and consent-based usage logging.

The Chrome extension and the Flask website are **separate**: the extension stores on the client (`chrome.storage`); the dashboard stores in SQLite for measurement.

**Data pipeline:** `webapp/analysis/analysis.py` reads the raw CSV → writes `data/survey_responses_anonymised.csv` (R01–R32), `docs/statistical_results.md`, and 5 charts in `data/charts/`. Re-runnable; this is the single source of truth. The `/results` page counts the anonymised CSV at runtime, so its numbers cannot drift.

---

## 2. The numbers (n = 32, target 30 met)

| Fact | Value |
|---|---|
| Responses | **32** (30 substantive; 2 flagged, **none deleted**) |
| Ages | 18–30, median **19**, mean **19.69**, SD **2.19** |
| Spotify / YouTube Music / Other / Apple | **72% / 13% / 9% / 6%** (23 / 4 / 3 / 2) |
| Daily / several times a week / occasionally | **59% / 25% / 16%** (19 / 8 / 5) |
| Use daily or several times a week | **84%** |
| Save or playlist a liked track | **84%** (17 playlist + 10 save/like) |
| Discover outside the app | **28%** (9) |
| Sometimes struggle to find old saves | **47%** (15) — the design target |
| Taste understood "very well" | **44%** (14) |
| Taste only somewhat / poorly | **56%** (14 + 4) |
| Ads / paywall complaint | **53%** (17) — biggest, **out of scope** |
| Themes: recs / UI / vibe / saving | **38% / 19% / 13% / 6%** |
| Vibe-finding ease: easy / average / difficult | **50% / 34% / 16%** |
| Ideas generated / selection weights | **10** / D 40 · F 35 · V 25 |
| Winning ideas / ad blocker score | **5.00** ×3 / **2.60** rejected |
| Hypothesis thresholds | alpha **0.05**, SUS benchmark **68** |
| Polling interval / DB tables / website pages | **2 s** / **5** / **6** |

---

## 3. Statistical results

One-sample t-tests vs neutral 2, two-tailed, df = 31:

| Measure | Mean | SD | t | p | 95% CI |
|---|---|---|---|---|---|
| Usage frequency | 2.44 | 0.76 | 3.259 | **0.0027** | [2.16, 2.71] |
| Vibe-finding ease | 2.34 | 0.75 | 2.609 | **0.0138** | [2.08, 2.61] |
| Taste understanding | 2.31 | 0.69 | 2.552 | **0.0159** | [2.06, 2.56] |
| Saved retrieval | 1.94 | 1.01 | -0.349 | **0.7297** | [1.57, 2.30] |

**Correlations** — Spearman (data are ordinal, n is small):

| Pair | Pearson | Spearman | p |
|---|---|---|---|
| Vibe ↔ Saved retrieval | +0.328 | **+0.331** | 0.0642 |
| Vibe ↔ Taste | +0.410 | +0.325 | 0.0700 |
| Retrieval ↔ Taste | +0.304 | +0.312 | 0.0817 |
| Usage ↔ Vibe | −0.103 | −0.132 | 0.4706 |
| Usage ↔ Taste | +0.222 | +0.240 | 0.1854 |
| Usage ↔ Retrieval | −0.047 | −0.023 | 0.8999 |

**Critical |r| at n=32 ≈ 0.349. Not one pair clears it. No correlation is significant.** The strongest is vibe ↔ saved retrieval at 0.331, p = 0.064. All six are weak and directional only. Never claim causation.

**Interpretation to say:** "Taste and vibe ease are significantly above neutral; saved retrieval is not. This is a **good-but-not-great baseline**, not a broken experience — the claim is refinement, not rescue."

---

## 4. Decisions and why

| Decision | Reason |
|---|---|
| Build familiarity control + saved library + vibe tags | Survey showed 84% save but 47% struggle to retrieve; 56% only somewhat/poorly understood taste |
| Reject the ad blocker (2.60) | A client-side utility cannot control playback/ads — recorded in "Won't", disclosed as a limitation |
| Flask + SQLite, not Django | Six pages and a few JSON APIs; small enough to explain and inspect line by line |
| Report the "good-but-not-great" baseline | Data do not support claiming users are deeply dissatisfied; honesty over drama |
| Anonymise to R01–R32 | Ethics: consent, no contact details, AI use disclosed; 2 low-quality rows flagged, none deleted |
| 2-second polling, not MutationObserver | Hosts are single-page apps that rebuild the DOM; polling is simpler and reliable |
| Single contributor | Brief assumes five roles; all consolidated and disclosed — no fabricated team or data |

**One author pilot (system check, not validation):** three timed tasks — Discover **46.6 s**, Vibe **27.0 s**, Retrieve **23.4 s** — all completed, **5 / 3 / 0** clicks, **0** errors, plus one SUS self-rating of **35.0 / 100**. Stored in SQLite (`test_tasks` + a `sus_score` event). n=1 by the designer, so this is **not** usability evidence and no participant result is claimed (§10.3).

**Not done / pending:** real recommendation model (rule-based demo dictionary), Understand section, offline downloads, cross-platform sync, and a proper paired study with real participants (SUS, effect sizes, CIs).

---

## 5. Likely questions — direct answers

1. **Tell me about the project.** → Extension + Flask/SQLite dashboard for discovery control, vibe search and saved-song retrieval, driven by a 32-response survey.
2. **Main problem?** → 84% save, but 47% struggle to find old saves; 56% say taste is only somewhat/poorly understood.
3. **Why these features?** → They are the in-scope themes; ads (53%) are out of scope.
4. **Sampling?** → Convenience sample of students, n = 32; target 30 met, still a modest sample.
5. **Which results are significant?** → Taste (p .0054) and vibe ease (p .0090). Retrieval is not (p .8564).
6. **Any significant correlation?** → No. Critical 0.349; strongest 0.331, p .064. Directional only.
7. **Isn't n=32 still small?** → Yes — that is why I report CIs, avoid causation, and call the evidence directional.
8. **Where's your usability result?** → Instrument built, runs incomplete; no SUS or task-time result claimed (§10.3).
9. **Did you fabricate data?** → No. 32 real responses, all rows retained, 2 flagged, names anonymised.
10. **Why no ad blocker?** → Outside a client-side utility's control; in "Won't", listed as a limitation.
11. **Why Flask not Django?** → Enough for 6 pages and a few APIs; simpler to explain and inspect.
12. **chrome.storage and SQLite both?** → Client convenience vs shared, queryable measurement; the brief requires a DB.
13. **How does Save work?** → `data-*` attributes → `app.js` `fetch('/api/save')` → Flask `INSERT OR IGNORE` into SQLite → button becomes "Saved ✓".
14. **How is SUS scored?** → Odd (answer−1), even (5−answer), sum × 2.5 → 0–100; 68 benchmark.
15. **What if a site changes its layout?** → That platform's adapter selectors break; one file to fix — documented limitation.
16. **How do you keep numbers consistent?** → `analysis.py` is canonical; the website counts the anonymised CSV at runtime.
17. **Biggest limitation?** → n=32 modest, 72% Spotify, demo recommendations, fragile selectors, single contributor.
18. **What next with more time?** → Learned model, Understand section, larger stratified sample, completed paired study with effect sizes.

**If you don't know:** "I'm not certain — the place to check would be ___." Never invent a number.

---

## 6. Source files

| Need | Open |
|---|---|
| Every number | `docs/statistical_results.md` |
| Design decisions | `docs/design_thinking_artefacts.md` |
| Full narrative | `docs/Research_Paper.docx` |
| What you say on stage | `docs/presentation_script.md` (English only) |
| Memory drill | `docs/viva_cheat_sheet.md`, `docs/viva_prep_guide.md` |
| Run the project | `README.md` |
