#!/usr/bin/env python3
"""
Statistical analysis for "Reimagining the Personal Music Experience".

Reads the raw Google Forms CSV, produces an anonymised copy, computes all
descriptive / inferential statistics required by the integrated assignment
brief, generates charts, and writes a Markdown report.

Re-runnable: point --csv at an updated export and every number updates.

Usage:
    python3 webapp/analysis/analysis.py \
        --csv "Music Streaming Platform Experience (Responses) - Form responses 1.csv"
"""

from __future__ import annotations

import argparse
import math
import re
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy import stats

# --------------------------------------------------------------------------- #
# Column names (exact, from the Google Form)
# --------------------------------------------------------------------------- #
C_TIME = "Timestamp"
C_NAME = "Name"
C_AGE = "Age"
C_PLATFORM = "Which music-streaming platform do you use most often?"
C_FREQ = "How often do you use it?"
C_DISCOVER = "How do you usually discover new music?"
C_VIBE = "When you know the kind of mood or vibe you want, how easy is it to find suitable music?"
C_SAVE_BEHAVIOUR = "When you find a song you like, what do you usually do with it?"
C_RETRIEVE = "How easy is it to find songs you saved a long time ago?"
C_TASTE = "How well does your music app understand your taste?"
C_PROBLEM = "What is the biggest problem you face while using your music-streaming app?"
C_WISH = "What do you wish your music app could do better?"
C_CHANGE = "If you could change one thing about your music-streaming experience, what would it be?"

OPEN_COLS = [C_PROBLEM, C_WISH, C_CHANGE]

ORDINAL_MAPS = {
    "Usage frequency": (C_FREQ, {"Daily": 3, "Several times a week": 2, "Occasionally": 1}),
    "Vibe-finding ease": (C_VIBE, {"Easy": 3, "Average": 2, "Difficult": 1}),
    "Saved-song retrieval": (C_RETRIEVE, {"Easy": 3, "Sometimes difficult": 1, "Difficult": 1}),
    "Taste understanding": (C_TASTE, {"Very well": 3, "Somewhat": 2, "Poorly": 1}),
}

THEMES = {
    "Ads / paywall": ("ad", "premium", "subscribe", "free music", "ad free", "advertisement"),
    "Recommendations / taste": ("recommend", "taste", "suggest", "repetitive", "related", "according to my"),
    "Saving / organising": ("save", "organise", "playlist", "collect"),
    "Vibe / mood": ("vibe", "mood"),
    "UI / customisation": ("ui", "interface", "custom", "queue", "shuffle", "download"),
}

# Low-effort / non-substantive open-text responses flagged during cleaning.
JUNK_TOKENS = {"mpgh", "idk", "none", "nothing", "no idea", "all great", "...", "....", "just like above"}


# --------------------------------------------------------------------------- #
# Helpers
# --------------------------------------------------------------------------- #
def fmt(x: float, d: int = 2) -> str:
    return f"{x:.{d}f}"


def tidx(s: str) -> str:
    """Short label for charts / tables."""
    return re.sub(r"[^a-z0-9]+", "_", s.lower()).strip("_")


def anonymise(df: pd.DataFrame, outpath: Path) -> pd.DataFrame:
    """Replace real names with R01..Rnn and preserve everything else."""
    out = df.copy()
    mapping = {name: f"R{i:02d}" for i, name in enumerate(out[C_NAME].astype(str), start=1)}
    out[C_NAME] = out[C_NAME].astype(str).map(mapping)
    out.to_csv(outpath, index=False)
    return out


def quality_flags(df: pd.DataFrame) -> list[str]:
    flags = []
    for idx, row in df.iterrows():
        answers = [str(row[c]).strip().lower() for c in OPEN_COLS]
        if all(a in JUNK_TOKENS or not a for a in answers):
            flags.append(f"row {idx + 2} (R{idx + 1:02d}): all open answers non-substantive")
        elif "iphone" in " ".join(answers) or "concert" in " ".join(answers):
            flags.append(f"row {idx + 2} (R{idx + 1:02d}): non-serious open answers")
    return flags


def duplicate_names(df: pd.DataFrame) -> list[str]:
    """Report duplicate counts without printing respondent names."""
    counts = df[C_NAME].astype(str).str.strip().str.lower().value_counts()
    return [f"{n} rows share a name" for _, n in counts[counts > 1].items()]


def ordinal_scores(df: pd.DataFrame) -> dict[str, pd.Series]:
    scores = {}
    for label, (col, mapping) in ORDINAL_MAPS.items():
        scores[label] = df[col].astype(str).str.strip().map(mapping).dropna().astype(float)
    return scores


