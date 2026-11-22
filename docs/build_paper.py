#!/usr/bin/env python3
"""Generate the research paper DOCX following Section 10 of the integrated brief."""

from pathlib import Path

from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn
from docx.shared import Pt, Inches, RGBColor

OUT = Path(__file__).with_name("Research_Paper.docx")
ROOT = Path(__file__).resolve().parents[1]
CHARTS = ROOT / "data" / "charts"

FONT_NAME = "Times New Roman"
BLACK = RGBColor(0, 0, 0)
BODY_SIZE = 12
CAPTION_SIZE = 10
TITLE_SIZE = 28
CHART_WIDTH = 7.1  # inches; page text width is 7.2" with the narrower margins below


def apply_font(obj, size=None):
    """Force Times New Roman and black on a style or a run."""
    obj.font.name = FONT_NAME
    obj.font.color.rgb = BLACK
    if size is not None:
        obj.font.size = Pt(size)
    element = obj.element if hasattr(obj, "element") else obj._element
    rpr = element.get_or_add_rPr()
    rfonts = rpr.get_or_add_rFonts()
    for attr in ("w:ascii", "w:hAnsi", "w:eastAsia", "w:cs"):
        rfonts.set(qn(attr), FONT_NAME)


def h(doc, text, level=1, new_page=False):
    par = doc.add_heading(text, level=level)
    if new_page:
        par.paragraph_format.page_break_before = True
    return par


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
    t.style = "Table Grid"
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
    run.font.size = Pt(CAPTION_SIZE)
    par.alignment = WD_ALIGN_PARAGRAPH.CENTER


def normalise_fonts(doc):
    """Final pass: no blue or Calibri can survive anywhere in the document."""
    for style in doc.styles:
        if hasattr(style, "font") and style.font is not None:
            apply_font(style)
    for par in doc.paragraphs:
        for run in par.runs:
            apply_font(run)
    for tbl in doc.tables:
        for row in tbl.rows:
            for cell in row.cells:
                for par in cell.paragraphs:
                    for run in par.runs:
                        apply_font(run)


def add_chart(doc, filename, caption_text, new_page=False):
    path = CHARTS / filename
    if path.exists():
        if new_page:
            doc.add_page_break()
        par = doc.add_paragraph()
        par.alignment = WD_ALIGN_PARAGRAPH.CENTER
        par.paragraph_format.keep_with_next = True  # image never leaves its caption
        run = par.add_run()
        run.add_picture(str(path), width=Inches(CHART_WIDTH))
        caption(doc, caption_text)


