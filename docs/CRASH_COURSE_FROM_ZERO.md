# Viva Crash Course From Zero

Read this file **in order, cover to cover**, over the next two days. It assumes you
know nothing. Every technical term is explained the first time it appears.

## The one rule for studying

For every section, do this four-step loop. **Do not skip the writing or the speaking.**

1. **Read** the section once (5–10 min). Don't highlight anything.
2. **Write** the key points on paper from memory, with the book closed (3 min).
3. **Say** them out loud as if teaching a friend (2 min).
4. **Check** against the text, put a star next to what you missed (1 min).

Reading alone creates the illusion of knowledge. Writing and speaking create
actual knowledge. Repeat starred items at the start of the next session.

---

# 1. What this project actually is (learn this first)

## In plain English

Somebody listens to music every day, saves songs they like, and then cannot find
them again. Their recommendations feel "okay" but not great. The biggest
complaint — ads — cannot be fixed by a student project, because removing ads
requires controlling the streaming company's playback.

So the project does three things:

1. **Find out if the problem is real.** A questionnaire with **25 real student
   responses**, analysed with statistics.
2. **Build a small fix.** A Chrome extension that adds a side panel on Spotify,
   YouTube Music and Apple Music. It offers **Discover** (Familiar / Balanced /
   Exploratory), **Find by Vibe** (mood tags), and a **saved-song library**.
3. **Build a dashboard.** A Flask + SQLite website to view saved songs, change
   preferences, and run a usability study.

## Why it counts as four subjects

| Subject | Where it appears |
|---|---|
| Design Thinking | The five stages: Empathise → Define → Ideate → Prototype → Test |
| Python | `webapp/app.py` (Flask server) and `webapp/analysis/analysis.py` (statistics) |
| Web Technology | HTML, CSS, JavaScript, the Flask website, the Chrome extension |
| Probability & Statistics | t-tests, confidence intervals, correlations, hypothesis testing |

## The one paragraph you must be able to say

> "I built a Chrome extension that adds a privacy-first personalisation panel to
> Spotify, YouTube Music and Apple Music, plus a Flask and SQLite dashboard.
> Its core features are Discover with three familiarity levels, Find by Vibe,
> and a saved-music library. The design was driven by a 25-response survey and
> measured with built-in usage logging and a SUS study."

---

# 2. Design Thinking, explained from zero

**Design Thinking** is a way of solving problems by starting with the *person*,
not the technology. It has **five stages** (Brown, 2008). You can move back and
forth between them — it is not a rigid ladder.

| Stage | What it means | What we actually did |
|---|---|---|
| **1. Empathise** | Understand the user's life and feelings | Questionnaire with 25 responses, coded the open-text answers, made an empathy map and a persona |
| **2. Define** | Turn the mess into one clear problem | Point of View (POV), How Might We (HMW), MoSCoW priorities, descriptive statistics |
| **3. Ideate** | Generate lots of possible solutions | 10 ideas, mind map, SWOT analysis, weighted selection matrix |
| **4. Prototype** | Build a rough, cheap version | The Chrome extension + the responsive Flask dashboard + SQLite |
| **5. Test** | Try it with users and measure | Three timed tasks, click/error logging, 10-item SUS form, hypothesis tests |

## Terms the professor may use

- **Double diamond:** the process diverges (explores widely) and converges
  (narrows down) twice — first on the *problem*, then on the *solution*. Our
  questionnaire→persona step is the first diamond; our 10-ideas→selection-matrix
  step is the second.
- **Empathy map:** four quadrants — **Says, Thinks, Does, Feels** — summarising
  real user responses. Ours surfaced ads, repetitive recommendations, and saving.
- **Persona:** one invented-but-realistic archetype representing the typical
  user. Ours is **Aarav, 19**, a B.Tech student and daily Spotify listener who
  saves tracks but rarely revisits them.
- **POV (Point of View):** a one-sentence problem statement with the shape
  *"[user] who [struggle] needs [solution] because [insight]."*
  Ours: a daily listener who saves but cannot rediscover, and feels
  recommendations only "somewhat" match their taste, needs familiarity control
  and mood-based retrieval, because discovery happens outside the app and saved
  collections are hard to navigate.
