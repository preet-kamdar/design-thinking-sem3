# Viva Crash Course — From Zero (English + light Hinglish)

Read this file in order. I assume you know nothing: every technical term is introduced with its **English definition** first, then a short **Hinglish line** (mostly English, with a little Hindi mixed in — the way you actually speak). The full course is below, but **if exams are also running, start with the FAST TRACK right under this**.

> **Note:** `docs/presentation_script.md` stays **English only** — that's what you recite on stage. Everything else here is English-dominant Hinglish. Term definitions always follow the same order: English first, Hinglish second.

---

# FAST TRACK — about 4 hours total, no writing

This is for someone with limited time. You will **not write a single line**. You only look, look away, and speak. Four short sessions spread across Saturday and Sunday — spacing matters more than total duration.

## The no-writing memory loop

For each fact or answer:

1. **Look** at it for 15 seconds.
2. **Cover** the screen with your thumb, or look away.
3. **Say** it out loud in your own words in 20–30 seconds.
4. **Reveal** and check. If you missed it, say the correct version once.

Hard items 3×, easy items 1×: **look → cover → say → check**. You must hear your own voice — silent reading doesn't build recall.

Two tricks that replace writing completely:

- **Voice note:** record your answers, play them back while walking or eating. Re-record only weak ones. 15 answers ≈ 6 minutes of listening.
- **Always say the number with its label.** Never say "44". Say "44 percent — sometimes struggle to find old saves". A naked number is useless; number + meaning together actually sticks.

## The 14 numbers that cover almost everything

Say each one with its label, five times per session:

1. **27** responses, target 30
2. **85%** save or playlist a liked track
3. **44%** sometimes struggle to find old saves
4. **48%** mention ads — out of scope
5. **67%** Spotify — platform imbalance
6. **52%** say taste is only somewhat or poorly understood
7. **2.41, p 0.003** — taste above neutral, significant
8. **2.44, p 0.003** — vibe ease above neutral, significant
9. **2.04, p 0.852** — retrieval, **not** significant
10. **0.381** — critical |r| at n=27
11. **+0.385, p 0.047** — vibe ease ↔ saved retrieval, the only significant pair
12. **68** — SUS benchmark
13. **0.05** — alpha
14. **5** stages, and 40/35/25 weights

## The 15 questions that cover most of the marks

Use the full answers in §8, but prioritise these: **1, 6, 9, 12, 17, 23, 30, 31, 32, 34, 38, 43, 45, 53, 67.** Fifteen answers — the whole exam in miniature. Do the rest only if 10 spare minutes appear.

## The four sessions

| When | Time | What to do |
|---|---|---|
| **Saturday now** | 18:00–19:30 | Read §1, §2, §3, §4. Run look–cover–say on the 14 numbers and questions 1, 6, 9, 12, 17, 23, 30, 31, 32, 34, 38. Finish by recording the 14 numbers as a voice note. |
| **Sunday morning** | 08:30–09:00 | Listen to the voice note. Answer those 11 questions out loud without looking. Redo only what you missed. |
| **Sunday late afternoon** | 16:00–17:15 | Read §6 and §6.12. Open `http://127.0.0.1:5000`, click all six pages, say each page's route and table out loud. Practise questions 43, 45, 53. |
| **Sunday night** | 20:30–21:15 | Record all 15 priority answers. Play back. Re-record weak ones. Finish with the three killer answers and the honesty lines (§4.5, Appendix D). Then sleep. |

Total **4 hours 15 minutes**. Everything else is backup — read it only if a question takes you there.

## The three killer answers (say these perfectly)

**"Are your results significant?"**
> "Taste and vibe ease are significantly above neutral — p = 0.0026 and p = 0.0027. Saved retrieval is not, at p = 0.852. So my claim is *good but not great* — refinement, not rescue."

**"Isn't n=27 too small for that correlation?"**
> "It's n=27 now. Critical value is 0.381; vibe ease with saved retrieval reaches 0.385 at p = 0.047. Small sample, several comparisons — I treat it as directional and never claim causation."

**"Where's your actual usability result?"**
> "I built and instrumented the study page, but participant runs were still being collected. I don't claim a SUS score or task-time result; Section 10.3 says so."

## When you don't know

> "I'm not certain about that detail — the place to check would be ___."

Say it and move on. Never invent a number.

---

## How to study the full course

1. **Read** the section once (5–10 min). No highlighting.
2. **Look away and say** the key points in your own words (3 min).
3. **Check** against the text and star what you missed (1 min).
4. At the start of the next session, redo only the starred items.

Reading alone creates the feeling of knowing. Speaking and listening create actual recall.

---

# 1. What this project actually is — learn this first

## In simple terms

Someone listens to music daily, saves the tracks they like, and then can't find them again. Recommendations feel "okay" but not great. The biggest complaint — ads — can't be fixed by a student project, because removing ads needs control over the streaming company's playback. So, kya karte hain? Three things:

