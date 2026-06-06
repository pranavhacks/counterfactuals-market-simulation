# Counterfactual Valuation Simulator

A simple Python model showing how implied valuation changes when investors reweight possible futures after new information arrives.

This is not a trading model. It is an investment reasoning tool: valuation as a probability-weighted sum of scenario outcomes.

## Core idea

A stock, or any financial asset, can be thought of as a distribution over future states. Each state has:

- a **scenario value**: what the asset is worth today if that future unfolds
- a **probability weight**: how credible that future seems today

The implied valuation at any moment is:

```text
Implied Valuation = Σ (Probability_i × Value_i)
