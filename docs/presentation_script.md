# Presentation Script — 20 Slides
**Reimagining the Personal Music Experience**
Target: 12–15 minutes + 5 minutes Q&A. Memorise the **bold numbers** in each slide.

---

### Slide 1 — Title
**On slide:** Project title · Preet Kamdar / 256019 · combined Python, Web Tech, Design Thinking and Statistics project
**Say:** "Good morning. I'm presenting *Reimagining the Personal Music Experience* — a
privacy-first personalisation layer for Spotify, YouTube Music and Apple Music, backed by
survey data and a working Python backend."

---

### Slide 2 — Introduction
**On slide:** Music streaming is routine; personalisation is a top expectation; ads dominate complaints.
**Say:** "Music streaming is part of daily life for our respondents — **85% use their app
daily or several times a week**. But personalisation is uneven: **52% say their app only
'somewhat' or 'poorly' understands their taste**. This project asks whether a lightweight
utility can improve discovery and rediscovery without needing account APIs."

---

### Slide 3 — Project overview
**On slide:** Scope, objectives, intended outcomes.
**Say:** "Objectives: one, give users control over how familiar or exploratory recommendations
are; two, make saved music easy to find; three, prove with statistics that the design addresses
real pain points. Outcomes: a Chrome extension, a responsive Flask dashboard with SQLite, and
an analysis pipeline that reruns on updated data."

---

### Slide 4 — User research
**On slide:** Target users: students 18–30. Convenience sampling. Questionnaire: MCQ + ordinal + numeric + open-ended. n = 27.
**Say:** "We used convenience sampling of students. The questionnaire mixes multiple-choice,
ordinal ease ratings, numeric age, and three open-ended questions. **27 responses** — below
the brief's target of 30, which we state openly as a limitation. The sample is **67% Spotify**,
so platform conclusions are strongest for Spotify."

---

### Slide 5 — Empathise
**On slide:** Empathy map (Says / Thinks / Does / Feels) + top 3 pain points.
**Say:** "Users *say* 'remove ads' and 'better recommendations'. They *do* save songs —
**85% add to playlist or like** — but **44% sometimes struggle to find old saves**. They
*feel* mildly satisfied, not delighted. Ranked pain points: ads **48%** — out of scope;
recommendations/taste **37%**; UI **19%**."

---

### Slide 6 — Statistical findings
**On slide:** Three summary cards + honest reading. The five full-size charts are on slides 7–11.
**Say:** "Ordinal coding was 1–3 with neutral 2. One-sample t-tests show responses were
significantly *above* neutral for vibe-finding ease, **mean 2.44, p = 0.0027**, and taste
understanding, **mean 2.41, p = 0.0026**. Saved retrieval was **mean 2.04, p = 0.852** —
not significant. Correlations were weak, with one significant pair. So we do not overclaim: the
baseline is good-but-not-great, and the opportunity is refinement."

---

### Slide 7 — Evidence 1: platform and usage
**On slide:** Primary-platform and usage-frequency bar charts, full width.
**Say:** "This is our platform mix: **18 of 27 use Spotify — 67%**, four use YouTube Music,
two Apple Music and three other. **Eighteen listen daily** and five several times a week.
The imbalance is a limitation we state rather than hide."

---

### Slide 8 — Evidence 2: discovery and saving
**On slide:** Discovery-source and post-like action charts, full width.
**Say:** "Discovery is split: **eight find music outside the app**, seven by search, seven through recommendations
and five via playlists. Yet **23 of 27 save or like tracks**. That gap between
saving and finding them again is exactly what our library feature addresses."

---

### Slide 9 — Evidence 3: ordinal distributions
**On slide:** Four bar charts showing the raw 1–3 counts behind the baseline tests.
**Say:** "These are the raw counts behind the tests. Vibe-finding ease averages **2.44, p = 0.0027**,
taste understanding **2.41, p = 0.0026**, but saved-song retrieval is **2.04, p = 0.852**. Above
neutral is not dissatisfaction — it is room to refine."

---

### Slide 10 — Evidence 4: age and score spread
**On slide:** Age histogram and box plots of the three ordinal scores.
**Say:** "We have **27 numeric ages, mean 19.7, median 19**. The box
plots show the spread — retrieval is the widest. With n = 27 we treat this as directional
evidence only, not proof."

---

### Slide 11 — Evidence 5: correlations
**On slide:** Spearman correlation heatmap with grids and readable labels.
**Say:** "Only one correlation clears the bar. At n = 27 a coefficient needs about **0.381**; vibe ease with saved retrieval reaches **0.385 (p = 0.047)**. So we do not claim that one habit
causes another — we only describe what we observed."