1. **Check if the problem is real.** A questionnaire with **27 real student responses**, analysed with statistics.
2. **Build a small fix.** A Chrome extension that adds a side panel on Spotify, YouTube Music and Apple Music — with **Discover** (Familiar / Balanced / Exploratory), **Find by Vibe** (mood tags), and a **saved-song library**.
3. **Build a dashboard.** Flask + SQLite website for saved songs, preferences, and a usability study.

## Why it counts as four subjects

| Subject | Where it appears |
|---|---|
| Design Thinking | Five stages: Empathise → Define → Ideate → Prototype → Test |
| Python | `webapp/app.py` (Flask server) and `webapp/analysis/analysis.py` (statistics) |
| Web Technology | HTML, CSS, JavaScript, Flask website, Chrome extension |
| Probability & Statistics | t-tests, confidence intervals, correlations, hypothesis testing |

## The one paragraph you must be able to say

> "I built a Chrome extension that adds a privacy-first personalisation panel to Spotify, YouTube Music and Apple Music, plus a Flask and SQLite dashboard. Core features: Discover with three familiarity levels, Find by Vibe, and a saved-music library. The design was driven by a 27-response survey and measured with built-in usage logging and a SUS study."

---

# 2. Design Thinking — from zero

**Design Thinking**
- *English: A human-centred way of solving problems, starting with the person rather than the technology (Brown, 2008).*
- **Hinglish:** Design Thinking matlab pehle insaan ko samjho, technology nahi. Five stages hain, aur aage-peechhe ja sakte ho — it's not a rigid ladder.

| Stage | What it means | What we actually did |
|---|---|---|
| **1. Empathise** | Understand the user's life and feelings | 25→27 responses questionnaire, coded open answers, empathy map and persona |
| **2. Define** | Turn the mess into one clear problem | POV, HMW, MoSCoW, descriptive statistics |
| **3. Ideate** | Generate lots of solutions | 10 ideas, mind map, SWOT, weighted matrix |
| **4. Prototype** | Build a rough, cheap version | Chrome extension + responsive Flask dashboard + SQLite |
| **5. Test** | Try it with users and measure | Three timed tasks, click/error logging, 10-item SUS form, hypothesis tests |

## Terms the professor may use

- **Double diamond**
  - *English: The process diverges and converges twice — first in the problem space, then in the solution space.*
  - **Hinglish:** Do baar phailna aur do baar simitna — pehle problem par, phir solution par. Questionnaire→persona pehla diamond; 10-ideas→matrix dusra.
- **Empathy map**
  - *English: A four-quadrant summary — Says, Thinks, Does, Feels — built from real user responses.*
  - **Hinglish:** Chaar boxes — Says, Thinks, Does, Feels — real answers se bana. Isme ads, repetitive recommendations aur saving nikal ke aaya.
- **Persona**
  - *English: One invented but realistic archetype representing the typical user.*
  - **Hinglish:** Ek made-up but realistic character jo typical user ko represent kare. Ours: **Aarav, 19** — B.Tech student, daily Spotify, saves but rarely revisits.
- **POV (Point of View)**
  - *English: A one-sentence problem statement of the form "[user] who [struggle] needs [solution] because [insight]."*
  - **Hinglish:** Ek line ka problem statement. Ours: daily listener who saves but can't rediscover, feels recommendations only "somewhat" match taste — needs familiarity control aur mood-based retrieval, kyunki discovery app ke bahar hai aur saved collection dhoondhna mushkil hai.
- **HMW (How Might We)**
  - *English: An open question that invites solutions, not a yes/no question.*
  - **Hinglish:** Khula sawaal jiska jawab solution nikale, haan/naa mein nahi. Ours: *"How might we give listeners control over recommendation familiarity and let them rediscover saved music by mood — without a paid subscription or a new account?"*
- **MoSCoW**
  - *English: Must / Should / Could / Won't prioritisation.*
  - **Hinglish:** Must = Discover, My Music, backend. Won't = ads hatana, offline downloads.
- **SWOT**
  - *English: Strengths, Weaknesses, Opportunities, Threats — a check on the chosen idea.*
  - **Hinglish:** Strengths, Weaknesses, Opportunities, Threats — chune gaye idea ko fragile selectors aur chhote sample ke against check karne ke liye.
- **Weighted selection matrix**
  - *English: Score each idea 1–5 on desirability (40%), feasibility (35%) and viability (25%), then multiply by weights and add.*
  - **Hinglish:** Har idea ko 1–5 par score karo, weights se multiply karke jodo. **10 ideas**; teen ka score **5.00** (slider, vibe tags, library). Ad blocker **2.80** — reject, kyunki feasible nahi.

---

# 3. Research methodology — from zero

## Sampling