def main():
    doc = Document()
    for section in doc.sections:
        section.top_margin = Inches(0.7)
        section.bottom_margin = Inches(0.7)
        section.left_margin = Inches(0.65)
        section.right_margin = Inches(0.65)
    for style_name, size in (("Normal", BODY_SIZE), ("Heading 1", 16),
                             ("Heading 2", 14), ("List Bullet", BODY_SIZE),
                             ("Caption", CAPTION_SIZE)):
        if style_name in doc.styles:
            apply_font(doc.styles[style_name], size)

    # ---- Title page ----
    title = doc.add_paragraph()
    title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = title.add_run("Reimagining the Personal Music Experience")
    run.bold = True
    run.font.size = Pt(TITLE_SIZE)
    run.font.color.rgb = BLACK
    sub = doc.add_paragraph()
    sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
    sub.add_run("A Design Thinking study with statistical validation of a cross-platform\n"
                "personalisation prototype").italic = True
    doc.add_paragraph()
    meta = doc.add_paragraph()
    meta.alignment = WD_ALIGN_PARAGRAPH.CENTER
    meta.add_run("Integrated Group Project — B.Tech Second Year\n"
                 "Introduction to Design Thinking · Web Technology · Python · Probability and Statistics\n\n"
                 "Preet Kamdar · 256019\n"
                 "B.Tech CSE (AI & ML) · JG University\n"
                 "Faculty mentors: Suryansh Rajput · Tanya Verma · Harsh Bhojak · Neelu Verma\n\n"
                 "Combined project: Python · Web Technology · Design Thinking · Probability & Statistics")
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
           "by a Flask/SQLite dashboard. A 32-response survey found taste understanding significantly "
           "above neutral but modest (mean 2.31, t=2.55, p=0.016), while 47% sometimes struggled to "
           "find old saves. The prototype addresses these in-scope gaps with local, private data and "
           "built-in usage measurement. n=32 and single-contributor scope are disclosed as limits.")
    p(doc, "Word count: approximately 115 words (brief recommends about 50; this version includes "
           "the required main statistical finding and model details).", italic=True)

    # ---- 2 Keywords ----
    h(doc, "2. Keywords", 1)
    p(doc, "Design Thinking; music personalisation; recommendation systems; usability testing; "
           "System Usability Scale; hypothesis testing; Chrome extension; Flask; SQLite.")

    # ---- 3 Introduction ----
    h(doc, "3. Introduction", 1)
    p(doc, "Music streaming is a routine activity for young adults. The survey conducted for this "
           "project found that 84% of respondents used their primary platform daily or several times "
           "a week. Yet routine use does not imply satisfaction with personalisation: 44% said their "
           "app understood their taste only 'somewhat' and a further 13% said 'poorly'. Only 44% "
           "chose 'very well'.")
    p(doc, "At the same time, 84% of respondents add a liked song to a playlist or save/like it, but "
           "47% reported that finding songs saved a long time ago is sometimes difficult. This "
           "save-and-retrieve gap is directly addressable by a lightweight utility that does not need "
           "access to a streaming service's private APIs.")
    p(doc, "The integrated brief asks a sharper question than earlier versions: can we prove with "
           "data that a solution is better than what users have today? Accordingly, this project "
           "combines the five Design Thinking stages with a questionnaire, descriptive and "
           "inferential statistics, a working frontend and Python backend, and an instrumented "
           "usability study.")
    p(doc, "The scope of this document is deliberately honest. The survey has 32 responses, meeting a "
           "target of 30, the recommendation database is demo content, and the largest single complaint "
           "— advertisements, mentioned by 53% — is outside the technical reach of a client-side "
           "utility. Each of these is treated as a limitation rather than hidden.")

    # ---- 4 Literature review ----
    h(doc, "4. Literature Review", 1, new_page=True)
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
    h(doc, "6. Research Methodology", 1, new_page=True)
    h(doc, "6.1 Participants and sampling", 2)
    p(doc, "Convenience sampling was used to recruit 32 respondents, mostly students aged 18–30 "
           "(median 19; numeric mean 19.69, SD 2.19). 72% named Spotify as their primary platform, "
           "13% YouTube Music, 9% 'Other' and 6% Apple Music. Limitations: small sample, "
           "platform imbalance, self-selection bias and no "
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
    p(doc, "Participants were informed of the purpose and data use. Names were replaced by R01–R32 in "
           "the anonymised dataset. No contact details or sensitive information were collected. Two "
           "non-substantive responses were flagged rather than deleted, and no responses were "
           "invented or altered. AI tools were used for code and documentation drafting and are "
           "disclosed here.")

    # ---- 7 Findings ----
    h(doc, "7. User Research and Findings", 1, new_page=True)
    h(doc, "7.1 Descriptive findings", 2)
    table(doc, ["Measure", "Result"], [
        ["Responses", "32 (30 assessed as substantive)"],
        ["Primary platform", "Spotify 23 (72%); YouTube Music 4 (13%); Other 3 (9%); Apple Music 2 (6%)"],
        ["Usage frequency", "Daily 19 (59%); several times/week 8 (25%); occasionally 5 (16%)"],
        ["Discovery source", "Outside app 9 (28%); search 9 (28%); recommendations 8 (25%); playlist 6 (19%)"],
        ["Vibe-finding ease", "Easy 16 (50%); Average 11 (34%); Difficult 5 (16%)"],
        ["Action after liking", "Playlist 17 (53%); save/like 10 (31%); just listen 5 (16%)"],
        ["Saved retrieval", "Easy 15 (47%); sometimes difficult 15 (47%); difficult 2 (6%)"],
        ["Taste understanding", "Very well 14 (44%); somewhat 14 (44%); poorly 4 (13%)"],
    ])
    doc.add_page_break()  # keep the enlarged charts off the descriptive table
    add_chart(doc, "platform_and_frequency.png", "Figure 1: Primary platform and usage frequency")
    add_chart(doc, "discovery_and_saving.png", "Figure 2: Discovery source and saving behaviour")
    add_chart(doc, "ordinal_distributions.png", "Figure 3: Distributions of ordinal questions",
              new_page=True)
    add_chart(doc, "age_and_boxplots.png", "Figure 4: Age distribution and ordinal score spread")

    h(doc, "7.2 Empathy map", 2, new_page=True)
    table(doc, ["Quadrant", "Evidence from responses"], [
        ["Says", "'Remove ads'; 'better recommendations'; 'organise all my music according to its vibe'"],
        ["Thinks", "'Why the same songs again?'; 'Will I find that saved track later?'"],
        ["Does", "84% save or playlist; 28% discover outside the app"],
        ["Feels", "Annoyed by ads (53%); mildly satisfied with recommendations"],
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
        ["Usage frequency", "2.44", "0.76", "3.259", "31", "0.0027", "[2.16, 2.71]"],
        ["Vibe-finding ease", "2.34", "0.75", "2.609", "31", "0.0138", "[2.08, 2.61]"],
        ["Saved retrieval", "1.94", "1.01", "-0.349", "31", "0.7297", "[1.57, 2.30]"],
        ["Taste understanding", "2.31", "0.69", "2.552", "31", "0.0159", "[2.06, 2.56]"],
    ])
    p(doc, "Interpretation. Vibe-finding ease and taste understanding were significantly above neutral, "
           "while saved retrieval was not significantly different from neutral. These results do not "
           "support a claim that users are deeply dissatisfied; they support a narrower claim that "
           "personalisation is good but not great, and that retrieval friction is common enough to "
           "address.")
    h(doc, "7.5 Correlations", 2)
    table(doc, ["Pair", "Pearson r", "Spearman rho", "p (Spearman)"], [
        ["Vibe ease vs saved retrieval", "+0.328", "+0.331", "0.0642"],
        ["Vibe ease vs taste", "+0.410", "+0.325", "0.0700"],
        ["Saved retrieval vs taste", "+0.304", "+0.312", "0.0817"],
        ["Frequency vs taste", "+0.222", "+0.240", "0.1854"],
    ])
    p(doc, "At n=32 the critical |r| is about 0.349. None of the six pairs reaches it; the strongest is vibe-finding ease versus saved retrieval "
           "(rho +0.331, p = 0.064), followed by vibe ease versus taste (rho +0.325, p = 0.070). All associations are weak and directional only.")
    add_chart(doc, "correlation_heatmap.png", "Figure 5: Spearman correlation matrix",
              new_page=True)
    h(doc, "7.6 Open-text themes", 2)
    table(doc, ["Theme", "Respondents", "Percent"], [
        ["Ads / paywall", "17", "53.1%"],
        ["Recommendations / taste", "12", "37.5%"],
        ["UI / customisation", "6", "18.8%"],
        ["Vibe / mood", "4", "12.5%"],
        ["Saving / organising", "2", "6.2%"],
    ])

    # ---- 8 Ideation ----
    h(doc, "8. Ideation and Concept Development", 1, new_page=True)
    p(doc, "Ten ideas were generated individually and compared using a weighted selection matrix "
           "(desirability 40%, feasibility 35%, viability 25%). A SWOT analysis checked the concept "
           "against the fragile client-side nature of the extension and the small sample.")
    table(doc, ["Idea", "D", "F", "V", "Weighted", "Decision"], [
        ["Familiar/Balanced/Exploratory slider", "5", "5", "5", "5.00", "Build"],
        ["Vibe-tag browser", "5", "5", "5", "5.00", "Build"],
        ["Save + personal library", "5", "5", "5", "5.00", "Build"],
        ["Preferences panel", "4", "5", "5", "4.60", "Build"],
        ["Usage logging + SUS", "3", "5", "5", "4.20", "Build"],
        ["Current-track context", "4", "4", "4", "4.00", "Keep"],
        ["Understand (lyrics)", "4", "2", "2", "2.80", "Future"],
        ["AI chatbot", "4", "1", "2", "2.45", "Future"],
        ["Ad blocker", "5", "1", "1", "2.60", "Reject — infeasible"],
    ])
    p(doc, "The selected concept is a privacy-first personalisation layer: Discover, Find by Vibe and "
           "My Music at its core, with a companion dashboard and measurement, and an explicit "
           "exclusion of ad removal.")

    # ---- 9 Prototype ----
    h(doc, "9. Proposed Solution and Prototype", 1, new_page=True)
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
    h(doc, "9.2 Key features", 2)
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
    h(doc, "10. Testing, Statistical Validation and Discussion", 1, new_page=True)
    h(doc, "10.1 Hypotheses (fixed before testing)", 2)
    bullets(doc, [
        "H1a: median time to find a saved song is lower with the prototype; H0a: no difference.",
        "H1b: mean taste rating after using discovery exceeds the survey baseline of 2.31; H0b: unchanged.",
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
    p(doc, "No participant usability study was completed, so this paper claims no SUS result and no "
           "task-time effect. A single author pilot was run afterwards to verify that the instrument "
           "works: three timed tasks (46.6 s, 27.0 s and 23.4 s; all completed) and one SUS "
           "self-rating of 35.0 were written to SQLite. Because this is one self-assessment by the "
           "designer, it is reported as a system check, not as usability evidence. Proper paired "
           "runs with real participants, with test statistics, confidence intervals and effect "
           "sizes, remain future work.")
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
           "than rescue. Limitations: n=32 modest sample; 72% Spotify and only 6% Apple Music "
           "respondents; demo rather than learned recommendations; fragile site selectors; two "
           "flagged low-quality responses; and a single contributor covering all five brief roles. "
           "These limit generalisation and are stated plainly rather than minimised.")

    # ---- 11 Conclusion ----
    h(doc, "11. Conclusion and Future Scope", 1, new_page=True)
    p(doc, "This project applied all five Design Thinking stages to a real, measured problem and "
           "produced a working cross-platform prototype with a Python backend, a SQLite database "
           "and built-in measurement. The strongest evidence-backed contribution is the save-and-"
           "retrieve loop: 84% save music while 47% sometimes struggle to find old saves. The "
           "prototype also gives users explicit control over recommendation familiarity and mood.")
    p(doc, "Future work includes replacing the demo recommendation database with a learned model, "
           "implementing the Understand section, collecting a larger stratified sample of at least "
           "60 responses, completing the paired usability study with effect sizes, and "
           "investigating whether mood-based retrieval improves measured task time.")

    # ---- 12 References ----
    h(doc, "12. References", 1, new_page=True)
    p(doc, "Brown, T. (2008). Design Thinking. Harvard Business Review, 86(6), 84–92.")
    p(doc, "Brooke, J. (1996). SUS: a 'quick and dirty' usability scale. In P. W. Jordan et al. "
           "(Eds.), Usability Evaluation in Industry. Taylor & Francis.")
    p(doc, "Integrated Assignment Brief (2026). Design for Impact: Finding a Real-World Problem and "
           "Proving Your Solution Works. B.Tech Second Year.")
    p(doc, "Google Forms (2026). Music Streaming Platform Experience questionnaire and anonymised "
           "response dataset (R01–R32).")
    p(doc, "Flask, pandas, NumPy, SciPy and matplotlib documentation (open-source libraries used "
           "for the backend and statistical analysis).")
    p(doc, "Spotify, YouTube Music and Apple Music web players (interface structures observed for "
           "track detection).")

    # ---- 13 Appendices ----
    h(doc, "13. Appendices", 1, new_page=True)
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
           "identifiers R01–R32 in the shared dataset and no contact details were collected.")
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

    normalise_fonts(doc)
    doc.save(OUT)
    print(f"Wrote {OUT}")


if __name__ == "__main__":
    main()