---

### Slide 12 — Define
**On slide:** Persona "Aarav, 19" · POV · HMW · MoSCoW highlights.
**Say:** "Our composite persona is Aarav, a 19-year-old daily Spotify user who discovers
music outside the app and saves tracks he rarely revisits. POV: a listener who saves but
can't rediscover, and feels recommendations only somewhat match their taste, needs control
over familiarity and mood-based retrieval. HMW: how might we give that control without a
paid subscription? MoSCoW put Discover, My Music and the backend in Must; ads and offline
downloads in Won't."

---

### Slide 13 — Ideation
**On slide:** Mind map + 10 ideas (show the list, highlight the top four).
**Say:** "We generated ten ideas, from a discovery slider and vibe tags to an AI chatbot and
an ad blocker. We mapped them across discovery, mood, library, understanding and preferences,
then scored each on desirability, feasibility and viability."

---

### Slide 14 — Idea selection + hypotheses
**On slide:** Weighted matrix (D 40% / F 35% / V 25%); top score 5.00; H₀/H₁ written in advance.
**Say:** "Weighted scoring put the discovery slider, vibe tags, and save-plus-library at
**5.00**, highest. AI chatbot scored **2.45** and ad blocker **2.80** — rejected on
feasibility, since we have no API access. Before testing we fixed three hypotheses:
retrieval time, taste satisfaction above baseline 2.41, and SUS above 68, at alpha 0.05."

---

### Slide 15 — Prototype
**On slide:** Architecture diagram: Extension (HTML/CSS/JS) → Flask routes → SQLite; screenshots of panel, dashboard, study page.
**Say:** "The prototype has two parts. The Chrome extension injects a side panel into three
music sites and detects the current track using one adapter per platform. The companion
dashboard is responsive HTML, CSS and JavaScript served by Flask, with a SQLite database
holding saved songs, preferences, usage events and test tasks. Everything stays local —
no login, no external API. Let me demonstrate [open /discover, save a song, show /My Music]."

---

### Slide 16 — Testing and validation
**On slide:** Paired design · timed tasks · SUS · tests chosen · [insert results once collected].
**Say:** "Testing uses the same participants on both methods — a paired design. The study
page times three tasks and counts clicks and errors, then computes a SUS score out of 100.
For time we will use a Wilcoxon signed-rank test if data are non-normal, otherwise a paired
t-test; for SUS a one-sample t-test against 68. **[Insert actual participant count, test
statistic, p-value and confidence interval here once runs are complete.]**"

---

### Slide 17 — Results and iterations
**On slide:** Three improvements made; before/after numbers [fill after testing].
**Say:** "Iteration one: we split track detection into per-platform adapters after the
single-file version broke on YouTube Music's changing DOM. Iteration two: we added a
companion dashboard because saved songs existed in extension storage but had no view.
Iteration three: we added explicit usage logging and a consent toggle so testing is based
on measurement. **[Add SUS and task-time changes from real testing here.]**"

---

### Slide 18 — Impact and limitations
**On slide:** Benefits · feasibility · threats to validity.
**Say:** "Benefits: no account required, data never leaves the browser, works across three
platforms. Limitations: **n = 27 not 30**; **67% Spotify, only 7% Apple Music**; ads —
the biggest complaint — are out of scope; recommendation data is a demo database; and this
was a single-contributor project, so team-role breadth was consolidated. We disclose all of
these rather than hide them."

---

### Slide 19 — Conclusion and future scope
**On slide:** Key learning · conclusion · future work.
**Say:** "We learned that a small, focused utility can address a real, measured gap —
saved-song retrieval and taste control — without complex infrastructure. The prototype
addresses the ranked in-scope pain points; it does not claim to fix ads. Future work: a real
recommendation model, the Understand section, and a larger, stratified sample."

---

### Slide 20 — References and Q&A
**On slide:** Google Forms dataset · brief · libraries (Flask, pandas, scipy, matplotlib) · sites' UI.
**Say:** "Sources: our anonymised survey dataset, the assignment brief, and the open-source
libraries used. AI tools were used for code drafting and documentation, disclosed per the
brief. Thank you — questions?"

---

## Demo sequence to rehearse (keep under 2 minutes)
1. `cd webapp && python3 app.py` → open `http://127.0.0.1:5000`
2. `/discover` → choose Familiar → save a song
3. `/` → show it in the SQLite-backed My Music list
4. `/vibe` → pick "chill" → save another
5. `/study` → start a task, show SUS form
6. `/results` → show charts and anonymised rows

**If the live demo fails:** have screenshots of these six pages ready as fallback.
