#!/usr/bin/env python3
"""Generate the 15-slide PPTX from docs/presentation_script.md content."""

from pathlib import Path

from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.util import Inches, Pt

OUT = Path(__file__).with_name("Presentation.pptx")

BG = RGBColor(18, 18, 18)
GREEN = RGBColor(29, 185, 84)
WHITE = RGBColor(245, 245, 245)
MUTED = RGBColor(160, 160, 160)

SLIDES = [
    ("Title", [
        "Reimagining the Personal Music Experience",
        "A Design Thinking project with statistical validation",
        "Name · Roll number · Department · Institution",
        "Faculty mentor",
    ], "Good morning. I'm presenting Reimagining the Personal Music Experience — a privacy-first "
       "personalisation layer for Spotify, YouTube Music and Apple Music, backed by survey data "
       "and a working Python backend."),

    ("Introduction", [
        "Music streaming is part of daily life: 78% use their app daily or several times a week",
        "61% say the app only 'somewhat' or 'poorly' understands their taste",
        "Question: can a lightweight utility improve discovery and rediscovery without account APIs?",
    ], "Music streaming is routine for our respondents, but personalisation is uneven. Only 39% "
       "say their app understands their taste very well. This project asks whether a lightweight "
       "utility can improve discovery and rediscovery without needing account APIs."),

    ("Project overview", [
        "Objective 1: give users control over familiarity of recommendations",
        "Objective 2: make saved music easy to rediscover",
        "Objective 3: prove with statistics that the design addresses real pain points",
        "Outcomes: Chrome extension + Flask/SQLite dashboard + re-runnable analysis pipeline",
    ], "Objectives: control over recommendation familiarity, easy rediscovery of saved music, "
       "and statistical proof. Outcomes are a Chrome extension, a responsive Flask dashboard "
       "with SQLite, and an analysis pipeline that reruns on updated data."),

    ("User research", [
        "Target users: students and young adults, age 18–30 (median 19)",
        "Sampling: convenience; questionnaire with MCQ, ordinal, numeric and open-ended items",
        "Sample size: 18 responses (below the brief's target of 30 — declared limitation)",
        "78% Spotify · 17% YouTube Music · 1 'Other'",
    ], "We used convenience sampling of students. The questionnaire mixes multiple choice, "
       "ordinal ratings, numeric age and three open-ended questions. 18 responses — below the "
       "target of 30, which we state openly. The sample is 78% Spotify."),

    ("Empathise", [
        "Says: 'remove ads' · 'better recommendations' · 'organise music by vibe'",
        "Does: 78% save or like tracks; 44% sometimes struggle to find old saves",
        "Feels: mildly satisfied, not delighted",
        "Ranked pain points: ads 50% (out of scope) · recommendations 44% · retrieval 44%",
    ], "Users say remove ads and better recommendations. They do save songs — 78% — but 44% "
       "struggle to find old saves. Ranked pain points: ads 50%, out of scope; recommendations "
       "and retrieval both 44%."),

    ("Statistical findings", [
        "Ordinal coding 1–3; neutral = 2; one-sample t-tests",
        "Vibe ease: mean 2.50, t=3.43, p=0.003, CI [2.19, 2.81]",
        "Taste understanding: mean 2.33, t=2.38, p=0.029, CI [2.04, 2.63]",
        "Saved retrieval: mean 2.11, t=0.46, p=0.651 — not significant",
        "Correlations weak (rho 0.31–0.36), none significant → no overclaiming",
    ], "One-sample t-tests against neutral show responses above neutral for vibe ease and taste "
       "understanding. Saved retrieval was not significant. Correlations were weak. So we do not "
       "overclaim: the baseline is good-but-not-great and the opportunity is refinement."),

    ("Define", [
        "Persona: 'Aarav, 19' — daily Spotify user, discovers music outside the app",
        "POV: saves but cannot rediscover; taste only 'somewhat' understood",
        "HMW: give familiarity control and mood-based retrieval without a paid subscription",
        "MoSCoW: Must = Discover, My Music, backend · Won't = ads, offline downloads",
    ], "Our composite persona is Aarav, a 19-year-old daily Spotify user. POV: a listener who "
       "saves but cannot rediscover and feels recommendations only somewhat match their taste. "
       "HMW: how might we give that control without a paid subscription? MoSCoW puts Discover, "
       "My Music and the backend in Must."),

    ("Ideation", [
        "10 ideas generated: discovery slider, vibe tags, save/library, current-track context,",
        "preferences panel, usage logging, Understand, AI chatbot, ad blocker, offline mode",
        "Mind map across five branches: discovery, mood, library, understanding, preferences",
        "Techniques: individual brainstorming + SWOT",
    ], "We generated ten ideas, from a discovery slider and vibe tags to an AI chatbot and an ad "
       "blocker, mapped them across five branches, then scored each on desirability, feasibility "
       "and viability."),

    ("Idea selection & hypotheses", [
        "Weighted matrix: desirability 40% · feasibility 35% · viability 25%",
        "Top score 5.00: discovery slider, vibe tags, save + library",
        "AI chatbot 2.45 and ad blocker 2.80 — rejected on feasibility",
        "H0/H1 fixed before testing: retrieval time, taste > 2.33, SUS > 68; alpha = 0.05",
    ], "Weighted scoring put the discovery slider, vibe tags and save-plus-library at 5.00. The "
       "AI chatbot scored 2.45 and ad blocker 2.80 — rejected on feasibility. Before testing we "
       "fixed three hypotheses at alpha 0.05."),

    ("Prototype", [
        "Extension: injected panel + per-platform track adapters (2s polling)",
        "Frontend: responsive HTML/CSS/JS templates in the companion dashboard",
        "Backend: Flask routes + JSON APIs",
        "Database: SQLite — users, saved_songs, preferences, usage_events, test_tasks",
        "Privacy: all data local; no login, no external API",
    ], "The prototype has two parts: a Chrome extension with per-platform adapters, and a "
       "responsive Flask dashboard with SQLite. Everything stays local — no login, no external "
       "API. Let me demonstrate: Discover, save a song, My Music, Vibe, and the study page."),

    ("Testing and validation", [
        "Paired design: same users try current method and prototype",
        "Three timed tasks; clicks and errors logged to SQLite automatically",
        "System Usability Scale (SUS), 0–100; benchmark 68",
        "Wilcoxon/paired t-test for time; one-sample t-test for SUS",
        "[Insert real participant count, test statistic, p-value and CI after testing]",
    ], "Testing uses the same participants on both methods. The study page times three tasks and "
       "counts clicks and errors, then computes SUS. For time, Wilcoxon if non-normal otherwise "
       "paired t-test; for SUS a one-sample t-test against 68. Insert actual results here once "
       "runs are complete."),

    ("Results and iterations", [
        "Iteration 1: split track detection into per-platform adapters",
        "Iteration 2: added dashboard because saved songs had no view",
        "Iteration 3: added usage logging and consent toggle for measurement",
        "[Add SUS and task-time changes from real testing]",
    ], "Iteration one: we split track detection into per-platform adapters after the single-file "
       "version broke on YouTube Music. Iteration two: a dashboard gave saved songs a view. "
       "Iteration three: usage logging and a consent toggle made testing measurable."),

    ("Impact and limitations", [
        "Benefits: no account, local data, works across three platforms",
        "Limitations: n=18 not 30; 78% Spotify, zero Apple Music; ads out of scope",
        "Demo recommendation database, not a production recommender",
        "Single-contributor scope: five roles consolidated, reductions disclosed",
    ], "Benefits: no account required, data never leaves the browser, three platforms. "
       "Limitations: n=18 not 30, 78% Spotify and zero Apple Music, ads out of scope, demo "
       "recommendation data, and single-contributor scope. We disclose all of these."),

    ("Conclusion and future scope", [
        "A small focused utility addresses a measured gap without complex infrastructure",
        "Addresses in-scope pain points; does not claim to fix ads",
        "Future: real recommendation model, Understand section, larger stratified sample",
    ], "We learned that a small focused utility can address a real measured gap — saved-song "
       "retrieval and taste control — without complex infrastructure. Future work: a real "
       "recommendation model, the Understand section, and a larger stratified sample."),

    ("References and Q&A", [
        "Anonymised survey dataset (R01–R18)",
        "Integrated assignment brief",
        "Libraries: Flask, pandas, scipy, matplotlib, python-pptx",
        "AI tools used for code and documentation drafting — disclosed",
        "Thank you — questions?",
    ], "Sources: our anonymised survey dataset, the assignment brief, and the open-source "
       "libraries used. AI tools were used for code drafting and documentation, disclosed per "
       "the brief. Thank you — questions?"),
]


