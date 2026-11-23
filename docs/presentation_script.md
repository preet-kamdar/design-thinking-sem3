# Presentation Script — 20 Slides
**Reimagining the Personal Music Experience**
Target: 10–12 minutes including pauses, plus 5 minutes of questions. **Bold** marks the words and numbers to say slowly and clearly. The joining sentences are meant to be spoken — they carry the flow between slides.

---

### Slide 1 — Title
**On slide:** Project title · Preet Kamdar / 256019 · combined Python, Web Tech, Design Thinking and Statistics project
**Say:** "Good morning. I am Preet Kamdar, and I am presenting Reimagining the Personal Music Experience. The project is a **privacy-first personalisation layer** for Spotify, YouTube Music and Apple Music. It is backed by a survey of **32 real responses** and by a working Python backend. I will show you the evidence, the prototype, and the limits I found."

---

### Slide 2 — Introduction
**On slide:** Music streaming is routine; personalisation is a top expectation; ads dominate complaints.
**Say:** "We began with a simple observation: music streaming is routine for our respondents. **84%** use their app daily or several times a week. Yet routine use is not the same as satisfaction. **56%** say the app understands their taste only 'somewhat' or 'poorly'. That gap between habit and satisfaction is the question this project asks: can a lightweight utility improve discovery and rediscovery without account APIs?"

---

### Slide 3 — Project overview
**On slide:** Scope, objectives, intended outcomes.
**Say:** "To answer that question, I set three objectives. First, give users control over how familiar or exploratory recommendations are. Second, make saved music easy to find again. Third, test the design with statistics rather than opinion. Those objectives produced three outcomes: a Chrome extension, a responsive Flask dashboard backed by SQLite, and an analysis pipeline that reruns whenever the survey data changes."

---

### Slide 4 — User research
**On slide:** Target users: students 18–30. Convenience sampling. Questionnaire: MCQ + ordinal + numeric + open-ended. n = 32.
**Say:** "Before designing anything, I collected evidence by using **convenience sampling** of people aged **18 to 30**. The questionnaire contains multiple-choice items, ordinal ease ratings, numeric age and three open-ended questions. We received **32 responses**, which meets the brief's target of **30**, although it remains a modest sample. Because **72%** named Spotify, our platform conclusions are strongest for Spotify."

---

### Slide 5 — Empathise
**On slide:** Empathy map (Says / Thinks / Does / Feels) + top 3 pain points.
**Say:** "That sample gives us a clear user picture. In the empathy map, users say 'remove ads' and 'improve recommendations'. They do save songs — **84%** add to a playlist or like a track — but **47%** sometimes struggle to find old saves, and they feel mildly satisfied rather than delighted. Ranked pain points put ads at **53%**, recommendations and taste at **38%**, and interface issues at **19%**. Ads are the largest complaint, but they are outside our technical scope."

---

### Slide 6 — Statistical findings
**On slide:** Three summary cards + honest reading. The five full-size charts are on slides 7–11.
**Say:** "To move from opinion to evidence, I coded the ordinal answers from **1 to 3**, with **2** as neutral, and ran **one-sample t-tests** against that midpoint. Vibe-finding ease was significantly above neutral, with a mean of **2.34** and **p = 0.0138**. Taste understanding was also above neutral at **2.31**, with **p = 0.0159**. Saved retrieval was **1.94** with **p = 0.730**, so it was not significant. I am deliberately not overclaiming: this is a good-but-not-great baseline, and the opportunity is refinement."

---

### Slide 7 — Evidence 1: platform and usage
**On slide:** Primary-platform and usage-frequency bar charts, full width.
**Say:** "Let me ground those tests in the charts. This first chart shows the platform mix: **23 of 32**, or **72%**, use Spotify, while four use YouTube Music, two use Apple Music and three use another service. Usage is concentrated too — **19 listen daily** and eight several times a week. That imbalance is a limitation, and I state it openly rather than hide it."

---

### Slide 8 — Evidence 2: discovery and saving
**On slide:** Discovery-source and post-like action charts, full width.
**Say:** "Discovery is more scattered than usage. **Nine** respondents find music outside the app, nine by search, eight through recommendations and six through playlists. Yet **27 of 32 save or like tracks**. That is the practical gap: people save music, but discovery often happens elsewhere. Our saved-music library addresses exactly that moment of finding a track again."

---

### Slide 9 — Evidence 3: ordinal distributions
**On slide:** Four bar charts showing the raw 1–3 counts behind the baseline tests.
**Say:** "These bar charts show the raw counts behind the averages I just quoted. Vibe-finding ease averages **2.34**, taste understanding **2.31**, and saved retrieval **1.94**, with the p-values we saw on the previous slide. The important reading is that above neutral does not mean dissatisfaction. It means there is room to refine a system that already works reasonably well."

---

### Slide 10 — Evidence 4: age and score spread
**On slide:** Age histogram and box plots of the three ordinal scores.
**Say:** "The spread matters as much as the average. We have **32 numeric ages**, with a mean of about **19.7** and a median of **19**. The box plots show that saved retrieval has the widest spread of the three ordinal scores, which is why I treat it as the clearest in-scope target. With a sample of **32**, I call this directional evidence, not proof."

---

