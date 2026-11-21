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

**Data pipeline:** `webapp/analysis/analysis.py` reads the raw CSV → writes `data/survey_responses_anonymised.csv` (R01–R29), `docs/statistical_results.md`, and 5 charts in `data/charts/`. Re-runnable; this is the single source of truth. The `/results` page counts the anonymised CSV at runtime, so its numbers cannot drift.

---

## 2. The numbers (n = 29, target 30)

| Fact | Value |
|---|---|
| Responses | **29** (27 substantive; 2 flagged, **none deleted**) |
| Ages | 18–30, median **19**, mean **19.79**, SD **2.27** |
| Spotify / YouTube Music / Other / Apple | **69% / 14% / 10% / 7%** (20 / 4 / 3 / 2) |
| Daily / several times a week / occasionally | **62% / 24% / 14%** (18 / 7 / 4) |
| Use daily or several times a week | **86%** |
| Save or playlist a liked track | **86%** (16 playlist + 9 save/like) |
| Discover outside the app | **31%** (9) |
| Sometimes struggle to find old saves | **45%** (13) — the design target |
| Taste understood "very well" | **48%** (14) |
| Taste only somewhat / poorly | **52%** (12 + 3) |
| Ads / paywall complaint | **52%** (15) — biggest, **out of scope** |
| Themes: recs / UI / vibe / saving | **38% / 21% / 10% / 3%** |
| Vibe-finding ease: easy / average / difficult | **52% / 34% / 14%** |
| Ideas generated / selection weights | **10** / D 40 · F 35 · V 25 |
| Winning ideas / ad blocker score | **5.00** ×3 / **2.80** rejected |
| Hypothesis thresholds | alpha **0.05**, SUS benchmark **68** |
| Polling interval / DB tables / website pages | **2 s** / **5** / **6** |

---

## 3. Statistical results

One-sample t-tests vs neutral 2, two-tailed, df = 28:

| Measure | Mean | SD | t | p | 95% CI |
|---|---|---|---|---|---|
| Usage frequency | 2.48 | 0.74 | 3.524 | **0.0015** | [2.20, 2.76] |
| Vibe-finding ease | 2.38 | 0.73 | 2.807 | **0.0090** | [2.10, 2.66] |
| Taste understanding | 2.38 | 0.68 | 3.018 | **0.0054** | [2.12, 2.64] |
| Saved retrieval | 2.03 | 1.02 | 0.183 | **0.8564** | [1.65, 2.42] |

**Correlations** — Spearman (data are ordinal, n is small):

| Pair | Pearson | Spearman | p |
|---|---|---|---|
| Vibe ↔ Saved retrieval | +0.319 | **+0.324** | 0.0869 |
| Vibe ↔ Taste | +0.350 | +0.263 | 0.1679 |
| Retrieval ↔ Taste | +0.240 | +0.246 | 0.1975 |
| Usage ↔ Vibe | −0.220 | −0.200 | 0.2992 |
| Usage ↔ Taste | +0.121 | +0.172 | 0.3733 |
| Usage ↔ Retrieval | −0.118 | −0.086 | 0.6574 |

**Critical |r| at n=29 ≈ 0.367. Not one pair clears it. No correlation is significant.** The strongest is vibe ↔ saved retrieval at 0.324, p = 0.087. All six are weak and directional only. Never claim causation.

**Interpretation to say:** "Taste and vibe ease are significantly above neutral; saved retrieval is not. This is a **good-but-not-great baseline**, not a broken experience — the claim is refinement, not rescue."

---

## 4. Decisions and why

| Decision | Reason |
|---|---|
| Build familiarity control + saved library + vibe tags | Survey showed 86% save but 45% struggle to retrieve; 52% only somewhat/poorly understood taste |
| Reject the ad blocker (2.80) | A client-side utility cannot control playback/ads — recorded in "Won't", disclosed as a limitation |
| Flask + SQLite, not Django | Six pages and a few JSON APIs; small enough to explain and inspect line by line |
| Report the "good-but-not-great" baseline | Data do not support claiming users are deeply dissatisfied; honesty over drama |
| Anonymise to R01–R29 | Ethics: consent, no contact details, AI use disclosed; 2 low-quality rows flagged, none deleted |
| 2-second polling, not MutationObserver | Hosts are single-page apps that rebuild the DOM; polling is simpler and reliable |
| Single contributor | Brief assumes five roles; all consolidated and disclosed — no fabricated team or data |

**Not done / pending:** real recommendation model (rule-based demo dictionary), Understand section, offline downloads, cross-platform sync. **No SUS score and no task-time result are claimed** — the study page was built and instrumented, but participant runs were still being collected (paper §10.3, slides 16–17).

---

## 5. Likely questions — direct answers

1. **Tell me about the project.** → Extension + Flask/SQLite dashboard for discovery control, vibe search and saved-song retrieval, driven by a 29-response survey.
2. **Main problem?** → 86% save, but 45% struggle to find old saves; 52% say taste is only somewhat/poorly understood.
3. **Why these features?** → They are the in-scope themes; ads (52%) are out of scope.
4. **Sampling?** → Convenience sample of students, n = 29; below target 30, disclosed.
5. **Which results are significant?** → Taste (p .0054) and vibe ease (p .0090). Retrieval is not (p .8564).
6. **Any significant correlation?** → No. Critical 0.367; strongest 0.324, p .087. Directional only.
7. **Isn't n=29 too small?** → Yes — that is why I report CIs, avoid causation, and call the evidence directional.
8. **Where's your usability result?** → Instrument built, runs incomplete; no SUS or task-time result claimed (§10.3).
9. **Did you fabricate data?** → No. 29 real responses, all rows retained, 2 flagged, names anonymised.
10. **Why no ad blocker?** → Outside a client-side utility's control; in "Won't", listed as a limitation.
11. **Why Flask not Django?** → Enough for 6 pages and a few APIs; simpler to explain and inspect.
12. **chrome.storage and SQLite both?** → Client convenience vs shared, queryable measurement; the brief requires a DB.
13. **How does Save work?** → `data-*` attributes → `app.js` `fetch('/api/save')` → Flask `INSERT OR IGNORE` into SQLite → button becomes "Saved ✓".
14. **How is SUS scored?** → Odd (answer−1), even (5−answer), sum × 2.5 → 0–100; 68 benchmark.
15. **What if a site changes its layout?** → That platform's adapter selectors break; one file to fix — documented limitation.
16. **How do you keep numbers consistent?** → `analysis.py` is canonical; the website counts the anonymised CSV at runtime.
17. **Biggest limitation?** → n=29, 69% Spotify, demo recommendations, fragile selectors, single contributor.
18. **What next with more time?** → Learned model, Understand section, 30+ stratified sample, completed paired study with effect sizes.

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
