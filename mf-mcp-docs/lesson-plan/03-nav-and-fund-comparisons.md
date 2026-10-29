# Lesson 3: Compare fund performance

[Previous lesson](02-aum-and-flows.md) | [Course overview](README.md) | [Next lesson](04-indices-equities-and-risk.md)

## Question and outcomes

Two funds report different returns. Before you compare them, check which plans, options, and observation windows those figures describe.

After this lesson, you can resolve exact plan codes, interpret NAV metrics, and identify an unfair performance comparison.

Prerequisite: lessons 1–2 and access to NAV observations. Allow about 75 minutes.

## Concepts to learn

NAV is the unit value of a mutual fund. A higher NAV does not mean a fund is more expensive in the stock-valuation sense, or that it has performed better. You need the change over a stated interval.

Direct and Regular plans can have different expenses. Growth and distribution options treat payouts differently. Raw NAV is not distribution-adjusted, so a distribution-option NAV change is not a complete investor return. This course uses verified Direct Growth plans to reduce, not eliminate, comparison problems.

CAGR describes an annualized growth rate between endpoints. Volatility measures variability, not the worst loss. Sharpe compares excess return with volatility under a stated risk-free-rate convention. Maximum drawdown measures the deepest peak-to-trough decline within the selected window; current drawdown measures the endpoint's distance below that window's peak. Neither promises a future loss limit.

For `get_nav_metrics`, CAGR uses elapsed calendar days; Sharpe uses consecutive-observation returns and 252-observation annualization. Drawdowns are nonpositive fractions. Missing days are not filled. A null Sharpe is not a zero Sharpe.

## Guided lab

1. Choose two funds from a broadly comparable category. Use short `get_amfi_scheme_aum` searches to inspect exact names and codes in its latest report. Verify Direct Growth identity; do not let the agent choose a code from a generic fund name.
2. Inspect each plan's NAV coverage. Use targeted `list_nav_schemes` only if needed; broad historical catalog scans can be slow, and its representative name is not necessarily the latest official name.
3. Select an explicit shared covered window and annual fractional risk-free assumption before seeing the comparison. A zero assumption is acceptable for this exercise if you label it as an assumption, not an observed cash return.
4. Call `get_nav_metrics` with both actual codes. Inspect per-scheme statuses, actual first/last observations, clamping, and warnings. Identical requested dates do not guarantee identical observed dates.
5. If observed boundaries differ, find a defensible common window and rerun, or explain why you decline a direct ranking.
6. Save a comparison card with CAGR, Sharpe, maximum and current drawdown, observed coverage, and limitations. Use code for percent display and differences.

Paste this prompt:

```text
Help me compare two specified mutual funds as a research exercise. First resolve
and show their actual Direct Growth plan names and codes using targeted
get_amfi_scheme_aum searches; ask me to confirm any ambiguous plan. Establish a
shared covered window and state the annual fractional risk-free assumption before
calling get_nav_metrics. Report actual boundaries, per-scheme statuses, CAGR,
Sharpe, maximum/current drawdowns, and warnings. Explain differences in metrics
without declaring a personalized investment recommendation. Do not treat absent
values as zero or a NAV level as a valuation ranking.
```

## Independent exercise

Ask the agent to repeat the comparison over a second, shorter covered window chosen before viewing its results. Does the ordering change? If it does not, explain why two windows still do not prove a permanent advantage. Record the window-selection rule so the exercise is not a search for a flattering start date.

Write one sentence each about taxes, exit loads, and investor cash-flow timing that these NAV metrics do not capture as your personal realized return. Do not subtract a guessed expense ratio from NAV returns: plan expenses are generally reflected in NAV, while investor-specific costs require separate treatment.

## Completion check

Submit the comparison card and sensitivity note. You pass when another learner can identify the precise plans and windows, interpret a negative drawdown, and explain why the larger CAGR alone does not settle an investment decision.

Optional programming task: after lesson 7, export full NAV histories and reproduce endpoint return and window drawdown with explicit duplicate-date validation. Raw NAV history and the metrics tool have different duplicate policies; do not silently drop conflicting values. State your formula and actual observation dates.

## Reading

Read [NAV metrics and conventions](../samples/mcp-service-tool-samples.md#tool-get_nav_metrics), [NAV discovery](../samples/mcp-service-tool-samples.md#tool-list_nav_schemes), and [raw NAV history](../samples/mcp-service-tool-samples.md#tool-get_nav_history).
