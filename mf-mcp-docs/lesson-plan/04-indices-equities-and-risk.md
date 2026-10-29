# Lesson 4: Read market risk

[Previous lesson](03-nav-and-fund-comparisons.md) | [Course overview](README.md) | [Next lesson](05-strategies-and-backtests.md)

## Question and outcomes

An index delivered the highest return. How much did it fall along the way, and is its return series comparable to the alternatives?

After this lesson, you can distinguish price return from total return, discover exact index names, interpret window risk, and explain why raw equity history needs additional care.

Prerequisite: lesson 3's return and drawdown concepts. Allow about 60 minutes.

## Concepts to learn

An index summarizes a defined basket under a methodology. A price-return index excludes the reinvestment of distributions; a total-return index includes them according to its methodology. Do not rename or convert one into the other because a preferred series is missing. An index is also not directly investable without implementation costs.

Raw stock prices can jump because of splits and other corporate actions. A fall in raw price need not equal an investor's economic loss. Symbol and exchange series together identify the instrument; a symbol alone is insufficient for the equity-history tool.

Risk depends on measurement. Daily and weekly observations can show different maximum drawdowns. A selected-window peak is not necessarily a lifetime high. High past return does not establish a low-risk asset or a forecast.

## Guided lab

1. Use `list_indices` with a targeted search to discover two comparable indices and their coverage. Preserve exact returned names and return conventions.
2. Choose a covered common window. Call `get_index_metrics` with explicit `indices`, `start`, and `end`; do not rely on its configured default selection.
3. Read total return, risk metrics, `FirstValue`, `LatestValue`, `PeakValue`, `PeakDate`, and `CurrentDD` together with the actual window and statuses.
4. Check that the comparison succeeds under the tool's identical-observation-date requirement. If it returns `data_gap`, explain the coverage problem rather than filling prices or dropping one index silently.
5. Discover one equity with `list_equities`; preserve its exact symbol/series pair. Retrieve only a short explicit window with `get_equity_history` and follow every page needed for that window.
6. Write why those raw prices are not sufficient for a long-term total-return backtest.

Paste this prompt:

```text
Discover two comparable StockViz indices using list_indices. Show their exact
names, coverage, and price-return or total-return convention before selecting an
explicit shared window. Call get_index_metrics with both names and report return,
risk, peak/latest dates and values, and current/maximum drawdowns. Explain that
the tool's winner is based on total return, not Sharpe or my risk tolerance.
Separately discover one equity's exact symbol/series pair and retrieve a short
raw-history window. Keep the equity exercise separate from index performance.
Do not invent adjustments, fill gaps, or substitute a different index.
```

## Independent exercise

Write a short response to "The winner is the safest index." Identify what the API's `winner` means and at least one risk measure that could support a different description. Explain why the tool's 252-observation annualization is not the same convention as NAV calendar-day CAGR.

If you download history instead of using metrics, show that all pages succeeded before claiming the window's peak or endpoint. A page-size limit is not a trailing-date selector.

## Completion check

Submit an index risk note plus a raw-price warning. You pass when you preserve return conventions, distinguish current from maximum drawdown, and refuse to interpret an alignment failure as an economic result.

Optional programming task: export index history in lesson 7 and plot a rebased observed-level curve. Label actual dates, return convention, and missing observations. Do not forward-fill to make curves appear comparable.

## Reading

Read [index discovery](../samples/mcp-service-tool-samples.md#tool-list_indices), [index metrics](../samples/mcp-service-tool-samples.md#tool-get_index_metrics), [equity discovery](../samples/mcp-service-tool-samples.md#tool-list_equities), and [raw equity history](../samples/mcp-service-tool-samples.md#tool-get_equity_history).