- **HMW (How Might We):** an open question that invites solutions, not a yes/no
  question. Ours: *"How might we give listeners control over the familiarity of
  recommendations and let them rediscover saved music by mood, without requiring
  a paid subscription or a new account?"*
- **MoSCoW:** Must / Should / Could / Won't prioritisation. **Must** = Discover,
  My Music, backend. **Won't** = ad removal, offline downloads.
- **SWOT:** Strengths, Weaknesses, Opportunities, Threats — used to check the
  chosen idea against fragile site selectors and the small sample.
- **Weighted selection matrix:** score each idea 1–5 on **desirability (40%)**,
  **feasibility (35%)** and **viability (25%)**, multiply by the weights and add.
  We generated **10 ideas**; three scored **5.00** (discovery slider, vibe tags,
  save + library). The ad blocker scored **2.80** and was rejected as infeasible.

---

# 3. Research methodology, explained from zero

## Sampling

**Convenience sampling** means using whoever was easy to reach — here, students.
It is *not* random. Consequence: you cannot claim the result applies to all music
listeners; you must state that as a limitation. We got **25 responses** against a
brief target of **30**.

## Question types in the questionnaire

| Type | Example | Why it matters |
|---|---|---|
| Multiple choice | "Which platform do you use most?" | Gives clean counts/percentages |
| **Ordinal** | "Easy / Average / Difficult" | Ordered categories, but the gaps are not equal |
| Numeric | "Age" | Can compute mean, median, spread |
| Open-ended | "What is the biggest problem you face?" | Gives real quotes and themes |

**Ordinal** is a word you must know: the answers have an order (Easy > Average >
Difficult) but you cannot say the distance from Easy to Average equals Average
to Difficult. That is why Spearman correlation is safer than Pearson.

## How we coded the answers

To do maths on words, we map them to numbers:

- **3** = positive: Easy / Very well / Daily
- **2** = middle: Average / Somewhat / Several times a week
- **1** = negative: Difficult / Poorly / Occasionally / Sometimes difficult

**Neutral = 2.** This "2" is the comparison point for every t-test below.

## Ethics

Participants were told the purpose, participation was voluntary, names were
replaced with **R01–R25**, no contact details were collected, and AI tool use was
disclosed. Two low-quality responses were **flagged, not deleted**, and no data
was invented or altered.

---

# 4. Statistics, explained from zero

This is the section professors dig into hardest. Learn the ideas, then the numbers.

## 4.1 Mean, median, standard deviation

- **Mean** = average: add the values, divide by how many.
- **Median** = the middle value when sorted.
- **Standard deviation (SD)** = the typical distance from the mean. Small SD =
  everyone answered similarly; large SD = answers were spread out.

Our ages: range **18–30**, median **19**, numeric mean **19.76**, SD **2.44**.

## 4.2 The one-sample t-test

**Question it answers:** "Is our sample mean different from a known number?"

Here the known number is **2 (neutral)**. We run one test per measure.

- **t** = how far our mean is from 2, measured in standard errors. Larger |t| =
  stronger evidence of a real difference.
- **p-value** = if there were *no* real difference, how likely would we see data
  this extreme? Small p (under **0.05**) means that is unlikely, so we call the
  result **statistically significant**.
- **alpha = 0.05** is the threshold we fixed before testing.
- **95% confidence interval (CI)** = the range of plausible values for the true
  mean. If the interval does **not** contain 2, that agrees with p < 0.05.
- **df = 24** = degrees of freedom = n − 1 = 25 − 1.

### Our four results — memorise as pairs

| Measure | Mean | SD | t | p | 95% CI | Reading |
|---|---|---|---|---|---|---|
| Usage frequency | **2.48** | 0.77 | 3.116 | **0.0047** | [2.16, 2.80] | above neutral |
| Vibe-finding ease | **2.48** | 0.65 | 3.674 | **0.0012** | [2.21, 2.75] | above neutral |
| Saved retrieval | **2.12** | 1.01 | 0.592 | **0.5593** | [1.70, 2.54] | **not** significant |
| Taste understanding | **2.40** | 0.65 | 3.098 | **0.0049** | [2.13, 2.67] | above neutral |

