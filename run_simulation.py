import os

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.ticker import FuncFormatter

# ------------------------------------------------------------
# Chart theme — light institutional / Google-tech aesthetic
# ------------------------------------------------------------

THEME = {
    "bg": "#ffffff",
    "panel": "#f8f9fb",
    "grid": "#e6eaf0",
    "border": "#d5dbe5",
    "text": "#1b2430",
    "muted": "#5f6b7a",
    "accent": "#1a73e8",
    "accent_soft": "#d2e3fc",
    "positive": "#137333",
    "negative": "#c5221f",
}

SCENARIO_COLORS = {
    "AI Supercycle": "#1a73e8",
    "Strong Adoption": "#137333",
    "Gradual Adoption": "#e37400",
    "Overbuild": "#9334e6",
    "Disappointment": "#c5221f",
}

STAGE_LABELS = {
    "Initial view": "T0  Initial",
    "After adoption signal": "T1  Adoption",
    "After capex concern": "T2  Capex risk",
    "After monetisation evidence": "T3  Monetisation",
}


def setup_style() -> None:
    plt.rcParams.update(
        {
            "figure.facecolor": THEME["bg"],
            "axes.facecolor": THEME["panel"],
            "axes.edgecolor": THEME["border"],
            "axes.labelcolor": THEME["muted"],
            "axes.titleweight": 600,
            "axes.titlesize": 13,
            "axes.labelsize": 10,
            "xtick.color": THEME["muted"],
            "ytick.color": THEME["muted"],
            "text.color": THEME["text"],
            "font.family": "sans-serif",
            "font.sans-serif": [
                "Inter",
                "Roboto",
                "Helvetica Neue",
                "Arial",
                "DejaVu Sans",
            ],
            "grid.color": THEME["grid"],
            "grid.linewidth": 0.8,
            "legend.facecolor": THEME["bg"],
            "legend.edgecolor": THEME["bg"],
            "legend.labelcolor": THEME["text"],
            "figure.dpi": 120,
            "savefig.facecolor": THEME["bg"],
            "savefig.edgecolor": THEME["bg"],
        }
    )


def style_axes(ax, *, title: str, subtitle: str | None = None) -> None:
    ax.set_title(title, loc="left", color=THEME["text"], pad=20, fontsize=13, fontweight=600)
    if subtitle:
        ax.text(
            0.0,
            1.03,
            subtitle,
            transform=ax.transAxes,
            fontsize=9,
            color=THEME["muted"],
            va="bottom",
        )
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_color(THEME["border"])
    ax.spines["bottom"].set_color(THEME["border"])
    ax.spines["left"].set_linewidth(0.8)
    ax.spines["bottom"].set_linewidth(0.8)
    ax.grid(True, axis="y", alpha=0.9)
    ax.set_axisbelow(True)
    ax.tick_params(axis="both", length=0, pad=8)


def label_color_for_bar(hex_color: str) -> str:
    rgb = tuple(int(hex_color.strip("#")[i : i + 2], 16) / 255 for i in (0, 2, 4))
    luminance = 0.2126 * rgb[0] + 0.7152 * rgb[1] + 0.0722 * rgb[2]
    return THEME["bg"] if luminance < 0.62 else THEME["text"]


def format_stage_labels(stages: list[str]) -> list[str]:
    return [STAGE_LABELS.get(stage, stage) for stage in stages]


def save_figure(fig, path: str) -> None:
    fig.savefig(path, dpi=300, bbox_inches="tight", facecolor=fig.get_facecolor())
    print(f"Saved chart: {path}")

# ------------------------------------------------------------
# Counterfactual Valuation Simulator
# ------------------------------------------------------------
# Purpose:
# Show how valuation changes when investors reweight possible futures
# after new information arrives.
#
# This is not a trading model. It is a simple investment reasoning model.
# ------------------------------------------------------------

OUTPUT_DIR = "outputs"
os.makedirs(OUTPUT_DIR, exist_ok=True)


# ------------------------------------------------------------
# 1. Define scenario values
# ------------------------------------------------------------

scenarios = pd.DataFrame({
    "Scenario": [
        "AI Supercycle",
        "Strong Adoption",
        "Gradual Adoption",
        "Overbuild",
        "Disappointment"
    ],
    "Value": [260, 180, 110, 70, 35],
    "Interpretation": [
        "AI creates a major productivity cycle and monetisation exceeds expectations.",
        "AI adoption is commercially strong and capex produces attractive returns.",
        "AI is useful, but adoption and monetisation are gradual.",
        "Infrastructure spending rises faster than economic returns.",
        "Adoption, pricing power, regulation, or competition disappoints sharply."
    ]
})