**Convenience sampling**
- *English: Using whoever was easy to reach rather than a random sample.*
- **Hinglish:** Jo aasani se mil gaya — yahan students. Random nahi, isliye sab listeners par daava nahi kar sakte. **27 responses**, brief ka target **30** tha.

## Questionnaire types

| Type | Example | Why it matters |
|---|---|---|
| Multiple choice | "Which platform do you use most?" | Clean counts and percentages |
| **Ordinal** | "Easy / Average / Difficult" | Order hai, but gaps equal nahi |
| Numeric | "Age" | Mean, median, spread nikal sakte hain |
| Open-ended | "What's the biggest problem?" | Real quotes and themes |

**Ordinal data**
- *English: Ordered categories where the gaps between values are not equal.*
- **Hinglish:** Order to hai (Easy > Average > Difficult), par gap barabar nahi. Isi liye Pearson se zyada Spearman safe hai.

## Coding the answers

- **3** = positive: Easy / Very well / Daily
- **2** = middle: Average / Somewhat / Several times a week
- **1** = negative: Difficult / Poorly / Occasionally / Sometimes difficult

**Neutral = 2.** Ye "2" har t-test ka comparison point hai.

## Ethics

**Ethics**
- *English: Informed consent, anonymisation, no fabrication, and disclosure of AI use.*
- **Hinglish:** Participants ko purpose bataya, voluntary tha, naam **R01–R27** se replace kiye, contact details nahi li, AI tool use disclose kiya. Do low-quality rows **flag kiye, delete nahi**. Koi data nahi ghadha.

---

# 4. Statistics — from zero, and the most important section

Professors yahin sabse zyada ghot te hain. Pehle concepts, phir numbers.

## 4.1 Mean, median, standard deviation

- **Mean**
  - *English: The average — add all values and divide by the count.*
  - **Hinglish:** Mean matlab average — saare values jodo, count se divide karo.
- **Median**
  - *English: The middle value after sorting the data.*
  - **Hinglish:** Sort karne ke baad beech wala value.
- **Standard deviation (SD)**
  - *English: The typical distance of values from the mean; small SD = similar answers, large SD = spread-out answers.*
  - **Hinglish:** Mean se doori ka andaza. Kam SD = sabne similar jawab diya; zyada SD = jawab phaile hue.

Ages: range **18–30**, median **19**, mean **19.74**, SD **2.35**.

## 4.2 One-sample t-test

**One-sample t-test**
- *English: A test that checks whether a sample mean differs from a known value — here, the neutral value 2.*
- **Hinglish:** Test jo dekhta hai ki mean kisi pakke number se alag hai ya nahi — yahan number hai 2. Har measure ke liye ek test.

- **t**
  - *English: How far the mean is from 2, measured in standard errors; larger |t| = stronger evidence.*
  - **Hinglish:** Mean 2 se kitni door hai, standard errors mein. |t| bada = stronger evidence.
- **p-value**
  - *English: If there were no real difference, the probability of seeing data this extreme.*
  - **Hinglish:** Agar farq hi na ho, to itna extreme data milne ki probability. Chhota p (< 0.05) = mushkil = result **significant**.
- **Statistically significant**
  - *English: Unlikely to be due to chance, based on a threshold fixed before testing.*
  - **Hinglish:** Chance se hona mushkil — pehle se tay threshold par.
- **alpha = 0.05**
  - *English: The significance threshold fixed before testing.*
  - **Hinglish:** Pehle se tay gate — p 0.05 se kam mila to significant.
- **95% confidence interval (CI)**
  - *English: A range of plausible values for the true mean; if it excludes 2, that agrees with p < 0.05.*
  - **Hinglish:** Asli mean ke liye possible range. Agar 2 andar nahi hai, to p < 0.05 se match.
- **df = 26**
  - *English: Degrees of freedom = n − 1 = 27 − 1.*
  - **Hinglish:** Degrees of freedom = n − 1 = 27 − 1 = 26.

### The four results — learn as pairs

| Measure | Mean | SD | t | p | 95% CI | Reading |
|---|---|---|---|---|---|---|
| Usage frequency | **2.52** | 0.75 | 3.578 | **0.0014** | [2.22, 2.82] | above neutral |
| Vibe-finding ease | **2.44** | 0.70 | 3.309 | **0.0027** | [2.17, 2.72] | above neutral |
| Saved retrieval | **2.04** | 1.02 | 0.189 | **0.8516** | [1.63, 2.44] | **not** significant |
| Taste understanding | **2.41** | 0.64 | 3.328 | **0.0026** | [2.16, 2.66] | above neutral |

**Interpretation — word for word:**
> "Vibe-finding ease and taste understanding were significantly above neutral, while saved retrieval was not. These results do not support a claim that users are deeply dissatisfied. They support a narrower claim: personalisation is good but not great, and retrieval friction is common enough to address."

**"Good-but-not-great baseline"** — ye phrase baar baar bolo. Kabhi mat bolo users "broken" hain — data support nahi karta.

