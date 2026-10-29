# Lesson 6: Investigate a dashboard

[Previous lesson](05-strategies-and-backtests.md) | [Course overview](README.md) | [Next lesson](07-reproducible-exports.md)

## Question and outcomes

A report contains a useful chart. Does access to its upstream facts mean you can reproduce the chart or the model behind it?

After this lesson, you can discover published datasets, inspect grain and units, form valid filters, and explain the difference between related data and exact report parity.

Prerequisite: lesson 1's metadata checks and lesson 4's risk concepts. Allow about 75 minutes.

## Concepts to learn

Dashboard publication is catalog-driven. A dataset in the source documentation may not be published or populated on your connection. Discover names, column/type pairs, quality, refresh time, and content digest before querying.

`query_dashboard_dataset` supports one entity-column filter and one date-column filter, not SQL, arbitrary predicates, joins, or server-side aggregation. Text entity matching is a literal case-insensitive substring, not equality. Integer entity matching requires an exact canonical decimal string. Apply additional selection in code after retrieving the appropriate bounded data.

`ROW_ID` is a paging key, not rank or economic identity. Numeric database values are text; JSON null is missing, not zero. Default compact return curves are weekly. Filtering them cannot manufacture daily observations or exact daily drawdowns.

## Guided lab

1. Discover PMS datasets with `list_dashboard_datasets`. Inspect current schemas and metadata for `DASHBOARD_PMS_META`, `DASHBOARD_PMS_AUM`, and `DASHBOARD_PMS_MONTHLY` if available.
2. Preview each with a two-row query, explicitly labeling it a preview. Identify the grain: manager identity, manager-month AUM, and manager/strategy-month source occurrences.
3. Select an actual manager from the returned metadata. Confirm `ID` is an advertised integer filter and `AS_OF` a date column in the dated tables. Choose a short covered completed-month window.
4. Retrieve all needed AUM and monthly rows for that manager/window. Pass the manager ID as a string to `entity`; preserve the same dataset, filters, and limit across continuations.
5. Join manager identity on internal `ID`. Preserve `SOURCE_STRATEGY`, `FORMAT`, and null asset labels. Inspect quality and conflicting canonical keys before calculating; do not silently first-wins or sum conflicting records.
6. Explain one observed manager-AUM change and one monthly strategy return, if valid rows permit. These describe different grains. Do not sum strategy AUM into manager AUM or claim report-equivalent Sharpe from a monthly return column.

Paste this prompt:

```text
Use the remote StockViz dashboard catalog to investigate one PMS manager.
Discover the PMS datasets and inspect their live schemas, units, quality,
publication generation, and coverage. Preview rows, then choose one actual
manager ID and a short covered completed-month window. Retrieve all pages needed
for the bounded analysis, join metadata on ID, and retain source strategy names,
format diagnostics, and conflicting observations. Distinguish manager AUM from
strategy AUM and monthly return. Explain which report calculations are absent.
If a required table is unavailable, stop that inference and record the blocker.
```

Example discovery and preview requests:

```json
{"name":"list_dashboard_datasets","arguments":{"search":"PMS","limit":20}}
```

```json
{"name":"query_dashboard_dataset","arguments":{"dataset_name":"DASHBOARD_PMS_MONTHLY","limit":2}}
```

The preview is conditional on catalog publication. It is not a complete sample or evidence that recent rows exist. Query metadata contains the catalog row at `metadata`; schema is `metadata.schema`, while source metadata is nested at `metadata.metadata`.

## Independent exercise

Choose one extension after completing the PMS lab, or use it as a documented alternate if PMS is unavailable:

- Mutual funds: inspect `DASHBOARD_MF_COHORT` and `DASHBOARD_MF_RETURNS`. Explain why the current eligible cohort applied backward is not a historical investable universe.
- US ETFs: inspect `DASHBOARD_ETF_META` and `DASHBOARD_ETF_RETURNS`. Verify currency/units rather than assuming them, and describe current-universe bias.
- Macro: inspect `DASHBOARD_YIELD_CURVE`. Explain why a yield change is not a bond investor's total return.

Discover every dataset first. Save a contract card: name, row grain, valid filters, units, date meanings, source warnings, and one claim the data cannot support. This is a reasoning exercise, not a requirement to scan the entire catalog.

## Completion check

Submit the contract card and bounded analysis with counts and generation metadata. You pass when you can explain substring filtering, restart after a publication change, and identify at least one gap between upstream facts and exact report calculations.

Optional programming task: validate join cardinality before merging. Retain conflicts for inspection instead of making a many-to-many join look like additional independent observations.

## Reading

Read [dashboard query contracts](../samples/mcp-service-tool-samples.md#tool-query_dashboard_dataset), the [PMS worked example](../samples/mcp-service-tool-samples.md#pms-worked-example), and the recipe for your extension in the [report guide](../samples/mcp-service-tool-samples.md#dashboard-report-recipes).