# ------------------------------------------------------------
# 2. Define probability distributions over time
# ------------------------------------------------------------

probability_sets = pd.DataFrame({
    "Scenario": scenarios["Scenario"],

    # Initial balanced view
    "Initial view": [0.10, 0.25, 0.35, 0.20, 0.10],

    # Positive event: stronger demand / customer adoption
    "After adoption signal": [0.16, 0.32, 0.31, 0.15, 0.06],

    # Negative event: capex concern / return on investment worry
    "After capex concern": [0.13, 0.27, 0.33, 0.19, 0.08],

    # Positive event: early monetisation evidence
    "After monetisation evidence": [0.20, 0.34, 0.28, 0.13, 0.05]
})

# Check probabilities sum to 1
for col in probability_sets.columns[1:]:
    assert np.isclose(probability_sets[col].sum(), 1.0), f"{col} does not sum to 1"


# ------------------------------------------------------------
# 3. Calculate implied valuation at each stage
# ------------------------------------------------------------

def implied_price(values, probabilities):
    return float(np.sum(values * probabilities))


values = scenarios["Value"].to_numpy(dtype=float)

stage_names = probability_sets.columns[1:].tolist()

price_results = []

for stage in stage_names:
    probs = probability_sets[stage].to_numpy(dtype=float)
    price = implied_price(values, probs)
    price_results.append({
        "Stage": stage,
        "Implied Price": price
    })

price_df = pd.DataFrame(price_results)
price_df["Change vs Initial"] = price_df["Implied Price"] / price_df["Implied Price"].iloc[0] - 1

print("\nScenario values:")
print(scenarios[["Scenario", "Value"]])

print("\nProbability distributions:")
print(probability_sets)

print("\nImplied valuation by stage:")
print(price_df)


# ------------------------------------------------------------
# 4. Contribution table
# ------------------------------------------------------------
# This shows how much each scenario contributes to the final valuation.

contribution_table = probability_sets.copy()

for stage in stage_names:
    contribution_table[f"{stage} contribution"] = (
        contribution_table[stage] * scenarios["Value"]
    )

print("\nScenario contribution table:")
print(contribution_table)

# Save tables
scenarios.to_csv(os.path.join(OUTPUT_DIR, "scenario_values.csv"), index=False)
probability_sets.to_csv(os.path.join(OUTPUT_DIR, "probability_sets.csv"), index=False)
price_df.to_csv(os.path.join(OUTPUT_DIR, "implied_prices.csv"), index=False)
contribution_table.to_csv(os.path.join(OUTPUT_DIR, "scenario_contributions.csv"), index=False)


setup_style()

# ------------------------------------------------------------
# 5. Chart 1: Implied valuation by stage
# ------------------------------------------------------------

x = np.arange(len(price_df))
prices = price_df["Implied Price"].to_numpy()
stage_labels = format_stage_labels(price_df["Stage"].tolist())
baseline = prices[0]

fig, ax = plt.subplots(figsize=(10, 5.5))
fig.patch.set_facecolor(THEME["bg"])

ax.fill_between(
    x,
    prices,
    baseline,
    color=THEME["accent"],
    alpha=0.10,
    interpolate=True,
)
ax.axhline(
    baseline,
    color=THEME["border"],
    linestyle=(0, (4, 4)),
    linewidth=1.1,
    zorder=1,
)
ax.plot(
    x,
    prices,
    color=THEME["accent"],
    linewidth=2.2,
    marker="o",
    markersize=7,
    markerfacecolor=THEME["bg"],
    markeredgecolor=THEME["accent"],
    markeredgewidth=2,
    zorder=3,
)

for i, row in price_df.iterrows():
    change = row["Change vs Initial"]
    change_color = THEME["positive"] if change >= 0 else THEME["negative"]
    ax.annotate(
        f"${row['Implied Price']:.1f}",
        (i, row["Implied Price"]),
        textcoords="offset points",
        xytext=(0, 12),
        ha="center",
        fontsize=9,
        fontweight=600,
        color=THEME["text"],
    )
    if i > 0:
        ax.annotate(
            f"{change:+.1%}",
            (i, row["Implied Price"]),
            textcoords="offset points",
            xytext=(0, -18),
            ha="center",
            fontsize=8,
            color=change_color,
            fontweight=500,
        )

