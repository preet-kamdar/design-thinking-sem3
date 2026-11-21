# Viva Cheat Sheet
**Reimagining the Personal Music Experience**

Memorise the **bold** values. Full detail: `docs/design_thinking_artefacts.md`,
`docs/statistical_results.md`, `docs/presentation_script.md`.

---

## The project in 30 seconds
"A Chrome extension that adds a personalisation side panel to Spotify, YouTube Music and
Apple Music, plus a responsive Flask dashboard backed by SQLite. Its core features are
Discover with three familiarity levels, Find by Vibe, and a saved-song library. Its design
was driven by a **29-response** survey and validated with usage logging and a SUS study."

---

## Research & statistics

**Q: What was your sample and sampling method?**
Convenience sample of students; **n = 29**, ages 18–30 (median **19**). **69% Spotify**,
14% YouTube Music, 10% Other, 7% Apple Music. Below the brief's target of 30 — declared as a limitation.

**Q: What question types did you use?**
Multiple choice (platform, frequency, discovery source, save behaviour), ordinal 1–3 ease
ratings, numeric age, and three open-ended questions — matching the brief's requirement.

**Q: How did you code the data?**
Easy / Very well / Daily = **3**; Average / Somewhat / Several times a week = **2**;
Difficult / Poorly / Occasionally / Sometimes difficult = **1**. Neutral = **2**.

**Q: Which statistics did you run and why?**
Descriptive counts and means; one-sample t-tests against neutral 2 for the baseline;
Pearson **and** Spearman correlations between ordinal variables; 95% confidence intervals.
Spearman is safer because the data are ordinal and n is small.

**Q: Give me the key results.**
Taste understanding **mean 2.38, t = 3.02, p = 0.0054, CI [2.12, 2.64]** — above neutral.
Vibe ease **2.38, t = 2.81, p = 0.0090**. Saved retrieval **2.03, t = 0.18, p = 0.856** —
not significant. No correlation clears the critical 0.367; the strongest is vibe ease ↔ saved retrieval ρ = +0.32 (p = 0.087).

**Q: What do those results actually mean?**
Users are *satisfied but not delighted*. We deliberately do **not** claim a broken
experience. The gap is that only **48%** say the app understands taste "very well", and
**45%** sometimes struggle to find old saved songs.

**Q: What is a p-value / confidence interval?**
p-value: probability of data this extreme if the null were true. CI: range of plausible
population values. Our taste CI [2.12, 2.64] excludes 2, which matches p < 0.05.

**Q: What is an effect size / why report it?**
It quantifies *how big* the improvement is, not just whether it is statistically
detectable. The brief requires it; report mean difference and SUS change, not only p.

**Q: Why didn't you reach 30 responses?**
Time constraint — presentation was scheduled two days after the analysis. We report the
**29 real responses** honestly and list small-sample bias as a limitation. No data was
fabricated.

---

## Design Thinking

**Q: Name the five stages.** Empathise → Define → Ideate → Prototype → Test.

**Q: What is an empathy map?** A four-quadrant summary — Says, Thinks, Does, Feels — built
from real user responses. Ours surfaced ads, recommendation fatigue, and saving behaviour.

**Q: Persona vs empathy map?** Persona is one composite archetype ("Aarav, 19"); empathy
map is the aggregated emotional picture across users.

**Q: POV and HMW?**
POV: a listener who saves but can't rediscover, and feels recommendations only somewhat
match their taste, needs familiarity control and mood-based retrieval.
HMW: how might we give that control without requiring a paid subscription or new account?

**Q: What is MoSCoW?** Must / Should / Could / Won't prioritisation. Must = Discover, My
Music, backend. Won't = ad removal, offline downloads.

**Q: How many ideas and how did you select?**
**10 ideas**, scored on desirability **40%**, feasibility **35%**, viability **25%**. Top
score **5.00** — discovery slider, vibe tags, save-plus-library. Ad blocker scored **2.80**
and was rejected as infeasible without API access.

**Q: What is SWOT?** Strengths, Weaknesses, Opportunities, Threats — used to sanity-check the
chosen concept against site-selector fragility and the small sample.

**Q: What were your hypotheses?** H₀: no improvement in retrieval time / taste rating / SUS.
H₁: retrieval faster, taste rating above **2.38**, SUS above **68**. α = **0.05**.

---

## Technical

**Q: Where is the frontend?**
Two places: the extension's injected panel and popup (`popup.html/css/js`, `content.js/css`),
and the responsive dashboard templates in `webapp/templates/` with `static/style.css` and
`static/app.js`. The dashboard uses media queries for mobile.

**Q: Where is Python?**
`webapp/app.py` — a Flask server with routes for pages and JSON APIs. `webapp/recommendations.py`
holds server-side demo data. `webapp/analysis/analysis.py` is the statistical script
(pandas, scipy, matplotlib) that regenerates every number and chart.

**Q: Where is the database and what is in it?**
`webapp/pme.db` (SQLite). Tables: `users`, `saved_songs`, `preferences`, `usage_events`,
`test_tasks`. Created automatically by `init_db()`.

**Q: Why both chrome.storage and SQLite?**
The extension stores quickly on the client with no server; the dashboard needs a shared,
queryable store for testing measurement. The brief explicitly requires a database.

**Q: How does platform detection work?**
Each platform adapter has a `detect()` checking `window.location.hostname`. `content.js`
picks the matching adapter and polls `getCurrentTrack()` every **2 seconds**.

**Q: Why polling, not MutationObserver?**
These sites are single-page apps that constantly tear down and rebuild DOM nodes;
`MutationObserver` becomes fragile and complex. A 2-second poll is simpler and reliable
enough for a prototype.

**Q: What if a site changes its layout?**
The CSS selectors in that platform's adapter break; only that one file needs updating.
This is a documented limitation.

**Q: What is SUS and how is it scored?**
System Usability Scale — 10 items, 1–5. Odd items contribute (response − 1), even items
(5 − response); sum × **2.5** gives 0–100. **68** is the average benchmark.

**Q: What usage data does the prototype record?**
Page views, saves, preference changes, task start events, and per-task duration, clicks,
errors and completion — all written to SQLite, never sent anywhere.

---

## Scope, ethics, honesty

**Q: You worked alone — what did you cut?**
The brief assumes a five-member team. I consolidated all five roles into one contributor
and disclosed reductions: no separate interview transcripts (used open-text survey answers
instead), individual rather than team brainstorming, mentor review instead of peer review.
No data was fabricated.

**Q: What is the biggest complaint and why didn't you fix it?**
Ads — **52%** of respondents. Removing ads needs control of the streaming service's
playback, which a client-side utility does not have. We put it in Won't and listed it as a
limitation rather than pretending to solve it.

**Q: How did you protect participant data?**
Anonymised names to R01–R29 in `data/survey_responses_anonymised.csv`; no contact details
collected; consent and data use explained in the form; AI tool use disclosed.

**Q: What is the single strongest justification for your solution?**
**45%** sometimes struggle to find songs saved long ago, while **86%** actively save —
so the save-and-retrieve loop is a real gap, and the data layer for it already existed.

**Q: What would you do next with more time?**
A real recommendation model instead of demo data, the Understand section, a larger
stratified sample (30+), and a completed paired SUS study with effect sizes.