**Interpretation, word for word:**
> "Vibe-finding ease and taste understanding were significantly above neutral,
> while saved retrieval was not. These results do not support a claim that users
> are deeply dissatisfied. They support a narrower claim: personalisation is
> good but not great, and retrieval friction is common enough to address."

**Good-but-not-great baseline** is the phrase to keep repeating. Never say users
are broken or deeply unhappy — the data does not support it.

## 4.3 Correlation

**Question it answers:** "When one answer goes up, does another go up or down?"

- **r** or **rho (ρ)** ranges from **−1 to +1**.
- **Sign:** + means both rise together; − means one rises as the other falls.
- **Size:** 0.1 weak, 0.3 moderate, 0.5+ strong (rough guide).
- **Pearson** assumes a straight-line relationship and interval data.
- **Spearman** uses **ranks** instead of raw values — safer for **ordinal** data
  and small samples. We report both and rely on Spearman.
- **p** says whether the association is unlikely to be chance.
- **Critical |r| at n=25 ≈ 0.396.** A coefficient must be at least this big to
  be significant at alpha 0.05.

### Our correlations

| Pair | Pearson | Spearman | p | Reading |
|---|---|---|---|---|
| Vibe ease ↔ saved retrieval | +0.413 | +0.393 | 0.0522 | just misses |
| Vibe ease ↔ taste | +0.415 | +0.334 | 0.1027 | weak, directional |
| **Saved retrieval ↔ taste** | +0.433 | **+0.417** | **0.0380** | **the only significant pair** |
| Usage frequency ↔ taste | +0.101 | +0.166 | 0.4280 | weak |

**The cautious answer:**
> "At n=25 the critical value is about 0.396. Only saved retrieval with taste
> clears it, at +0.417 and p = 0.038. Because the sample is small and I ran
> several comparisons, I treat it as directional evidence and never claim
> causation."

**Correlation is not causation** — always say this if asked.

## 4.4 Hypotheses (fixed BEFORE testing)

| | Claim |
|---|---|
| **H1a** | Median time to find a saved song is **lower** with the prototype |
| **H0a** | No difference in retrieval time |
| **H1b** | Mean taste rating after using discovery **exceeds 2.40** |
| **H0b** | Unchanged from 2.40 |
| **H1c** | Mean SUS score **exceeds 68** |
| **H0c** | SUS is 68 or lower |

- **H0 (null)** = "nothing happens"; **H1 (alternative)** = "something happens".
- **Paired design** = the same participants try both methods, so each person is
  their own control.
- Planned tests: **Wilcoxon signed-rank** for time if the difference is not
  normal, otherwise a **paired t-test**; **one-sample t-test** for SUS vs 68.
- **Effect size** = *how big* the improvement is, not just whether it is
  statistically detectable. Report the mean difference too.

## 4.5 The honest status of the usability study

We built and instrumented the Study page — timed tasks, clicks, errors, SUS form.
**Participant runs were still being collected.** Therefore **no SUS score and no
task-time result is claimed**. Section 10.3 of the paper says so explicitly.
Never invent one.

---

# 5. Every important number in one place