def one_sample_tests(scores: dict[str, pd.Series]) -> pd.DataFrame:
    """H0: population mean equals neutral (2 = 'Average' / 'Somewhat')."""
    records = []
    for label, x in scores.items():
        n, mean, sd = len(x), x.mean(), x.std(ddof=1)
        se = sd / math.sqrt(n)
        t = (mean - 2.0) / se
        p = 2 * (1 - stats.t.cdf(abs(t), df=n - 1))
        tcrit = stats.t.ppf(0.975, df=n - 1)
        lo, hi = mean - tcrit * se, mean + tcrit * se
        records.append(
            dict(Measure=label, n=n, Mean=mean, SD=sd, SE=se, t=t, df=n - 1,
                 p=p, CI_low=lo, CI_high=hi)
        )
    return pd.DataFrame(records)


def correlation_table(scores: dict[str, pd.Series]) -> pd.DataFrame:
    labels = list(scores)
    rows = []
    for i, a in enumerate(labels):
        for b in labels[i + 1:]:
            common = scores[a].index.intersection(scores[b].index)
            x, y = scores[a].loc[common], scores[b].loc[common]
            pearson = stats.pearsonr(x, y)
            spearman = stats.spearmanr(x, y)
            rows.append(dict(A=a, B=b, n=len(x), Pearson=pearson.statistic,
                             p_pearson=pearson.pvalue, Spearman=spearman.statistic,
                             p_spearman=spearman.pvalue))
    return pd.DataFrame(rows)


def theme_counts(df: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for theme, words in THEMES.items():
        n = 0
        for _, row in df.iterrows():
            text = " ".join(str(row[c]).lower() for c in OPEN_COLS)
            if any(w in text for w in words):
                n += 1
        rows.append(dict(Theme=theme, Respondents=n, Percent=100 * n / len(df)))
    return pd.DataFrame(rows).sort_values("Respondents", ascending=False)


def value_counts_table(df: pd.DataFrame, col: str) -> pd.DataFrame:
    vc = df[col].astype(str).str.strip().value_counts()
    return pd.DataFrame({"Count": vc, "Percent": 100 * vc / len(df)})


# --------------------------------------------------------------------------- #
# Charts
# --------------------------------------------------------------------------- #
def make_charts(df: pd.DataFrame, scores: dict[str, pd.Series], outdir: Path) -> list[str]:
    outdir.mkdir(parents=True, exist_ok=True)
    paths = []

    def save(fig, filename: str):
        p = outdir / filename
        fig.patch.set_facecolor("#FFFFFF")
        fig.tight_layout(pad=0.5)
        fig.savefig(p, dpi=150, facecolor=fig.get_facecolor(),
                    bbox_inches="tight", pad_inches=0.12)
        plt.close(fig)
        paths.append(str(p))

    # Light, soft palette that matches the official presentation theme. All
    # five colours stay legible against white with the dark green ink below.
    palette = ["#E3D27A", "#2FB4C2", "#7FCB6B", "#E89A8A", "#6E8C7C"]
    ink = "#14201A"
    ink_soft = "#1B5E3F"

    def style_axes(ax):
        ax.set_facecolor("#FFFFFF")
        ax.grid(True, axis="both", color="#D5DFD2", linestyle="-", linewidth=0.8, alpha=0.9)
        ax.set_axisbelow(True)
        for spine in ax.spines.values():
            spine.set_color("#C9D4C2")
            spine.set_linewidth(1.0)
        ax.tick_params(colors=ink_soft, labelsize=16)
        ax.title.set_color(ink)
        ax.title.set_fontsize(21)
        ax.title.set_fontweight("bold")
        if ax.get_ylabel():
            ax.yaxis.label.set_color(ink_soft)
            ax.yaxis.label.set_fontsize(15)
        if ax.get_xlabel():
            ax.xaxis.label.set_color(ink_soft)
            ax.xaxis.label.set_fontsize(15)

    # Platform + frequency
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))
    for ax, col, title in zip(axes, [C_PLATFORM, C_FREQ], ["Primary platform", "Usage frequency"]):
        vc = df[col].astype(str).str.strip().value_counts()
        ax.bar(vc.index, vc.values, color=palette[: len(vc)])
        ax.set_title(title)
        ax.set_ylabel("Respondents")
        ax.tick_params(axis="x", rotation=20)
        style_axes(ax)
    save(fig, "platform_and_frequency.png")

    # Discovery + save behaviour
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))
    for ax, col, title in zip(axes, [C_DISCOVER, C_SAVE_BEHAVIOUR], ["Discovery source", "Action after liking a song"]):
        vc = df[col].astype(str).str.strip().value_counts()
        ax.bar(vc.index, vc.values, color=palette[: len(vc)])
        ax.set_title(title)
        ax.set_ylabel("Respondents")
        ax.tick_params(axis="x", rotation=20)
        style_axes(ax)
    save(fig, "discovery_and_saving.png")

    # Ordinal distributions
    fig, axes = plt.subplots(1, 4, figsize=(16, 5))
    for ax, (label, (col, mapping)) in zip(axes, ORDINAL_MAPS.items()):
        vc = df[col].astype(str).str.strip().value_counts()
        order = [k for k in mapping if k in vc.index]
        ax.bar(order, [vc[k] for k in order], color=palette[: len(order)])
        ax.set_title(label)
        ax.tick_params(axis="x", rotation=20)
        style_axes(ax)
    save(fig, "ordinal_distributions.png")

    # Age histogram + box plot of ordinal scores
    ages = pd.to_numeric(df[C_AGE], errors="coerce").dropna()
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))
    axes[0].hist(ages, bins=max(4, int(ages.max() - ages.min()) + 1), color="#7FCB6B", edgecolor="#FFFFFF")
    axes[0].set_title(f"Age (n={len(ages)}, mean={ages.mean():.1f})")
    axes[1].boxplot([scores[k].values for k in scores], tick_labels=list(scores))
    axes[1].set_title("Ordinal score distributions (1–3)")
    axes[1].tick_params(axis="x", rotation=25)
    style_axes(axes[0]); style_axes(axes[1])
    save(fig, "age_and_boxplots.png")

    # Correlation heatmap
    keys = list(scores)
    mat = np.eye(len(keys))
    for i, a in enumerate(keys):
        for j, b in enumerate(keys):
            if i == j:
                continue
            common = scores[a].index.intersection(scores[b].index)
            mat[i, j] = stats.spearmanr(scores[a].loc[common], scores[b].loc[common]).statistic
    fig, ax = plt.subplots(figsize=(11, 4.5))
    ax.set_facecolor("#FFFFFF")
    im = ax.imshow(mat, cmap="RdYlGn", vmin=-1, vmax=1, alpha=0.85)
    ax.set_xticks(range(len(keys)), keys, rotation=30, ha="right")
    ax.set_yticks(range(len(keys)), keys)
    ax.set_xticks(np.arange(-0.5, len(keys), 1), minor=True)
    ax.set_yticks(np.arange(-0.5, len(keys), 1), minor=True)
    ax.grid(which="minor", color="#D5DFD2", linestyle="-", linewidth=0.9)
    ax.tick_params(colors=ink_soft, labelsize=15)
    ax.title.set_color(ink)
    ax.title.set_fontsize(21)
    ax.title.set_fontweight("bold")
    for i in range(len(keys)):
        for j in range(len(keys)):
            ax.text(j, i, f"{mat[i, j]:.2f}", ha="center", va="center",
                    fontsize=15, color=ink, fontweight="bold")
    cbar = fig.colorbar(im, ax=ax, label="Spearman rho")
    cbar.ax.yaxis.label.set_color(ink_soft)
    cbar.ax.yaxis.label.set_fontsize(15)
    cbar.ax.tick_params(colors=ink_soft, labelsize=14)
    ax.set_title("Correlation matrix (Spearman)")
    save(fig, "correlation_heatmap.png")

    return paths


