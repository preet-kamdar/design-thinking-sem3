# Presentation Script — 15 Slides
**Reimagining the Personal Music Experience**
Target: 10–12 minutes + 5 minutes Q&A. Memorise the **bold numbers** in each slide.

---

### Slide 1 — Title
**On slide:** Project title · Your name / roll number · Department · Institution · Faculty mentor
**Say:** "Good morning. I'm presenting *Reimagining the Personal Music Experience* — a
privacy-first personalisation layer for Spotify, YouTube Music and Apple Music, backed by
survey data and a working Python backend."

---

### Slide 2 — Introduction
**On slide:** Music streaming is routine; personalisation is a top expectation; ads dominate complaints.
**Say:** "Music streaming is part of daily life for our respondents — **78% use their app
daily or several times a week**. But personalisation is uneven: **61% say their app only
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
**On slide:** Target users: students 18–30. Convenience sampling. Questionnaire: MCQ + ordinal + numeric + open-ended. n = 18.
**Say:** "We used convenience sampling of students. The questionnaire mixes multiple-choice,
ordinal ease ratings, numeric age, and three open-ended questions. **18 responses** — below
the brief's target of 30, which we state openly as a limitation. The sample is **78% Spotify**,
so platform conclusions are strongest for Spotify."

---

### Slide 5 — Empathise
**On slide:** Empathy map (Says / Thinks / Does / Feels) + top 3 pain points.
**Say:** "Users *say* 'remove ads' and 'better recommendations'. They *do* save songs —
**78% add to playlist or like** — but **44% sometimes struggle to find old saves**. They
*feel* mildly satisfied, not delighted. Ranked pain points: ads **50%** — out of scope;
recommendations/taste **44%**; retrieval **44%**."

---

### Slide 6 — Statistical findings
**On slide:** Charts + table: taste 2.33, t=2.38, p=0.029, CI [2.04, 2.63]; vibe 2.50, p=0.003; retrieval 2.11, p=0.651.
**Say:** "Ordinal coding was 1–3 with neutral 2. One-sample t-tests show responses were
significantly *above* neutral for vibe-finding ease, **mean 2.50, p = 0.003**, and taste
understanding, **mean 2.33, p = 0.029**. Saved retrieval was **mean 2.11, p = 0.651** —
not significant. Correlations were weak and non-significant. So we do not overclaim: the
baseline is good-but-not-great, and the opportunity is refinement."

---

### Slide 7 — Define
**On slide:** Persona "Aarav, 19" · POV · HMW · MoSCoW highlights.
**Say:** "Our composite persona is Aarav, a 19-year-old daily Spotify user who discovers
music outside the app and saves tracks he rarely revisits. POV: a listener who saves but
can't rediscover, and feels recommendations only somewhat match their taste, needs control
over familiarity and mood-based retrieval. HMW: how might we give that control without a
paid subscription? MoSCoW put Discover, My Music and the backend in Must; ads and offline
downloads in Won't."

---

### Slide 8 — Ideation
**On slide:** Mind map + 10 ideas (show the list, highlight the top four).
**Say:** "We generated ten ideas, from a discovery slider and vibe tags to an AI chatbot and
an ad blocker. We mapped them across discovery, mood, library, understanding and preferences,
then scored each on desirability, feasibility and viability."

---

### Slide 9 — Idea selection + hypotheses
**On slide:** Weighted matrix (D 40% / F 35% / V 25%); top score 5.00; H₀/H₁ written in advance.
**Say:** "Weighted scoring put the discovery slider, vibe tags, and save-plus-library at
**5.00**, highest. AI chatbot scored **2.45** and ad blocker **2.80** — rejected on
feasibility, since we have no API access. Before testing we fixed three hypotheses:
retrieval time, taste satisfaction above baseline 2.33, and SUS above 68, at alpha 0.05."

---

### Slide 10 — Prototype
**On slide:** Architecture diagram: Extension (HTML/CSS/JS) → Flask routes → SQLite; screenshots of panel, dashboard, study page.
**Say:** "The prototype has two parts. The Chrome extension injects a side panel into three
music sites and detects the current track using one adapter per platform. The companion
dashboard is responsive HTML, CSS and JavaScript served by Flask, with a SQLite database
holding saved songs, preferences, usage events and test tasks. Everything stays local —
no login, no external API. Let me demonstrate [open /discover, save a song, show /My Music]."

---

### Slide 11 — Testing and validation
**On slide:** Paired design · timed tasks · SUS · tests chosen · [insert results once collected].
**Say:** "Testing uses the same participants on both methods — a paired design. The study
page times three tasks and counts clicks and errors, then computes a SUS score out of 100.
For time we will use a Wilcoxon signed-rank test if data are non-normal, otherwise a paired
t-test; for SUS a one-sample t-test against 68. **[Insert actual participant count, test
statistic, p-value and confidence interval here once runs are complete.]**"

---

### Slide 12 — Results and iterations
**On slide:** Three improvements made; before/after numbers [fill after testing].
**Say:** "Iteration one: we split track detection into per-platform adapters after the
single-file version broke on YouTube Music's changing DOM. Iteration two: we added a
companion dashboard because saved songs existed in extension storage but had no view.
Iteration three: we added explicit usage logging and a consent toggle so testing is based
on measurement. **[Add SUS and task-time changes from real testing here.]**"

---

### Slide 13 — Impact and limitations
**On slide:** Benefits · feasibility · threats to validity.
**Say:** "Benefits: no account required, data never leaves the browser, works across three
platforms. Limitations: **n = 18 not 30**; **78% Spotify, zero Apple Music users**; ads —
the biggest complaint — are out of scope; recommendation data is a demo database; and this
was a single-contributor project, so team-role breadth was consolidated. We disclose all of
these rather than hide them."

---

### Slide 14 — Conclusion and future scope
**On slide:** Key learning · conclusion · future work.
**Say:** "We learned that a small, focused utility can address a real, measured gap —
saved-song retrieval and taste control — without complex infrastructure. The prototype
addresses the ranked in-scope pain points; it does not claim to fix ads. Future work: a real
recommendation model, the Understand section, and a larger, stratified sample."

---

### Slide 15 — References and Q&A
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
