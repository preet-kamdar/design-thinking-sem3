#!/usr/bin/env python3
"""Generate the research paper DOCX following Section 10 of the integrated brief."""

from pathlib import Path

from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.shared import Pt, Inches, RGBColor

OUT = Path(__file__).with_name("Research_Paper.docx")
ROOT = Path(__file__).resolve().parents[1]
CHARTS = ROOT / "data" / "charts"

GREEN = RGBColor(29, 185, 84)


def h(doc, text, level=1):
    doc.add_heading(text, level=level)


def p(doc, text, italic=False, bold=False):
    par = doc.add_paragraph()
    run = par.add_run(text)
    run.italic = italic
    run.bold = bold
    par.paragraph_format.space_after = Pt(8)
    return par


def bullets(doc, items):
    for item in items:
        doc.add_paragraph(item, style="List Bullet")


def table(doc, headers, rows, widths=None):
    t = doc.add_table(rows=1, cols=len(headers))
    t.style = "Light Grid Accent 1"
    for i, head in enumerate(headers):
        t.rows[0].cells[i].text = str(head)
    for row in rows:
        cells = t.add_row().cells
        for i, val in enumerate(row):
            cells[i].text = str(val)
    if widths:
        for row in t.rows:
            for i, w in enumerate(widths):
                row.cells[i].width = Inches(w)
    return t


def caption(doc, text):
    par = doc.add_paragraph()
    run = par.add_run(text)
    run.italic = True
    run.font.size = Pt(9)
    par.alignment = WD_ALIGN_PARAGRAPH.CENTER


def add_chart(doc, filename, caption_text):
    path = CHARTS / filename
    if path.exists():
        doc.add_picture(str(path), width=Inches(5.8))
        caption(doc, caption_text)