# --------------------------------------------------------------------------- #
# Report
# --------------------------------------------------------------------------- #
def write_report(df: pd.DataFrame, tests: pd.DataFrame, corrs: pd.DataFrame,
                 themes: pd.DataFrame, flags: list[str], dups: list[str],
                 chart_paths: list[str], outpath: Path, csv_name: str) -> None:
    n = len(df)
    ages = pd.to_numeric(df[C_AGE], errors="coerce").dropna()
    age_note = (f" {n - len(ages)} non-numeric age response(s) treated as "
                "categorical and excluded." if len(ages) < n else "")
    lines = [
        "# Statistical Analysis — Reimagining the Personal Music Experience",
        "",
        f"**Source:** `{csv_name}`  ",
        f"**Responses:** {n}  ",
        "**Generated by:** `webapp/analysis/analysis.py` (re-run after any CSV update)",
        "",
        "## 1. Data cleaning and quality",
        "",
        f"- {n} responses received; all rows retained in the descriptive analysis.",
        f"- Numeric ages: n={len(ages)}, mean={fmt(ages.mean())}, median={fmt(ages.median(), 0)}, "
        f"SD={fmt(ages.std(ddof=1))}, range={int(ages.min())}-{int(ages.max())}." + age_note,
        "- Ordinal coding: Easy / Very well / Daily = 3; Average / Somewhat / Several times a week = 2; "
        "Difficult / Poorly / Occasionally / Sometimes difficult = 1.",
        "- Neutral comparison value = 2 (the middle category).",
        "",
        "**Flagged low-quality / duplicate responses (declared, not silently removed):**",
        "",
    ]
    lines += [f"- {f}" for f in flags] or ["- None flagged."]
    lines += [f"- Possible duplicate: {d}" for d in dups] or []
    lines += ["", "## 2. Descriptive statistics", ""]

    for col, title in [(C_PLATFORM, "Primary platform"), (C_FREQ, "Usage frequency"),
                       (C_DISCOVER, "Discovery source"), (C_VIBE, "Vibe-finding ease"),
                       (C_SAVE_BEHAVIOUR, "Action after liking a song"),
                       (C_RETRIEVE, "Saved-song retrieval"), (C_TASTE, "Taste understanding")]:
        tbl = value_counts_table(df, col)
        lines += [f"### {title}", "", "| Response | Count | % |", "|---|---:|---:|"]
        lines += [f"| {k} | {int(v.Count)} | {v.Percent:.1f} |" for k, v in tbl.iterrows()]
        lines.append("")

    lines += ["## 3. Ordinal measures, t-tests and 95% confidence intervals", "",
              "H0: mean = 2 (neutral). H1: mean differs from 2. Two-tailed, alpha = 0.05.", "",
              "| Measure | n | Mean | SD | t | df | p | 95% CI |", "|---|---:|---:|---:|---:|---:|---:|---|"]
    for _, r in tests.iterrows():
        lines.append(f"| {r.Measure} | {int(r.n)} | {r.Mean:.2f} | {r.SD:.2f} | {r.t:.3f} | "
                     f"{int(r.df)} | {r.p:.4f} | [{r.CI_low:.2f}, {r.CI_high:.2f}] |")
    lines += ["", "**Interpretation:** positive t-values indicate responses above the neutral midpoint. "
               "Where p < 0.05 the mean is significantly above neutral; where p >= 0.05 there is no "
               "significant difference. Report this honestly — a good-but-not-great baseline is still a "
               "valid finding.", ""]

    lines += ["## 4. Correlations (Pearson and Spearman)", "",
              "| Pair | n | Pearson r | p | Spearman rho | p |", "|---|---:|---:|---:|---:|---:|"]
    for _, r in corrs.iterrows():
        lines.append(f"| {r.A} vs {r.B} | {int(r.n)} | {r.Pearson:+.3f} | {r.p_pearson:.4f} | "
                     f"{r.Spearman:+.3f} | {r.p_spearman:.4f} |")
    df_r = n - 2
    t_crit = stats.t.ppf(0.975, df_r)
    crit = t_crit / math.sqrt(t_crit ** 2 + df_r)
    lines += ["", f"Critical |r| at n≈{n}, alpha=0.05 (two-tailed) ≈ {crit:.3f}. "
               "Associations below this are weak and statistically non-significant — describe them as "
               "directional only.", ""]

    lines += ["## 5. Open-text themes", "",
              "| Theme | Respondents | % |", "|---|---:|---:|"]
    for _, r in themes.iterrows():
        lines.append(f"| {r.Theme} | {int(r.Respondents)} | {r.Percent:.1f} |")
    lines += ["", "## 6. Charts", ""]
    lines += [f"![{Path(p).stem}]({Path(p).name})" for p in chart_paths]
    lines += ["", "---", "", "*Regenerate with:* `python3 webapp/analysis/analysis.py --csv <updated.csv>`"]

    outpath.write_text("\n".join(lines) + "\n", encoding="utf-8")


