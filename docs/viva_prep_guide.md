# Viva Prep Guide — Research Paper + Website

**Project:** Reimagining the Personal Music Experience
**Student:** Preet Kamdar · 256019 · B.Tech CSE (AI & ML), JG University

This is the *how to learn it* document. `viva_cheat_sheet.md` is what to memorise;
this file tells you **how** to memorise it and **what to say** when someone points
at a piece of the website and asks "what does that do?"

---

## Part 0 — The only study method that works for this

Do **not** re-read the paper five times. Re-reading feels productive and recalls
almost nothing. Use this instead:

### The 3-pass loop (about 90 minutes total)

| Pass | Time | What you do |
|---|---|---|
| 1. Skim for structure | 15 min | Read only the headings of the paper and the names of the 6 website pages. Close it. Write the skeleton from memory. |
| 2. Active recall | 45 min | Open the blank sheet. Write every number you can remember and what it means. Then check against `viva_cheat_sheet.md`. Mark misses with a star. |
| 3. Teach it out loud | 30 min | Explain the project out loud, without notes, as if to a friend. Get stuck? Look once, then say the sentence again from memory. |

The third pass is the important one. **If you cannot say it out loud, you do not know it.**

### Spaced repetition schedule

Review the cheat sheet at increasing gaps so it moves into long-term memory:

- **Tonight:** Pass 1 + 2 + 3.
- **Tomorrow morning:** 10 minutes, write all numbers from memory.
- **2 days later:** 10 minutes, same.
- **4 days later:** 10 minutes, same.
- **Day before viva:** full mock viva, out loud, 30 minutes.

Each review should be *closed-book first, check second*. Stars get reviewed every time.

### "Blurting" (best for the paper)

Take a blank A4 sheet. In 5 minutes, dump everything you remember — numbers,
stage names, table names, page names. Then compare with the paper. Anything
missing gets written three times and said out loud three times. Do this once a day.

### Mock viva

Give `viva_cheat_sheet.md` to a friend. Ask them to read the **questions only**
and interrupt with follow-ups: "Why?", "How do you know?", "What if it fails?".
If nobody is available, record yourself on your phone and play it back.

---

## Part 1 — Number anchors (memorise this table first)

Everything in the paper comes back to these. Learn them as **pairs** (number + meaning).

| Anchor | Meaning |
|---|---|
| **29** | survey responses (target was 30) |
| **27** | responses judged substantive; 2 flagged, none deleted |
| **19** | median age (range 18–30, numeric mean 19.69) |
| **72%** | Spotify — biggest platform, so platform imbalance is a limitation |
| **84%** | use daily/several times **and** save or playlist a liked track |
| **47%** | sometimes struggle to find old saves (the design target) |
| **53%** | mention ads — biggest complaint, out of scope |
| **56%** | say taste is only somewhat/poorly understood |
| **2.31 / p .016** | taste rating, significantly above neutral 2 |
| **2.34 / p .014** | vibe-finding ease, significantly above neutral |
| **1.94 / p .730** | saved retrieval, **not** significant — honest framing |
| **0.349** | critical |r| at n=32 |
| **+0.331 / p .064** | vibe ease ↔ saved retrieval — strongest pair, still not significant |
| **68** | SUS benchmark score |
| **0.05** | alpha (significance level) |
| **5** | Design Thinking stages, and the winning matrix score (5.00) |
| **40/35/25** | desirability / feasibility / viability weights |
| **10** | ideas generated |
| **5** | database tables, and website pages |

**Sentence that ties it together (learn this verbatim):**
> "The baseline was good but not great: 84% save music yet 47% struggle to find
> old saves, and only 44% feel their taste is understood very well. So my project
> claims refinement, not rescue."

---

## Part 2 — Paper section map

Learn one "hook sentence" per section. If asked about any section, start with its hook.