### Slide 11 — Evidence 5: correlations
**On slide:** Spearman correlation heatmap with grids and readable labels.
**Say:** "Correlations need the same caution. I used **Spearman's rank correlation**, because the data are ordinal. At this sample size a coefficient needs about **0.349** to be significant, and our strongest pair, vibe ease with saved retrieval, is only **0.331**, with **p = 0.064**. So I do not claim that one habit causes another. I describe the association, and I stop there."

---

### Slide 12 — Define
**On slide:** Persona "Aarav, 19" · POV · HMW · MoSCoW highlights.
**Say:** "From that evidence, I defined the user. Our composite persona is Aarav, a **19-year-old** daily Spotify user who discovers music outside the app and saves tracks he rarely revisits. The point of view statement is direct: a listener who saves but cannot rediscover, and who feels recommendations only somewhat match his taste, needs control over familiarity and mood-based retrieval. The how-might-we question follows: how do we give that control without a paid subscription? MoSCoW put Discover, My Music and the backend in **Must**; ads and offline downloads in **Won't**."

---

### Slide 13 — Ideation
**On slide:** Mind map + 10 ideas (show the list, highlight the top four).
**Say:** "Ideation started broad. We generated **ten ideas**, from a discovery slider and vibe tags to an AI chatbot and an ad blocker. I mapped them across discovery, mood, library, understanding and preferences, then scored every idea on **desirability, feasibility and viability**. That scoring was deliberate: it stops us choosing ideas simply because they sound exciting."

---

### Slide 14 — Idea selection + hypotheses
**On slide:** Weighted matrix (D 40% / F 35% / V 25%); top score 5.00; H₀/H₁ written in advance.
**Say:** "The weighted matrix used **40% desirability, 35% feasibility and 25% viability**. The discovery slider, vibe tags and save-plus-library each scored **5.00**, the highest. The AI chatbot scored **2.45** and the ad blocker **2.60**, so both were rejected on feasibility, mainly because we have no API access. Before testing, I also fixed three hypotheses: lower retrieval time, taste satisfaction above the **2.31** baseline, and SUS above **68**, at **alpha = 0.05**."

---

### Slide 15 — Prototype
**On slide:** Architecture diagram: Extension (HTML/CSS/JS) → Flask routes → SQLite; screenshots of panel, dashboard, study page.
**Say:** "The prototype has two connected parts. The Chrome extension injects a side panel into three music sites and detects the current track through one adapter per platform. The companion dashboard is responsive HTML, CSS and JavaScript served by Flask, with SQLite storing saved songs, preferences, usage events and test tasks. Everything stays local, with no login and no external API. I will now show the live build: Discover, one save, and the My Music list."

---

### Slide 16 — Testing and validation
**On slide:** Paired design · timed tasks · SUS · tests chosen · one author pilot.
**Say:** "For validation, the intended design is paired: the same participants try both approaches. The study page times three tasks and counts clicks and errors, then computes a **System Usability Scale** score out of **100**. For task time I would use a **Wilcoxon signed-rank test** if the data are non-normal, otherwise a paired t-test; for SUS, a one-sample t-test against **68**. I ran one author pilot to check the instrument: **46.6**, **27.0** and **23.4 seconds**, all completed, plus a self-rating of **35.0**. That is a system check, not participant validation, and I keep the two separate."

---

### Slide 17 — Results and iterations
**On slide:** Three improvements made; one author pilot verified the logging.
**Say:** "Iteration was driven by failures, not guesswork. First, I split track detection into per-platform adapters after the single-file version broke on YouTube Music's changing DOM. Second, I added the companion dashboard because saved songs existed in extension storage but had no view. Third, I added usage logging and a consent toggle, so testing is based on measurement rather than recall. The pilot confirmed that task times, clicks and the SUS score are stored correctly; real participant runs remain future work."

---

### Slide 18 — Impact and limitations
**On slide:** Benefits · feasibility · threats to validity.
**Say:** "The benefits are concrete: no account is required, data never leaves the browser, and the utility works across three platforms. The limits are equally concrete. The sample is **32**, which is modest; **72%** are Spotify users and only **6%** Apple Music; ads, the biggest complaint, are out of scope; the recommendations are demo data; and this was a single-contributor project, so team roles were consolidated. I disclose these rather than hide them, because that is what makes the rest of the claim credible."

---

### Slide 19 — Conclusion and future scope
**On slide:** Key learning · conclusion · future work.
**Say:** "What I learned is that a small, focused utility can address a real, measured gap — saved-song retrieval and taste control — without complex infrastructure. The prototype addresses the in-scope pain points; it does not claim to fix ads. Future work is clear: replace the demo database with a learned model, implement the Understand section, and collect a larger, stratified sample."

---

### Slide 20 — References and Q&A
**On slide:** Google Forms dataset · brief · libraries (Flask, pandas, scipy, matplotlib) · sites' UI.
**Say:** "Sources are our anonymised survey dataset, the assignment brief, and the open-source libraries behind the backend and analysis. AI tools were used for code and documentation drafting, and that is disclosed in the paper. With that, I am done. Thank you — I am happy to take questions."

---

## Demo sequence to rehearse (keep under 2 minutes)
1. `cd webapp && python3 app.py` → open `http://127.0.0.1:5000`
2. `/discover` → choose Familiar → save a song
3. `/` → show it in the SQLite-backed My Music list
4. `/vibe` → pick "chill" → save another
5. `/study` → start a task, show SUS form
6. `/results` → show charts and anonymised rows

**If the live demo fails:** have screenshots of these six pages ready as fallback.