# --------------------------------------------------------------------------- #
def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--csv", required=True, help="Path to the Google Forms CSV export")
    ap.add_argument("--outdir", default=str(Path(__file__).resolve().parents[2] / "data"))
    ap.add_argument("--report", default=str(Path(__file__).resolve().parents[2] / "docs" / "statistical_results.md"))
    args = ap.parse_args()

    csv_path = Path(args.csv)
    outdir = Path(args.outdir)
    report_path = Path(args.report)
    outdir.mkdir(parents=True, exist_ok=True)
    report_path.parent.mkdir(parents=True, exist_ok=True)

    df = pd.read_csv(csv_path)
    anonymised = anonymise(df, outdir / "survey_responses_anonymised.csv")
    scores = ordinal_scores(df)
    tests = one_sample_tests(scores)
    corrs = correlation_table(scores)
    themes = theme_counts(df)
    flags = quality_flags(df)
    dups = duplicate_names(df)
    charts = make_charts(df, scores, outdir / "charts")
    write_report(df, tests, corrs, themes, flags, dups, charts, report_path, csv_path.name)

    print(f"Analysed {len(df)} responses.")
    print(f"Anonymised CSV : {outdir / 'survey_responses_anonymised.csv'}")
    print(f"Report         : {report_path}")
    print(f"Charts         : {len(charts)} PNGs in {outdir / 'charts'}")
    print("\nBaseline tests:")
    print(tests[["Measure", "Mean", "SD", "t", "p", "CI_low", "CI_high"]].to_string(index=False))
    print("\nThemes:")
    print(themes.to_string(index=False))


if __name__ == "__main__":
    main()