| § | Section | Hook sentence / what they may ask |
|---|---|---|
| — | Title page | Preet Kamdar · 256019 · B.Tech CSE (AI & ML) · JG University; 4 mentors listed. |
| 1 | Abstract | One paragraph: problem → prototype → 32-response finding → limits. "Why is the abstract long?" Brief recommends ~50 words; mine includes the required statistic. |
| 2 | Keywords | 9 terms. Rarely asked, but know that SUS, hypothesis testing and Flask/SQLite are there. |
| 3 | Introduction | 84% routine use, 84% save, 47% retrieval trouble, 53% ads. Honest limits stated up front. |
| 4 | Literature review | Brown (2008) Design Thinking; Brooke (1996) SUS; collaborative filtering vs my rule-based demo DB; Spearman for ordinal data. |
| 5 | Objectives & problem | 5 objectives; POV and HMW statements. Know the HMW by heart: "How might we give listeners control over the familiarity of recommendations and let them rediscover saved music by mood, without requiring a paid subscription or a new account?" |
| 6 | Methodology | Convenience sample, 29 students, questionnaire types, 3→2→1 coding, neutral = 2, 5-stage table, stack, ethics. |
| 7 | Findings | Descriptive table, 5 charts, empathy map, persona Aarav (19), 4 t-tests, 4 correlations, 5 open-text themes. **Most likely section to be questioned.** |
| 8 | Ideation | 10 ideas, 40/35/25 weights, top 5.00 (slider, vibe tags, library), ad blocker 2.80 rejected as infeasible. |
| 9 | Prototype | Extension + dashboard, hostname adapters, 2-second polling, 5 DB tables, 6 features. |
| 10 | Testing | 3 hypotheses, SUS formula, Wilcoxon/paired t-test planned. **Section 10.3 is honest: no SUS or task-time result is claimed because runs were not complete.** |
| 11 | Conclusion | Strongest evidence = save-and-retrieve loop. Future work: learned model, Understand section, 30+ sample, completed paired study. |
| 12 | References | Brown, Brooke, brief, Google Forms, library docs, web players. |
| 13 | Appendices | A questionnaire, B interview guide (prepared, **not** administered), C consent, D single-contributor scope, E analysis code pointer. |

### The three paper questions you will almost certainly get

**"Are your results significant?"**
> "Taste understanding and vibe-finding ease are significantly above neutral —
> p = 0.0159 and p = 0.0138. Saved retrieval is not, at p = 0.730. So I do not
> claim users are deeply dissatisfied; I claim personalisation is good but not
> great, and retrieval friction is common enough to address."

**"Are any of your correlations significant?"**
> "No. At n=32 the critical value is about 0.349; the strongest pair is vibe ease with saved
> retrieval at +0.331 (p = 0.064). With a small sample and several comparisons I describe all
> six as weak and directional only — no claim of significance or causation."

**"Where is your actual usability result?"**
> "I built and instrumented the study page — timed tasks, clicks, errors and the SUS form — and then ran one author pilot: 46.6, 27.0 and 23.4 seconds, all completed, with a SUS self-rating of 35.0. That verifies the logging, but it is one biased self-assessment by the designer, so I do not claim a participant SUS result or a task-time effect. Section 10.3 says exactly that."

---

## Part 3 — Website map (what each file does)

```
webapp/
├── app.py                  Flask server: routes, database, JSON APIs
├── recommendations.py      Demo song data + 2 lookup functions
├── pme.db                  SQLite database (5 tables)
├── templates/
│   ├── base.html           Shared header, nav, footer, JS include
│   ├── index.html          My Music (saved songs)
│   ├── discover.html       Discover form + cards
│   ├── vibe.html           Mood tags + cards
│   ├── preferences.html    Settings form
│   ├── study.html          Timed tasks + SUS form
│   └── results.html        Charts + anonymised response table
├── static/
│   ├── style.css           All styling, incl. mobile media query
│   └── app.js              All browser click behaviour
└── analysis/analysis.py    Regenerates every number and chart
```

**The five-line explanation of the whole website (memorise):**
> "You type a URL, Flask matches it to a function with the same `@app.route`
> label. The function reads or writes SQLite, passes the result to a Jinja
> template, and the template becomes HTML. `app.js` in the browser handles the
> clicks and calls the JSON APIs; `analysis.py` is separate and regenerates the
> statistics."

### The six pages and their routes

