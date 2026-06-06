# Counterfactual Valuation Simulator

This codebase accompanies my essay on counterfactual thinking in financial markets:

**Counterfactual Thinking in Financial Markets: AI Narratives, Valuation, and the Risk of Persuasive Scenarios**

## What this is

I build a small valuation simulator for an AI-exposed company.

The model starts from a simple idea: a stock price can be thought of as a probability-weighted set of possible futures. Each future has a value, and the market gives each future some probability weight.

The point of the simulator is not to value a real company. It is to show how implied valuation can move when investors reweight possible futures after new information arrives.

In the default setup, the underlying scenario values never change. Only the probability weights move.

That is the whole mechanism.

## Why this matters

Markets rarely move from uncertainty to certainty. More often, they move from one uncertain distribution to another.

A new data point might not prove that an AI supercycle is coming. But it can make investors give more weight to that possibility. A capex concern might not kill the bull case. But it can shift weight back toward overbuild or disappointment.

This simulator makes that process visible.

## Model

The model uses five possible future states:

| Scenario | Value | Interpretation |
|---|---:|---|
| AI Supercycle | 260 | Major productivity cycle; monetisation exceeds expectations |
| Strong Adoption | 180 | Commercially strong adoption; capex earns attractive returns |
| Gradual Adoption | 110 | Useful AI, but slower adoption and monetisation |
| Overbuild | 70 | Infrastructure spending outruns economic returns |
| Disappointment | 35 | Adoption, pricing, regulation, or competition disappoints |

At each information stage, the model calculates:

```text
Implied Valuation = Σ (Probability_i × Value_i)
```

## Information stages

The simulation follows four stages:

| Stage | Interpretation |
|---|---|
| T0 — Initial view | Balanced starting distribution |
| T1 — Adoption signal | Positive evidence around demand or usage |
| T2 — Capex risk | Concern that infrastructure spending may outrun returns |
| T3 — Monetisation evidence | Early signs that usage is turning into revenue, pricing power, or operating leverage |

At each stage, the probabilities across the five scenarios are updated. The scenario values stay fixed.

## Example result

With the default inputs:

| Stage | Implied Valuation | Change vs Initial |
|---|---:|---:|
| Initial view | 127.00 | 0.0% |
| After adoption signal | 145.90 | +14.9% |
| After capex concern | 134.80 | +6.1% |
| After monetisation evidence | 154.85 | +21.9% |

The valuation rises, falls, and rises again even though the underlying scenario values never change. Only the probability weights move.

## What the script does

`run_simulation.py`:

1. defines five future states and assigns each one a fixed present value
2. defines probability weights across four information stages
3. calculates implied valuation at each stage
4. decomposes valuation into per-scenario contributions
5. saves charts and CSV outputs to `outputs/`

There are no random shocks in the model. That is deliberate. The goal is not to imitate market noise, but to isolate the effect of belief revision.

## Outputs

The script saves:

```text
outputs/
├── scenario_values.csv
├── probability_sets.csv
├── implied_prices.csv
├── scenario_contributions.csv
├── implied_valuation_by_stage.png
├── probability_weights_by_stage.png
└── scenario_contributions.png
```

The three charts show:

- implied valuation across information stages
- probability weights across scenarios
- scenario contributions to total implied valuation

## Setup

```bash
pip install -r requirements.txt
```

## Run

```bash
python run_simulation.py
```

The script prints the main tables to the terminal and saves the outputs to `outputs/`.

## Customisation

Edit the inputs at the top of `run_simulation.py`.

Change `scenarios` to adjust the future states, values, or interpretations.

Change `probability_sets` to adjust how beliefs shift across information stages.

Each probability column must sum to `1.0`. The script checks this before running.

## Project structure

```text
.
├── run_simulation.py
├── requirements.txt
├── outputs/
└── README.md
```

## Note

This is a stylised model, not an investment recommendation or fair value estimate.

The point is narrower: to show how counterfactual reweighting can move implied valuation before the future is resolved.