| Number | Meaning |
|---|---|
| **25** | survey responses (target 30) |
| **23** | substantive responses; 2 flagged, none deleted |
| **19** | median age (range 18–30, mean 19.76, SD 2.44) |
| **64%** | Spotify (16 people) — platform imbalance |
| **16% / 12% / 8%** | YouTube Music / Other / Apple Music |
| **84%** | daily or several times a week **and** save/playlist a liked song |
| **44%** | sometimes struggle to find old saves (11 people) — the design target |
| **48%** | ads/paywall complaint (12 people) — biggest, out of scope |
| **36% / 20% / 12% / 4%** | recommendations / UI / vibe / saving themes |
| **52%** | taste only somewhat or poorly understood (11 somewhat + 2 poorly) |
| **2.40, p .0049** | taste above neutral |
| **2.48, p .0012** | vibe ease above neutral |
| **2.12, p .5593** | retrieval **not** significant |
| **0.396** | critical |r| at n=25 |
| **+0.417, p .038** | retrieval ↔ taste, only significant correlation |
| **68** | SUS benchmark |
| **0.05** | alpha |
| **5** | Design Thinking stages; winning matrix score (5.00); DB tables; website pages |
| **40/35/25** | desirability / feasibility / viability weights |
| **10** | ideated concepts |
| **2 seconds** | how often the extension polls for the current track |

---

# 6. The website, explained from zero

## 6.1 What happens when you open a web page

1. You type a URL like `http://127.0.0.1:5000/discover`.
2. Your browser sends an **HTTP request** to the **server** (here: Flask running
   on your own machine).
3. The server runs a function and returns **HTML** in an **HTTP response**.
4. Your browser renders the HTML; the **CSS** makes it look good and the
   **JavaScript** makes it interactive.

**GET vs POST:** GET asks for a page and puts data in the URL
(`?level=familiar&platform=Spotify`). POST submits data in the request body,
used for forms and saving data.

## 6.2 The roles of HTML, CSS and JavaScript

- **HTML** = structure and content (headings, buttons, forms, tables).
- **CSS** = appearance (colours, spacing, layout, mobile rules).
- **JavaScript** = behaviour (react to clicks, talk to the server, update the page).

## 6.3 Flask and routes

**Flask** is a small Python web framework. A **decorator** like
`@app.route("/discover")` tells Flask: *"when someone requests /discover, run the
function directly underneath."* The function returns a rendered template.

| URL | Function | What happens |
|---|---|---|
| `/` | `index()` | Reads `saved_songs`, shows 3 counts |
| `/discover` | `discover()` | Reads `?platform=` and `?level=` from the URL, computes recommendations |
| `/vibe` | `vibe()` | Reads `?vibe=`, computes mood recommendations |
| `/preferences` | `preferences()` | GET shows the form; POST saves it |
| `/study` | `study()` | Shows past tasks and the SUS form |
| `/results` | `results()` | Reads the anonymised CSV, counts stats, shows charts |
| `/api/save` | `api_save()` | JSON API: inserts a saved song |
| `/api/unsave/<id>` | `api_unsave()` | JSON API: deletes a saved song |
| `/api/event` | `api_event()` | JSON API: logs a click/task/SUS event |
| `/api/task` | `api_task()` | JSON API: stores a completed timed task |
| `/api/summary` | `api_summary()` | Raw database counts |
| `/health` | `health()` | Is the server alive, is the CSV present? |

`request.args.get("level")` reads URL values; `request.form.get(...)` reads POST
form values; `request.get_json()` reads JSON sent by JavaScript.

## 6.4 Jinja templates

**Jinja** is the template language: it lets Python values appear inside HTML.

- `{{ variable }}` prints a value.
- `{% for x in items %}` loops; `{% if saved %}` conditionally shows a block.
- `{% extends "base.html" %}` + `{% block content %}` means all pages share the
  same header/nav/footer from `base.html` and only replace the middle.
- `url_for('index')` builds a URL from a function name instead of hard-coding `/`.

## 6.5 SQLite and the five tables

**SQLite** is a database stored in a single file (`webapp/pme.db`). A **table**
is like a spreadsheet: rows are records, columns are fields.

| Table | Stores |
|---|---|
| `users` | Anonymous browser ID from a cookie — no name, no login |
| `saved_songs` | title, artist, genre, reason, source |
| `preferences` | default level, preferred vibe, tracking consent |
| `usage_events` | event type and detail — every view, save and task start |
| `test_tasks` | task name, duration, clicks, errors, completed |

SQL words you should know: `SELECT` (read), `INSERT` (add), `UPDATE` (change),
`DELETE` (remove), `WHERE` (filter), `UNIQUE` (no duplicates), `FOREIGN KEY`
(a row must refer to a real row in another table), `INDEX` (faster lookup).