def add_slide(prs: Presentation, title: str, bullets: list[str], notes: str, index: int) -> None:
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    bg = slide.background.fill
    bg.solid()
    bg.fore_color.rgb = BG

    bar = slide.shapes.add_shape(1, Inches(0), Inches(0), Inches(0.15), Inches(7.5))
    bar.fill.solid(); bar.fill.fore_color.rgb = GREEN
    bar.line.fill.background()

    tb = slide.shapes.add_textbox(Inches(0.6), Inches(0.45), Inches(12), Inches(1.1))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = f"{index:02d}  {title}"
    p.font.size = Pt(30)
    p.font.bold = True
    p.font.color.rgb = GREEN if index != 1 else WHITE

    body = slide.shapes.add_textbox(Inches(0.65), Inches(1.7), Inches(12), Inches(5.2))
    tf = body.text_frame
    tf.word_wrap = True
    for i, line in enumerate(bullets):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.text = "• " + line
        p.font.size = Pt(18 if len(line) < 95 else 16)
        p.font.color.rgb = WHITE
        p.space_after = Pt(12)

    foot = slide.shapes.add_textbox(Inches(0.65), Inches(7.05), Inches(10), Inches(0.3))
    foot.text_frame.paragraphs[0].text = "Reimagining the Personal Music Experience"
    foot.text_frame.paragraphs[0].font.size = Pt(10)
    foot.text_frame.paragraphs[0].font.color.rgb = MUTED

    slide.notes_slide.notes_text_frame.text = notes


def main() -> None:
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    for i, (title, bullets, notes) in enumerate(SLIDES, start=1):
        add_slide(prs, title, bullets, notes, i)
    prs.save(OUT)
    print(f"Wrote {OUT} ({len(SLIDES)} slides)")


if __name__ == "__main__":
    main()