## 4.3 Correlation

**Correlation**
- *English: A number describing the direction and strength of a relationship between two variables.*
- **Hinglish:** Do cheezon ke rishte ki direction aur strength batane wala number.

- **r / rho (ρ)**
  - *English: Ranges from −1 to +1. Positive = both rise together; negative = one rises as the other falls. Roughly 0.1 weak, 0.3 moderate, 0.5+ strong.*
  - **Hinglish:** −1 se +1. + matlab dono saath badhte; − matlab ek badhe to doosra ghire. 0.1 weak, 0.3 moderate, 0.5+ strong.
- **Pearson**
  - *English: Correlation on raw values, assuming a straight-line relationship.*
  - **Hinglish:** Sachche values par correlation, straight-line assumption ke saath.
- **Spearman**
  - *English: Correlation on ranks rather than raw values — safer for ordinal data and small samples.*
  - **Hinglish:** Values ki jagah ranks par — ordinal aur chhote sample ke liye safer. Hum dono batate hain, bharosa Spearman par.
- **Critical |r| at n=27 ≈ 0.381**
  - *English: The minimum coefficient needed for significance at alpha 0.05 with n=27.*
  - **Hinglish:** n=27 par significant hone ke liye coefficient kam se kam 0.381 hona chahiye.

### Our correlations

| Pair | Pearson | Spearman | p | Reading |
|---|---|---|---|---|
| Usage ↔ Vibe | −0.309 | −0.316 | 0.1082 | weak |
| Usage ↔ Retrieval | −0.126 | −0.091 | 0.6505 | weak |
| Usage ↔ Taste | +0.104 | +0.168 | 0.4031 | weak |
| **Vibe ↔ Retrieval** | +0.409 | **+0.385** | **0.0473** | **only significant pair** |
| Vibe ↔ Taste | +0.270 | +0.212 | 0.2893 | weak |
| Retrieval ↔ Taste | +0.391 | +0.377 | 0.0523 | just misses |

**Cautious answer:**
> "At n=27 the critical value is 0.381. Only vibe ease with saved retrieval clears it — 0.385, p = 0.047. Retrieval with taste comes close at 0.377, p = 0.052. Small sample aur kai comparisons ki wajah se main isse directional maanta hoon, causation kabhi nahi."

**Correlation is not causation** — hamesha bolo agar poocha jaye.

## 4.4 Hypotheses (fixed BEFORE testing)

| | Claim |
|---|---|
| **H1a** | Median time to find a saved song is **lower** with the prototype |
| **H0a** | No difference in retrieval time |
| **H1b** | Mean taste rating after discovery **exceeds 2.41** |
| **H0b** | Unchanged from 2.41 |
| **H1c** | Mean SUS score **exceeds 68** |
| **H0c** | SUS is 68 or lower |

- **H0 (null)**
  - *English: The claim that nothing happens.*
  - **Hinglish:** "Kuch nahi hota" wala default claim.
- **H1 (alternative)**
  - *English: The claim that something does happen.*
  - **Hinglish:** "Kuch hota hai" wala claim.
- **Paired design**
  - *English: The same participants try both methods, so each person is their own control.*
  - **Hinglish:** Ek hi participant dono methods try karta hai — har insaan khud ka control.
- **Wilcoxon signed-rank**
  - *English: A non-parametric test for paired differences when normality is doubtful.*
  - **Hinglish:** Paired time ke liye test jab difference normal na lage.
- **Paired t-test**
  - *English: The paired test used when the difference is approximately normal.*
  - **Hinglish:** Paired test jab difference normal jaisa ho.
- **Effect size**
  - *English: How big the improvement is, not merely whether it is detectable.*
  - **Hinglish:** Sudhaar kitna bada hai — sirf "detect ho gaya" nahi. Mean difference bhi batana padega.

## 4.5 The honest status of the usability study

Study page banaya aur instrument kiya — timed tasks, clicks, errors, SUS form. **Participant runs abhi collect ho rahe the.** Isliye **koi SUS score ya task-time result claim nahi karte**. Paper ka Section 10.3 ye clearly kehta hai. Kabhi number mat ghadho.

---

# 5. Every important number in one place

| Number | Meaning |
|---|---|
| **27** | survey responses (target 30) |
| **25** | substantive responses; 2 flagged, none deleted |
| **19** | median age (range 18–30, mean 19.74, SD 2.35) |
| **67%** | Spotify (18 people) — platform imbalance |
| **15% / 11% / 7%** | YouTube Music / Other / Apple Music |
| **85%** | daily or several times a week **and** save/playlist a liked track |
| **44%** | sometimes struggle to find old saves (12 people) — the design target |
| **48%** | ads/paywall complaint (13 people) — biggest, out of scope |
| **37% / 19% / 11% / 4%** | recommendations / UI / vibe / saving themes |
| **52%** | taste only somewhat or poorly understood (12 + 2) |
| **2.41, p .0026** | taste above neutral |
| **2.44, p .0027** | vibe ease above neutral |
| **2.04, p .8516** | retrieval **not** significant |
| **0.381** | critical correlation at n=27 |
| **+0.385, p .047** | vibe ↔ retrieval — the only significant correlation |
| **68** | SUS benchmark |
| **0.05** | alpha |
| **5** | Design Thinking stages; matrix score 5.00; DB tables; website pages |
| **40/35/25** | desirability / feasibility / viability weights |
| **10** | ideas |
| **2 seconds** | how often the extension checks the current track |

