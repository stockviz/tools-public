# Lesson 5: Audit a strategy

[Previous lesson](04-indices-equities-and-risk.md) | [Course overview](README.md) | [Next lesson](06-dashboard-research.md)

## Question and outcomes

A strategy's historical chart looks attractive. What rules produced it, and what information would you need before believing it could have been traded?

After this lesson, you can trace a published strategy to its explicitly linked backtest, compare compatible evidence, and distinguish unavailable decision history from an explanation invented after the event.

Prerequisite: lessons 3–4. Allow about 60 minutes.

## Concepts to learn

A backtest applies rules to historical data. It is not an executed track record. Fees, turnover, trading timing, data revisions, and selection choices can change the interpretation.

_Look-ahead bias_ uses information unavailable at a decision time. _Survivorship bias_ omits failed or disappeared instruments. _Overfitting_ selects rules that fit the observed sample rather than a repeatable effect. If you test your own ideas, freeze choices on a training period before inspecting a later holdout. Choosing today's winners and looking backward is a descriptive exercise, not evidence of a historical selection method.

A published current portfolio does not establish historical holdings, fills, or your account exposure. An attractive metric cannot fill in missing trading rules.

## Guided lab

1. Call `list_strategies`. Select an actual published ID, then retrieve its definition and current model portfolio.
2. Resolve `get_strategy_backtest` for that strategy. Use the explicit linked run; do not substitute the newest or a similarly named run. Missing linkage is an audit finding.
3. Retrieve `get_backtest_summary`. Inspect metric status, provenance, observed series, and coverage.
4. If sufficient observations exist, choose an explicit subwindow and use `get_backtest_metrics` with the actual run ID and exact series labels. Bounds select entire monthly returns by period-end date; they do not prorate months.
5. Optional: use `compare_strategies` for two discovered run IDs. Its `comparable` flag means summaries exist, not that dates, fees, risks, or methods match. Check those yourself. Recalculate shared windows where possible, while retaining methodology differences.
6. Request `explain_signal` for a discovered strategy and an explicit date. The source documentation says archived decision-time inputs are unavailable and this tool returns `data_gap`. Record the actual response without inventing a trade explanation.

Paste this prompt:

```text
Audit one published StockViz strategy. Discover its ID, retrieve exact rules and
the current model portfolio, and resolve its explicit backtest link. Inspect the
linked summary and, if supported by coverage, one preselected subwindow using
get_backtest_metrics. Separate documented rules, calculated evidence, and missing
information. Check costs, execution timing, universe/classification history, and
selection/holdout provenance; mark anything undocumented as unknown. Request an
archived explanation through explain_signal but do not reconstruct missing
signals from later realized returns. Do not treat the model as my holdings.
```

## Independent exercise

Create an audit table with rows for rules, decision-time inputs, trade timing, costs, benchmark, sample dates, holdout provenance, and live execution evidence. For each, mark `documented`, `not documented`, or `unavailable` and give an evidence reference.

Then rewrite "This strategy will outperform" as a claim your table can support. A valid conclusion may be that published metrics are available but execution realism cannot be established.

## Completion check

Submit the audit table and a cautious conclusion. You pass when you distinguish strategy IDs from run IDs, explain the monthly metrics' zero-risk-free and 12-observation annualization conventions, and do not compare them directly with daily NAV Sharpe as if methods were identical.

Optional programming task: write a validation specification for a future backtest. Define what is known at close t, when the next trade can occur, and how fees and missing data are handled. Do not claim those rules describe the published strategy unless its definition says so.

## Reading

Read [strategy discovery](../samples/mcp-service-tool-samples.md#tool-list_strategies), [explicit backtest linkage](../samples/mcp-service-tool-samples.md#tool-get_strategy_backtest), [comparison limits](../samples/mcp-service-tool-samples.md#tool-compare_strategies), [monthly metric conventions](../samples/mcp-service-tool-samples.md#tool-get_backtest_metrics), and [signal limitations](../samples/mcp-service-tool-samples.md#tool-explain_signal).