style_axes(
    ax,
    title="Implied Valuation Across Counterfactual Revisions",
    subtitle="Probability-weighted fair value as beliefs update through new information",
)
ax.set_xticks(x)
ax.set_xticklabels(stage_labels)
ax.set_ylabel("Implied price ($)")
ax.yaxis.set_major_formatter(FuncFormatter(lambda value, _: f"${value:,.0f}"))
ax.set_xlim(-0.25, len(x) - 0.75)
ax.margins(y=0.14)

fig.tight_layout()
path = os.path.join(OUTPUT_DIR, "implied_valuation_by_stage.png")
save_figure(fig, path)
plt.show()


# ------------------------------------------------------------
# 6. Chart 2: Probability weights by stage
# ------------------------------------------------------------

probability_plot = probability_sets.set_index("Scenario")[stage_names].T
x = np.arange(len(stage_names))
stage_labels = format_stage_labels(stage_names)

fig, ax = plt.subplots(figsize=(10.5, 5.8))
fig.patch.set_facecolor(THEME["bg"])

for scenario in probability_plot.columns:
    series = probability_plot[scenario].to_numpy()
    color = SCENARIO_COLORS[scenario]
    ax.plot(
        x,
        series,
        color=color,
        linewidth=2.0,
        marker="o",
        markersize=6,
        markerfacecolor=THEME["bg"],
        markeredgecolor=color,
        markeredgewidth=1.8,
        label=scenario,
        zorder=3,
    )

style_axes(
    ax,
    title="Scenario Probability Weights",
    subtitle="How mass shifts across futures as each information event arrives",
)
ax.set_xticks(x)
ax.set_xticklabels(stage_labels)
ax.set_ylabel("Probability weight")
ax.set_ylim(0, 0.42)
ax.yaxis.set_major_formatter(FuncFormatter(lambda value, _: f"{value:.0%}"))
ax.legend(
    loc="upper center",
    bbox_to_anchor=(0.5, -0.14),
    ncol=3,
    frameon=False,
    fontsize=9,
)

fig.tight_layout()
path = os.path.join(OUTPUT_DIR, "probability_weights_by_stage.png")
save_figure(fig, path)
plt.show()


# ------------------------------------------------------------
# 7. Chart 3: Scenario contributions to valuation
# ------------------------------------------------------------

contribution_plot = pd.DataFrame(index=stage_names, columns=scenarios["Scenario"])

for stage in stage_names:
    contribution_plot.loc[stage] = probability_sets[stage].to_numpy(dtype=float) * values

contribution_plot = contribution_plot.astype(float)

x = np.arange(len(stage_names))
stage_labels = format_stage_labels(stage_names)
bar_width = 0.62

fig, ax = plt.subplots(figsize=(10.5, 5.8))
fig.patch.set_facecolor(THEME["bg"])

bottom = np.zeros(len(contribution_plot))

for scenario in contribution_plot.columns:
    segment = contribution_plot[scenario].to_numpy()
    bar_color = SCENARIO_COLORS[scenario]
    bars = ax.bar(
        x,
        segment,
        bar_width,
        bottom=bottom,
        label=scenario,
        color=bar_color,
        edgecolor=THEME["bg"],
        linewidth=1.4,
        zorder=3,
    )
    for bar, value in zip(bars, segment):
        if value >= 14:
            ax.text(
                bar.get_x() + bar.get_width() / 2,
                bar.get_y() + value / 2,
                f"{value:.0f}",
                ha="center",
                va="center",
                fontsize=8,
                color=label_color_for_bar(bar_color),
                fontweight=600,
            )
    bottom += segment

totals = contribution_plot.sum(axis=1).to_numpy()
for idx, total in enumerate(totals):
    ax.text(
        idx,
        total + 2.5,
        f"${total:.0f}",
        ha="center",
        va="bottom",
        fontsize=9,
        fontweight=600,
        color=THEME["text"],
    )

style_axes(
    ax,
    title="Scenario Contributions to Implied Valuation",
    subtitle="Stacked probability × scenario value at each information stage",
)
ax.set_xticks(x)
ax.set_xticklabels(stage_labels)
ax.set_ylabel("Contribution ($)")
ax.yaxis.set_major_formatter(FuncFormatter(lambda value, _: f"${value:,.0f}"))
ax.legend(
    loc="upper center",
    bbox_to_anchor=(0.5, -0.14),
    ncol=3,
    frameon=False,
    fontsize=9,
)

fig.tight_layout()
path = os.path.join(OUTPUT_DIR, "scenario_contributions.png")
save_figure(fig, path)
plt.show()