---

# 6. The website — from zero

## 6.1 What happens when you open a page

1. You type a URL like `http://127.0.0.1:5000/discover`.
2. Your browser sends an **HTTP request** to the **server** (Flask, running on your own machine).
3. The server runs a function and returns **HTML** in an **HTTP response**.
4. Browser renders it; **CSS** makes it look good, **JavaScript** makes it interactive.

**HTTP request**
- *English: A message sent by the browser to the server asking for a page or sending data.*
- **Hinglish:** Browser se server ko bheja gaya message — page maangna ya data bhejna.

**GET vs POST**
- *English: GET asks for a page and puts data in the URL; POST sends data in the request body.*
- **Hinglish:** GET page maangta hai aur data URL mein daalta hai (`?level=familiar&platform=Spotify`). POST data body mein bhejta hai — forms aur save ke liye.

## 6.2 Roles of HTML, CSS, JavaScript

- **HTML**
  - *English: The structure and content of a page — headings, buttons, forms, tables.*
  - **Hinglish:** Page ki haddi aur content — heading, button, form, table.
- **CSS**
  - *English: The appearance — colours, spacing, layout, mobile rules.*
  - **Hinglish:** Dikhaav aur decoration — rang, spacing, layout, mobile rules.
- **JavaScript**
  - *English: The behaviour — reacting to clicks, talking to the server, updating the page.*
  - **Hinglish:** Vyavhaar — click par karna, server se baat karna, page update karna.

## 6.3 Flask and routes

**Flask**
- *English: A small Python web framework that maps URLs to functions and returns web pages.*
- **Hinglish:** Chhota Python framework jo URL ko function se jodta hai aur page wapas deta hai.

**Decorator**
- *English: A line like `@app.route("/discover")` that tells Flask which URL runs the function below it.*
- **Hinglish:** `@app.route("/discover")` jaisi line jo Flask ko batati hai — ye URL aaye to neeche wala function chalao.

| URL | Function | What happens |
|---|---|---|
| `/` | `index()` | Read `saved_songs`, show 3 counts |
| `/discover` | `discover()` | Read `?platform=` and `?level=` from URL, compute recommendations |
| `/vibe` | `vibe()` | Read `?vibe=`, compute mood recommendations |
| `/preferences` | `preferences()` | GET shows form, POST saves it |
| `/study` | `study()` | Shows past tasks and SUS form |
| `/results` | `results()` | Reads anonymised CSV, counts stats, shows charts |
| `/api/save` | `api_save()` | JSON API: insert saved song |
| `/api/unsave/<id>` | `api_unsave()` | JSON API: delete saved song |
| `/api/event` | `api_event()` | JSON API: log click/task/SUS event |
| `/api/task` | `api_task()` | JSON API: store completed timed task |
| `/api/summary` | `api_summary()` | Raw database counts |
| `/health` | `health()` | Is the server alive, is the CSV present? |

`request.args.get("level")` reads URL values; `request.form.get(...)` reads POST form values; `request.get_json()` reads the JSON JavaScript sent.

**render_template**
- *English: Fills a Jinja template with variables and returns the finished HTML.*
- **Hinglish:** Jinja template mein values bhar ke tayyar HTML wapas deta hai.

## 6.4 Jinja templates

**Jinja**
- *English: The template language that lets Python values appear inside HTML.*
- **Hinglish:** Template language jo Python ki values HTML mein dikhata hai.

- `{{ variable }}` — prints a value.
- `{% for x in items %}` — loop; `{% if saved %}` — condition.
- `{% extends "base.html" %}` + `{% block content %}` — all pages share one header/nav/footer; only the middle changes.
- **url_for**
  - *English: Builds a URL from a function name instead of hard-coding it.*
  - **Hinglish:** URL hard-code karne ki jagah function ke naam se banata hai.

## 6.5 SQLite and the five tables

**SQLite**
- *English: A database stored in a single file (`webapp/pme.db`).*
- **Hinglish:** Database jo ek hi file mein hoti hai — `webapp/pme.db`.

**Table**
- *English: Like a spreadsheet — rows are records, columns are fields.*
- **Hinglish:** Spreadsheet jaisa — row = record, column = field.