`ON CONFLICT` was replaced with a simple **upsert**: try `UPDATE`; if no row
changed, `INSERT` a new one.

## 6.6 The cookie

`pme_session` is a random ID stored in the browser. It lets the server recognise
the same browser on repeat visits **without any login or name**. That is how we
keep the data anonymous and still measure a single user across pages.

## 6.7 Follow one click end-to-end (very likely question)

**"User presses Save on a recommendation":**

1. HTML button holds `data-title`, `data-artist`, `data-genre`, `data-reason`,
   `data-source` — the song's details.
2. `app.js` listens for a click, reads those into `button.dataset.title` etc.
3. `postJSON('/api/save', song)` sends them as JSON via `fetch()`.
4. Flask's `api_save()` reads the JSON, checks title and artist are present.
5. It runs `INSERT OR IGNORE INTO saved_songs ...` — SQLite adds the row.
6. It logs a `save_song` event into `usage_events`.
7. It replies `{"ok": true}`; JavaScript changes the button to "Saved ✓".

**"User opens /discover":** Flask reads the URL values → calls
`get_recommendations(platform, level, artist)` in `recommendations.py` → that
looks up a plain demo dictionary → Flask checks which songs are already saved →
logs a `discover_view` event → renders `discover.html`.

## 6.8 JavaScript vocabulary

| Code | Meaning |
|---|---|
| `querySelector` / `querySelectorAll` | Find one element / all matching elements |
| `addEventListener('click', fn)` | Run `fn` when clicked |
| `button.dataset.title` | Read the HTML `data-title="..."` attribute |
| `classList.add/toggle` | Change CSS classes, which changes appearance |
| `fetch(...)` | Send a request from the browser to Flask |
| `async` / `await` | Wait for the reply, then use the result |
| `event.preventDefault()` | Stop the browser's default action (e.g. page reload) |
| `performance.now()` | High-precision timer for the task study |
| `i % 2 === 1` | Remainder — true for odd question numbers |
| `location.reload()` | Refresh the page to show the new task row |

**SUS scoring:** sum of (answer − 1) for odd questions and (5 − answer) for even
questions, then multiply by **2.5** to get 0–100. **68** is the benchmark.

## 6.9 CSS vocabulary

`:root { --green: #1DB954; }` defines a reusable **variable**;
`var(--green)` uses it. `display: flex` arranges items in a line;
`display: grid` arranges rows and columns. `@media (max-width: 720px)` applies
extra rules only on small screens — that is the **responsive** part.

## 6.10 The Chrome extension (separate from the website)

A **content script** is injected into Spotify / YouTube Music / Apple Music
pages and adds a side panel. Each platform has an **adapter** that checks
`window.location.hostname` to decide if it applies, then finds the current track.
`content.js` polls `getCurrentTrack()` every **2 seconds** — polling was chosen
over `MutationObserver` because these single-page apps constantly rebuild their
DOM, which breaks observers. `chrome.storage` holds data on the client;
SQLite holds data for the dashboard and measurement. If a site changes its
HTML selectors, only that adapter file needs fixing — a documented limitation.

## 6.11 `analysis.py` — where the numbers come from

Run: `python3 webapp/analysis/analysis.py --csv "Music Streaming Platform Experience (Responses) - Form responses 1.csv"`

It reads the raw Google Forms CSV → writes `data/survey_responses_anonymised.csv`
(R01–R25) → computes counts, one-sample t-tests, Pearson/Spearman correlations,
confidence intervals and theme counts → writes `docs/statistical_results.md` →
draws 5 charts into `data/charts/`. It is **re-runnable**, so new responses
update every deliverable. It is the **canonical source of truth**.

## 6.12 Inspect Element — what to say when they point