| Page | URL | Flask function | What it does |
|---|---|---|---|
| My Music | `/` | `index()` | Reads `saved_songs`, shows 3 counts |
| Discover | `/discover` | `discover()` | Reads `?platform=` and `?level=` from the URL, calls `get_recommendations()` |
| Find by Vibe | `/vibe` | `vibe()` | Reads `?vibe=`, calls `get_vibe_recommendations()` |
| Preferences | `/preferences` | `preferences()` | GET shows form, POST updates/inserts a preferences row |
| Study | `/study` | `study()` | Shows last 10 tasks and the SUS form |
| Findings | `/results` | `results()` | Reads the anonymised CSV, counts 6 headline stats, shows 5 charts |

### The five database tables

| Table | One-line purpose |
|---|---|
| `users` | Anonymous browser ID from a cookie — no name, no login |
| `saved_songs` | Songs saved from Discover or Vibe |
| `preferences` | Default level, preferred vibe, tracking consent |
| `usage_events` | Every view, save and task-start — the built-in measurement |
| `test_tasks` | Duration, clicks, errors, completion for each timed task |

---

## Part 4 — Inspect Element survival guide

This is the high-risk part: they point at something on screen and ask "what is
that and what does it do?" Here is the answer for each common target.

### Visible things on the page

| They point at… | Say |
|---|---|
| **Top bar with 6 links** | "That's `base.html`. It is shared by every page using Jinja's `{% extends %}`. The links are Flask `url_for()` calls, so the URLs stay correct if routes change." |
| **The green highlighted link** | "The template adds `class="active"` to the current page based on the `active` value app.py passes. CSS paints `.nav a.active` green." |
| **Big number cards (32, 72%, 84%…)** | "Those are counted from the anonymised CSV by `survey_summary()` in app.py, so they can never drift from the survey data." |
| **A song card with Save** | "That card is one item from `recommendations.py`. The Save button carries `data-title`, `data-artist`… — those become `button.dataset.title` in app.js and get POSTed to `/api/save`." |
| **"Saved ✓" after clicking** | "app.js adds the CSS class `saved` and changes the label. The row is inserted into `saved_songs` by Flask." |
| **Remove button** | "Its `data-id` is the SQLite row id. app.js POSTs to `/api/unsave/<id>`, Flask deletes the row, and JS removes the list item from the page." |
| **Vibe tags** | "Plain links with `?vibe=chill` in the URL. Flask reads that with `request.args` — no JavaScript needed." |
| **Platform / level dropdowns** | "A GET form. Submitting puts the values in the URL, e.g. `/discover?platform=Spotify&level=familiar`, which Flask reads with `request.args.get()`." |
| **Preferences checkbox** | "An unchecked checkbox sends nothing, so Flask treats it as `tracking = 0`. The POST saves the form with a simple UPDATE, or INSERT if no row exists yet." |
| **Study timer button** | "app.js listens for clicks on `#task-panel`, uses `performance.now()` for the duration, counts all clicks globally, then POSTs to `/api/task`." |
| **SUS radio buttons** | "Each question has five radios with the same `name` (q1, q2…), so only one can be selected. All ten are required before the form computes the score." |
| **"SUS score: … / 100"** | "Sum of (answer−1) for odd items and (5−answer) for even items, times 2.5. 68 is the benchmark. The score is logged as an event." |
| **The 5 charts** | "Generated by `analysis.py` into `data/charts`. Flask serves them through `/charts/<filename>`; the page just displays them." |
| **Response table** | "Jinja `{% for r in rows %}` loop over the CSV rows. The bracketed names like `r['Name']` must match the CSV header exactly." |
| **Dark background / green buttons** | "CSS variables in `:root` at the top of `style.css`. Changing `--green` there recolours the whole site." |
| **Mobile layout** | "The `@media (max-width: 720px)` block at the bottom of `style.css`: it hides the nav, shows the menu button and stacks the cards." |

### Code constructs they may point at in the source