| Table | Stores |
|---|---|
| `users` | Anonymous browser ID from a cookie — no name, no login |
| `saved_songs` | title, artist, genre, reason, source |
| `preferences` | default level, preferred vibe, tracking consent |
| `usage_events` | event type and detail — every view, save, task start |
| `test_tasks` | task name, duration, clicks, errors, completed |

SQL words: `SELECT` (read), `INSERT` (add), `UPDATE` (change), `DELETE` (remove), `WHERE` (filter), `UNIQUE` (no duplicates), `FOREIGN KEY` (row must refer to a real row elsewhere), `INDEX` (faster lookup).

**Upsert**
- *English: Try UPDATE; if no row changed, INSERT a new one.*
- **Hinglish:** Pehle UPDATE; agar row na badle to INSERT kar do.

## 6.6 Cookie

**Cookie**
- *English: A small value stored in the browser that identifies the same visitor on repeat visits.*
- **Hinglish:** Browser mein chhota value jo baar-baar aane par ek hi visitor ko pehchanta hai.

`pme_session` is a random ID. It lets the server recognise the same browser without login or name — anonymity bhi bachti hai, measurement bhi hota hai.

## 6.7 Follow one click end-to-end (very likely question)

**"User pressed Save on a recommendation":**

1. HTML button holds `data-title`, `data-artist`, `data-genre`, `data-reason`, `data-source` — the song's details.
2. `app.js` listens for the click and reads them as `button.dataset.title` etc.
3. `postJSON('/api/save', song)` sends them as JSON using `fetch()`.
4. Flask's `api_save()` reads the JSON and checks title and artist are present.
5. It runs `INSERT OR IGNORE INTO saved_songs ...` — SQLite adds the row.
6. It logs a `save_song` event in `usage_events`.
7. It replies `{"ok": true}`; JavaScript changes the button to "Saved ✓".

**"User opened /discover":** Flask reads URL values → calls `get_recommendations(platform, level, artist)` in `recommendations.py` → that looks up a demo dictionary → Flask checks which songs are already saved → logs a `discover_view` event → renders `discover.html`.

## 6.8 JavaScript vocabulary

| Code | Meaning |
|---|---|
| `querySelector` / `querySelectorAll` | Find one element / all matching elements |
| `addEventListener('click', fn)` | Run `fn` when clicked |
| `button.dataset.title` | Read the HTML `data-title="..."` attribute |
| `classList.add/toggle` | Change CSS class, appearance changes |
| `fetch(...)` | Send a request from browser to Flask |
| `async` / `await` | Wait for the reply, then use the result |
| `event.preventDefault()` | Stop the browser's default action, e.g. page reload |
| `performance.now()` | High-precision timer for the task study |
| `i % 2 === 1` | Remainder — true for odd question numbers |
| `location.reload()` | Refresh the page to show the new task row |

**SUS scoring**
- *English: Odd items contribute (answer − 1), even items (5 − answer); sum × 2.5 gives 0–100, with 68 as the benchmark.*
- **Hinglish:** Odd par (answer − 1), even par (5 − answer). Jod × 2.5 = 0–100 score. **68** benchmark hai.

## 6.9 CSS vocabulary

**CSS variable**
- *English: A reusable value defined as `--green` and used with `var(--green)`.*
- **Hinglish:** Reusable value — `:root { --green: #1DB954; }` mein define, `var(--green)` se use.

`display: flex` arranges items in a line; `display: grid` in rows and columns. `@media (max-width: 720px)` applies extra rules only on small screens — yahi **responsive** hai.

## 6.10 Chrome extension (separate from website)

**Content script**
- *English: JavaScript injected into a web page to read or modify that page.*
- **Hinglish:** JS jo page mein inject hoke usse padhta ya badalta hai — yahan Spotify/YouTube Music/Apple Music par side panel add karta hai.

**Adapter**
- *English: A small platform-specific piece that checks `window.location.hostname` and finds the current track.*
- **Hinglish:** Har platform ka chhota hissa jo hostname dekh ke decide karta hai lagoo hai ya nahi, aur current track dhoondhta hai.

**Polling**
- *English: Repeatedly checking for a value at fixed intervals — here every 2 seconds.*
- **Hinglish:** Har 2 second par baar-baar check. `MutationObserver` se isliye behtar kyunki ye single-page apps DOM tod kar dobara banati hain, jisse observer toot jata hai.

`chrome.storage` client par data rakhta hai; SQLite dashboard aur measurement ke liye. Agar site ka layout badle to sirf us adapter ko fix karna padega — documented limitation.

## 6.11 `analysis.py` — where numbers come from

```
python3 webapp/analysis/analysis.py --csv "Music Streaming Platform Experience (Responses) - Form responses 1.csv"
```

It reads the raw CSV → writes `data/survey_responses_anonymised.csv` (R01–R27) → computes counts, t-tests, Pearson/Spearman, CIs and themes → writes `docs/statistical_results.md` → draws 5 charts in `data/charts/`. Re-runnable.