| They point at | Say |
|---|---|
| Top bar with 6 links | "That's `base.html`, shared by all pages with Jinja `{% extends %}`." |
| Green highlighted link | "The template adds `class="active"`; CSS paints `.nav a.active` green." |
| Stat cards | "Counted from the CSV by `survey_summary()` in `app.py`, so they match the survey." |
| Song card + Save | "One item from `recommendations.py`; `data-*` attributes travel to `/api/save` through app.js." |
| "Saved ✓" | "app.js added the `saved` CSS class and changed the label; Flask inserted a SQLite row." |
| Remove button | "`data-id` is the row id; POST to `/api/unsave/<id>`, then JS removes the list item." |
| Vibe tags | "Links with `?vibe=chill`; Flask reads them with `request.args`. No JS needed." |
| Dropdowns / GET form | "Values go in the URL; Flask reads them with `request.args.get()`." |
| Preferences checkbox | "Unchecked sends nothing, so Flask treats it as tracking = 0." |
| Task button | "app.js times it with `performance.now()`, counts clicks, POSTs to `/api/task`." |
| SUS radios | "Five radios share `name=q1`, so only one can be chosen. All ten are required." |
| SUS score text | "Odd items −1, even items 5−answer, sum × 2.5. 68 is the benchmark." |
| Charts | "Generated by `analysis.py`, served by Flask through `/charts/<filename>`." |
| Response table | "A Jinja `{% for %}` loop over CSV rows; bracket names must match the CSV header." |
| Dark theme / green | "CSS variables in `:root` at the top of `style.css`." |
| Mobile layout | "The `@media (max-width: 720px)` block at the bottom of `style.css`." |
| `@app.route(...)` | "Decorator: maps a URL to the function below it." |
| `render_template(...)` | "Fills a Jinja template with variables and returns HTML." |
| `{{ var }}` / `{% %}` | "Jinja prints a value / runs logic." |
| `g` / `get_db()` | "Flask's per-request box: one SQLite connection per request, closed afterwards." |
| Cookie | "Anonymous random ID — no login, no personal data." |
| `UNIQUE`, `FOREIGN KEY` | "Prevent duplicate saves; ensure every song belongs to a real user." |
| `fetch` / `async await` | "Browser-to-server JSON call, waiting for the response." |
| `if __name__ == "__main__":` | "Start the server only when this file is run directly." |
| `debug=True` | "Auto-reload on edits; prototype only." |

---

# 7. How to answer any question under pressure

Use this four-part shape. It keeps you calm and sounds authoritative:

1. **Direct answer first** — one sentence.
2. **Evidence** — the number, file or stage that supports it.
3. **Why** — the reasoning behind the choice.
4. **Limitation** — one honest caveat.

Example: *"Yes, one correlation is significant (1). Retrieval with taste is
+0.417 at p = 0.038 (2). I used Spearman because the data are ordinal and n is
small (3). But with 25 responses and several comparisons I treat it as
directional, not causal (4)."*

**If you genuinely don't know:** say *"I'm not certain about that detail; the
place to check would be ___."* Never invent a number. An honest "I don't know
that detail" costs far less than a wrong figure.

**Buying time phrases:** "Let me frame that in two parts…" / "The short answer
is…, and the reason is…"

---

# 8. The question bank (practise these out loud)

## Overview

1. **Tell me about your project.** → the one paragraph in §1.
2. **Why is it an integrated project?** → four subjects table in §1.
3. **What was the main problem you solved?** → save-and-retrieve gap: 84% save,
   44% struggle to find old saves.
4. **What is the strongest evidence for your solution?** → same numbers.
5. **What did you cut?** → ad blocker (needs playback control), offline
   downloads, Understand section.

## Design Thinking

6. **Name the five stages.** → Empathise, Define, Ideate, Prototype, Test.
7. **What is Design Thinking?** → human-centred problem solving (Brown 2008).
8. **What is a double diamond?** → diverge/converge on problem, then solution.
9. **What is an empathy map?** → Says/Thinks/Does/Feels from real responses.
10. **Persona vs empathy map?** → one archetype vs aggregated emotional picture.
11. **What is your POV?** → §2.
12. **What is your HMW?** → §2.
13. **What is MoSCoW?** → Must/Should/Could/Won't.
14. **What is SWOT?** → Strengths/Weaknesses/Opportunities/Threats.
15. **How did you select ideas?** → 10 ideas, 40/35/25 weights, top 5.00, ad
    blocker 2.80 rejected.