def main():
    doc = Document()
    style = doc.styles["Normal"]
    style.font.name = "Calibri"
    style.font.size = Pt(11)

    # ---- Title page ----
    title = doc.add_paragraph()
    title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = title.add_run("Reimagining the Personal Music Experience")
    run.bold = True
    run.font.size = Pt(26)
    run.font.color.rgb = GREEN
    sub = doc.add_paragraph()
    sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
    sub.add_run("A Design Thinking study with statistical validation of a cross-platform\n"
                "personalisation prototype").italic = True
    doc.add_paragraph()
    meta = doc.add_paragraph()
    meta.alignment = WD_ALIGN_PARAGRAPH.CENTER
    meta.add_run("Integrated Group Project — B.Tech Second Year\n"
                 "Introduction to Design Thinking · Web Technology · Python · Probability and Statistics\n\n"
                 "Student: [Name] · [Roll Number]\nDepartment · Institution\nFaculty mentor: [Name]")
    doc.add_paragraph()
    note = doc.add_paragraph()
    note.alignment = WD_ALIGN_PARAGRAPH.CENTER
    note.add_run("Scope note: executed by a single contributor; role consolidation and "
                 "reductions are disclosed in Section 7 and Appendix D.").italic = True
    doc.add_page_break()

    # ---- 1 Abstract ----
    h(doc, "1. Abstract", 1)
    p(doc, "Music listeners often save tracks they later struggle to rediscover, and many feel "
           "recommendations only partially match their taste. This project applied Design Thinking "
           "to build a cross-platform personalisation prototype: a Chrome extension with Familiar, "
           "Balanced and Exploratory discovery, vibe-based browsing, and a saved-music library backed "
           "by a Flask/SQLite dashboard. An 18-response survey found taste understanding significantly "
           "above neutral but modest (mean 2.33, t=2.38, p=0.029), while 44% sometimes struggled to "
           "find old saves. The prototype addresses these in-scope gaps with local, private data and "
           "built-in usage measurement. n=18 and single-contributor scope are disclosed as limits.")
    p(doc, "Word count: approximately 100 words (brief recommends about 50; this version includes "
           "the required main statistical finding and model details).", italic=True)

    # ---- 2 Keywords ----
    h(doc, "2. Keywords", 1)
    p(doc, "Design Thinking; music personalisation; recommendation systems; usability testing; "
           "System Usability Scale; hypothesis testing; Chrome extension; Flask; SQLite.")

    # ---- 3 Introduction ----
    h(doc, "3. Introduction", 1)
    p(doc, "Music streaming is a routine activity for young adults. The survey conducted for this "
           "project found that 78% of respondents used their primary platform daily or several times "
           "a week. Yet routine use does not imply satisfaction with personalisation: 55.6% said their "
           "app understood their taste only 'somewhat' and a further 5.6% said 'poorly'. Only 38.9% "
           "chose 'very well'.")
    p(doc, "At the same time, 77.8% of respondents add a liked song to a playlist or save/like it, but "
           "44.4% reported that finding songs saved a long time ago is sometimes difficult. This "
           "save-and-retrieve gap is directly addressable by a lightweight utility that does not need "
           "access to a streaming service's private APIs.")
    p(doc, "The integrated brief asks a sharper question than earlier versions: can we prove with "
           "data that a solution is better than what users have today? Accordingly, this project "
           "combines the five Design Thinking stages with a questionnaire, descriptive and "
           "inferential statistics, a working frontend and Python backend, and an instrumented "
           "usability study.")
    p(doc, "The scope of this document is deliberately honest. The survey has 18 responses against a "
           "target of 30, the recommendation database is demo content, and the largest single complaint "
           "— advertisements, mentioned by 50% — is outside the technical reach of a client-side "
           "utility. Each of these is treated as a limitation rather than hidden.")

    # ---- 4 Literature review ----
    h(doc, "4. Literature Review", 1)
    p(doc, "Commercial streaming services personalise through collaborative filtering and behavioural "
           "modelling. For this prototype, a rule-based demo database was used instead, because the "
           "brief requires a working, measurable system rather than production-grade recommendation "
           "quality. This is a stated limitation.")
    p(doc, "Design Thinking provides the five-stage frame: Empathise, Define, Ideate, Prototype and Test "
           "(Brown, 2008). The double-diamond pattern — diverging and converging at problem and "
           "solution spaces — is reflected in the questionnaire-to-persona and idea-to-selection "
           "steps respectively.")
    p(doc, "Usability evaluation commonly uses the System Usability Scale (Brooke, 1996), a ten-item "
           "instrument producing a 0–100 score with 68 as the average benchmark. Task time, error "
           "counts and click counts are standard objective complements to such subjective scales.")
    p(doc, "For ordinal Likert-style data, non-parametric correlation (Spearman) is more appropriate "
           "than Pearson when normality is doubtful, and small samples require explicit assumptions "
           "checks and confidence intervals rather than p-values alone.")
    p(doc, "Ethical requirements in the brief — informed consent, anonymisation, no fabrication and "
           "AI disclosure — shaped the data handling described in Section 7.")

    # ---- 5 Objectives and problem definition ----
    h(doc, "5. Objectives and Problem Definition", 1)
    h(doc, "5.1 Objectives", 2)
    bullets(doc, [
        "Identify real pain points in personal music streaming using a questionnaire and open-text responses.",
        "Design a privacy-first utility giving control over recommendation familiarity and mood-based discovery.",
        "Make saved music easy to retrieve and inspect.",
        "Build a working frontend (HTML/CSS/JS) and Python backend with a database and usage logging.",
        "Validate the design with descriptive statistics, hypothesis tests and a usability study.",
    ])
    h(doc, "5.2 Point of View", 2)
    p(doc, "A daily music-streaming listener who saves tracks but struggles to rediscover them, and who "
           "feels recommendations only 'somewhat' match their taste, needs control over how familiar or "
           "exploratory suggestions are and a way to revisit saved music by mood — because discovery "
           "currently happens outside the app and saved collections are hard to navigate.")
    h(doc, "5.3 How Might We", 2)
    p(doc, "How might we give listeners control over the familiarity of recommendations and let them "
           "rediscover saved music by mood, without requiring a paid subscription or a new account?")

    # ---- 6 Methodology ----
    h(doc, "6. Research Methodology", 1)
    h(doc, "6.1 Participants and sampling", 2)
    p(doc, "Convenience sampling was used to recruit 18 respondents, mostly students aged 18–30 "
           "(median 19; numeric mean 19.71, SD 2.73). 77.8% named Spotify as their primary platform, "
           "16.7% YouTube Music and one respondent selected 'Other'. No Apple Music user was "
           "represented. Limitations: small sample, platform imbalance, self-selection bias and no "
           "stratification.")
    h(doc, "6.2 Questionnaire design", 2)
    p(doc, "The instrument combined multiple-choice items (platform, usage frequency, discovery "
           "source, action after liking a song), ordinal three-point ease/quality ratings, a numeric "
           "age field, and three open-ended questions about problems, wishes and one desired change. "
           "Ordinal responses were coded 3 = positive (Easy / Very well / Daily), 2 = middle "
           "(Average / Somewhat / Several times a week), 1 = negative (Difficult / Poorly / "
           "Occasionally / Sometimes difficult). The neutral comparison value was 2.")
    h(doc, "6.3 The five stages and tools", 2)
    table(doc, ["Stage", "Activity", "Tool / output"], [
        ["Empathise", "Questionnaire, open-text coding, empathy map", "Google Forms; CSV; empathy map"],
        ["Define", "Persona, POV, HMW, MoSCoW, descriptive stats", "pandas, scipy, matplotlib"],
        ["Ideate", "10 ideas, mind map, SWOT, weighted matrix", "Selection matrix (D40/F35/V25)"],
        ["Prototype", "Extension + responsive dashboard + DB", "HTML/CSS/JS, Flask, SQLite"],
        ["Test", "Timed tasks, SUS, hypothesis tests", "Study page, /api/task, SUS script"],
    ])
    h(doc, "6.4 Technology stack", 2)
    p(doc, "Frontend: HTML5, CSS3 (responsive media queries), vanilla JavaScript, Chrome Manifest V3 "
           "content scripts. Backend: Python 3 with Flask, SQLite via sqlite3. Analysis: pandas, "
           "NumPy, SciPy, matplotlib. Documentation: python-docx and python-pptx.")
    h(doc, "6.5 Ethical handling", 2)
    p(doc, "Participants were informed of the purpose and data use. Names were replaced by R01–R18 in "
           "the anonymised dataset. No contact details or sensitive information were collected. Two "
           "non-substantive responses were flagged rather than deleted, and no responses were "
           "invented or altered. AI tools were used for code and documentation drafting and are "
           "disclosed here.")

    # ---- 7 Findings ----
    h(doc, "7. User Research and Findings", 1)
    h(doc, "7.1 Descriptive findings", 2)
    table(doc, ["Measure", "Result"], [
        ["Responses", "18 (16 assessed as substantive)"],
        ["Primary platform", "Spotify 14 (77.8%); YouTube Music 3 (16.7%); Other 1 (5.6%)"],
        ["Usage frequency", "Daily 9 (50%); several times/week 5 (27.8%); occasionally 4 (22.2%)"],
        ["Discovery source", "Outside app 6 (33.3%); recommendations 5 (27.8%); search 4 (22.2%); playlist 3 (16.7%)"],
        ["Vibe-finding ease", "Easy 10 (55.6%); Average 7 (38.9%); Difficult 1 (5.6%)"],
        ["Action after liking", "Playlist 9 (50%); save/like 5 (27.8%); just listen 4 (22.2%)"],
        ["Saved retrieval", "Easy 10 (55.6%); sometimes difficult 8 (44.4%)"],
        ["Taste understanding", "Very well 7 (38.9%); somewhat 10 (55.6%); poorly 1 (5.6%)"],
    ])
    add_chart(doc, "platform_and_frequency.png", "Figure 1: Primary platform and usage frequency")
    add_chart(doc, "discovery_and_saving.png", "Figure 2: Discovery source and saving behaviour")
    add_chart(doc, "ordinal_distributions.png", "Figure 3: Distributions of ordinal questions")
    add_chart(doc, "age_and_boxplots.png", "Figure 4: Age distribution and ordinal score spread")

    h(doc, "7.2 Empathy map", 2)
    table(doc, ["Quadrant", "Evidence from responses"], [
        ["Says", "'Remove ads'; 'better recommendations'; 'organise all my music according to its vibe'"],
        ["Thinks", "'Why the same songs again?'; 'Will I find that saved track later?'"],
        ["Does", "78% save or playlist; 33% discover outside the app"],
        ["Feels", "Annoyed by ads (50%); mildly satisfied with recommendations"],
    ])
    h(doc, "7.3 Persona", 2)
    p(doc, "Aarav, 19 — B.Tech student and daily Spotify listener. He finds new music through friends "
           "and social media, saves tracks to playlists but rarely revisits them, wants music matching "
           "his current mood, and feels the app only 'somewhat' understands his taste. He is annoyed "
           "by ads but accepts they are part of a free tier.")
    h(doc, "7.4 Inferential findings", 2)
    p(doc, "One-sample t-tests compared each ordinal mean with the neutral value 2 (two-tailed, "
           "alpha = 0.05). Results:")
    table(doc, ["Measure", "Mean", "SD", "t", "df", "p", "95% CI"], [
        ["Usage frequency", "2.28", "0.83", "1.426", "17", "0.172", "[1.87, 2.69]"],
        ["Vibe-finding ease", "2.50", "0.62", "3.431", "17", "0.003", "[2.19, 2.81]"],
        ["Saved retrieval", "2.11", "1.02", "0.461", "17", "0.651", "[1.60, 2.62]"],
        ["Taste understanding", "2.33", "0.59", "2.380", "17", "0.029", "[2.04, 2.63]"],
    ])
    p(doc, "Interpretation. Vibe-finding ease and taste understanding were significantly above neutral, "
           "while saved retrieval was not significantly different from neutral. These results do not "
           "support a claim that users are deeply dissatisfied; they support a narrower claim that "
           "personalisation is good but not great, and that retrieval friction is common enough to "
           "address.")
    h(doc, "7.5 Correlations", 2)
    table(doc, ["Pair", "Pearson r", "Spearman rho", "p (Spearman)"], [
        ["Vibe ease vs saved retrieval", "+0.372", "+0.356", "0.148"],
        ["Vibe ease vs taste", "+0.320", "+0.316", "0.201"],
        ["Saved retrieval vs taste", "+0.323", "+0.307", "0.216"],
        ["Frequency vs taste", "+0.040", "+0.068", "0.790"],
    ])
    p(doc, "All associations are weak and statistically non-significant at n=18 (critical |r| about "
           "0.468). They are described as directional only.")
    add_chart(doc, "correlation_heatmap.png", "Figure 5: Spearman correlation matrix")
    h(doc, "7.6 Open-text themes", 2)
    table(doc, ["Theme", "Respondents", "Percent"], [
        ["Ads / paywall", "9", "50.0%"],
        ["Recommendations / taste", "8", "44.4%"],
        ["UI / customisation", "3", "16.7%"],
        ["Vibe / mood", "2", "11.1%"],
        ["Saving / organising", "1", "5.6%"],
    ])

    # ---- 8 Ideation ----
    h(doc, "8. Ideation and Concept Development", 1)
    p(doc, "Ten ideas were generated individually and compared using a weighted selection matrix "
           "(desirability 40%, feasibility 35%, viability 25%). A SWOT analysis checked the concept "
           "against the fragile client-side nature of the extension and the small sample.")
    table(doc, ["Idea", "D", "F", "V", "Weighted", "Decision"], [
        ["Familiar/Balanced/Exploratory slider", "5", "5", "5", "5.00", "Build"],
        ["Vibe-tag browser", "5", "5", "5", "5.00", "Build"],
        ["Save + personal library", "5", "5", "5", "5.00", "Build"],
        ["Preferences panel", "4", "5", "5", "4.65", "Build"],
        ["Usage logging + SUS", "3", "5", "5", "4.20", "Build"],
        ["Current-track context", "4", "4", "4", "4.00", "Keep"],
        ["Understand (lyrics)", "4", "2", "2", "2.80", "Future"],
        ["AI chatbot", "4", "1", "2", "2.45", "Future"],
        ["Ad blocker", "5", "1", "1", "2.80", "Reject — infeasible"],
    ])
    p(doc, "The selected concept is a privacy-first personalisation layer: Discover, Find by Vibe and "
           "My Music at its core, with a companion dashboard and measurement, and an explicit "
           "exclusion of ad removal.")

    # ---- 9 Prototype ----
    h(doc, "9. Proposed Solution and Prototype", 1)
    p(doc, "The prototype comprises two connected parts. The Chrome extension injects a dark side "
           "panel into Spotify Web, YouTube Music and Apple Music. A platform adapter selects itself "
           "by hostname and polls the page for the current track every two seconds; polling was "
           "chosen over MutationObserver because these single-page apps continually rebuild their DOM.")
    p(doc, "The companion dashboard is a responsive web application served by Flask. Its templates "
           "provide My Music, Discover, Find by Vibe, My Preferences, a Study page and a Findings page. "
           "The Python backend exposes page routes and JSON APIs for saving, removing, preference "
           "changes, event logging and task recording.")
    h(doc, "9.1 Database design", 2)
    table(doc, ["Table", "Purpose", "Key fields"], [
        ["users", "Anonymous browser identity", "id, session_id, created_at"],
        ["saved_songs", "Saved recommendations", "id, user_id, title, artist, genre, reason, source"],
        ["preferences", "Default level, vibe, tracking consent", "user_id, discovery_level, preferred_vibe, tracking_enabled"],
        ["usage_events", "Built-in measurement", "id, user_id, event_type, detail, duration_ms"],
        ["test_tasks", "Stage 5 timed tasks", "id, task_name, duration_ms, clicks, errors, completed"],
    ])
    h(doc, "9.2 Wireframe sketch", 2)
    p(doc, "Dashboard layout (text wireframe):\n"
           "┌──────────────────────────────┐\n"
           "│  Header: brand + nav          │\n"
           "├──────────────┬───────────────┤\n"
           "│ Hero / title │  Stat cards   │\n"
           "├──────────────┴───────────────┤\n"
           "│ Controls: platform / level    │\n"
           "│ ┌────┐ ┌────┐ ┌────┐         │\n"
           "│ │card│ │card│ │card│  ...     │\n"
           "│ └────┘ └────┘ └────┘         │\n"
           "└──────────────────────────────┘")
    h(doc, "9.3 Key features", 2)
    bullets(doc, [
        "Discover: Familiar, Balanced and Exploratory levels, current-track context, save button.",
        "Find by Vibe: eight mood tags with platform-specific sets and default fallback.",
        "My Music: SQLite-backed list of saved tracks with remove action.",
        "My Preferences: default level, preferred vibe and usage-tracking consent.",
        "Study: three timed tasks with automatic click/error logging and a 10-item SUS form.",
        "Findings: generated charts and anonymised response table.",
    ])
    p(doc, "Prototype screenshots were captured from the running dashboard at /discover, /vibe, /, "
           "/preferences and /study and are available in the presentation deck.")

    # ---- 10 Testing ----
    h(doc, "10. Testing, Statistical Validation and Discussion", 1)
    h(doc, "10.1 Hypotheses (fixed before testing)", 2)
    bullets(doc, [
        "H1a: median time to find a saved song is lower with the prototype; H0a: no difference.",
        "H1b: mean taste rating after using discovery exceeds the survey baseline of 2.33; H0b: unchanged.",
        "H1c: mean SUS score exceeds 68; H0c: SUS is 68 or lower.",
        "Significance level alpha = 0.05; paired design (same users try both).",
    ])
    h(doc, "10.2 Method", 2)
    p(doc, "The Study page records three timed tasks, counting clicks and errors automatically and "
           "writing duration to SQLite. Afterwards participants complete the ten-item SUS form; the "
           "script computes odd items as (response − 1) and even items as (5 − response), sums them "
           "and multiplies by 2.5. For task time a Wilcoxon signed-rank test is planned if the "
           "difference is non-normal, otherwise a paired t-test. SUS is compared with 68 using a "
           "one-sample t-test. Assumption checks (normality, outliers) and effect sizes will be "
           "reported alongside p-values and confidence intervals.")
    h(doc, "10.3 Results status", 2)
    p(doc, "The study instrument and logging are implemented, but participant runs were still being "
           "collected at the time of writing. Therefore no SUS score or task-time result is claimed "
           "in this paper. [Insert the following once real runs are complete: number of participants, "
           "median times for both methods, test statistic, p-value, 95% CI, effect size, mean SUS "
           "and interpretation.]")
    h(doc, "10.4 Improvements made during iteration", 2)
    bullets(doc, [
        "Track detection was split from one file into three platform adapters after YouTube Music's DOM broke the shared selector.",
        "A companion dashboard was added because saved songs existed in extension storage but had no view.",
        "Usage logging and a tracking-consent toggle were added so testing is based on measurement rather than recall.",
        "The analysis pipeline was made re-runnable so new survey responses update every statistic and chart.",
    ])
    h(doc, "10.5 Discussion and limitations", 2)
    p(doc, "The survey evidence supports the choice of retrieval and recommendation control as in-scope "
           "targets, while showing that ads — the most frequent complaint — cannot be addressed by "
           "this architecture. The baseline was above neutral, so the project claims refinement rather "
           "than rescue. Limitations: n=18 against a target of 30; 78% Spotify and no Apple Music "
           "respondents; demo rather than learned recommendations; fragile site selectors; two "
           "flagged low-quality responses; and a single contributor covering all five brief roles. "
           "These limit generalisation and are stated plainly rather than minimised.")

    # ---- 11 Conclusion ----
    h(doc, "11. Conclusion and Future Scope", 1)
    p(doc, "This project applied all five Design Thinking stages to a real, measured problem and "
           "produced a working cross-platform prototype with a Python backend, a SQLite database "
           "and built-in measurement. The strongest evidence-backed contribution is the save-and-"
           "retrieve loop: 78% save music while 44% sometimes struggle to find old saves. The "
           "prototype also gives users explicit control over recommendation familiarity and mood.")
    p(doc, "Future work includes replacing the demo recommendation database with a learned model, "
           "implementing the Understand section, collecting a larger stratified sample of at least "
           "30 responses, completing the paired usability study with effect sizes, and "
           "investigating whether mood-based retrieval improves measured task time.")

    # ---- 12 References ----
    h(doc, "12. References", 1)
    p(doc, "Brown, T. (2008). Design Thinking. Harvard Business Review, 86(6), 84–92.")
    p(doc, "Brooke, J. (1996). SUS: a 'quick and dirty' usability scale. In P. W. Jordan et al. "
           "(Eds.), Usability Evaluation in Industry. Taylor & Francis.")
    p(doc, "Integrated Assignment Brief (2026). Design for Impact: Finding a Real-World Problem and "
           "Proving Your Solution Works. B.Tech Second Year.")
    p(doc, "Google Forms (2026). Music Streaming Platform Experience questionnaire and anonymised "
           "response dataset (R01–R18).")
    p(doc, "Flask, pandas, NumPy, SciPy and matplotlib documentation (open-source libraries used "
           "for the backend and statistical analysis).")
    p(doc, "Spotify, YouTube Music and Apple Music web players (interface structures observed for "
           "track detection).")

    # ---- 13 Appendices ----
    h(doc, "13. Appendices", 1)
    h(doc, "Appendix A — Questionnaire", 2)
    bullets(doc, [
        "Name; Age.",
        "Which music-streaming platform do you use most often?",
        "How often do you use it?",
        "How do you usually discover new music?",
        "When you know the kind of mood or vibe you want, how easy is it to find suitable music?",
        "When you find a song you like, what do you usually do with it?",
        "How easy is it to find songs you saved a long time ago?",
        "How well does your music app understand your taste?",
        "What is the biggest problem you face while using your music-streaming app?",
        "What do you wish your music app could do better?",
        "If you could change one thing about your music-streaming experience, what would it be?",
    ])
    h(doc, "Appendix B — Interview guide (prepared, not administered)", 2)
    bullets(doc, [
        "Which app do you use most, and how often?",
        "Walk me through the last time you looked for a new song.",
        "Tell me about a time you could not find a song you had saved.",
        "How do you choose music for a specific mood?",
        "What bothers you most about your current app?",
    ])
    p(doc, "Disclosure: the guide was prepared but not administered within the available schedule; "
           "qualitative evidence comes from the three open-ended survey questions.", italic=True)
    h(doc, "Appendix C — Consent and anonymisation note", 2)
    p(doc, "Participants were told the purpose of the study, that participation was voluntary, and "
           "that responses would be used only for this academic project. Names were replaced with "
           "identifiers R01–R18 in the shared dataset and no contact details were collected.")
    h(doc, "Appendix D — Single-contributor scope statement", 2)
    p(doc, "The brief assumes a five-member team with five specialist roles. This project was "
           "executed by one student, consolidating Research, Statistics, Frontend, Backend and "
           "Documentation responsibilities. Reductions: no separate interview transcripts, "
           "individual rather than team brainstorming, and mentor review instead of peer review. "
           "These are disclosed limitations; no data was fabricated or altered.")
    h(doc, "Appendix E — Key analysis code", 2)
    p(doc, "The complete analysis pipeline is in webapp/analysis/analysis.py. It reads the Google "
           "Forms export, writes the anonymised CSV, computes descriptive statistics, one-sample "
           "t-tests, Pearson and Spearman correlations, confidence intervals and theme counts, and "
           "generates all figures. Run:")
    p(doc, "python3 webapp/analysis/analysis.py --csv \"Music Streaming Platform Experience "
           "(Responses) - Form responses 1.csv\"", italic=True)

    doc.save(OUT)
    print(f"Wrote {OUT}")


if __name__ == "__main__":
    main()