**Canonical source of truth**
- *English: The single official source that every other number must agree with.*
- **Hinglish:** Ek hi pakka source jisse baaki sab numbers match karne chahiye.

## 6.12 Inspect Element — when the professor points

| They point at | Say |
|---|---|
| Top bar with 6 links | "That's `base.html`, shared via Jinja `{% extends %}`." |
| Green highlighted link | "Template adds `class="active"`; CSS paints `.nav a.active` green." |
| Stat cards | "Counted from the CSV by `survey_summary()` in `app.py` — they match the survey." |
| Song card + Save | "One item from `recommendations.py`; `data-*` attributes go to `/api/save` via app.js." |
| "Saved ✓" | "app.js added the `saved` class and changed the label; Flask inserted a SQLite row." |
| Remove button | "`data-id` is the row id; POST to `/api/unsave/<id>`, then JS removes the list item." |
| Vibe tags | "Links with `?vibe=chill`; Flask reads them with `request.args`. No JS needed." |
| Dropdown / GET form | "Values go in the URL; Flask reads them with `request.args.get()`." |
| Preferences checkbox | "Unchecked sends nothing, so Flask treats it as tracking = 0." |
| Task button | "app.js times it with `performance.now()`, counts clicks, POSTs to `/api/task`." |
| SUS radios | "Five radios share `name=q1`, so only one can be chosen. All ten are required." |
| SUS score | "Odd −1, even 5 − answer, sum × 2.5. 68 benchmark." |
| Charts | "Generated by `analysis.py`, served by Flask through `/charts/<filename>`." |
| Response table | "Jinja `{% for %}` loop over CSV rows; bracket names must match the CSV header." |
| Dark theme / green | "CSS variables in `:root` at the top of `style.css`." |
| Mobile layout | "The `@media (max-width: 720px)` block at the bottom of `style.css`." |
| `@app.route(...)` | "Decorator — maps a URL to the function below it." |
| `render_template(...)` | "Fills a Jinja template with values and returns HTML." |
| `{{ var }}` / `{% %}` | "Jinja prints a value / runs logic." |
| `g` / `get_db()` | "Flask's per-request box — one SQLite connection per request, closed after." |
| Cookie | "Anonymous random ID — no login, no personal data." |
| `UNIQUE`, `FOREIGN KEY` | "Prevent duplicate saves; ensure every song belongs to a real user." |
| `fetch` / `async await` | "Browser-to-server JSON call, waiting for the response." |
| `if __name__ == "__main__":` | "Start the server only when this file is run directly." |
| `debug=True` | "Auto-reload on edits; prototype only." |

---

# 7. How to answer any question under pressure

Four-part structure — ye tumhe calm aur authoritative banata hai:

1. **Direct answer first** — one line.
2. **Evidence** — the number, file or stage.
3. **Why** — the reasoning.
4. **Limitation** — one honest caveat.

Example: *"Yes, one correlation is significant (1). Vibe ease with saved retrieval is 0.385, p = 0.047 (2). I used Spearman because the data are ordinal and n is small (3). But 27 responses and several comparisons — I treat it as directional, not causal (4)."*

**If you genuinely don't know:** *"I'm not certain about that detail — the place to check would be ___."* Never invent a number. Honest "I don't know" se kam nuksaan hota hai galat number se.

**Buying time:** "Let me frame that in two parts…" / "The short answer is…, and the reason is…"

---

# 8. Question bank (practise out loud)

## Overview
1. **Tell me about your project.** → §1 paragraph.
2. **Why is it an integrated project?** → §1 four-subjects table.
3. **Main problem?** → save-and-retrieve gap: 85% save, 44% struggle.
4. **Strongest evidence?** → same numbers.
5. **What did you cut?** → ad blocker (needs playback control), offline downloads, Understand section.

## Design Thinking
6. **Five stages.** → Empathise, Define, Ideate, Prototype, Test.
7. **Design Thinking?** → human-centred problem solving (Brown 2008).
8. **Double diamond?** → diverge/converge on problem, then solution.
9. **Empathy map?** → Says/Thinks/Does/Feels from real responses.
10. **Persona vs empathy map?** → one archetype vs aggregate emotional picture.
11. **POV?** → §2.
12. **HMW?** → §2.
13. **MoSCoW?** → Must/Should/Could/Won't.
14. **SWOT?** → Strengths/Weaknesses/Opportunities/Threats.
15. **How were ideas selected?** → 10 ideas, 40/35/25, top 5.00, ad blocker 2.80 rejected.
16. **Why no ad blocker?** → client-side utility can't control ads; in Won't, disclosed.