16. **Why not build the ad blocker?** → client-side utility cannot control ads;
    put in Won't and disclosed as a limitation.

## Research and statistics

17. **Sampling method?** → convenience, students, n=25.
18. **Why not 30?** → time constraint; report real 25 honestly, no fabrication.
19. **Question types?** → MCQ, ordinal, numeric, open-ended.
20. **What is ordinal data?** → ordered categories, unequal gaps; use Spearman.
21. **How did you code responses?** → 3/2/1, neutral = 2.
22. **Which tests and why?** → one-sample t-test vs 2; Pearson + Spearman; CIs.
23. **What is a p-value?** → probability of data this extreme if H0 were true.
24. **What is a confidence interval?** → range of plausible true values.
25. **What is alpha?** → threshold 0.05 fixed before testing.
26. **What is a t-test?** → compares a sample mean with a known value.
27. **What is a correlation?** → direction and strength of a relationship.
28. **Pearson vs Spearman?** → Pearson on raw values, Spearman on ranks;
    Spearman safer for ordinal/small n.
29. **Correlation vs causation?** → association does not prove one causes the other.
30. **Give me your key results.** → the four t-tests in §4.2.
31. **Which are significant?** → vibe and taste; retrieval is not.
32. **Any significant correlation?** → retrieval ↔ taste, +0.417, p 0.038,
    critical 0.396, described cautiously.
33. **What is effect size?** → how big the change is, not just detectable.
34. **What is SUS?** → 10 items, 0–100, 68 benchmark, formula in §6.8.
35. **What are your hypotheses?** → H1a/b/c in §4.4.
36. **Paired design?** → same users try both methods.
37. **Wilcoxon vs paired t-test?** → Wilcoxon if difference non-normal; paired
    t-test otherwise.
38. **What do the results actually mean?** → "good but not great" in §4.2.
39. **How did you protect participant data?** → R01–R25, no contact details,
    consent, AI disclosure.
40. **Any flagged data?** → two non-substantive rows flagged, not deleted;
    possible duplicate names; all rows retained and disclosed.
41. **Why is 64% Spotify a limitation?** → platform imbalance, limits
    generalisation.
42. **What are the open-text themes?** → ads 48%, recommendations 36%, UI 20%,
    vibe 12%, saving 4%.

## Technical / website

43. **Where is the frontend?** → extension panel + `webapp/templates/` with
    `static/style.css` and `static/app.js`.
44. **Where is Python?** → `app.py` (Flask), `recommendations.py` (demo data),
    `analysis/analysis.py` (statistics).
45. **Where is the database and what's in it?** → `pme.db`, five tables in §6.5.
46. **Why both chrome.storage and SQLite?** → client convenience vs shared,
    queryable measurement store; brief requires a database.
47. **Explain the request flow.** → §6.1 and §6.3.
48. **What does `@app.route` do?** → maps URL to function.
49. **What does `render_template` do?** → fills Jinja template, returns HTML.
50. **GET vs POST?** → URL vs body; §6.1.
51. **What is Jinja?** → template language; `{{ }}` and `{% %}`.
52. **What is `url_for`?** → builds URL from function name.
53. **How does a Save work?** → the seven steps in §6.7.
54. **What does `fetch` do?** → browser-to-server request.
55. **What are `data-*` attributes?** → custom HTML attributes read by JS as
    `dataset`.
56. **What is the cookie for?** → anonymous identity without login.
57. **What is `UNIQUE` / foreign key?** → §6.5.
58. **How does platform detection work?** → adapter checks hostname.
59. **Why poll instead of MutationObserver?** → SPAs rebuild DOM constantly.
60. **What if a site changes its layout?** → that adapter's selectors break;
    one file to fix; documented limitation.
61. **What does `analysis.py` do?** → §6.11.
62. **How do you regenerate everything?** → run analysis script, then
    `python3 docs/build_presentation.py` and `python3 docs/build_paper.py`.