| Construct | Plain-English answer |
|---|---|
| `@app.route("/discover")` | "A decorator — it tells Flask: when this URL is requested, run the function underneath." |
| `request.args.get(...)` | "Reads a value from the URL after the `?`, e.g. `?level=familiar`." |
| `request.form.get(...)` | "Reads a value submitted by a POST form." |
| `request.get_json()` | "Reads the JSON body that app.js sent with fetch." |
| `render_template(...)` | "Fills a Jinja template with variables and returns the finished HTML." |
| `{% block content %}` | "A placeholder in base.html that each child page replaces with its own content." |
| `{{ variable }}` | "Jinja prints the value of a variable into the HTML." |
| `url_for('index')` | "Builds the URL for a named Flask function instead of hard-coding `/`." |
| `g` / `get_db()` | "Flask's per-request box. One SQLite connection is opened per request and closed after." |
| `sqlite3.Row` | "Lets us read a row like a dictionary: `row['title']` instead of `row[0]`." |
| Cookie `pme_session` | "A random ID stored in the browser so repeat visits are the same anonymous user. No login." |
| `UNIQUE(user_id, title, artist)` | "Stops the same song being saved twice for the same user." |
| `FOREIGN KEY(user_id)` | "Every saved song must belong to a real user row." |
| `INSERT OR IGNORE` | "Insert the row, but silently do nothing if it would break the UNIQUE rule." |
| `UPDATE` then `INSERT` | "My simple upsert: change the existing row; if nothing changed, create it." |
| `fetch(...)` in app.js | "Browser-to-server request. JSON goes out, JSON comes back." |
| `async` / `await` | "Wait for the server's reply, then continue using the result." |
| `button.dataset.title` | "Reads the HTML `data-title="..."` attribute." |
| `classList.toggle('open')` | "Adds the class if missing, removes it if present — that opens the mobile menu." |
| `event.preventDefault()` | "Stops the browser's default action (here, reloading the page on form submit)." |
| `querySelectorAll(...).forEach` | "Find every matching element and run the same function on each." |
| `i % 2 === 1` | "Remainder operator — true for odd question numbers, which are scored differently." |
| `--green: #1DB954` | "A CSS variable. `var(--green)` reuses it everywhere." |
| `flex` / `grid` | "Two CSS layout systems: flex for a line of items, grid for rows and columns." |
| `@media (max-width: 720px)` | "Apply these rules only on narrow screens." |
| `from __future__ import annotations` | "Lets Python read the type hints written in a relaxed order. No behaviour change." |
| Type hints like `-> dict` | "Documentation only — says what a function returns. Python does not enforce them." |
| `if __name__ == "__main__":` | "Run the server only when this file is executed directly, not when imported." |
| `debug=True` | "Auto-reloads on edits and shows errors in the browser. Prototype only." |

---

## Part 5 — If you blank out

Use these fallback sentences. They are honest and always true:

- **On any number:** "That comes from the analysis script, which reads the real
  Google Forms export; I can point you to the exact row in `statistical_results.md`."
- **On any code line:** "That's the browser half / server half of the same flow:
  click → API → SQLite → template → page."
- **On a missing participant result:** "I ran one author pilot to verify the instrument,
  but no participant study was completed. Section 10.3 says exactly that."
- **On working alone:** "I consolidated the five brief roles into one contributor
  and disclosed every reduction in Appendix D. No data was invented."
- **If you genuinely don't know:** "I'm not certain about that detail; the file to
  check would be ___." Never guess a number.

---

## Part 6 — Your checklist

**Tonight**
- [ ] Learn the 19 number anchors in Part 1 (write them twice, say them once).
- [ ] Learn the 5-line website explanation word for word.
- [ ] Do one blurting pass on the paper headings.

**Tomorrow**
- [ ] Closed-book: write the 4 t-test results and the 5 themes.
- [ ] Open the site, right-click → Inspect, and go through every row of Part 4 out loud.
- [ ] Change one CSS variable in DevTools and watch the page update — then say why it worked.

**Two days before**
- [ ] Mock viva with the cheat sheet, 30 minutes, out loud.
- [ ] Practise the three "almost certain" paper questions in Part 2.

**Day before**
- [ ] 10-minute closed-book recall of all anchors.
- [ ] Re-read Appendix D (single-contributor scope) and Section 10.3 (no claimed SUS result).
- [ ] Sleep. Recall collapses when you are tired.

---

## Companion files

- `docs/viva_cheat_sheet.md` — memorise-first Q&A
- `docs/statistical_results.md` — the canonical numbers and flags
- `docs/design_thinking_artefacts.md` — empathy map, matrix, hypotheses
- `docs/presentation_script.md` — what to say on each of the 20 slides
- `README.md` — how to run the website and regenerate everything