## Research and statistics
17. **Sampling?** → convenience, students, n=27.
18. **Why not 30?** → time constraint; real 27 reported honestly, no fabrication.
19. **Question types?** → MCQ, ordinal, numeric, open-ended.
20. **Ordinal data?** → ordered categories, unequal gaps; use Spearman.
21. **Coding?** → 3/2/1, neutral = 2.
22. **Tests and why?** → one-sample t-test vs 2; Pearson + Spearman; CIs.
23. **p-value?** → probability of data this extreme if H0 true.
24. **Confidence interval?** → plausible range for the true value.
25. **Alpha?** → 0.05, fixed in advance.
26. **t-test?** → compares sample mean with a known value.
27. **Correlation?** → direction and strength of a relationship.
28. **Pearson vs Spearman?** → raw values vs ranks; Spearman safer for ordinal/small n.
29. **Correlation vs causation?** → association doesn't prove one caused the other.
30. **Key results.** → §4.2 four t-tests.
31. **Which are significant?** → vibe and taste; retrieval is not.
32. **Significant correlation?** → vibe ↔ retrieval, +0.385, p 0.047, critical 0.381; cautious tone.
33. **Effect size?** → how big the change is, not just detectable.
34. **SUS?** → 10 items, 0–100, 68 benchmark, formula in §6.8.
35. **Hypotheses?** → H1a/b/c in §4.4.
36. **Paired design?** → same users try both methods.
37. **Wilcoxon vs paired t-test?** → Wilcoxon if non-normal, else paired t-test.
38. **What do results mean?** → "good but not great" in §4.2.
39. **Participant data protection?** → R01–R27, no contact details, consent, AI disclosure.
40. **Flagged data?** → two rows flagged, not deleted; possible duplicate names; all rows retained.
41. **Why is 67% Spotify a limitation?** → platform imbalance limits generalisation.
42. **Open-text themes?** → ads 48%, recommendations 37%, UI 19%, vibe 11%, saving 4%.

## Technical / website
43. **Frontend?** → extension panel + `webapp/templates/`, `static/style.css`, `static/app.js`.
44. **Python?** → `app.py` (Flask), `recommendations.py` (demo data), `analysis/analysis.py` (stats).
45. **Database?** → `pme.db`, five tables in §6.5.
46. **chrome.storage and SQLite both?** → client convenience vs shared queryable measurement; brief requires a DB.
47. **Request flow.** → §6.1 and §6.3.
48. **`@app.route`?** → maps URL to function.
49. **`render_template`?** → fills template, returns HTML.
50. **GET vs POST?** → URL vs body; §6.1.
51. **Jinja?** → template language; `{{ }}` and `{% %}`.
52. **`url_for`?** → builds URL from function name.
53. **How does Save work?** → seven steps in §6.7.
54. **`fetch`?** → browser-to-server request.
55. **`data-*` attributes?** → custom HTML attributes read by JS as `dataset`.
56. **Cookie?** → anonymous identity without login.
57. **`UNIQUE` / foreign key?** → §6.5.
58. **Platform detection?** → adapter checks hostname.
59. **Polling not MutationObserver?** → SPAs rebuild DOM constantly.
60. **Site layout changes?** → that adapter's selectors break; one file to fix; limitation.
61. **`analysis.py`?** → §6.11.
62. **Regenerate everything?** → run analysis, then `python3 docs/build_presentation.py` and `python3 docs/build_paper.py`.
63. **Real AI?** → no, rule-based demo database; stated limitation.
64. **Flask not Django?** → Flask is small, enough for six pages and APIs, easy to explain and inspect.
65. **Dark theme?** → matches music-player context; CSS variables make it easy to change.

## Honesty and scope
66. **Worked alone — what was cut?** → one contributor, five roles; no separate interview transcripts, individual brainstorming, mentor review; Appendix D; no fabrication.
67. **SUS result?** → instrument built, runs incomplete, no result claimed (§4.5).
68. **More time?** → learned model, Understand section, 30+ stratified sample, completed paired study with effect sizes, mood-retrieval time test.
69. **Biggest limitation?** → small n, platform imbalance, demo recommendations, fragile selectors, single contributor.
70. **Why accept?** → real measured problem, working system, honest statistics, reproducible pipeline.

---

# 9. If you get extra time

Fast track is enough. With 20 extra minutes, do look → cover → say on:

- §5 full numbers table
- §6.12 Inspect Element table
- Remaining §8 questions (16, 18, 25, 28, 35, 39, 40, 46, 50, 63, 66)
- Three killer answers once more

Monday morning, 15 minutes: only 14 numbers, the one paragraph, and questions 31, 32, 67. Then focus on the presentation.

---

# 10. Companion files

- `docs/presentation_script.md` — **English only**, recite this on stage (unchanged)
- `docs/viva_cheat_sheet.md` — short Q&A
- `docs/viva_prep_guide.md` — study method, paper map, Inspect Element table
- `docs/statistical_results.md` — the canonical numbers
- `docs/design_thinking_artefacts.md` — empathy map, matrix, hypotheses
- `README.md` — how to run the site and regenerate outputs