63. **Is the recommendation engine real AI?** → no, a rule-based demo database;
    stated limitation.
64. **Why Flask and not Django?** → Flask is small, enough for six pages and
    JSON APIs, easier to explain and inspect.
65. **Why dark theme?** → matches the music-player context; CSS variables make
    it easy to change.

## Honesty and scope

66. **You worked alone — what did you cut?** → one contributor covering five
    roles; individual brainstorming, no separate interview transcripts, mentor
    review instead of peer review; all disclosed in Appendix D; no fabrication.
67. **Where is your SUS result?** → instrument built, runs incomplete, no result
    claimed (§4.5).
68. **What would you do with more time?** → learned recommendation model,
    Understand section, 30+ stratified sample, completed paired study with
    effect sizes, mood-retrieval task-time test.
69. **What is the biggest limitation?** → small n, platform imbalance, demo
    recommendations, fragile selectors, single contributor.
70. **Why should this project be accepted?** → real measured problem, working
    system, honest statistics, reproducible pipeline.

---

# 9. Your two-day timetable

Times assume you start now (Sat ~18:00) and finish Sunday ~23:00.

## Saturday

**18:00–19:00 — Foundations.** Read §1 and §2. Write the one paragraph and the
five stages from memory. Say both out loud.

**19:00–19:15 — break.**

**19:15–20:45 — Research + statistics (most important block).** Read §3 and §4
slowly. You must understand *why* p<0.05 matters and *why* retrieval is not
significant. Write the four-row results table twice from memory. Say the
interpretation paragraph out loud 5 times.

**20:45–21:00 — break.**

**21:00–21:45 — Numbers.** Read §5. Write all numbers from memory, check, star
misses. Say each number with its meaning: say "forty-four percent — struggle to
find old saves", never just "44".

**21:45–22:30 — Answer technique + overview questions.** Read §7 and questions
1–5 of §8. Answer each out loud in the four-part shape.

**Stop around 22:30.**

## Sunday

**09:00–10:00 — Recall warm-up.** Rewrite §5 from memory. Re-do starred items.

**10:00–12:00 — Paper.** Read §5's section map in `viva_prep_guide.md` plus
questions 6–42 of §8. Answer every one out loud. Star the ones you cannot answer
without looking.

**12:00–13:00 — lunch / break.**

**13:00–15:00 — Website.** Read §6 in full. Open `http://127.0.0.1:5000` and
click through all six pages. After each page, say its route, function and table
out loud. Then read §6.7 (the Save flow) three times and say it without notes.

**15:00–15:15 — break.**

**15:15–17:00 — Inspect-element drill.** Right-click → Inspect on the live site.
Work down the table in §6.12. For every row: **say the answer first**, then check.
Also open `app.py`, `app.js` and a template and practise the construct table.

**17:00–17:45 — Remaining questions.** Questions 43–70 of §8, out loud.

**17:45–18:30 — break / food.**

**18:30–20:00 — Mock viva.** Get someone to read questions from §8 at random.
If alone, record yourself. Answer out loud, follow every answer with "Why?"
Look up what you missed, then immediately re-answer from memory.

**20:00–20:30 — Weak spots only.** Just your starred list. Nothing new.

**20:30–21:00 — The honesty block.** Reread §4.5 and Appendix D (§7 Q66–69).
These are the questions that catch people out.

**21:00–21:30 — Final recall.** §5 numbers + the three killer answers + the
five-line website explanation. Then stop and sleep.

## Monday morning (15 min, no new material)

Anchors, the one paragraph, and Q31/32/67. Then go.

---

# 10. Companion files

- `docs/viva_cheat_sheet.md` — short memorisation Q&A
- `docs/viva_prep_guide.md` — study method, paper map, inspect-element table
- `docs/statistical_results.md` — the canonical numbers
- `docs/design_thinking_artefacts.md` — empathy map, matrix, hypotheses
- `docs/presentation_script.md` — what to say on each slide
- `README.md` — how to run the site and regenerate outputs
