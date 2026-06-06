# Counterfactual Valuation Simulator

A simple Python model that shows how **implied valuation** changes when investors reweight possible futures after new information arrives.

This is not a trading model. It is an investment reasoning tool: valuation as a probability-weighted sum of scenario outcomes.

## Core idea

A stock (or any asset) can be thought of as a distribution over future states. Each state has:

- a **scenario value** — what the asset might be worth if that future unfolds
- a **probability weight** — how credible that future seems today

The implied price at any moment is:

```
Implied Price = Σ (Probability_i × Value_i)
```

When new information arrives, investors do not always change fundamentals immediately. They often **reweight probabilities** across scenarios. This model tracks how that reweighting moves implied valuation through time.

## Scenarios

| Scenario | Value | Interpretation |
|---|---:|---|
| AI Supercycle | 260 | Major productivity cycle; monetisation exceeds expectations |
| Strong Adoption | 180 | Commercially strong adoption; capex earns attractive returns |
| Gradual Adoption | 110 | Useful AI, but slower adoption and monetisation |
| Overbuild | 70 | Infrastructure spending outruns economic returns |
| Disappointment | 35 | Adoption, pricing, regulation, or competition disappoint |

## Information stages

The model steps through four belief states:

| Stage | Event |
|---|---|
| T0 — Initial view | Starting balanced probability distribution |
| T1 — Adoption signal | Positive demand / customer adoption news |
| T2 — Capex risk | Negative capex / ROI concern |
| T3 — Monetisation | Positive early monetisation evidence |

At each stage, probabilities shift. Implied price is recalculated from the updated weights.

## Quick start

**Requirements:** Python 3.10+

```bash
cd "Counterfactuals market simulation"
pip install -r requirements.txt
python run_simulation.py
```

The script prints tables to the terminal and opens three charts. Outputs are also saved to `outputs/`.

## Outputs

### CSV files

| File | Description |
|---|---|
| `scenario_values.csv` | Scenario names, values, and interpretations |
| `probability_sets.csv` | Probability weights at each information stage |
| `implied_prices.csv` | Implied valuation and % change vs initial |
| `scenario_contributions.csv` | Per-scenario contribution to implied price |

### Charts

| File | Description |
|---|---|
| `implied_valuation_by_stage.png` | Implied price path across information stages |
| `probability_weights_by_stage.png` | How scenario probabilities evolve |
| `scenario_contributions.png` | Stacked contribution of each scenario to valuation |

## Project structure

```
.
├── run_simulation.py   # Main script: data, calculations, charts
├── requirements.txt    # Python dependencies
├── outputs/            # Generated CSVs and PNGs (gitignored)
└── README.md
```

## Customisation

Edit the inputs at the top of `run_simulation.py`:

- **`scenarios`** — change scenario names, values, or interpretations
- **`probability_sets`** — change how beliefs shift at each information stage

Probabilities in each column must sum to `1.0`. The script validates this before running.

Chart styling (colors, fonts, labels) is defined in the `THEME` and `SCENARIO_COLORS` blocks at the top of the same file.

## Example results

With the default inputs:

| Stage | Implied Price | Change vs Initial |
|---|---:|---:|
| Initial view | $127.00 | 0.0% |
| After adoption signal | $145.90 | +14.9% |
| After capex concern | $134.80 | +6.1% |
| After monetisation evidence | $154.85 | +21.9% |

Valuation rises on positive signals, pulls back on capex concern, and ends highest after monetisation evidence — even though underlying scenario values never change. Only beliefs move.

## License

MIT
