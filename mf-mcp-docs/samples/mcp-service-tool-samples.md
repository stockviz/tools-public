# StockViz MCP tool samples and dashboard report guide

This guide covers the remote StockViz mutual-fund MCP service at
`https://mutual-fund-mcp.stockviz.workers.dev/mcp`. It documents every tool advertised
by the deployed service, including AMFI datasets and analytics, NAV and market
histories, published strategy research, and dashboard datasets behind the reports
website. The dashboard recipes cover all producer-defined datasets; discovery
still determines which publications and sources are available when you call.

## Table of contents

- [Using the examples](#using-the-examples)
- [Pagination and data quality](#pagination-and-data-quality)
- [Dashboard tool reference](#remote-tool-reference)
  - [`list_dashboard_datasets`](#tool-list_dashboard_datasets)
  - [`query_dashboard_dataset`](#tool-query_dashboard_dataset)
- [AMFI, market history, and strategy tools](#non-dashboard-tools)
  - [`get_amfi_datasets`](#tool-get_amfi_datasets)
  - [`get_amfi_monthly_stats`](#tool-get_amfi_monthly_stats)
  - [`search_amfi_scheme_classification`](#tool-search_amfi_scheme_classification)
  - [`get_amfi_fund_aum`](#tool-get_amfi_fund_aum)
  - [`get_amfi_scheme_aum`](#tool-get_amfi_scheme_aum)
  - [`get_amfi_category_aum`](#tool-get_amfi_category_aum)
  - [`get_amfi_aum_ranking`](#tool-get_amfi_aum_ranking)
  - [`get_amfi_aum_growth`](#tool-get_amfi_aum_growth)
  - [`get_amfi_category_aum_history`](#tool-get_amfi_category_aum_history)
  - [`query_amfi_flows`](#tool-query_amfi_flows)
  - [`get_nav_metrics`](#tool-get_nav_metrics)
  - [`list_equities`](#tool-list_equities)
  - [`get_equity_history`](#tool-get_equity_history)
  - [`list_indices`](#tool-list_indices)
  - [`get_index_history`](#tool-get_index_history)
  - [`list_nav_schemes`](#tool-list_nav_schemes)
  - [`get_nav_history`](#tool-get_nav_history)
  - [`list_strategies`](#tool-list_strategies)
  - [`get_strategy_definition`](#tool-get_strategy_definition)
  - [`get_strategy_portfolio`](#tool-get_strategy_portfolio)
  - [`get_strategy_backtest`](#tool-get_strategy_backtest)
  - [`search_backtests`](#tool-search_backtests)
  - [`compare_strategies`](#tool-compare_strategies)
  - [`get_backtest_summary`](#tool-get_backtest_summary)
  - [`get_backtest_metrics`](#tool-get_backtest_metrics)
  - [`get_index_metrics`](#tool-get_index_metrics)
  - [`get_data_quality`](#tool-get_data_quality)
  - [`explain_signal`](#tool-explain_signal)
- [Dashboard report recipes](#dashboard-report-recipes)
  - [Worked PMS report example](#pms-worked-example)
  - [Report-to-dataset coverage](#report-to-dataset-coverage)
  - [`DASHBOARD_BROKER_NARRATIVES`](#dataset-DASHBOARD_BROKER_NARRATIVES)
  - [`DASHBOARD_BROKER_TIMELINE`](#dataset-DASHBOARD_BROKER_TIMELINE)
  - [`DASHBOARD_CME_FRONT_CONTRACT`](#dataset-DASHBOARD_CME_FRONT_CONTRACT)
  - [`DASHBOARD_COMPOSITION_CHANGE`](#dataset-DASHBOARD_COMPOSITION_CHANGE)
  - [`DASHBOARD_CONSTITUENT_VALUATION`](#dataset-DASHBOARD_CONSTITUENT_VALUATION)
  - [`DASHBOARD_COUNTRY_ETF_REFERENCE`](#dataset-DASHBOARD_COUNTRY_ETF_REFERENCE)
  - [`DASHBOARD_DISPERSION`](#dataset-DASHBOARD_DISPERSION)
  - [`DASHBOARD_EARNINGS_CALENDAR`](#dataset-DASHBOARD_EARNINGS_CALENDAR)
  - [`DASHBOARD_EQUITY_NARRATIVES`](#dataset-DASHBOARD_EQUITY_NARRATIVES)
  - [`DASHBOARD_EQUITY_STREAK`](#dataset-DASHBOARD_EQUITY_STREAK)
  - [`DASHBOARD_EQUITY_TECHNICAL`](#dataset-DASHBOARD_EQUITY_TECHNICAL)
  - [`DASHBOARD_EQUITY_UNIVERSE`](#dataset-DASHBOARD_EQUITY_UNIVERSE)
  - [`DASHBOARD_EQ_IN_FINANCIALS`](#dataset-DASHBOARD_EQ_IN_FINANCIALS)
  - [`DASHBOARD_EQ_IN_FREE_FLOAT`](#dataset-DASHBOARD_EQ_IN_FREE_FLOAT)
  - [`DASHBOARD_EQ_IN_MARGIN`](#dataset-DASHBOARD_EQ_IN_MARGIN)
  - [`DASHBOARD_EQ_IN_MTF`](#dataset-DASHBOARD_EQ_IN_MTF)
  - [`DASHBOARD_EQ_IN_OWNERSHIP`](#dataset-DASHBOARD_EQ_IN_OWNERSHIP)
  - [`DASHBOARD_EQ_IN_RETURNS`](#dataset-DASHBOARD_EQ_IN_RETURNS)
  - [`DASHBOARD_ETF_CAPM`](#dataset-DASHBOARD_ETF_CAPM)
  - [`DASHBOARD_ETF_COHORT`](#dataset-DASHBOARD_ETF_COHORT)
  - [`DASHBOARD_ETF_CONSTITUENTS`](#dataset-DASHBOARD_ETF_CONSTITUENTS)
  - [`DASHBOARD_ETF_META`](#dataset-DASHBOARD_ETF_META)
  - [`DASHBOARD_ETF_REGRESSION`](#dataset-DASHBOARD_ETF_REGRESSION)
  - [`DASHBOARD_ETF_RETURNS`](#dataset-DASHBOARD_ETF_RETURNS)
  - [`DASHBOARD_ETF_RISK`](#dataset-DASHBOARD_ETF_RISK)
  - [`DASHBOARD_FF_DEFS`](#dataset-DASHBOARD_FF_DEFS)
  - [`DASHBOARD_FF_REGRESSION`](#dataset-DASHBOARD_FF_REGRESSION)
  - [`DASHBOARD_FF_RETURNS`](#dataset-DASHBOARD_FF_RETURNS)
  - [`DASHBOARD_INDEX_MEMBERSHIP`](#dataset-DASHBOARD_INDEX_MEMBERSHIP)
  - [`DASHBOARD_INDEX_RETURNS`](#dataset-DASHBOARD_INDEX_RETURNS)
  - [`DASHBOARD_INDEX_RISK`](#dataset-DASHBOARD_INDEX_RISK)
  - [`DASHBOARD_INDUSTRY_FUNDAMENTALS`](#dataset-DASHBOARD_INDUSTRY_FUNDAMENTALS)
  - [`DASHBOARD_INDUSTRY_MEMBERS`](#dataset-DASHBOARD_INDUSTRY_MEMBERS)
  - [`DASHBOARD_INDUSTRY_NARRATIVES`](#dataset-DASHBOARD_INDUSTRY_NARRATIVES)
  - [`DASHBOARD_INDUSTRY_STATISTICS`](#dataset-DASHBOARD_INDUSTRY_STATISTICS)
  - [`DASHBOARD_MARKET_DISTRIBUTION`](#dataset-DASHBOARD_MARKET_DISTRIBUTION)
  - [`DASHBOARD_MARKET_HORIZON`](#dataset-DASHBOARD_MARKET_HORIZON)
  - [`DASHBOARD_MARKET_RISK`](#dataset-DASHBOARD_MARKET_RISK)
  - [`DASHBOARD_MARKET_SERIES`](#dataset-DASHBOARD_MARKET_SERIES)
  - [`DASHBOARD_MARKET_SMA`](#dataset-DASHBOARD_MARKET_SMA)
  - [`DASHBOARD_METRIC_DICTIONARY`](#dataset-DASHBOARD_METRIC_DICTIONARY)
  - [`DASHBOARD_MF_CAPM`](#dataset-DASHBOARD_MF_CAPM)
  - [`DASHBOARD_MF_COHORT`](#dataset-DASHBOARD_MF_COHORT)
  - [`DASHBOARD_MF_REGRESSION`](#dataset-DASHBOARD_MF_REGRESSION)
  - [`DASHBOARD_MF_RETURNS`](#dataset-DASHBOARD_MF_RETURNS)
  - [`DASHBOARD_OPTION_IV`](#dataset-DASHBOARD_OPTION_IV)
  - [`DASHBOARD_OPTION_POSITIONING`](#dataset-DASHBOARD_OPTION_POSITIONING)
  - [`DASHBOARD_PMS_AUM`](#dataset-DASHBOARD_PMS_AUM)
  - [`DASHBOARD_PMS_META`](#dataset-DASHBOARD_PMS_META)
  - [`DASHBOARD_PMS_MONTHLY`](#dataset-DASHBOARD_PMS_MONTHLY)
  - [`DASHBOARD_REALIZED_VOL`](#dataset-DASHBOARD_REALIZED_VOL)
  - [`DASHBOARD_VALUATION`](#dataset-DASHBOARD_VALUATION)
  - [`DASHBOARD_VIX`](#dataset-DASHBOARD_VIX)
  - [`DASHBOARD_VIX_FORWARD_SAMPLE`](#dataset-DASHBOARD_VIX_FORWARD_SAMPLE)
  - [`DASHBOARD_YIELD_CURVE`](#dataset-DASHBOARD_YIELD_CURVE)
- [Exporting with mcp-consumer](#exporting-with-mcp-consumer)
- [Verification and scope](#verification-and-scope)

<a id="using-the-examples"></a>
## Using the examples

The JSON blocks below are parameters for the MCP `tools/call` method, not HTTP
request bodies by themselves. Pass them through an initialized MCP client. For
example, a complete JSON-RPC message wraps the same parameters as follows:

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "tools/call",
  "params": {
    "name": "list_dashboard_datasets",
    "arguments": {"search": "PMS", "limit": 20}
  }
}
```

Protocol initialization and tool discovery are public. Every tool invocation
requires a valid authenticated user token with `research:read`; discovery is not
permission to invoke tools anonymously. Use your MCP client's OAuth sign-in flow.
Do not paste credentials or access/refresh tokens into tool arguments.

All tools in this guide are research reads. A strategy portfolio is a published
model portfolio, not an account's private holdings. These tools do not place orders,
modify portfolios, or accept arbitrary SQL.

Argument tables distinguish mandatory arguments from optional ones. Omit optional
arguments unless you need them. Pass `null` only where the advertised schema allows
it; a required argument is not satisfied by `null`. Defaults apply when the server
normalizes an omitted optional input. Cross-field rules below still apply even when
each individual value has the right type. Unknown arguments are not a supported
extension mechanism.

Examples with placeholder IDs or names show request structure. Discover and copy
the actual identifiers before using them. An example request is not a claim that
its chosen date range has data or that a source is currently published. This guide
does not invent successful responses.

<a id="pagination-and-data-quality"></a>
## Pagination and data quality

- Follow each tool's own pagination contract. When a response has
  `page.has_more: true`, use its exact `page.next_cursor` with the same tool,
  filters, and page size. Do not decode, shorten, or reconstruct the cursor.
  Some tools use other selectors or bounded result limits rather than cursors;
  their argument tables say which.
- A page is not a complete export. Accumulate every page before calculating full
  sample statistics. Account-wide rate, volume, concurrency, and dataset-access
  limits still apply. A smaller page size is not a way around those limits.
- Check the response's status, metadata, source dates, quality warnings, and
  coverage before interpreting the rows. An unavailable publication or
  `data_gap` is not a successful empty result. An available source can legitimately
  have no matches for your filters.
- Preserve numeric strings as exact decimal text until you choose a suitable
  numeric type. JavaScript numbers cannot represent every database integer
  exactly. Do not convert NULLs to zero or interpret a missing coefficient as zero.
- Units differ by dataset: a return fraction of `0.01` means 1%, but a field
  explicitly stored in percent units uses `1` for 1%. Use the units described
  for that dataset and its publication metadata. Do not assume every price is
  adjusted or every index is total return.
- A report page and its MCP materialization can have different refresh times,
  retained history, and eligible universes. The recipes identify source facts and
  stored calculations, not a promise to reproduce every image or report statistic.

<a id="remote-tool-reference"></a>
## Remote tool reference

<a id="tool-list_dashboard_datasets"></a>
### `list_dashboard_datasets`

Discover published public dashboard datasets through the publication catalog.
Each returned catalog row has `dataset_name`, a decimal-string `row_count`,
`schema` column/type pairs, source `metadata`, `refreshed_at`, and `content_digest`.
“Public” distinguishes research datasets from private account data; the tool call
still requires authentication. There is no hard-coded per-table allowlist; the
publication catalog defines the ownership and access boundary.

| Argument | Required? | Type and rules |
| --- | --- | --- |
| `search` | Optional | String, 1–256 UTF-16 code units, or null. Literal case-insensitive substring search on dataset names; not SQL wildcard syntax. |
| `limit` | Optional | Integer, 1–200, or null; default 100. Catalog rows per page. |
| `cursor` | Optional | String, 1–8192 UTF-16 code units, or null. Copy the previous response's continuation unchanged; keep `search` and `limit` identical. |

Find the PMS datasets first:

```json
{
  "name": "list_dashboard_datasets",
  "arguments": {"search": "PMS", "limit": 20}
}
```

To enumerate the complete catalog, omit `search` and continue until
`page.has_more` is false. Use each row's exact dataset name and advertised schema
for the next tool; do not infer columns from a report's display labels.

<a id="tool-query_dashboard_dataset"></a>
### `query_dashboard_dataset`

Read one bounded page from a catalog-owned dashboard dataset. The result includes
`dataset_name`, `rows`, `page`, and `metadata`. Here `metadata` is the complete
catalog row, so the schema is `metadata.schema` and the source publication's own
metadata is `metadata.metadata`. The server returns numeric database values as
text and preserves SQL NULL as JSON null.

| Argument | Required? | Type and rules |
| --- | --- | --- |
| `dataset_name` | Mandatory | Exact case-sensitive published name matching `^DASHBOARD_[A-Z0-9_]{1,54}$`. `DASHBOARD_CATALOG` is not a queryable dataset. |
| `entity_column` | Optional | Advertised text or integer column name matching `^[A-Za-z_][A-Za-z0-9_]{0,63}$`, or null. Requires `entity`. |
| `entity` | Optional | String, 1–256 UTF-16 code units, or null. Requires `entity_column`. Text columns use literal case-insensitive substring matching, not exact equality or SQL patterns. Integer columns use an exact canonical signed decimal string within the SQL type's range; no plus sign or leading zeros. |
| `date_column` | Optional | Advertised DATE, DATETIME, or supported TIMESTAMP column name, or null. Requires at least one of `start` or `end`. |
| `start` | Optional | Real ISO calendar date `YYYY-MM-DD`, or null; inclusive lower bound. Requires `date_column`. |
| `end` | Optional | Real ISO calendar date `YYYY-MM-DD`, or null; inclusive upper bound. Requires `date_column`. If both dates are present, `start` must not follow `end`. |
| `limit` | Optional | Integer, 1–200, or null; default 100. Rows per page. |
| `cursor` | Optional | String, 1–8192 UTF-16 code units, or null. Copy the previous continuation unchanged with identical dataset, filters, and limit. |

Inspect mutual-fund return rows without assuming any entity or date column:

```json
{
  "name": "query_dashboard_dataset",
  "arguments": {"dataset_name": "DASHBOARD_MF_RETURNS", "limit": 2}
}
```

The published schema for this dataset includes `AS_OF`. To bound the weekly
observations by their stored observation dates:

```json
{
  "name": "query_dashboard_dataset",
  "arguments": {
    "dataset_name": "DASHBOARD_MF_RETURNS",
    "date_column": "AS_OF",
    "start": "2026-09-01",
    "end": "2026-09-30",
    "limit": 200
  }
}
```

An entity filter cannot target DOUBLE, DECIMAL, or DATE columns. The API supports
one entity-column filter plus one date-column filter, not arbitrary predicates,
projection, aggregation, or joins. If a report needs several categorical filters,
retrieve the appropriate bounded rows and apply the additional selection in your
client. Keep the dataset's grain intact while joining or grouping rows.

Rows use an increasing `ROW_ID` keyset. `ROW_ID` is a publication paging key, not a
business identifier or a rank. Continuations are tied to the dataset's content digest
and refreshed timestamp. If publication changes between pages, restart the query
rather than combining generations. Inspect source-quality warnings even when the
page status is `ok`.


<a id="non-dashboard-tools"></a>
## Non-dashboard remote tool reference

These 28 sections cover the deployed remote service tools other than the two dashboard tools. They do not include local consumer tools or an internal/legacy analytics dispatcher. Argument names, required fields, null acceptance, defaults, and structural bounds below follow the deployed `inputSchema`; additional backend checks and calculation limits are called out in each section. Do not send internal operation names or fields that a public tool does not advertise. These are read-only research tools; authenticated calls require the applicable `research:read` access. Public tool discovery does not establish data availability.

Each JSON block is the **params object** for an MCP `tools/call` request: `{"name": "TOOL_NAME", "arguments": {...}}`, not a full JSON-RPC envelope or a successful response. Examples are schema-valid request shapes, not executed requests. Dates and search strings are illustrative and do not assert matching reports or records exist. Replace `STRATEGY_ID_FROM_DISCOVERY`, `RUN_ID_FROM_DISCOVERY`, `INDEX_NAME_FROM_DISCOVERY`, `SYMBOL_FROM_DISCOVERY`, and `SERIES_FROM_DISCOVERY` with exact values returned by their discovery tools. The numeric code `1` in NAV examples is a schema-valid numeric stand-in, **not a verified scheme**: replace it with a discovered actual plan code. Do not replace numeric identifiers with nonnumeric placeholder strings. A valid request can return empty results, null, `data_gap`, `unavailable`, partial coverage, or an error.

A type that includes `null` explicitly accepts JSON null. Unless stated otherwise, nullable optional inputs treat null as omission, including application of defaults. An optional type without null must be omitted rather than set to null. Required inputs must always be supplied. “None declared” means the catalog declares no literal default; it does not mean the backend has no selection behavior. Regexes below are shown literally, not JSON-string escaped.

<a id="tool-get_amfi_datasets"></a>

### `get_amfi_datasets`

Discovers `AMFI_MONTHLY_STATS`, `MF_SCHEME_CLASS`, `MF_FUNDWISE_AUM`, and `MF_SCHEMEWISE_AUM`. Returns each dataset's availability, actual date coverage, row key, granularity, units, and column dictionary. This is metadata discovery, not proof that all four sources are populated. No pagination; the response describes four datasets.

| Argument | Required | Type, including null support | Default | Bounds, enum, and meaning |
| --- | --- | --- | --- | --- |
| None | — | — | — | Pass an empty arguments object `{}`. |

Example `tools/call` params:

```json
{
  "name": "get_amfi_datasets",
  "arguments": {}
}
```

<a id="tool-get_amfi_monthly_stats"></a>

### `get_amfi_monthly_stats`

Reads `AMFI_MONTHLY_STATS` at category/report granularity. Subscriptions (`FUNDS_MOBILIZED`), redemptions (`REPURCHASES`), net flows, period-end AUM, and average AUM are different quantities. Monetary source values are exact decimal text in INR crore; folios count accounts, not unique investors. Missing values remain null, not zero.

`period` is an exact report date and cannot be combined with `start` or `end`. Bounds are inclusive and must be ordered. With no date selector, the latest source report is selected. `flow_totals=true` requires one `section`, `category_group`, and `category`, plus either `period` or both `start` and `end`. It sums only the three flow columns over all matching observations, not only the current page; the maximum is 1,200 observations. Totals remain in INR crore even when converted row values are requested. No AUM, AAUM, or folio sums, cross-group sums, annualization, or guarantee of consecutive monthly coverage. For rankings, use `query_amfi_flows`.

Pagination defaults to 100 rows and permits 1–500. Omit `cursor` or pass null on the first request; for continuation, copy the returned `next_cursor` unchanged with identical filters and limit until `has_more=false`. AMFI cursors are bound to query/publication context and can become invalid after a publication change. Dates must be real `YYYY-MM-DD` calendar dates in 1900–2100. Optional arguments accept null, which is treated as omission; defaulted arguments then use their defaults. `convert_to` adds converted monetary values without replacing raw source values.

| Argument | Required | Type, including null support | Default | Bounds, enum, and meaning |
| --- | --- | --- | --- | --- |
| `start` | Optional | string or null | None declared; see behavior above | pattern: `^\d{4}-\d{2}-\d{2}$`. Inclusive lower date bound; see this section for snapshot-cutoff or observation semantics. |
| `end` | Optional | string or null | None declared; see behavior above | pattern: `^\d{4}-\d{2}-\d{2}$`. Inclusive upper date bound; see this section for omitted-end behavior. |
| `period` | Optional | string or null | None declared; see behavior above | pattern: `^\d{4}-\d{2}-\d{2}$`. Exact source report date (AS_OF snapshot date for classification), not an inferred month-end. |
| `limit` | Optional | integer or null | `100` | minimum 1; maximum 500. Maximum output rows per page, not a source-scan cost bound. |
| `cursor` | Optional | string or null | None declared; see behavior above | minimum characters 1; maximum characters 4096. Opaque continuation token returned by this same tool; omit or use null on the first request. Never invent a token. |
| `convert_to` | Optional | string or null | None declared; see behavior above | enum: `"lakh"`, `"crore"`. Optional INR monetary conversion target; raw values are preserved. No conversion is added when omitted. |
| `section` | Optional | string or null | None declared; see behavior above | enum: `"A"`, `"B"`, `"C"`. Source section: A = open-ended, B = closed-ended, C = interval. |
| `category_group` | Optional | string or null | None declared; see behavior above | minimum characters 1; maximum characters 254. Exact source report group code; membership can change historically. |
| `category` | Optional | string or null | None declared; see behavior above | minimum characters 1; maximum characters 254. Category selector; matching rules depend on this tool, as described above. |
| `flow_totals` | Optional | boolean or null | `false` | No additional catalog bounds. Calculate all-matching-window flow sums only when single-category and explicit-date requirements are met. |

Example `tools/call` params:

```json
{
  "name": "get_amfi_monthly_stats",
  "arguments": {
    "period": "2025-12-31",
    "section": "A",
    "limit": 20
  }
}
```

<a id="tool-search_amfi_scheme_classification"></a>

### `search_amfi_scheme_classification`

Reads `MF_SCHEME_CLASS`, keyed by scheme code and ingestion snapshot `AS_OF`. `AS_OF` is not an effective classification date. `latest=true` selects the latest snapshot separately for each scheme, including schemes absent from the global latest snapshot. Use `latest=false` for snapshot history. Date filters apply to the selected snapshot rows; latest selection does not mean “latest before end.”

`period` matches exact `AS_OF` and excludes `start`/`end`; range bounds are inclusive and ordered. `class_1`, `class_2`, and `scheme_code` are exact filters. `search` matches literal class-label text or scheme names in the latest exact scheme-AUM report, not all historical names. Name search also requires the scheme-AUM publication. Scheme codes join directly to scheme AUM and raw NAV codes.

Pagination defaults to 100 rows and permits 1–500. Omit `cursor` or pass null on the first request; for continuation, copy the returned `next_cursor` unchanged with identical filters and limit until `has_more=false`. AMFI cursors are bound to query/publication context and can become invalid after a publication change. Dates must be real `YYYY-MM-DD` calendar dates in 1900–2100. Optional arguments accept null, which is treated as omission; defaulted arguments then use their defaults.

| Argument | Required | Type, including null support | Default | Bounds, enum, and meaning |
| --- | --- | --- | --- | --- |
| `start` | Optional | string or null | None declared; see behavior above | pattern: `^\d{4}-\d{2}-\d{2}$`. Inclusive lower date bound; see this section for snapshot-cutoff or observation semantics. |
| `end` | Optional | string or null | None declared; see behavior above | pattern: `^\d{4}-\d{2}-\d{2}$`. Inclusive upper date bound; see this section for omitted-end behavior. |
| `period` | Optional | string or null | None declared; see behavior above | pattern: `^\d{4}-\d{2}-\d{2}$`. Exact source report date (AS_OF snapshot date for classification), not an inferred month-end. |
| `limit` | Optional | integer or null | `100` | minimum 1; maximum 500. Maximum output rows per page, not a source-scan cost bound. |
| `cursor` | Optional | string or null | None declared; see behavior above | minimum characters 1; maximum characters 4096. Opaque continuation token returned by this same tool; omit or use null on the first request. Never invent a token. |
| `scheme_code` | Optional | integer or null | None declared; see behavior above | greater than 0; maximum 2147483647. Exact AMFI/NAV scheme code; discover the code rather than infer it from a fund name. |
| `class_1` | Optional | string or null | None declared; see behavior above | minimum characters 1; maximum characters 254. Exact broad classification label. |
| `class_2` | Optional | string or null | None declared; see behavior above | minimum characters 1; maximum characters 254. Exact detailed classification label. |
| `search` | Optional | string or null | None declared; see behavior above | minimum characters 1; maximum characters 254. Literal text filter, not SQL, regex, or caller wildcard syntax; scope is described above. |
| `latest` | Optional | boolean or null | `true` | No additional catalog bounds. Select latest snapshot separately per scheme; false reads matching snapshot history. |

Example `tools/call` params:

```json
{
  "name": "search_amfi_scheme_classification",
  "arguments": {
    "search": "mid cap",
    "latest": true,
    "limit": 20
  }
}
```

<a id="tool-get_amfi_fund_aum"></a>

### `get_amfi_fund_aum`

Reads `MF_FUNDWISE_AUM`: one fund house per actual report date, not individual underlying funds or plans. Average AUM is in INR lakh. `TOTAL_AVG_AUM` adds the excluding-domestic-FOF and domestic-FOF components; overseas FOF is included. Source DOUBLE amounts, sums, and shares are approximate.

`period` is exact and excludes `start`/`end`; inclusive bounds must be ordered. `rank=true` requires an explicitly supplied exact `period` and sorts by total average AUM. At an exact period, market-share denominators include all fund houses in this dataset, not only filters or the returned page. With no dates and no exact `fund`, the latest report is selected; an exact `fund` without dates reads history. `fund` is an exact source label; `search` is a literal name substring. Never add fund-house totals to scheme-wise or monthly-category totals.

Pagination defaults to 100 rows and permits 1–500. Omit `cursor` or pass null on the first request; for continuation, copy the returned `next_cursor` unchanged with identical filters and limit until `has_more=false`. AMFI cursors are bound to query/publication context and can become invalid after a publication change. Dates must be real `YYYY-MM-DD` calendar dates in 1900–2100. Optional arguments accept null, which is treated as omission; defaulted arguments then use their defaults. `convert_to` adds converted monetary values without replacing raw source values.

| Argument | Required | Type, including null support | Default | Bounds, enum, and meaning |
| --- | --- | --- | --- | --- |
| `start` | Optional | string or null | None declared; see behavior above | pattern: `^\d{4}-\d{2}-\d{2}$`. Inclusive lower date bound; see this section for snapshot-cutoff or observation semantics. |
| `end` | Optional | string or null | None declared; see behavior above | pattern: `^\d{4}-\d{2}-\d{2}$`. Inclusive upper date bound; see this section for omitted-end behavior. |
| `period` | Optional | string or null | None declared; see behavior above | pattern: `^\d{4}-\d{2}-\d{2}$`. Exact source report date (AS_OF snapshot date for classification), not an inferred month-end. |
| `limit` | Optional | integer or null | `100` | minimum 1; maximum 500. Maximum output rows per page, not a source-scan cost bound. |
| `cursor` | Optional | string or null | None declared; see behavior above | minimum characters 1; maximum characters 4096. Opaque continuation token returned by this same tool; omit or use null on the first request. Never invent a token. |
| `convert_to` | Optional | string or null | None declared; see behavior above | enum: `"lakh"`, `"crore"`. Optional INR monetary conversion target; raw values are preserved. No conversion is added when omitted. |
| `fund` | Optional | string or null | None declared; see behavior above | minimum characters 1; maximum characters 254. Exact source fund-house label, not an individual fund or scheme name. |
| `search` | Optional | string or null | None declared; see behavior above | minimum characters 1; maximum characters 254. Literal text filter, not SQL, regex, or caller wildcard syntax; scope is described above. |
| `rank` | Optional | boolean or null | `false` | No additional catalog bounds. Sort raw fund-house or plan rows by total average AUM; true requires explicit period. |

Example `tools/call` params:

```json
{
  "name": "get_amfi_fund_aum",
  "arguments": {
    "period": "2025-12-31",
    "rank": true,
    "convert_to": "crore",
    "limit": 10
  }
}
```

<a id="tool-get_amfi_scheme_aum"></a>

### `get_amfi_scheme_aum`

Reads raw `MF_SCHEMEWISE_AUM` rows keyed by actual report date, AMFI code, and scheme/plan name. This is plan-level AUM, not consolidated underlying-fund AUM. Average AUM is in INR lakh; total is the sum of both FOF components, including overseas FOF. Source DOUBLE amounts and derived sums/shares are approximate.

Use a short `search` to inspect exact plan names and codes in the latest report, then choose actual Direct Growth codes for NAV metrics. A name alone does not validate the plan/option. With no dates and no `scheme_code`, the latest source report is selected; a code without dates reads its AUM history. `period` excludes `start`/`end`; bounds are inclusive and ordered. `rank=true` requires an explicitly supplied exact `period`. Rankings and shares are raw-plan measures; the share denominator is all source plan rows at that exact report, not the filter/page.

`class_1` and `class_2` use the latest available classification per code regardless of the AUM date, creating retrospective bias; missing classes remain visible. A missing exact historical report is missing data, not a ban on historical queries. Use `get_amfi_aum_ranking` for consolidated funds, `get_amfi_aum_growth` for AUM changes, and `get_amfi_category_aum_history` for consolidated category history.

Pagination defaults to 100 rows and permits 1–500. Omit `cursor` or pass null on the first request; for continuation, copy the returned `next_cursor` unchanged with identical filters and limit until `has_more=false`. AMFI cursors are bound to query/publication context and can become invalid after a publication change. Dates must be real `YYYY-MM-DD` calendar dates in 1900–2100. Optional arguments accept null, which is treated as omission; defaulted arguments then use their defaults. `convert_to` adds converted monetary values without replacing raw source values.

| Argument | Required | Type, including null support | Default | Bounds, enum, and meaning |
| --- | --- | --- | --- | --- |
| `start` | Optional | string or null | None declared; see behavior above | pattern: `^\d{4}-\d{2}-\d{2}$`. Inclusive lower date bound; see this section for snapshot-cutoff or observation semantics. |
| `end` | Optional | string or null | None declared; see behavior above | pattern: `^\d{4}-\d{2}-\d{2}$`. Inclusive upper date bound; see this section for omitted-end behavior. |
| `period` | Optional | string or null | None declared; see behavior above | pattern: `^\d{4}-\d{2}-\d{2}$`. Exact source report date (AS_OF snapshot date for classification), not an inferred month-end. |
| `limit` | Optional | integer or null | `100` | minimum 1; maximum 500. Maximum output rows per page, not a source-scan cost bound. |
| `cursor` | Optional | string or null | None declared; see behavior above | minimum characters 1; maximum characters 4096. Opaque continuation token returned by this same tool; omit or use null on the first request. Never invent a token. |
| `convert_to` | Optional | string or null | None declared; see behavior above | enum: `"lakh"`, `"crore"`. Optional INR monetary conversion target; raw values are preserved. No conversion is added when omitted. |
| `scheme_code` | Optional | integer or null | None declared; see behavior above | greater than 0; maximum 2147483647. Exact AMFI/NAV scheme code; discover the code rather than infer it from a fund name. |
| `search` | Optional | string or null | None declared; see behavior above | minimum characters 1; maximum characters 254. Literal text filter, not SQL, regex, or caller wildcard syntax; scope is described above. |
| `class_1` | Optional | string or null | None declared; see behavior above | minimum characters 1; maximum characters 254. Exact broad classification label. |
| `class_2` | Optional | string or null | None declared; see behavior above | minimum characters 1; maximum characters 254. Exact detailed classification label. |
| `rank` | Optional | boolean or null | `false` | No additional catalog bounds. Sort raw fund-house or plan rows by total average AUM; true requires explicit period. |

Example `tools/call` params:

```json
{
  "name": "get_amfi_scheme_aum",
  "arguments": {
    "search": "Parag Parikh",
    "limit": 20
  }
}
```

<a id="tool-get_amfi_category_aum"></a>

### `get_amfi_category_aum`

Groups all raw `MF_SCHEMEWISE_AUM` plan rows at one exact `period` by latest per-scheme `CLASS_1` and `CLASS_2`. Keeps unclassified groups visible. Amounts are approximate INR lakh and include both FOF components. Shares use all plan rows in the exact report as denominator. Latest classification can postdate the report; this is not historical point-in-time classification.

`compare_period` is another exact report, not an as-of cutoff. Change direction is **compare_period minus period**. Amount changes are INR lakh; share changes are percentage points. Only groups present in the base period are displayed; comparison-only groups are not added. A missing counterpart is null, not zero. Each period has its own full denominator. This raw-plan grouping differs from canonical-fund-consolidated category history.

Pagination defaults to 100 rows and permits 1–500. Omit `cursor` or pass null on the first request; for continuation, copy the returned `next_cursor` unchanged with identical filters and limit until `has_more=false`. AMFI cursors are bound to query/publication context and can become invalid after a publication change. Dates must be real `YYYY-MM-DD` calendar dates in 1900–2100. Optional arguments accept null, which is treated as omission; defaulted arguments then use their defaults. `convert_to` adds converted monetary values without replacing raw source values.

| Argument | Required | Type, including null support | Default | Bounds, enum, and meaning |
| --- | --- | --- | --- | --- |
| `period` | Required | string | No default | pattern: `^\d{4}-\d{2}-\d{2}$`. Exact source report date (AS_OF snapshot date for classification), not an inferred month-end. |
| `compare_period` | Optional | string or null | None declared; see behavior above | pattern: `^\d{4}-\d{2}-\d{2}$`. Exact comparison report date; changes are comparison minus base. |
| `convert_to` | Optional | string or null | None declared; see behavior above | enum: `"lakh"`, `"crore"`. Optional INR monetary conversion target; raw values are preserved. No conversion is added when omitted. |
| `limit` | Optional | integer or null | `100` | minimum 1; maximum 500. Maximum output rows per page, not a source-scan cost bound. |
| `cursor` | Optional | string or null | None declared; see behavior above | minimum characters 1; maximum characters 4096. Opaque continuation token returned by this same tool; omit or use null on the first request. Never invent a token. |

Example `tools/call` params:

```json
{
  "name": "get_amfi_category_aum",
  "arguments": {
    "period": "2025-12-31",
    "compare_period": "2024-12-31",
    "convert_to": "crore"
  }
}
```

<a id="tool-get_amfi_aum_ranking"></a>

### `get_amfi_aum_ranking`

Ranks canonical underlying funds or categories from `MF_SCHEMEWISE_AUM` joined to latest `MF_SCHEME_CLASS`. `group_by=fund` means an underlying investment fund, not a fund house. Direct, regular, growth, dividend, and IDCW variants are consolidated before filtering, including unclassified variants of a known fund.

Choose at most one of `period`, `year`, and `as_of`. `period` requires the exact source report: absent dates never silently roll back. `year` chooses the latest report within that year. `as_of` chooses the last report on or before its cutoff; for January 2019 use `2019-01-31`. Disclose the resolved report date, which may precede the requested month. With no selector, the latest report is used. `category` matches normalized classification labels and supported aliases such as `mid cap`; it is not free-text scheme-name search. `search` is a literal canonical fund-name substring applied after consolidation.

Amounts are average AUM, not month-end assets, NAV returns, or flows. Each source row contributes `AVG_AUM_WO_FOFD + AVG_AUM_FOFD` once, in INR lakh; crore values divide by 100. DOUBLE sums are approximate. Canonical fund grouping is a versioned name heuristic, not an authoritative merger/rename identity. Latest classification is not historical point-in-time and can introduce retrospective classification/survivorship bias. Inspect missing/conflicting classification coverage. Complete snapshots above 30,000 raw rows, ambiguous latest classifications, or invalid AUM components fail closed. Mirror ownership does not prove source completeness/freshness; there is no alternate-backend fallback.

Pagination defaults to 20 rows, with 1–100 permitted. Optional arguments accept null as omission. First request omits `cursor` or uses null; forward the exact returned `next_cursor` with identical filters and limit until `has_more=false`. Cursors are context-bound and pages do not share a database snapshot. Although the catalog gives `cursor` no minimum length, use only actual returned continuation tokens. These public schemas reject additional properties.

| Argument | Required | Type, including null support | Default | Bounds, enum, and meaning |
| --- | --- | --- | --- | --- |
| `group_by` | Optional | string or null | `"fund"` | enum: `"fund"`, `"category"`. Consolidate and rank underlying funds or categories; fund does not mean fund house. |
| `period` | Optional | string or null | None declared; see behavior above | pattern: `^\d{4}-\d{2}-\d{2}$`. Exact source report date (AS_OF snapshot date for classification), not an inferred month-end. |
| `year` | Optional | integer or null | None declared; see behavior above | minimum 1900; maximum 9998. Calendar-year selector; see whether this tool chooses a snapshot or sums reported flows. |
| `as_of` | Optional | string or null | None declared; see behavior above | pattern: `^\d{4}-\d{2}-\d{2}$`. Choose the last source report on or before this cutoff and disclose its resolved date. |
| `category` | Optional | string or null | None declared; see behavior above | minimum characters 1; maximum characters 200. Category selector; matching rules depend on this tool, as described above. |
| `search` | Optional | string or null | None declared; see behavior above | minimum characters 1; maximum characters 200. Literal canonical underlying fund-name substring after all source variants are consolidated. |
| `limit` | Optional | integer or null | `20` | minimum 1; maximum 100. Maximum output rows per page, not a source-scan cost bound. |
| `cursor` | Optional | string or null | None declared; see behavior above | maximum characters 16000. Opaque continuation token returned by this same tool; omit or use null on the first request. Never invent a token. |

Example `tools/call` params:

```json
{
  "name": "get_amfi_aum_ranking",
  "arguments": {
    "category": "mid cap",
    "as_of": "2019-01-31",
    "limit": 10
  }
}
```

<a id="tool-get_amfi_aum_growth"></a>

### `get_amfi_aum_growth`

Compares common source snapshots from `MF_SCHEMEWISE_AUM` with latest `MF_SCHEME_CLASS`. `start` is required: “since 2020” uses `2020-01-01`. The baseline is the latest report on or before `start`; the endpoint is the latest report on or before `end`, or the latest observed report when end is omitted. Bounds must be ordered. Disclose both resolved dates and endpoint amounts; these need not equal the requested cutoffs.

`rank_by=percent` ranks percentage AUM change and excludes missing/nonpositive baselines. `rank_by=absolute` ranks changes in AUM, not net inflows or investment returns. Matching is by canonical fund name; renamed funds are not linked using overlapping codes. With an explicit category, endpoint totals include all observed category assets, including fund entries and exits, not only survivors. `search` filters canonical fund names after consolidation. `group_by=fund` means underlying funds, not fund houses.

Amounts are average AUM, not month-end assets, NAV returns, or flows. Each source row contributes `AVG_AUM_WO_FOFD + AVG_AUM_FOFD` once, in INR lakh; crore values divide by 100. DOUBLE sums are approximate. Canonical fund grouping is a versioned name heuristic, not an authoritative merger/rename identity. Latest classification is not historical point-in-time and can introduce retrospective classification/survivorship bias. Inspect missing/conflicting classification coverage. Complete snapshots above 30,000 raw rows, ambiguous latest classifications, or invalid AUM components fail closed. Mirror ownership does not prove source completeness/freshness; there is no alternate-backend fallback.

Pagination defaults to 20 rows, with 1–100 permitted. Optional arguments accept null as omission. First request omits `cursor` or uses null; forward the exact returned `next_cursor` with identical filters and limit until `has_more=false`. Cursors are context-bound and pages do not share a database snapshot. Although the catalog gives `cursor` no minimum length, use only actual returned continuation tokens. These public schemas reject additional properties.

| Argument | Required | Type, including null support | Default | Bounds, enum, and meaning |
| --- | --- | --- | --- | --- |
| `start` | Required | string | No default | pattern: `^\d{4}-\d{2}-\d{2}$`. Required baseline cutoff: latest common report on or before this date. |
| `end` | Optional | string or null | None declared; see behavior above | pattern: `^\d{4}-\d{2}-\d{2}$`. Endpoint cutoff: latest common report on or before this date; omitted/null uses latest observed report. |
| `group_by` | Optional | string or null | `"fund"` | enum: `"fund"`, `"category"`. Consolidate and rank underlying funds or categories; fund does not mean fund house. |
| `category` | Optional | string or null | None declared; see behavior above | minimum characters 1; maximum characters 200. Category selector; matching rules depend on this tool, as described above. |
| `search` | Optional | string or null | None declared; see behavior above | minimum characters 1; maximum characters 200. Literal canonical underlying fund-name substring after all source variants are consolidated. |
| `rank_by` | Optional | string or null | `"percent"` | enum: `"absolute"`, `"percent"`. Descending ranking measure; AUM growth is not inflows or NAV performance. |
| `limit` | Optional | integer or null | `20` | minimum 1; maximum 100. Maximum output rows per page, not a source-scan cost bound. |
| `cursor` | Optional | string or null | None declared; see behavior above | maximum characters 16000. Opaque continuation token returned by this same tool; omit or use null on the first request. Never invent a token. |

Example `tools/call` params:

```json
{
  "name": "get_amfi_aum_growth",
  "arguments": {
    "start": "2020-01-01",
    "end": "2025-12-31",
    "category": "mid cap",
    "rank_by": "percent",
    "limit": 10
  }
}
```

<a id="tool-get_amfi_category_aum_history"></a>

### `get_amfi_category_aum_history`

Reads category average AUM history from `MF_SCHEMEWISE_AUM` and latest `MF_SCHEME_CLASS` over inclusive, ordered optional bounds. Omitted bounds leave that side unbounded within available source reports. Each report is a separate stock: never sum AUM across reporting dates. Each complete report is consolidated into canonical underlying funds before category selection and summation. Grouping is always category; there are no `group_by`, `search`, or individual-fund-history inputs.

Processes up to two complete snapshots per page in a window of at most 1,000 report dates. A page can contain fewer rows than `limit` while `has_more` remains true; follow every continuation. Narrow the date window if the report-date budget is exceeded. An oversized complete snapshot fails closed, rather than truncating source variants.

Amounts are average AUM, not month-end assets, NAV returns, or flows. Each source row contributes `AVG_AUM_WO_FOFD + AVG_AUM_FOFD` once, in INR lakh; crore values divide by 100. DOUBLE sums are approximate. Canonical fund grouping is a versioned name heuristic, not an authoritative merger/rename identity. Latest classification is not historical point-in-time and can introduce retrospective classification/survivorship bias. Inspect missing/conflicting classification coverage. Complete snapshots above 30,000 raw rows, ambiguous latest classifications, or invalid AUM components fail closed. Mirror ownership does not prove source completeness/freshness; there is no alternate-backend fallback.

Pagination defaults to 20 rows, with 1–100 permitted. Optional arguments accept null as omission. First request omits `cursor` or uses null; forward the exact returned `next_cursor` with identical filters and limit until `has_more=false`. Cursors are context-bound and pages do not share a database snapshot. Although the catalog gives `cursor` no minimum length, use only actual returned continuation tokens. These public schemas reject additional properties.

| Argument | Required | Type, including null support | Default | Bounds, enum, and meaning |
| --- | --- | --- | --- | --- |
| `category` | Optional | string or null | None declared; see behavior above | minimum characters 1; maximum characters 200. Category selector; matching rules depend on this tool, as described above. |
| `start` | Optional | string or null | None declared; see behavior above | pattern: `^\d{4}-\d{2}-\d{2}$`. Inclusive lower date bound; see this section for snapshot-cutoff or observation semantics. |
| `end` | Optional | string or null | None declared; see behavior above | pattern: `^\d{4}-\d{2}-\d{2}$`. Inclusive upper date bound; see this section for omitted-end behavior. |
| `limit` | Optional | integer or null | `20` | minimum 1; maximum 100. Maximum output rows per page, not a source-scan cost bound. |
| `cursor` | Optional | string or null | None declared; see behavior above | maximum characters 16000. Opaque continuation token returned by this same tool; omit or use null on the first request. Never invent a token. |

Example `tools/call` params:

```json
{
  "name": "get_amfi_category_aum_history",
  "arguments": {
    "category": "mid cap",
    "start": "2025-01-01",
    "end": "2025-12-31",
    "limit": 20
  }
}
```

<a id="tool-query_amfi_flows"></a>

### `query_amfi_flows`

Reads `AMFI_MONTHLY_STATS` category flows as exact fixed-point decimal text in INR crore. `subscriptions` means `FUNDS_MOBILIZED`; `redemptions` means `REPURCHASES`; `net_flow` is the reported source net flow. `granularity=fund` is schema-valid but returns `data_gap`: fund-level flows are unavailable and never proxied by AUM changes.

`period` is an exact report date and excludes `year`, `start`, and `end`. `year` excludes `start`/`end`. Supply `start` and `end` together, in order; bounds are inclusive. Dates must be real calendar dates in 1900–2100. With no time selector, ranking uses the latest report; history uses the available full range. A year or range ranking sums reported monthly flows by source identity, not AUM or AAUM, and does not annualize missing coverage. `rank_by` chooses the descending ranking measure; history returns source rows in date/identity order.

Identity is `SECTION + CATEGORY_GROUP + exact SCHEME_CATEGORY`. Category matching normalizes case/whitespace and selected aliases, rather than doing substring search. Historical label/group changes remain separate identities; an ambiguous history label requires `category_group`. Explicit total/subtotal labels are excluded, but “Other Schemes” and “Others” are retained. Categories/groups can overlap; no cross-category grand total is computed. Inspect reported/missing counts and per-category missing-month coverage. Selections exceeding 10,000 source rows fail closed; narrow the window. Cursors also bind a source fingerprint, so corrections can invalidate continuation.

Pagination defaults to 20 rows, with 1–100 permitted. Optional inputs accept null as omission. Omit `cursor` or use null first; forward returned `next_cursor` unchanged with identical filters and limit until `has_more=false`.

| Argument | Required | Type, including null support | Default | Bounds, enum, and meaning |
| --- | --- | --- | --- | --- |
| `operation` | Optional | string or null | `"ranking"` | enum: `"ranking"`, `"history"`. Choose category flow ranking or source-row history. |
| `granularity` | Optional | string or null | `"category"` | enum: `"fund"`, `"category"`. Requested flow level; fund is accepted by schema but returns data_gap. |
| `period` | Optional | string or null | None declared; see behavior above | pattern: `^\d{4}-\d{2}-\d{2}$`. Exact source report date (AS_OF snapshot date for classification), not an inferred month-end. |
| `year` | Optional | integer or null | None declared; see behavior above | minimum 1900; maximum 2100. Calendar-year selector; see whether this tool chooses a snapshot or sums reported flows. |
| `start` | Optional | string or null | None declared; see behavior above | pattern: `^\d{4}-\d{2}-\d{2}$`. Inclusive lower date bound; see this section for snapshot-cutoff or observation semantics. |
| `end` | Optional | string or null | None declared; see behavior above | pattern: `^\d{4}-\d{2}-\d{2}$`. Inclusive upper date bound; see this section for omitted-end behavior. |
| `category` | Optional | string or null | None declared; see behavior above | minimum characters 1; maximum characters 254. Category selector; matching rules depend on this tool, as described above. |
| `section` | Optional | string or null | `"A"` | enum: `"A"`, `"B"`, `"C"`. Source section: A = open-ended, B = closed-ended, C = interval. |
| `category_group` | Optional | string or null | None declared; see behavior above | minimum characters 1; maximum characters 32. Exact source report group code; membership can change historically. |
| `rank_by` | Optional | string or null | `"net_flow"` | enum: `"net_flow"`, `"subscriptions"`, `"redemptions"`. Descending category flow measure; has no effect on history row ordering. |
| `limit` | Optional | integer or null | `20` | minimum 1; maximum 100. Maximum output rows per page, not a source-scan cost bound. |
| `cursor` | Optional | string or null | None declared; see behavior above | minimum characters 1; maximum characters 4096. Opaque continuation token returned by this same tool; omit or use null on the first request. Never invent a token. |

Example `tools/call` params:

```json
{
  "name": "query_amfi_flows",
  "arguments": {
    "operation": "ranking",
    "year": 2025,
    "granularity": "category",
    "rank_by": "net_flow",
    "limit": 10
  }
}
```

<a id="tool-get_nav_metrics"></a>

### `get_nav_metrics`

Calculates metrics from the MariaDB NAV mirror `MF_NAV_HISTORY`, not published backtest observations. Resolve codes and exact Direct Growth options with `get_amfi_scheme_aum` first. Duplicate requested codes are deduplicated.

Dates are real `YYYY-MM-DD` calendar dates, inclusive, with `start <= end`. Omitted start uses available history; omitted end uses each scheme's latest observed NAV, not today. The backend also rejects string codes above `2147483647`, even though that refinement is not expressed by the catalog regex. No cursor or pagination; the cap is 30,000 raw rows per scheme. Invalid/nonpositive NAV or conflicting duplicate-date values refuse metrics; identical duplicate-date NAV rows are collapsed.

CAGR uses actual elapsed UTC calendar days divided by `365.2425`, with at least two distinct dates and no predecessor return. Sharpe uses consecutive-observation simple returns, sample standard deviation (`n-1`), and `sqrt(252)` annualization. `risk_free_rate` is an annual effective fractional rate, converted to daily `(1 + rate)^(1/252) - 1`; zero volatility or fewer than two returns produces null Sharpe. Non-observation days are not filled. CAGR and current/maximum drawdowns are fractions; Sharpe is a ratio. Drawdowns are nonpositive and confined to observed peaks inside the selected window, not lifetime peaks.

Raw NAV is not distribution-adjusted. Inspect actual first/last dates, coverage warnings, end clamping, and per-scheme statuses before comparing schemes. Mirror ownership does not independently verify freshness/completeness, and separate bounded reads are not a shared snapshot.

| Argument | Required | Type, including null support | Default | Bounds, enum, and meaning |
| --- | --- | --- | --- | --- |
| `scheme_codes` | Required | array of (string or integer) | No default | minimum items 1; maximum items 10; each item: pattern: `^[1-9]\d{0,9}$`; or greater than 0; maximum 2147483647. Exact AMFI/NAV codes for the desired plans/options; integer codes or canonical decimal strings. |
| `start` | Optional | string or null | None declared; see behavior above | No additional catalog bounds. Inclusive lower date bound; see this section for snapshot-cutoff or observation semantics. |
| `end` | Optional | string or null | None declared; see behavior above | No additional catalog bounds. Inclusive upper date bound; see this section for omitted-end behavior. |
| `risk_free_rate` | Optional | number or null | `0` | greater than -1; maximum 1. Annual effective fractional rate, not percent points; 0.05 means 5% per year. |

Example `tools/call` params:

```json
{
  "name": "get_nav_metrics",
  "arguments": {
    "scheme_codes": [
      1
    ],
    "start": "2020-01-01",
    "end": "2025-12-31",
    "risk_free_rate": 0.05
  }
}
```

<a id="tool-list_equities"></a>

### `list_equities`

Discovers exact `SYMBOL`/`SERIES` pairs and available date ranges from MariaDB `PX_HISTORY`. `search` is a literal case-insensitive symbol substring; `series` is an exact series filter. Use returned identifiers together for history. Broad discovery scans history and can be slow or time out despite bounded output.

Pagination defaults to 250 rows and permits 1–1,000. First request omits `cursor` or uses null. Continue with the exact returned `next_cursor`, unchanged selectors, search, dates, format, and limit, until `has_more=false`. Pages do not share a database snapshot; restart after mirror replacement if needed. Optional arguments accept null as omission; defaulted arguments then use their defaults. Mirror ownership does not independently verify freshness or completeness.

| Argument | Required | Type, including null support | Default | Bounds, enum, and meaning |
| --- | --- | --- | --- | --- |
| `limit` | Optional | integer or null | `250` | minimum 1; maximum 1000. Maximum output rows per page, not a source-scan cost bound. |
| `cursor` | Optional | string or null | None declared; see behavior above | minimum characters 1; maximum characters 4096. Opaque continuation token returned by this same tool; omit or use null on the first request. Never invent a token. |
| `search` | Optional | string or null | None declared; see behavior above | minimum characters 1; maximum characters 256. Literal text filter, not SQL, regex, or caller wildcard syntax; scope is described above. |
| `series` | Optional | string or null | None declared; see behavior above | minimum characters 1; maximum characters 256. Exact instrument series returned by discovery. |

Example `tools/call` params:

```json
{
  "name": "list_equities",
  "arguments": {
    "search": "RELIANCE",
    "series": "EQ",
    "limit": 20
  }
}
```

<a id="tool-get_equity_history"></a>

### `get_equity_history`

Downloads raw `PX_HISTORY` observations for an explicit symbol **and** series, discovered with `list_equities`. Fields include OHLC, last/previous close, traded quantity/value, and transaction count. These are stored prices/activity, not adjusted prices or total returns. Nullable source fields stay null. Source DOUBLE price/quantity/value fields are represented as database text, not invented arbitrary-precision decimals.

Dates must be real calendar dates, inclusive and ordered. Omitted bounds use available history on that side; bounded windows are preferable because broad reads can time out. Duplicate symbol/series/date observations, even identical ones, fail closed with `data_gap` because no stable source tie key exists. Require every page to succeed before claiming a complete download; one partial page cannot establish the window peak or latest value. No account holdings are exposed.

Pagination defaults to 250 rows and permits 1–1,000. First request omits `cursor` or uses null. Continue with the exact returned `next_cursor`, unchanged selectors, search, dates, format, and limit, until `has_more=false`. Pages do not share a database snapshot; restart after mirror replacement if needed. Optional arguments accept null as omission; defaulted arguments then use their defaults. Mirror ownership does not independently verify freshness or completeness.

| Argument | Required | Type, including null support | Default | Bounds, enum, and meaning |
| --- | --- | --- | --- | --- |
| `limit` | Optional | integer or null | `250` | minimum 1; maximum 1000. Maximum output rows per page, not a source-scan cost bound. |
| `cursor` | Optional | string or null | None declared; see behavior above | minimum characters 1; maximum characters 4096. Opaque continuation token returned by this same tool; omit or use null on the first request. Never invent a token. |
| `start` | Optional | string or null | None declared; see behavior above | No additional catalog bounds. Inclusive lower date bound; see this section for snapshot-cutoff or observation semantics. |
| `end` | Optional | string or null | None declared; see behavior above | No additional catalog bounds. Inclusive upper date bound; see this section for omitted-end behavior. |
| `format` | Optional | string or null | `"json"` | enum: `"json"`, `"csv"`. Representation for each bounded history page. csv adds an inline CSV string; it is not an automatic full-history file. |
| `symbol` | Required | string | No default | minimum characters 1; maximum characters 256. Exact symbol returned by list_equities; use with the returned series. |
| `series` | Required | string | No default | minimum characters 1; maximum characters 256. Exact instrument series returned by discovery. |

Example `tools/call` params:

```json
{
  "name": "get_equity_history",
  "arguments": {
    "symbol": "SYMBOL_FROM_DISCOVERY",
    "series": "SERIES_FROM_DISCOVERY",
    "start": "2025-01-01",
    "end": "2025-12-31",
    "format": "csv",
    "limit": 250
  }
}
```

<a id="tool-list_indices"></a>

### `list_indices`

Discovers exact names and available date ranges for all indices in MariaDB `BHAV_INDEX`; there is no factor-index allowlist. `search` is a literal case-insensitive name substring. Use returned names for history or metrics.

Pagination defaults to 250 rows and permits 1–1,000. First request omits `cursor` or uses null. Continue with the exact returned `next_cursor`, unchanged selectors, search, dates, format, and limit, until `has_more=false`. Pages do not share a database snapshot; restart after mirror replacement if needed. Optional arguments accept null as omission; defaulted arguments then use their defaults. Mirror ownership does not independently verify freshness or completeness.

| Argument | Required | Type, including null support | Default | Bounds, enum, and meaning |
| --- | --- | --- | --- | --- |
| `limit` | Optional | integer or null | `250` | minimum 1; maximum 1000. Maximum output rows per page, not a source-scan cost bound. |
| `cursor` | Optional | string or null | None declared; see behavior above | minimum characters 1; maximum characters 4096. Opaque continuation token returned by this same tool; omit or use null on the first request. Never invent a token. |
| `search` | Optional | string or null | None declared; see behavior above | minimum characters 1; maximum characters 256. Literal text filter, not SQL, regex, or caller wildcard syntax; scope is described above. |

Example `tools/call` params:

```json
{
  "name": "list_indices",
  "arguments": {
    "search": "NIFTY",
    "limit": 20
  }
}
```

<a id="tool-get_index_history"></a>

### `get_index_history`

Downloads raw stored daily closing levels from MariaDB `BHAV_INDEX` for an exact name discovered with `list_indices`. No inferred adjustments, total-return conversion, or filling of missing prices. Source DOUBLE levels are returned as database text. Dates must be real calendar dates, inclusive and ordered; omitted bounds leave that side open to available history.

Follow every page for a full download. Do not infer a full-window peak or latest stored observation from one partial page. Use `get_index_metrics` instead for peak, latest value, current drawdown, or performance without client pagination.

Pagination defaults to 250 rows and permits 1–1,000. First request omits `cursor` or uses null. Continue with the exact returned `next_cursor`, unchanged selectors, search, dates, format, and limit, until `has_more=false`. Pages do not share a database snapshot; restart after mirror replacement if needed. Optional arguments accept null as omission; defaulted arguments then use their defaults. Mirror ownership does not independently verify freshness or completeness.

| Argument | Required | Type, including null support | Default | Bounds, enum, and meaning |
| --- | --- | --- | --- | --- |
| `limit` | Optional | integer or null | `250` | minimum 1; maximum 1000. Maximum output rows per page, not a source-scan cost bound. |
| `cursor` | Optional | string or null | None declared; see behavior above | minimum characters 1; maximum characters 4096. Opaque continuation token returned by this same tool; omit or use null on the first request. Never invent a token. |
| `start` | Optional | string or null | None declared; see behavior above | No additional catalog bounds. Inclusive lower date bound; see this section for snapshot-cutoff or observation semantics. |
| `end` | Optional | string or null | None declared; see behavior above | No additional catalog bounds. Inclusive upper date bound; see this section for omitted-end behavior. |
| `format` | Optional | string or null | `"json"` | enum: `"json"`, `"csv"`. Representation for each bounded history page. csv adds an inline CSV string; it is not an automatic full-history file. |
| `index_name` | Required | string | No default | minimum characters 1; maximum characters 256. Exact index name from list_indices. |

Example `tools/call` params:

```json
{
  "name": "get_index_history",
  "arguments": {
    "index_name": "INDEX_NAME_FROM_DISCOVERY",
    "start": "2025-01-01",
    "end": "2025-12-31",
    "format": "json",
    "limit": 250
  }
}
```

<a id="tool-list_nav_schemes"></a>

### `list_nav_schemes`

Discovers codes, exact stored plan/option names, date coverage, and counts from MariaDB `MF_NAV_HISTORY`. `search` is a literal case-insensitive name substring. The catalog's representative name is `MAX(SCHEME_NAME)` by database collation per code, not necessarily its latest name; history retains stored row names.

This exhaustive catalog scans history and can be slow. For active-fund plan-to-code lookup, prefer a short `get_amfi_scheme_aum` search against its small latest report. A failed catalog lookup does not show that code-based NAV metrics are unavailable. Inspect actual Direct Growth names externally rather than assuming option identity from a generic fund name.

Pagination defaults to 250 rows and permits 1–1,000. First request omits `cursor` or uses null. Continue with the exact returned `next_cursor`, unchanged selectors, search, dates, format, and limit, until `has_more=false`. Pages do not share a database snapshot; restart after mirror replacement if needed. Optional arguments accept null as omission; defaulted arguments then use their defaults. Mirror ownership does not independently verify freshness or completeness.

| Argument | Required | Type, including null support | Default | Bounds, enum, and meaning |
| --- | --- | --- | --- | --- |
| `limit` | Optional | integer or null | `250` | minimum 1; maximum 1000. Maximum output rows per page, not a source-scan cost bound. |
| `cursor` | Optional | string or null | None declared; see behavior above | minimum characters 1; maximum characters 4096. Opaque continuation token returned by this same tool; omit or use null on the first request. Never invent a token. |
| `search` | Optional | string or null | None declared; see behavior above | minimum characters 1; maximum characters 256. Literal text filter, not SQL, regex, or caller wildcard syntax; scope is described above. |

Example `tools/call` params:

```json
{
  "name": "list_nav_schemes",
  "arguments": {
    "search": "Parag Parikh",
    "limit": 20
  }
}
```

<a id="tool-get_nav_history"></a>

### `get_nav_history`

Downloads raw MariaDB `MF_NAV_HISTORY` observations for an exact discovered scheme code. Raw NAV is a unit price, not portfolio holdings or distribution-adjusted total returns. Source DOUBLE NAV is represented as database text. Dates must be real calendar dates, inclusive and ordered; omitted bounds use available history. The backend also enforces a maximum code of `2147483647` for string inputs, beyond the catalog's regex.

Follow every continuation for full history. NAV history uses a stable source tie key for same-date rows and does not apply the duplicate-collapse/conflict policy of `get_nav_metrics`. Use the metrics tool for server-side CAGR, Sharpe, and drawdowns after selecting the actual plan/option.

Pagination defaults to 250 rows and permits 1–1,000. First request omits `cursor` or uses null. Continue with the exact returned `next_cursor`, unchanged selectors, search, dates, format, and limit, until `has_more=false`. Pages do not share a database snapshot; restart after mirror replacement if needed. Optional arguments accept null as omission; defaulted arguments then use their defaults. Mirror ownership does not independently verify freshness or completeness.

| Argument | Required | Type, including null support | Default | Bounds, enum, and meaning |
| --- | --- | --- | --- | --- |
| `limit` | Optional | integer or null | `250` | minimum 1; maximum 1000. Maximum output rows per page, not a source-scan cost bound. |
| `cursor` | Optional | string or null | None declared; see behavior above | minimum characters 1; maximum characters 4096. Opaque continuation token returned by this same tool; omit or use null on the first request. Never invent a token. |
| `start` | Optional | string or null | None declared; see behavior above | No additional catalog bounds. Inclusive lower date bound; see this section for snapshot-cutoff or observation semantics. |
| `end` | Optional | string or null | None declared; see behavior above | No additional catalog bounds. Inclusive upper date bound; see this section for omitted-end behavior. |
| `format` | Optional | string or null | `"json"` | enum: `"json"`, `"csv"`. Representation for each bounded history page. csv adds an inline CSV string; it is not an automatic full-history file. |
| `scheme_code` | Required | string or integer | No default | pattern: `^[1-9]\d{0,9}$`; or greater than 0; maximum 2147483647. Exact AMFI/NAV scheme code; discover the code rather than infer it from a fund name. |

Example `tools/call` params:

```json
{
  "name": "get_nav_history",
  "arguments": {
    "scheme_code": 1,
    "start": "2025-01-01",
    "end": "2025-12-31",
    "format": "csv",
    "limit": 250
  }
}
```

<a id="tool-list_strategies"></a>

### `list_strategies`

Lists strategy definitions in the active published research catalog. Use returned exact `strategy_id` values for strategy, portfolio, backtest-link, and signal tools. Publication metadata is not proof that a particular strategy or its observations are available. No caller-controlled pagination.

| Argument | Required | Type, including null support | Default | Bounds, enum, and meaning |
| --- | --- | --- | --- | --- |
| None | — | — | — | Pass an empty arguments object `{}`. |

Example `tools/call` params:

```json
{
  "name": "list_strategies",
  "arguments": {}
}
```

<a id="tool-get_strategy_definition"></a>

### `get_strategy_definition`

Reads one active published research strategy definition, including exact rules and provenance. A definition can include its current published model portfolio; inspect returned content rather than inferring missing rules or holdings. Obtain the exact ID with `list_strategies`; unknown/unpublished records can be null or gated as `data_gap`. No pagination.

| Argument | Required | Type, including null support | Default | Bounds, enum, and meaning |
| --- | --- | --- | --- | --- |
| `strategy_id` | Required | string | No default | No additional catalog bounds. Exact published strategy identifier from list_strategies. |

Example `tools/call` params:

```json
{
  "name": "get_strategy_definition",
  "arguments": {
    "strategy_id": "STRATEGY_ID_FROM_DISCOVERY"
  }
}
```

<a id="tool-get_strategy_portfolio"></a>

### `get_strategy_portfolio`

Reads the current model portfolio embedded in the active published strategy definition, including available scheme names/codes, factors, weights, and as-of information. This is a published model, not a user's holdings, executed trades, or a historical portfolio query. Preserve the returned weight conventions and as-of date; do not assume a snapshot is current today. Obtain the exact ID with `list_strategies`; a missing definition or model portfolio can return null. No pagination.

| Argument | Required | Type, including null support | Default | Bounds, enum, and meaning |
| --- | --- | --- | --- | --- |
| `strategy_id` | Required | string | No default | No additional catalog bounds. Exact published strategy identifier from list_strategies. |

Example `tools/call` params:

```json
{
  "name": "get_strategy_portfolio",
  "arguments": {
    "strategy_id": "STRATEGY_ID_FROM_DISCOVERY"
  }
}
```

<a id="tool-get_strategy_backtest"></a>

### `get_strategy_backtest`

Resolves a published strategy's single explicit `backtest_run_id` link to an active published backtest run. It does not choose the newest run or search by a similar strategy name. Obtain `strategy_id` with `list_strategies`; a missing link or unpublished run can return null. Use the returned run ID for summaries and metrics. No pagination.

| Argument | Required | Type, including null support | Default | Bounds, enum, and meaning |
| --- | --- | --- | --- | --- |
| `strategy_id` | Required | string | No default | No additional catalog bounds. Exact published strategy identifier from list_strategies. |

Example `tools/call` params:

```json
{
  "name": "get_strategy_backtest",
  "arguments": {
    "strategy_id": "STRATEGY_ID_FROM_DISCOVERY"
  }
}
```

<a id="tool-search_backtests"></a>

### `search_backtests`

Lists active published research backtest runs. Without `strategy_id`, returns published runs; with an ID, resolves only that strategy's explicitly linked run, not every historical run associated with the strategy. Discover strategy IDs with `list_strategies` and reuse exact returned `run_id` values. No search-string, date, limit, or cursor arguments. Omit an unused `strategy_id`; explicit null is not accepted.

| Argument | Required | Type, including null support | Default | Bounds, enum, and meaning |
| --- | --- | --- | --- | --- |
| `strategy_id` | Optional | string | None declared; see behavior above | No additional catalog bounds. Exact published strategy identifier from list_strategies. |

Example `tools/call` params:

```json
{
  "name": "search_backtests",
  "arguments": {}
}
```

<a id="tool-compare_strategies"></a>

### `compare_strategies`

Fetches published backtest summaries for 1–10 exact run IDs; it takes run IDs, not strategy IDs. Obtain IDs with `search_backtests` or `get_strategy_backtest`. The implementation sets `comparable` based on whether every summary exists, not on aligned dates, equivalent methodology, matching fees, or equal risk. Inspect summary coverage and provenance before making a performance comparison; no automatic common-window recalculation or winner is implied. No pagination.

| Argument | Required | Type, including null support | Default | Bounds, enum, and meaning |
| --- | --- | --- | --- | --- |
| `run_ids` | Required | array of (string) | No default | minimum items 1; maximum items 10; each item: no additional catalog bound. Published backtest run identifiers, not strategy identifiers. |

Example `tools/call` params:

```json
{
  "name": "compare_strategies",
  "arguments": {
    "run_ids": [
      "RUN_ID_FROM_DISCOVERY"
    ]
  }
}
```

<a id="tool-get_backtest_summary"></a>

### `get_backtest_summary`

Reads an active published `backtest_runs` record and calculates its available full-window per-series metrics from published `backtest_observations`. Obtain the run ID with `search_backtests` or `get_strategy_backtest`. Inspect `metric_status`, returned series, and metric provenance; record availability does not guarantee complete observations. An unknown/unpublished run can return null. No pagination or date arguments; use `get_backtest_metrics` for a custom window.

| Argument | Required | Type, including null support | Default | Bounds, enum, and meaning |
| --- | --- | --- | --- | --- |
| `run_id` | Required | string | No default | No additional catalog bounds. Exact published backtest run identifier from search_backtests or get_strategy_backtest. |

Example `tools/call` params:

```json
{
  "name": "get_backtest_summary",
  "arguments": {
    "run_id": "RUN_ID_FROM_DISCOVERY"
  }
}
```

<a id="tool-get_backtest_metrics"></a>

### `get_backtest_metrics`

Calculates metrics from published monthly `backtest_observations` for an active run. Obtain the run ID with `search_backtests` or `get_strategy_backtest`. Omit `series` to calculate all observed series; exact series labels can be learned from `get_backtest_summary`. Omitted bounds use available observations; reported requested bounds default to run coverage. Bounds select `period_end` inclusively and must be ordered. The deployed schema checks date shape, not a real-calendar-date refinement. Unlike the nullable market/AMFI inputs, optional `series`, `start`, and `end` reject explicit null.

Each selected monthly return is included in full based on its period-end label; dates do not prorate a month. Wealth compounds from an initial value of 1. Metrics use the finance-toolkit wrapper with annualization factor `12`, risk-free rate `0`, Sortino minimum acceptable return `0`, and Calmar numerator equal to annualized arithmetic mean. This is observation-count annualization, not NAV calendar-day CAGR. Returns, volatility, positive-month share, and drawdowns are fractional measures; Sharpe, Sortino, and Calmar are ratios. `MaxDD` is nonpositive; Sortino is null when downside deviation is zero.

At least two observations are needed per series. Unavailable requested series and series with fewer than two observations are omitted; if none qualifies, the tool returns `data_gap`. Duplicate dates, invalid returns, or nonfinite calculations can fail the calculation. Returned metrics do not guarantee that every requested series or calendar month was covered. No cursor, pagination, resampling, or NAV-history fallback.

| Argument | Required | Type, including null support | Default | Bounds, enum, and meaning |
| --- | --- | --- | --- | --- |
| `run_id` | Required | string | No default | No additional catalog bounds. Exact published backtest run identifier from search_backtests or get_strategy_backtest. |
| `series` | Optional | array of (string) | None declared; see behavior above | minimum items 1; maximum items 20; each item: no additional catalog bound. Exact published observation series labels; omit to include every observed series. Learn labels from get_backtest_summary. |
| `start` | Optional | string | None declared; see behavior above | pattern: `^\d{4}-\d{2}-\d{2}$`. Inclusive lower date bound; see this section for snapshot-cutoff or observation semantics. |
| `end` | Optional | string | None declared; see behavior above | pattern: `^\d{4}-\d{2}-\d{2}$`. Inclusive upper date bound; see this section for omitted-end behavior. |

Example `tools/call` params:

```json
{
  "name": "get_backtest_metrics",
  "arguments": {
    "run_id": "RUN_ID_FROM_DISCOVERY",
    "start": "2020-01-01",
    "end": "2025-12-31"
  }
}
```

<a id="tool-get_index_metrics"></a>

### `get_index_metrics`

Calculates full-window daily-level metrics from owned MariaDB `BHAV_INDEX` for up to 20 exact names discovered with `list_indices`. Omitted/null `indices` selects the four configured factor indices: `NIFTY500 LOW VOLATILITY 50 TR`, `NIFTY500 MOMENTUM 50 TR`, `NIFTY500 QUALITY 50 TR`, and `NIFTY500 VALUE 50 TR`. Explicit names are not limited to those four; duplicates are deduplicated. Names must not be blank or contain control characters.

Bounds are inclusive and ordered. Omitted/null start uses available history; omitted/null end uses latest observed data, not today. The schema checks date shape. Each requested index needs at least three levels (two returns), all indices must have identical observation dates, and observed boundaries must reach within seven calendar days of specified bounds. Otherwise the comparison returns `data_gap` without inferring a winner. The winner is highest full-window `TotalReturn`, with name ordering as a tie-breaker—not highest Sharpe.

The finance-toolkit wrapper uses simple consecutive-level returns, annualization factor `252`, risk-free rate `0`, and zero Sortino target. Annualization is based on observation count, not NAV calendar-day CAGR. `FirstValue`, `LatestValue` (dated by `window_end`), `PeakValue`, earliest tied `PeakDate`, and `CurrentDD` summarize the full selected history. Current drawdown is `LatestValue / PeakValue - 1`, a nonpositive fraction from the selected-window peak, not necessarily a lifetime peak. Returns, volatility, positive-day share, and drawdowns are fractions; risk ratios are ratios; Sortino can be null. No cursor or pagination. Raw levels are not inferred adjusted/total-return series; mirror ownership does not independently verify freshness.

| Argument | Required | Type, including null support | Default | Bounds, enum, and meaning |
| --- | --- | --- | --- | --- |
| `indices` | Optional | array of (string) or null | None declared; see behavior above | minimum items 1; maximum items 20; each item: minimum characters 1; maximum characters 256. Exact index names; omitted/null selects the four configured factor indices, not every available index. |
| `start` | Optional | string or null | None declared; see behavior above | pattern: `^\d{4}-\d{2}-\d{2}$`. Inclusive lower date bound; see this section for snapshot-cutoff or observation semantics. |
| `end` | Optional | string or null | None declared; see behavior above | pattern: `^\d{4}-\d{2}-\d{2}$`. Inclusive upper date bound; see this section for omitted-end behavior. |

Example `tools/call` params:

```json
{
  "name": "get_index_metrics",
  "arguments": {
    "indices": [
      "INDEX_NAME_FROM_DISCOVERY"
    ],
    "start": "2025-01-01"
  }
}
```

<a id="tool-get_data_quality"></a>

### `get_data_quality`

Reads publication-catalog status, available counts, coverage/freshness metadata, and validation warnings across research and market/AMFI sources. Reported availability or mirror ownership is not independent proof of source freshness, completeness, or reconciliation. Inspect each source's status and warnings rather than treating a top-level response as confirmation that every dataset is populated. No arguments or pagination.

| Argument | Required | Type, including null support | Default | Bounds, enum, and meaning |
| --- | --- | --- | --- | --- |
| None | — | — | — | Pass an empty arguments object `{}`. |

Example `tools/call` params:

```json
{
  "name": "get_data_quality",
  "arguments": {}
}
```

<a id="tool-explain_signal"></a>

### `explain_signal`

Looks up a published strategy and reports the limitation of explaining an archived factor-momentum decision. The current implementation returns `data_gap` because archived signals with exact decision-time inputs are unavailable; it does not reconstruct a trade signal from realized index returns or invent missing factor history. Obtain `strategy_id` with `list_strategies`. Use `YYYY-MM-DD` for `signal_date` as a convention; the deployed schema only requires a string. There is no historical-signal lookup guarantee or pagination.

| Argument | Required | Type, including null support | Default | Bounds, enum, and meaning |
| --- | --- | --- | --- | --- |
| `strategy_id` | Required | string | No default | No additional catalog bounds. Exact published strategy identifier from list_strategies. |
| `signal_date` | Required | string | No default | No additional catalog bounds. Requested signal date; use YYYY-MM-DD by convention, but schema imposes no date pattern. |

Example `tools/call` params:

```json
{
  "name": "explain_signal",
  "arguments": {
    "strategy_id": "STRATEGY_ID_FROM_DISCOVERY",
    "signal_date": "2025-12-31"
  }
}
```



<a id="dashboard-report-recipes"></a>
## Dashboard report recipes

These recipes cover all 55 code-level dashboard datasets in `dashboard-data-dictionary.md` and `dashboard-lineage.json`. Each recipe names the related report, explains the row grain and units, and supplies MCP `tools/call` parameters for `query_dashboard_dataset`. The mapping traces source facts and implemented transforms; it does not promise full report, chart-pixel, or model parity.

The report links below use existing rendered HTML files, checked with bounded HTTP GET requests on October 27, 2026. Case is significant. Parameterized detail pages are verified examples, not a complete list of every equity, ETF, index, industry, fund, or manager page. An R producer or helper does not automatically have an HTML route. For example, `rp-amfi-mktcap.Rmd` renders to `rp-MKT-CAP.html`; helper files such as `common/fan-chart.R` have no report link.

### Discover before filtering

Call `list_dashboard_datasets` before querying a dataset or adding filters:

```json
{
  "name": "list_dashboard_datasets",
  "arguments": {
    "limit": 100
  }
}
```

Treat its published inventory, column/type pairs, and metadata as authoritative. A code-level contract does not prove that a table is published, populated, or fresh. The deployed tool schemas were captured through public `tools/list`. Protected dashboard calls were not executed for this documentation pass, so live row counts, source quality, cutoffs, and published dataset schemas were not rechecked. The examples are request structures, not successful-response claims. Most use a two-row preview; optional filter columns were checked against the producer contract and must also appear in your live catalog.

When the catalog is reachable:

- Check the dataset's publication generation, refresh/source dates, quality, warnings, and limitations. Missing publication or `data_gap` is not a zero observation. Distinguish an authoritative empty view from an unavailable or partial input.
- Use only advertised textual or integer columns for `entity_column`; never use DOUBLE, DECIMAL, or DATE columns there. Text matching is literal, case-insensitive substring matching. Integer matching is exact; pass a canonical signed decimal string without a leading plus or leading zeros.
- Use an advertised DATE/DATETIME column for `date_column`. `start` and `end` are inclusive. Date columns are listed separately in each recipe as code-schema candidates, not evidence of live advertisement.
- The tool accepts one entity-column filter and one date-column filter. It does not accept SQL, arbitrary joins, a list of filters, or a report URL in place of `dataset_name`. Apply other selections and joins in your client.
- The limit is at most 200 rows. These two-row samples are previews, not complete histories or aggregates. Continue with `next_cursor` unchanged and the identical dataset, filters, and limit. If publication/refresh changes invalidate the cursor, restart the query. The publisher adds `ROW_ID BIGINT` for paging; it is not an economic key.
- Returned numeric values remain database text. Parse them deliberately and preserve NULL. All listed analytical grains are descriptions, not extra UNIQUE constraints; retain conflicting source occurrences.

Source observation dates are not publication-time or revision-vintage dates. Current cohorts, aliases, reference CSVs, and metadata can apply backward to selected history. Default compact return curves are weekly; daily, monthly, and yearly frequencies require loader opt-ins and cannot be created by changing query filters.

<a id="pms-worked-example"></a>
### Worked example: PMS report facts

The [PMS master report](https://stockviz.github.io/reports03/pms/rp-IN.html) is rendered by `reports03/pms/rp-IN.R` from `rp-IN.Rmd`. It shows manager discretionary AUM and recent strategy performance. The [manager detail example](https://stockviz.github.io/reports03/pms/analysis/rp-PMS.INP000000187.html) comes from `rp-PMS.Rmd`; the producer uses the SEBI registration in `analysis/rp-PMS.<SEBI_ID>.html`, not the internal numeric manager ID.

Start with the three fact tables. Each object below is the parameters object for a separate MCP `tools/call` request:

```json
{
  "name": "query_dashboard_dataset",
  "arguments": {
    "dataset_name": "DASHBOARD_PMS_META",
    "limit": 2
  }
}
```

```json
{
  "name": "query_dashboard_dataset",
  "arguments": {
    "dataset_name": "DASHBOARD_PMS_AUM",
    "limit": 2
  }
}
```

```json
{
  "name": "query_dashboard_dataset",
  "arguments": {
    "dataset_name": "DASHBOARD_PMS_MONTHLY",
    "limit": 2
  }
}
```

| Report fact | Dataset and fields | What you still need to do |
| --- | --- | --- |
| Manager name and registration | `DASHBOARD_PMS_META`: `ID`, `PMS_NAME`, `SEBI_ID` | Join other PMS facts on internal `ID`; use `SEBI_ID` to identify the existing detail page. Metadata is undated/current-state. |
| Discretionary manager AUM and its observation month | `DASHBOARD_PMS_AUM`: `ID`, `AS_OF`, `AUM_INR_CR` | Page through the chosen history, select the latest observed month per manager, and join names. The report applies further display/strategy eligibility joins; this table alone does not reproduce its displayed manager list. |
| Strategy name, monthly return, strategy AUM, and asset label | `DASHBOARD_PMS_MONTHLY`: `ID`, `AS_OF`, `STRATEGY`, `SOURCE_STRATEGY`, `RETURN`, `AUM_INR_CR`, `ASSET_CLASS`, `FORMAT` | `RETURN` is decimal, so multiply by 100 for percent display. Preserve source names and format-era diagnostics; do not sum conflicting/overlapping strategy AUM or confuse it with manager summary AUM. |
| Strategy count in the master AUM table | No emitted report-equivalent count | The Rmd counts non-total/nonzero `fundsInflow.investmentApproach` rows at each manager's latest month. Counting normalized performance strategies is not certified equivalent. |
| Recent strategy annualized return, Sharpe, and information ratio | Not stored in these three tables | The report reads a producer-generated `fileTracker` and applies recent-date/AUM gates. The producer computes benchmark-aligned annualized return, risk-free Sharpe, and IR (IR multiplied by 100). A monthly return column is not any of these statistics. |
| AUM growth and latest-two-month average | Underlying monthly facts only, where supplied | Require explicit calculations, source-era coverage, and the report's eligibility/window rules. Do not label them as precomputed report fields. |

After the live catalog confirms `SEBI_ID` as a textual entity column, this request locates metadata related to the verified manager page (substring match, not a relational lookup):

```json
{
  "name": "query_dashboard_dataset",
  "arguments": {
    "dataset_name": "DASHBOARD_PMS_META",
    "entity_column": "SEBI_ID",
    "entity": "INP000000187",
    "limit": 2
  }
}
```

After it confirms `AS_OF` as a date column, this request previews complete-month strategy facts in an illustrative date interval, across managers:

```json
{
  "name": "query_dashboard_dataset",
  "arguments": {
    "dataset_name": "DASHBOARD_PMS_MONTHLY",
    "date_column": "AS_OF",
    "start": "2026-01-01",
    "end": "2026-09-30",
    "limit": 2
  }
}
```

For a single manager, copy the returned `ID` exactly into `entity` with `entity_column` set to `ID`, after confirming that integer column in the catalog. The API requires the integer as a JSON string. Do not use `SEBI_ID` on the monthly/AUM tables or `ENTITY` on any of these three PMS schemas. Page fully before choosing latest months, computing growth, or joining.

The PMS loader normalizes pre-2021 manager summaries, 2021 arrays, and later flat/nested approach formats. `DASHBOARD_PMS_AUM` specifically extracts discretionary summary AUM where that source structure exists; older monthly strategy/manager AUM is not an interchangeable replacement. Regex aliases can reflect current state, flat-format asset classes remain NULL, and only completed month-ends at or before cutoff survive. Exact normalized duplicates collapse, but distinct rows with the same canonical manager/month/strategy key remain. Check `quality`, `conflicting_key_count`, and warnings before calculating: conflicting observations are not independent strategies and must not be silently first-wins or summed. Malformed JSON fails instead of silently skipping a manager.

These tables provide upstream facts for the report. They do not expose its cached `fileTracker`, factor/composite benchmark paths, strategy eligibility rules, leaderboards, or exact chart transforms. Recomputing statistics requires separate benchmark/risk-free inputs and an explicit method; it is not analytical parity merely because the inputs are available.

<a id="report-to-dataset-coverage"></a>
### Report-to-dataset coverage

The table lists every linked report page in this fragment. Detail pages stand for parameterized report families. Dataset links lead to contracts and request examples below; a relationship means related facts, not complete output reproduction. The mapping follows report source templates and producer lineage; linked detail pages are verified representative pages.

| Verified report page | Related datasets |
| --- | --- |
| [reports01/eq/52wk-IN.html](https://stockviz.github.io/reports01/eq/52wk-IN.html) | [EQUITY_TECHNICAL](#dataset-DASHBOARD_EQUITY_TECHNICAL), [EQUITY_UNIVERSE](#dataset-DASHBOARD_EQUITY_UNIVERSE), [INDEX_MEMBERSHIP](#dataset-DASHBOARD_INDEX_MEMBERSHIP) |
| [reports01/eq/52wk-US.html](https://stockviz.github.io/reports01/eq/52wk-US.html) | [EQUITY_TECHNICAL](#dataset-DASHBOARD_EQUITY_TECHNICAL), [EQUITY_UNIVERSE](#dataset-DASHBOARD_EQUITY_UNIVERSE), [ETF_CONSTITUENTS](#dataset-DASHBOARD_ETF_CONSTITUENTS) |
| [reports01/eq/ath-IN.html](https://stockviz.github.io/reports01/eq/ath-IN.html) | [EQUITY_TECHNICAL](#dataset-DASHBOARD_EQUITY_TECHNICAL), [EQUITY_UNIVERSE](#dataset-DASHBOARD_EQUITY_UNIVERSE), [INDEX_MEMBERSHIP](#dataset-DASHBOARD_INDEX_MEMBERSHIP) |
| [reports01/eq/ath-US.html](https://stockviz.github.io/reports01/eq/ath-US.html) | [EQUITY_TECHNICAL](#dataset-DASHBOARD_EQUITY_TECHNICAL), [EQUITY_UNIVERSE](#dataset-DASHBOARD_EQUITY_UNIVERSE), [ETF_CONSTITUENTS](#dataset-DASHBOARD_ETF_CONSTITUENTS) |
| [reports01/eq/drawdowns-IN.html](https://stockviz.github.io/reports01/eq/drawdowns-IN.html) | [EQUITY_TECHNICAL](#dataset-DASHBOARD_EQUITY_TECHNICAL), [EQUITY_UNIVERSE](#dataset-DASHBOARD_EQUITY_UNIVERSE), [INDEX_MEMBERSHIP](#dataset-DASHBOARD_INDEX_MEMBERSHIP) |
| [reports01/eq/drawdowns-US.html](https://stockviz.github.io/reports01/eq/drawdowns-US.html) | [EQUITY_TECHNICAL](#dataset-DASHBOARD_EQUITY_TECHNICAL), [EQUITY_UNIVERSE](#dataset-DASHBOARD_EQUITY_UNIVERSE), [ETF_CONSTITUENTS](#dataset-DASHBOARD_ETF_CONSTITUENTS) |
| [reports01/eq/results-IN.html](https://stockviz.github.io/reports01/eq/results-IN.html) | [EARNINGS_CALENDAR](#dataset-DASHBOARD_EARNINGS_CALENDAR), [INDEX_MEMBERSHIP](#dataset-DASHBOARD_INDEX_MEMBERSHIP) |
| [reports01/eq/streaks-IN.html](https://stockviz.github.io/reports01/eq/streaks-IN.html) | [EQUITY_STREAK](#dataset-DASHBOARD_EQUITY_STREAK), [EQUITY_UNIVERSE](#dataset-DASHBOARD_EQUITY_UNIVERSE), [INDEX_MEMBERSHIP](#dataset-DASHBOARD_INDEX_MEMBERSHIP) |
| [reports01/eq/streaks-US.html](https://stockviz.github.io/reports01/eq/streaks-US.html) | [EQUITY_STREAK](#dataset-DASHBOARD_EQUITY_STREAK), [EQUITY_UNIVERSE](#dataset-DASHBOARD_EQUITY_UNIVERSE), [ETF_CONSTITUENTS](#dataset-DASHBOARD_ETF_CONSTITUENTS) |
| [reports01/index/analysis/rp-NIFTY50.html](https://stockviz.github.io/reports01/index/analysis/rp-NIFTY50.html) | [COMPOSITION_CHANGE](#dataset-DASHBOARD_COMPOSITION_CHANGE), [INDEX_MEMBERSHIP](#dataset-DASHBOARD_INDEX_MEMBERSHIP) |
| [reports01/index/industry/rp-23Wheelers.html](https://stockviz.github.io/reports01/index/industry/rp-23Wheelers.html) | [INDUSTRY_FUNDAMENTALS](#dataset-DASHBOARD_INDUSTRY_FUNDAMENTALS), [INDUSTRY_MEMBERS](#dataset-DASHBOARD_INDUSTRY_MEMBERS), [INDUSTRY_NARRATIVES](#dataset-DASHBOARD_INDUSTRY_NARRATIVES), [INDUSTRY_STATISTICS](#dataset-DASHBOARD_INDUSTRY_STATISTICS), [MARKET_DISTRIBUTION](#dataset-DASHBOARD_MARKET_DISTRIBUTION), [MARKET_HORIZON](#dataset-DASHBOARD_MARKET_HORIZON), [MARKET_RISK](#dataset-DASHBOARD_MARKET_RISK), [MARKET_SERIES](#dataset-DASHBOARD_MARKET_SERIES), [MARKET_SMA](#dataset-DASHBOARD_MARKET_SMA), [METRIC_DICTIONARY](#dataset-DASHBOARD_METRIC_DICTIONARY) |
| [reports01/index/risk/rp-NIFTY50TR.html](https://stockviz.github.io/reports01/index/risk/rp-NIFTY50TR.html) | [INDEX_RISK](#dataset-DASHBOARD_INDEX_RISK), [MARKET_DISTRIBUTION](#dataset-DASHBOARD_MARKET_DISTRIBUTION), [MARKET_HORIZON](#dataset-DASHBOARD_MARKET_HORIZON), [MARKET_RISK](#dataset-DASHBOARD_MARKET_RISK), [MARKET_SERIES](#dataset-DASHBOARD_MARKET_SERIES), [MARKET_SMA](#dataset-DASHBOARD_MARKET_SMA) |
| [reports01/index/rp-IN.html](https://stockviz.github.io/reports01/index/rp-IN.html) | [COMPOSITION_CHANGE](#dataset-DASHBOARD_COMPOSITION_CHANGE), [INDEX_MEMBERSHIP](#dataset-DASHBOARD_INDEX_MEMBERSHIP) |
| [reports01/index/rp-MKT-CAP.html](https://stockviz.github.io/reports01/index/rp-MKT-CAP.html) | [COMPOSITION_CHANGE](#dataset-DASHBOARD_COMPOSITION_CHANGE) |
| [reports01/index/rp-industry.html](https://stockviz.github.io/reports01/index/rp-industry.html) | [MARKET_DISTRIBUTION](#dataset-DASHBOARD_MARKET_DISTRIBUTION), [MARKET_HORIZON](#dataset-DASHBOARD_MARKET_HORIZON), [MARKET_RISK](#dataset-DASHBOARD_MARKET_RISK), [MARKET_SERIES](#dataset-DASHBOARD_MARKET_SERIES), [MARKET_SMA](#dataset-DASHBOARD_MARKET_SMA), [METRIC_DICTIONARY](#dataset-DASHBOARD_METRIC_DICTIONARY) |
| [reports01/index/rp-risk.html](https://stockviz.github.io/reports01/index/rp-risk.html) | [INDEX_RISK](#dataset-DASHBOARD_INDEX_RISK), [MARKET_DISTRIBUTION](#dataset-DASHBOARD_MARKET_DISTRIBUTION), [MARKET_HORIZON](#dataset-DASHBOARD_MARKET_HORIZON), [MARKET_RISK](#dataset-DASHBOARD_MARKET_RISK), [MARKET_SERIES](#dataset-DASHBOARD_MARKET_SERIES), [MARKET_SMA](#dataset-DASHBOARD_MARKET_SMA), [METRIC_DICTIONARY](#dataset-DASHBOARD_METRIC_DICTIONARY) |
| [reports01/index/rp-syn.html](https://stockviz.github.io/reports01/index/rp-syn.html) | [DISPERSION](#dataset-DASHBOARD_DISPERSION), [MARKET_DISTRIBUTION](#dataset-DASHBOARD_MARKET_DISTRIBUTION), [MARKET_HORIZON](#dataset-DASHBOARD_MARKET_HORIZON), [MARKET_RISK](#dataset-DASHBOARD_MARKET_RISK), [MARKET_SERIES](#dataset-DASHBOARD_MARKET_SERIES), [MARKET_SMA](#dataset-DASHBOARD_MARKET_SMA) |
| [reports01/index/rp-valuations.html](https://stockviz.github.io/reports01/index/rp-valuations.html) | [CONSTITUENT_VALUATION](#dataset-DASHBOARD_CONSTITUENT_VALUATION), [VALUATION](#dataset-DASHBOARD_VALUATION) |
| [reports01/index/rp-vol-NIFTY.html](https://stockviz.github.io/reports01/index/rp-vol-NIFTY.html) | [OPTION_IV](#dataset-DASHBOARD_OPTION_IV), [OPTION_POSITIONING](#dataset-DASHBOARD_OPTION_POSITIONING), [REALIZED_VOL](#dataset-DASHBOARD_REALIZED_VOL), [VIX](#dataset-DASHBOARD_VIX), [VIX_FORWARD_SAMPLE](#dataset-DASHBOARD_VIX_FORWARD_SAMPLE) |
| [reports01/macro/rp-bnd.html](https://stockviz.github.io/reports01/macro/rp-bnd.html) | [MARKET_DISTRIBUTION](#dataset-DASHBOARD_MARKET_DISTRIBUTION), [MARKET_HORIZON](#dataset-DASHBOARD_MARKET_HORIZON), [MARKET_RISK](#dataset-DASHBOARD_MARKET_RISK), [MARKET_SERIES](#dataset-DASHBOARD_MARKET_SERIES), [MARKET_SMA](#dataset-DASHBOARD_MARKET_SMA), [YIELD_CURVE](#dataset-DASHBOARD_YIELD_CURVE) |
| [reports01/macro/rp-cmdy.html](https://stockviz.github.io/reports01/macro/rp-cmdy.html) | [CME_FRONT_CONTRACT](#dataset-DASHBOARD_CME_FRONT_CONTRACT), [MARKET_DISTRIBUTION](#dataset-DASHBOARD_MARKET_DISTRIBUTION), [MARKET_HORIZON](#dataset-DASHBOARD_MARKET_HORIZON), [MARKET_RISK](#dataset-DASHBOARD_MARKET_RISK), [MARKET_SERIES](#dataset-DASHBOARD_MARKET_SERIES), [MARKET_SMA](#dataset-DASHBOARD_MARKET_SMA) |
| [reports01/macro/rp-cur.html](https://stockviz.github.io/reports01/macro/rp-cur.html) | [MARKET_DISTRIBUTION](#dataset-DASHBOARD_MARKET_DISTRIBUTION), [MARKET_HORIZON](#dataset-DASHBOARD_MARKET_HORIZON), [MARKET_RISK](#dataset-DASHBOARD_MARKET_RISK), [MARKET_SERIES](#dataset-DASHBOARD_MARKET_SERIES), [MARKET_SMA](#dataset-DASHBOARD_MARKET_SMA) |
| [reports02/eq-in/risk/in.RELIANCE.html](https://stockviz.github.io/reports02/eq-in/risk/in.RELIANCE.html) | [BROKER_NARRATIVES](#dataset-DASHBOARD_BROKER_NARRATIVES), [BROKER_TIMELINE](#dataset-DASHBOARD_BROKER_TIMELINE), [EQUITY_NARRATIVES](#dataset-DASHBOARD_EQUITY_NARRATIVES), [EQ_IN_FINANCIALS](#dataset-DASHBOARD_EQ_IN_FINANCIALS), [EQ_IN_FREE_FLOAT](#dataset-DASHBOARD_EQ_IN_FREE_FLOAT), [EQ_IN_MTF](#dataset-DASHBOARD_EQ_IN_MTF), [EQ_IN_OWNERSHIP](#dataset-DASHBOARD_EQ_IN_OWNERSHIP), [EQ_IN_RETURNS](#dataset-DASHBOARD_EQ_IN_RETURNS) |
| [reports02/eq-in/rp-margin.html](https://stockviz.github.io/reports02/eq-in/rp-margin.html) | [EQ_IN_MARGIN](#dataset-DASHBOARD_EQ_IN_MARGIN) |
| [reports02/etf-us/analysis/rp-AAXJ.html](https://stockviz.github.io/reports02/etf-us/analysis/rp-AAXJ.html) | [ETF_CONSTITUENTS](#dataset-DASHBOARD_ETF_CONSTITUENTS), [ETF_META](#dataset-DASHBOARD_ETF_META) |
| [reports02/etf-us/risk/rp-IVV.html](https://stockviz.github.io/reports02/etf-us/risk/rp-IVV.html) | [ETF_CAPM](#dataset-DASHBOARD_ETF_CAPM), [ETF_COHORT](#dataset-DASHBOARD_ETF_COHORT), [ETF_META](#dataset-DASHBOARD_ETF_META), [ETF_REGRESSION](#dataset-DASHBOARD_ETF_REGRESSION), [ETF_RETURNS](#dataset-DASHBOARD_ETF_RETURNS), [ETF_RISK](#dataset-DASHBOARD_ETF_RISK) |
| [reports02/etf-us/rp-country.html](https://stockviz.github.io/reports02/etf-us/rp-country.html) | [COUNTRY_ETF_REFERENCE](#dataset-DASHBOARD_COUNTRY_ETF_REFERENCE), [ETF_COHORT](#dataset-DASHBOARD_ETF_COHORT), [ETF_META](#dataset-DASHBOARD_ETF_META), [ETF_RETURNS](#dataset-DASHBOARD_ETF_RETURNS) |
| [reports02/etf-us/rp-fama-french-factors.html](https://stockviz.github.io/reports02/etf-us/rp-fama-french-factors.html) | [FF_DEFS](#dataset-DASHBOARD_FF_DEFS), [FF_RETURNS](#dataset-DASHBOARD_FF_RETURNS) |
| [reports02/etf-us/rp-fama-french-industry.html](https://stockviz.github.io/reports02/etf-us/rp-fama-french-industry.html) | [FF_DEFS](#dataset-DASHBOARD_FF_DEFS), [FF_RETURNS](#dataset-DASHBOARD_FF_RETURNS) |
| [reports02/etf-us/rp-fama-french-regression.html](https://stockviz.github.io/reports02/etf-us/rp-fama-french-regression.html) | [ETF_COHORT](#dataset-DASHBOARD_ETF_COHORT), [ETF_META](#dataset-DASHBOARD_ETF_META), [FF_DEFS](#dataset-DASHBOARD_FF_DEFS), [FF_REGRESSION](#dataset-DASHBOARD_FF_REGRESSION) |
| [reports02/etf-us/rp-risk.html](https://stockviz.github.io/reports02/etf-us/rp-risk.html) | [ETF_CAPM](#dataset-DASHBOARD_ETF_CAPM), [ETF_COHORT](#dataset-DASHBOARD_ETF_COHORT), [ETF_META](#dataset-DASHBOARD_ETF_META), [ETF_REGRESSION](#dataset-DASHBOARD_ETF_REGRESSION), [ETF_RETURNS](#dataset-DASHBOARD_ETF_RETURNS), [ETF_RISK](#dataset-DASHBOARD_ETF_RISK), [METRIC_DICTIONARY](#dataset-DASHBOARD_METRIC_DICTIONARY) |
| [reports02/etf-us/rp-sector.html](https://stockviz.github.io/reports02/etf-us/rp-sector.html) | [ETF_COHORT](#dataset-DASHBOARD_ETF_COHORT), [ETF_META](#dataset-DASHBOARD_ETF_META), [ETF_RETURNS](#dataset-DASHBOARD_ETF_RETURNS) |
| [reports03/mf/analysis/rp-118269.html](https://stockviz.github.io/reports03/mf/analysis/rp-118269.html) | [INDEX_RETURNS](#dataset-DASHBOARD_INDEX_RETURNS), [METRIC_DICTIONARY](#dataset-DASHBOARD_METRIC_DICTIONARY), [MF_CAPM](#dataset-DASHBOARD_MF_CAPM), [MF_COHORT](#dataset-DASHBOARD_MF_COHORT), [MF_REGRESSION](#dataset-DASHBOARD_MF_REGRESSION), [MF_RETURNS](#dataset-DASHBOARD_MF_RETURNS) |
| [reports03/mf/rp-IN.html](https://stockviz.github.io/reports03/mf/rp-IN.html) | [INDEX_RETURNS](#dataset-DASHBOARD_INDEX_RETURNS), [METRIC_DICTIONARY](#dataset-DASHBOARD_METRIC_DICTIONARY), [MF_COHORT](#dataset-DASHBOARD_MF_COHORT), [MF_REGRESSION](#dataset-DASHBOARD_MF_REGRESSION), [MF_RETURNS](#dataset-DASHBOARD_MF_RETURNS) |
| [reports03/pms/analysis/rp-PMS.INP000000187.html](https://stockviz.github.io/reports03/pms/analysis/rp-PMS.INP000000187.html) | [PMS_AUM](#dataset-DASHBOARD_PMS_AUM), [PMS_META](#dataset-DASHBOARD_PMS_META), [PMS_MONTHLY](#dataset-DASHBOARD_PMS_MONTHLY) |
| [reports03/pms/rp-IN.html](https://stockviz.github.io/reports03/pms/rp-IN.html) | [PMS_AUM](#dataset-DASHBOARD_PMS_AUM), [PMS_META](#dataset-DASHBOARD_PMS_META), [PMS_MONTHLY](#dataset-DASHBOARD_PMS_MONTHLY) |

### Dataset recipes

Each fenced JSON object is the argument object for `query_dashboard_dataset`, not a fabricated response. Columns below exclude publisher-added `ROW_ID`. Filter candidates come from the code schema; confirm the deployed catalog before using them. Columns not in the entity/date lists are still returned facts, but are not valid entity/date filters under this tool's type rules.

<a id="dataset-DASHBOARD_BROKER_NARRATIVES"></a>
#### `DASHBOARD_BROKER_NARRATIVES`

Broker narrative text for eligible Indian equity detail pages.

- Grain and analytical keys: ENTITY, undated source row.
- Units: CONTENT_JSON.NARRATIVE is text; AS_OF is NULL.
- Columns: `ENTITY`, `AS_OF`, `CONTENT_JSON`.
- Code-schema filter candidates: textual entity columns `ENTITY`, `CONTENT_JSON`; exact integer entity columns none; date columns `AS_OF`.
- Related reports: [reports02/eq-in/risk/in.RELIANCE.html](https://stockviz.github.io/reports02/eq-in/risk/in.RELIANCE.html).
- Limits: Current SQLite RR_NARRATIVE only; no historical vintage or broker-author join.

```json
{
  "name": "query_dashboard_dataset",
  "arguments": {
    "dataset_name": "DASHBOARD_BROKER_NARRATIVES",
    "limit": 2
  }
}
```

<a id="dataset-DASHBOARD_BROKER_TIMELINE"></a>
#### `DASHBOARD_BROKER_TIMELINE`

Broker recommendation and outcome timeline for eligible equities.

- Grain and analytical keys: ENTITY, AS_OF, source recommendation occurrence.
- Units: CONTENT_JSON retains RECOMMENDATION, PREDICTED_RETURN, ACTUAL_RETURN, TARGET_DATE, and OUTCOME in source units.
- Columns: `ENTITY`, `AS_OF`, `CONTENT_JSON`.
- Code-schema filter candidates: textual entity columns `ENTITY`, `CONTENT_JSON`; exact integer entity columns none; date columns `AS_OF`.
- Related reports: [reports02/eq-in/risk/in.RELIANCE.html](https://stockviz.github.io/reports02/eq-in/risk/in.RELIANCE.html).
- Limits: Do not infer return scaling from field names. Invalid dates remain in JSON with NULL AS_OF and partial quality; blank recommendations are excluded.

```json
{
  "name": "query_dashboard_dataset",
  "arguments": {
    "dataset_name": "DASHBOARD_BROKER_TIMELINE",
    "limit": 2
  }
}
```

<a id="dataset-DASHBOARD_CME_FRONT_CONTRACT"></a>
#### `DASHBOARD_CME_FRONT_CONTRACT`

CME contract facts related to the commodity report's defined helper.

- Grain and analytical keys: PRODUCT_SYMBOL, CONTRACT, OBSERVED_DATE.
- Units: SETTLE and PRIOR_SETTLE retain contract quotations; VOLUME and PRIOR_OPEN_INTEREST retain native counts.
- Columns: `PRODUCT_SYMBOL`, `PRODUCT_DESCRIPTION`, `CONTRACT`, `CONTRACT_YEAR`, `CONTRACT_MONTH`, `CONTRACT_DAY`, `OBSERVED_DATE`, `SETTLE`, `PRIOR_SETTLE`, `VOLUME`, `PRIOR_OPEN_INTEREST`.
- Code-schema filter candidates: textual entity columns `PRODUCT_SYMBOL`, `PRODUCT_DESCRIPTION`, `CONTRACT`; exact integer entity columns `CONTRACT_YEAR`, `CONTRACT_MONTH`, `CONTRACT_DAY`; date columns `OBSERVED_DATE`.
- Related reports: [reports01/macro/rp-cmdy.html](https://stockviz.github.io/reports01/macro/rp-cmdy.html).
- Limits: The helper has no active caller. Contract year/month equals observation year/month; this is not a nearest-unexpired continuous or investable futures series.

```json
{
  "name": "query_dashboard_dataset",
  "arguments": {
    "dataset_name": "DASHBOARD_CME_FRONT_CONTRACT",
    "limit": 2
  }
}
```

<a id="dataset-DASHBOARD_COMPOSITION_CHANGE"></a>
#### `DASHBOARD_COMPOSITION_CHANGE`

Observed additions and removals for Indian index or AMFI market-cap snapshots.

- Grain and analytical keys: KIND, ENTITY, PREVIOUS_DATE, OBSERVED_DATE, SYMBOL, CHANGE.
- Units: CHANGE is ADDED or REMOVED; dates identify adjacent observed snapshots.
- Columns: `KIND`, `ENTITY`, `PREVIOUS_DATE`, `OBSERVED_DATE`, `SYMBOL`, `CHANGE`.
- Code-schema filter candidates: textual entity columns `KIND`, `ENTITY`, `SYMBOL`, `CHANGE`; exact integer entity columns none; date columns `PREVIOUS_DATE`, `OBSERVED_DATE`.
- Related reports: [reports01/index/analysis/rp-NIFTY50.html](https://stockviz.github.io/reports01/index/analysis/rp-NIFTY50.html), [reports01/index/rp-IN.html](https://stockviz.github.io/reports01/index/rp-IN.html), [reports01/index/rp-MKT-CAP.html](https://stockviz.github.io/reports01/index/rp-MKT-CAP.html).
- Limits: No initial additions, inferred causal replacements, or full point-in-time membership reconstruction.

```json
{
  "name": "query_dashboard_dataset",
  "arguments": {
    "dataset_name": "DASHBOARD_COMPOSITION_CHANGE",
    "limit": 2
  }
}
```

<a id="dataset-DASHBOARD_CONSTITUENT_VALUATION"></a>
#### `DASHBOARD_CONSTITUENT_VALUATION`

Constituent PE and cap weight used as inputs to index valuation comparisons.

- Grain and analytical keys: ENTITY, SYMBOL, OBSERVED_DATE.
- Units: PE is a ratio; CAP_WEIGHT retains source weight convention.
- Columns: `ENTITY`, `SYMBOL`, `OBSERVED_DATE`, `PE`, `CAP_WEIGHT`.
- Code-schema filter candidates: textual entity columns `ENTITY`, `SYMBOL`; exact integer entity columns none; date columns `OBSERVED_DATE`.
- Related reports: [reports01/index/rp-valuations.html](https://stockviz.github.io/reports01/index/rp-valuations.html).
- Limits: Uses latest available membership at each financial date, unlike the report's current-members-for-both-years comparison. Paired prior-year/log-PE bubbles are not stored.

```json
{
  "name": "query_dashboard_dataset",
  "arguments": {
    "dataset_name": "DASHBOARD_CONSTITUENT_VALUATION",
    "limit": 2
  }
}
```

<a id="dataset-DASHBOARD_COUNTRY_ETF_REFERENCE"></a>
#### `DASHBOARD_COUNTRY_ETF_REFERENCE`

Ordered ticker reference for country ETF comparisons.

- Grain and analytical keys: SYMBOL, DISPLAY_ORDER.
- Units: SYMBOL is a ticker; DISPLAY_ORDER is a sequence number.
- Columns: `SYMBOL`, `DISPLAY_ORDER`.
- Code-schema filter candidates: textual entity columns `SYMBOL`; exact integer entity columns `DISPLAY_ORDER`; date columns none.
- Related reports: [reports02/etf-us/rp-country.html](https://stockviz.github.io/reports02/etf-us/rp-country.html).
- Limits: Reads COUNTRY_ETFS.csv; it does not provide a country-name classification. Missing optional CSV is unavailable, not an empty country universe.

```json
{
  "name": "query_dashboard_dataset",
  "arguments": {
    "dataset_name": "DASHBOARD_COUNTRY_ETF_REFERENCE",
    "limit": 2
  }
}
```

<a id="dataset-DASHBOARD_DISPERSION"></a>
#### `DASHBOARD_DISPERSION`

Upstream synthetic CNX500 dispersion score series.

- Grain and analytical keys: OBSERVED_DATE, LOOK_BACK.
- Units: LOOK_BACK retains source lookback; SCORE_CNX500 is source-native.
- Columns: `OBSERVED_DATE`, `LOOK_BACK`, `SCORE_CNX500`.
- Code-schema filter candidates: textual entity columns none; exact integer entity columns `LOOK_BACK`; date columns `OBSERVED_DATE`.
- Related reports: [reports01/index/rp-syn.html](https://stockviz.github.io/reports01/index/rp-syn.html).
- Limits: The synthetic strategy model is upstream and unresolved; source observations do not establish model parity.

```json
{
  "name": "query_dashboard_dataset",
  "arguments": {
    "dataset_name": "DASHBOARD_DISPERSION",
    "limit": 2
  }
}
```

<a id="dataset-DASHBOARD_EARNINGS_CALENDAR"></a>
#### `DASHBOARD_EARNINGS_CALENDAR`

Upcoming result-related events already disclosed by the cutoff.

- Grain and analytical keys: EVENT_ID, SYMBOL, EVENT_DATE; multiple events per symbol are intentional.
- Units: FF_MKT_CAP_CR is INR crore; IS_FNO is an indicator; TITLE is text.
- Columns: `EVENT_ID`, `SYMBOL`, `DISCLOSURE_DATE`, `EVENT_DATE`, `TITLE`, `INDUSTRY`, `FF_MKT_CAP_CR`, `MISC_DATE`, `FNO_DATE`, `IS_FNO`.
- Code-schema filter candidates: textual entity columns `SYMBOL`, `TITLE`, `INDUSTRY`; exact integer entity columns `EVENT_ID`, `IS_FNO`; date columns `DISCLOSURE_DATE`, `EVENT_DATE`, `MISC_DATE`, `FNO_DATE`.
- Related reports: [reports01/eq/results-IN.html](https://stockviz.github.io/reports01/eq/results-IN.html).
- Limits: EVENT_DATE may be after the cutoff. BSE industry is current-state; membership joins separately by SYMBOL. Missing industry/cap remains NULL.

```json
{
  "name": "query_dashboard_dataset",
  "arguments": {
    "dataset_name": "DASHBOARD_EARNINGS_CALENDAR",
    "limit": 2
  }
}
```

<a id="dataset-DASHBOARD_EQUITY_NARRATIVES"></a>
#### `DASHBOARD_EQUITY_NARRATIVES`

Latest report-used equity summary text.

- Grain and analytical keys: ENTITY, AS_OF, source prompt/snapshot occurrence.
- Units: CONTENT_JSON contains SYMBOL, AS_OF, PROMPT, and SUMMARY text.
- Columns: `ENTITY`, `AS_OF`, `CONTENT_JSON`.
- Code-schema filter candidates: textual entity columns `ENTITY`, `CONTENT_JSON`; exact integer entity columns none; date columns `AS_OF`.
- Related reports: [reports02/eq-in/risk/in.RELIANCE.html](https://stockviz.github.io/reports02/eq-in/risk/in.RELIANCE.html).
- Limits: Preserves tied latest source rows. A missing SQLite file yields unavailable quality, not proof of no summary.

```json
{
  "name": "query_dashboard_dataset",
  "arguments": {
    "dataset_name": "DASHBOARD_EQUITY_NARRATIVES",
    "limit": 2
  }
}
```

<a id="dataset-DASHBOARD_EQUITY_STREAK"></a>
#### `DASHBOARD_EQUITY_STREAK`

Latest qualifying directional excess-return streak against the report benchmark.

- Grain and analytical keys: MARKET, SYMBOL, BENCHMARK, OBSERVED_DATE.
- Units: SESSIONS is a count; RETURN_PCT is compounded stock return percent, not compounded excess return.
- Columns: `MARKET`, `SYMBOL`, `BENCHMARK`, `OBSERVED_DATE`, `DIRECTION`, `SESSIONS`, `RETURN_PCT`.
- Code-schema filter candidates: textual entity columns `MARKET`, `SYMBOL`, `BENCHMARK`, `DIRECTION`; exact integer entity columns `SESSIONS`; date columns `OBSERVED_DATE`.
- Related reports: [reports01/eq/streaks-IN.html](https://stockviz.github.io/reports01/eq/streaks-IN.html), [reports01/eq/streaks-US.html](https://stockviz.github.io/reports01/eq/streaks-US.html).
- Limits: Only streaks longer than three sessions qualify; zero excess returns do not end a sign. US uses IVV and its current constituent cohort.

```json
{
  "name": "query_dashboard_dataset",
  "arguments": {
    "dataset_name": "DASHBOARD_EQUITY_STREAK",
    "limit": 2
  }
}
```

<a id="dataset-DASHBOARD_EQUITY_TECHNICAL"></a>
#### `DASHBOARD_EQUITY_TECHNICAL`

Latest price high/low states, drawdown depths, troughs, and bounce for report equities.

- Grain and analytical keys: MARKET, SYMBOL, OBSERVED_DATE.
- Units: CLOSE/HIGH/LOW are price units; drawdown/depth/bounce fields ending PCT are percentages; state/eligibility fields are categorical or indicators.
- Columns: `MARKET`, `SYMBOL`, `OBSERVED_DATE`, `IS_STALE`, `CLOSE`, `HIGH_52W`, `LOW_52W`, `HIGH_STATE`, `HIGH_10Y`, `ATH_ELIGIBLE`, `ATH_STATE`, `DRAWDOWN_1Y_PCT`, `TROUGH_DEPTH_1Y_PCT`, `TROUGH_DATE_1Y`, `BOUNCE_1Y_PCT`, `DRAWDOWN_2Y_PCT`, `TROUGH_DEPTH_2Y_PCT`, `TROUGH_DATE_2Y`, `BOUNCE_2Y_PCT`.
- Code-schema filter candidates: textual entity columns `MARKET`, `SYMBOL`, `HIGH_STATE`, `ATH_STATE`; exact integer entity columns `IS_STALE`, `ATH_ELIGIBLE`; date columns `OBSERVED_DATE`, `TROUGH_DATE_1Y`, `TROUGH_DATE_2Y`.
- Related reports: [reports01/eq/52wk-IN.html](https://stockviz.github.io/reports01/eq/52wk-IN.html), [reports01/eq/52wk-US.html](https://stockviz.github.io/reports01/eq/52wk-US.html), [reports01/eq/ath-IN.html](https://stockviz.github.io/reports01/eq/ath-IN.html), [reports01/eq/ath-US.html](https://stockviz.github.io/reports01/eq/ath-US.html), [reports01/eq/drawdowns-IN.html](https://stockviz.github.io/reports01/eq/drawdowns-IN.html), [reports01/eq/drawdowns-US.html](https://stockviz.github.io/reports01/eq/drawdowns-US.html).
- Limits: 52-week means 365 calendar days. ATH means a 3650-day high with at least 1825 closes, not lifetime high. IS_STALE compares price date with cutoff and can flag weekends; legacy drawdown episodes/freshness gates differ.

```json
{
  "name": "query_dashboard_dataset",
  "arguments": {
    "dataset_name": "DASHBOARD_EQUITY_TECHNICAL",
    "limit": 2
  }
}
```

<a id="dataset-DASHBOARD_EQUITY_UNIVERSE"></a>
#### `DASHBOARD_EQUITY_UNIVERSE`

Separately dated Indian index and US ETF membership used to select screens.

- Grain and analytical keys: MARKET, ENTITY, OBSERVED_DATE, SYMBOL.
- Units: WEIGHT retains source holdings weight convention; PRICE_SYMBOL is the price lookup identifier.
- Columns: `MARKET`, `ENTITY`, `OBSERVED_DATE`, `SYMBOL`, `PRICE_SYMBOL`, `WEIGHT`.
- Code-schema filter candidates: textual entity columns `MARKET`, `ENTITY`, `SYMBOL`, `PRICE_SYMBOL`; exact integer entity columns none; date columns `OBSERVED_DATE`.
- Related reports: [reports01/eq/52wk-IN.html](https://stockviz.github.io/reports01/eq/52wk-IN.html), [reports01/eq/52wk-US.html](https://stockviz.github.io/reports01/eq/52wk-US.html), [reports01/eq/ath-IN.html](https://stockviz.github.io/reports01/eq/ath-IN.html), [reports01/eq/ath-US.html](https://stockviz.github.io/reports01/eq/ath-US.html), [reports01/eq/drawdowns-IN.html](https://stockviz.github.io/reports01/eq/drawdowns-IN.html), [reports01/eq/drawdowns-US.html](https://stockviz.github.io/reports01/eq/drawdowns-US.html), [reports01/eq/streaks-IN.html](https://stockviz.github.io/reports01/eq/streaks-IN.html), [reports01/eq/streaks-US.html](https://stockviz.github.io/reports01/eq/streaks-US.html).
- Limits: Join screens on MARKET and SYMBOL=PRICE_SYMBOL, not blindly on original SYMBOL. US slash-to-dot normalization and up to 500 stock/equity holdings per XLG/XMHQ/IJR are explicit; membership and price dates differ.

```json
{
  "name": "query_dashboard_dataset",
  "arguments": {
    "dataset_name": "DASHBOARD_EQUITY_UNIVERSE",
    "limit": 2
  }
}
```

<a id="dataset-DASHBOARD_EQ_IN_FINANCIALS"></a>
#### `DASHBOARD_EQ_IN_FINANCIALS`

Raw Indian equity financial items plus report display conversions.

- Grain and analytical keys: SYMBOL, PERIOD_END, PERIOD_TYPE, ITEM_KEY, IS_CONSOLIDATED, IS_AUDITED.
- Units: ITEM_VAL is raw; DISPLAY_VALUE uses UNIT: selected money items divide by 10000 to INR crore, bank ratios are percent, EPS/BVPS/ABVPS INR per share, ASSETS_LAKH_CR lakh crore.
- Columns: `SYMBOL`, `PERIOD_END`, `PERIOD_TYPE`, `ITEM_KEY`, `ITEM_VAL`, `IS_CONSOLIDATED`, `IS_AUDITED`, `DISPLAY_VALUE`, `UNIT`.
- Code-schema filter candidates: textual entity columns `SYMBOL`, `PERIOD_TYPE`, `ITEM_KEY`, `UNIT`; exact integer entity columns `IS_CONSOLIDATED`, `IS_AUDITED`; date columns `PERIOD_END`.
- Related reports: [reports02/eq-in/risk/in.RELIANCE.html](https://stockviz.github.io/reports02/eq-in/risk/in.RELIANCE.html).
- Limits: Conversions follow legacy R behavior, not independent dimensional validation. No fallback-key aggregation, QoQ, zero suppression, or corporate-action EPS annotations; preserve raw consolidation flags.

```json
{
  "name": "query_dashboard_dataset",
  "arguments": {
    "dataset_name": "DASHBOARD_EQ_IN_FINANCIALS",
    "limit": 2
  }
}
```

<a id="dataset-DASHBOARD_EQ_IN_FREE_FLOAT"></a>
#### `DASHBOARD_EQ_IN_FREE_FLOAT`

Latest free-float market-cap snapshot for active equity report tickers.

- Grain and analytical keys: SYMBOL, TIME_STAMP.
- Units: FF_MKT_CAP_CR is INR crore.
- Columns: `SYMBOL`, `TIME_STAMP`, `FF_MKT_CAP_CR`.
- Code-schema filter candidates: textual entity columns `SYMBOL`; exact integer entity columns none; date columns `TIME_STAMP`.
- Related reports: [reports02/eq-in/risk/in.RELIANCE.html](https://stockviz.github.io/reports02/eq-in/risk/in.RELIANCE.html).
- Limits: Snapshot input, not full historical capitalization or a point-in-time archive.

```json
{
  "name": "query_dashboard_dataset",
  "arguments": {
    "dataset_name": "DASHBOARD_EQ_IN_FREE_FLOAT",
    "limit": 2
  }
}
```

<a id="dataset-DASHBOARD_EQ_IN_MARGIN"></a>
#### `DASHBOARD_EQ_IN_MARGIN`

Latest financing surveillance with cap and average trading-value denominators.

- Grain and analytical keys: SYMBOL, AS_OF; CAP_AS_OF identifies the cap snapshot.
- Units: TOT_FINANCED_LAKHS is INR lakh, FF_MKT_CAP_CR INR crore, AVG_TRD_VAL INR; FF_PCT and TRD_PCT are percent-form outputs.
- Columns: `SYMBOL`, `AS_OF`, `TOT_FINANCED_LAKHS`, `CAP_AS_OF`, `FF_MKT_CAP_CR`, `AVG_TRD_VAL`, `FF_PCT`, `TRD_PCT`.
- Code-schema filter candidates: textual entity columns `SYMBOL`; exact integer entity columns none; date columns `AS_OF`, `CAP_AS_OF`.
- Related reports: [reports02/eq-in/rp-margin.html](https://stockviz.github.io/reports02/eq-in/rp-margin.html).
- Limits: Uses latest MTF, latest global freefloat <= MTF, and ten observed trade sessions. FF_PCT retains the legacy extra factor 100: 100*financed_lakhs/(10000*cap_cr). This is not dimensional certification or historical ratio parity.

```json
{
  "name": "query_dashboard_dataset",
  "arguments": {
    "dataset_name": "DASHBOARD_EQ_IN_MARGIN",
    "limit": 2
  }
}
```

<a id="dataset-DASHBOARD_EQ_IN_MTF"></a>
#### `DASHBOARD_EQ_IN_MTF`

Latest margin-financing snapshot for active equity report tickers.

- Grain and analytical keys: SYMBOL, TIME_STAMP.
- Units: TOT_FINANCED_LAKHS is INR lakh.
- Columns: `SYMBOL`, `TIME_STAMP`, `TOT_FINANCED_LAKHS`.
- Code-schema filter candidates: textual entity columns `SYMBOL`; exact integer entity columns none; date columns `TIME_STAMP`.
- Related reports: [reports02/eq-in/risk/in.RELIANCE.html](https://stockviz.github.io/reports02/eq-in/risk/in.RELIANCE.html).
- Limits: Does not reproduce the report's regime-corrected historical financing chart.

```json
{
  "name": "query_dashboard_dataset",
  "arguments": {
    "dataset_name": "DASHBOARD_EQ_IN_MTF",
    "limit": 2
  }
}
```

<a id="dataset-DASHBOARD_EQ_IN_OWNERSHIP"></a>
#### `DASHBOARD_EQ_IN_OWNERSHIP`

Aggregated voting-right ownership categories.

- Grain and analytical keys: SYMBOL, AS_OF, CATEGORY.
- Units: PERCENT is voting-right percentage, not a fraction or a holder count.
- Columns: `SYMBOL`, `AS_OF`, `CATEGORY`, `PERCENT`.
- Code-schema filter candidates: textual entity columns `SYMBOL`, `CATEGORY`; exact integer entity columns none; date columns `AS_OF`.
- Related reports: [reports02/eq-in/risk/in.RELIANCE.html](https://stockviz.github.io/reports02/eq-in/risk/in.RELIANCE.html).
- Limits: Categories are DOMESTIC_INSTITUTION, FOREIGN_INSTITUTION, PROMOTER, GOVERNMENT, and INDIVIDUAL; no inferred shareholder identities.

```json
{
  "name": "query_dashboard_dataset",
  "arguments": {
    "dataset_name": "DASHBOARD_EQ_IN_OWNERSHIP",
    "limit": 2
  }
}
```

<a id="dataset-DASHBOARD_EQ_IN_RETURNS"></a>
#### `DASHBOARD_EQ_IN_RETURNS`

Selected-period Indian equity price, return, wealth change, and drawdown inputs.

- Grain and analytical keys: ENTITY, AS_OF, FREQUENCY.
- Units: PRICE retains price units; RETURN, CUM_RETURN, and DRAWDOWN are decimal fractions.
- Columns: `ENTITY`, `AS_OF`, `FREQUENCY`, `PRICE`, `RETURN`, `CUM_RETURN`, `DRAWDOWN`.
- Code-schema filter candidates: textual entity columns `ENTITY`, `FREQUENCY`; exact integer entity columns none; date columns `AS_OF`.
- Related reports: [reports02/eq-in/risk/in.RELIANCE.html](https://stockviz.github.io/reports02/eq-in/risk/in.RELIANCE.html).
- Limits: Default frequency W; D/M/Y require loader opt-ins. Initial return is NULL, periods use actual last observations, and no forward fill occurs. Weekly drawdown is not exact daily drawdown; SMA/rank/fan outputs are absent.

```json
{
  "name": "query_dashboard_dataset",
  "arguments": {
    "dataset_name": "DASHBOARD_EQ_IN_RETURNS",
    "limit": 2
  }
}
```

<a id="dataset-DASHBOARD_ETF_CAPM"></a>
#### `DASHBOARD_ETF_CAPM`

Latest report-relevant stored ETF metric observations.

- Grain and analytical keys: SYMBOL, ID, TIME_STAMP.
- Units: VAL retains upstream metric units; ID identifies the metric.
- Columns: `SYMBOL`, `ID`, `TIME_STAMP`, `VAL`.
- Code-schema filter candidates: textual entity columns `SYMBOL`, `ID`; exact integer entity columns none; date columns `TIME_STAMP`.
- Related reports: [reports02/etf-us/risk/rp-IVV.html](https://stockviz.github.io/reports02/etf-us/risk/rp-IVV.html), [reports02/etf-us/rp-risk.html](https://stockviz.github.io/reports02/etf-us/rp-risk.html).
- Limits: Metric labels are not formulas. Copying source metrics does not implement peer ranks, radar normalization, rank sums, or the report's exact eligibility gates.

```json
{
  "name": "query_dashboard_dataset",
  "arguments": {
    "dataset_name": "DASHBOARD_ETF_CAPM",
    "limit": 2
  }
}
```

<a id="dataset-DASHBOARD_ETF_COHORT"></a>
#### `DASHBOARD_ETF_COHORT`

Latest ETF metadata membership and report selector cohorts.

- Grain and analytical keys: COHORT, SYMBOL, MEMBERSHIP_DATE.
- Units: AUM is source-native; FUND and ASSET_CLASS are labels.
- Columns: `COHORT`, `SYMBOL`, `MEMBERSHIP_DATE`, `FUND`, `ASSET_CLASS`, `AUM`.
- Code-schema filter candidates: textual entity columns `COHORT`, `SYMBOL`, `FUND`, `ASSET_CLASS`; exact integer entity columns none; date columns `MEMBERSHIP_DATE`.
- Related reports: [reports02/etf-us/risk/rp-IVV.html](https://stockviz.github.io/reports02/etf-us/risk/rp-IVV.html), [reports02/etf-us/rp-country.html](https://stockviz.github.io/reports02/etf-us/rp-country.html), [reports02/etf-us/rp-fama-french-regression.html](https://stockviz.github.io/reports02/etf-us/rp-fama-french-regression.html), [reports02/etf-us/rp-risk.html](https://stockviz.github.io/reports02/etf-us/rp-risk.html), [reports02/etf-us/rp-sector.html](https://stockviz.github.io/reports02/etf-us/rp-sector.html).
- Limits: US_SECTOR uses U.S./Equity/State Street/Sector/AUM>1e9; FF_US_EQUITY excludes inverse, leveraged, and ETN funds. Metadata membership does not prove priced/fresh CAPM eligibility.

```json
{
  "name": "query_dashboard_dataset",
  "arguments": {
    "dataset_name": "DASHBOARD_ETF_COHORT",
    "limit": 2
  }
}
```

<a id="dataset-DASHBOARD_ETF_CONSTITUENTS"></a>
#### `DASHBOARD_ETF_CONSTITUENTS`

Each eligible ETF's latest available holdings snapshot.

- Grain and analytical keys: ETF, TIME_STAMP, SYMBOL, holding occurrence.
- Units: WEIGHT, ASSET_TYPE, and SECTOR retain source conventions.
- Columns: `ETF`, `TIME_STAMP`, `SYMBOL`, `NAME`, `ASSET_TYPE`, `WEIGHT`, `SECTOR`.
- Code-schema filter candidates: textual entity columns `ETF`, `SYMBOL`, `NAME`, `ASSET_TYPE`, `SECTOR`; exact integer entity columns none; date columns `TIME_STAMP`.
- Related reports: [reports01/eq/52wk-US.html](https://stockviz.github.io/reports01/eq/52wk-US.html), [reports01/eq/ath-US.html](https://stockviz.github.io/reports01/eq/ath-US.html), [reports01/eq/drawdowns-US.html](https://stockviz.github.io/reports01/eq/drawdowns-US.html), [reports01/eq/streaks-US.html](https://stockviz.github.io/reports01/eq/streaks-US.html), [reports02/etf-us/analysis/rp-AAXJ.html](https://stockviz.github.io/reports02/etf-us/analysis/rp-AAXJ.html).
- Limits: Each ETF has its own latest date, possibly before the display floor. The report's additions/removals between snapshots are not emitted; one retained snapshot cannot reconstruct them.

```json
{
  "name": "query_dashboard_dataset",
  "arguments": {
    "dataset_name": "DASHBOARD_ETF_CONSTITUENTS",
    "limit": 2
  }
}
```

<a id="dataset-DASHBOARD_ETF_META"></a>
#### `DASHBOARD_ETF_META`

Latest metadata for the eligible ETF report universe.

- Grain and analytical keys: SYMBOL, TIME_STAMP.
- Units: AUM and EXPENSE_RATIO remain source-native; INVERSE/LEVERAGED/ETN are indicators.
- Columns: `SYMBOL`, `TIME_STAMP`, `FUND`, `ASSET_CLASS`, `ISSUER`, `CATEGORY`, `GEO`, `AUM`, `EXPENSE_RATIO`, `INVERSE`, `LEVERAGED`, `ETN`.
- Code-schema filter candidates: textual entity columns `SYMBOL`, `FUND`, `ASSET_CLASS`, `ISSUER`, `CATEGORY`, `GEO`; exact integer entity columns `INVERSE`, `LEVERAGED`, `ETN`; date columns `TIME_STAMP`.
- Related reports: [reports02/etf-us/analysis/rp-AAXJ.html](https://stockviz.github.io/reports02/etf-us/analysis/rp-AAXJ.html), [reports02/etf-us/risk/rp-IVV.html](https://stockviz.github.io/reports02/etf-us/risk/rp-IVV.html), [reports02/etf-us/rp-country.html](https://stockviz.github.io/reports02/etf-us/rp-country.html), [reports02/etf-us/rp-fama-french-regression.html](https://stockviz.github.io/reports02/etf-us/rp-fama-french-regression.html), [reports02/etf-us/rp-risk.html](https://stockviz.github.io/reports02/etf-us/rp-risk.html), [reports02/etf-us/rp-sector.html](https://stockviz.github.io/reports02/etf-us/rp-sector.html).
- Limits: Do not assume USD or a percent/fraction expense convention without upstream verification. Classification is latest selected vintage, not historical membership.

```json
{
  "name": "query_dashboard_dataset",
  "arguments": {
    "dataset_name": "DASHBOARD_ETF_META",
    "limit": 2
  }
}
```

<a id="dataset-DASHBOARD_ETF_REGRESSION"></a>
#### `DASHBOARD_ETF_REGRESSION`

Generic rolling weekly ETF OLS coefficients and fit statistics.

- Grain and analytical keys: ENTITY, MODEL, AS_OF, TERM; START_DATE and OBSERVATIONS describe the window.
- Units: COEFFICIENT is unscaled: intercept decimal return/week, betas dimensionless; R_SQUARED/ADJ_R_SQUARED fractions; EXCESS_CUM_RETURN a decimal wealth difference.
- Columns: `ENTITY`, `MODEL`, `AS_OF`, `START_DATE`, `OBSERVATIONS`, `TERM`, `COEFFICIENT`, `R_SQUARED`, `ADJ_R_SQUARED`, `EXCESS_CUM_RETURN`, `STATUS`.
- Code-schema filter candidates: textual entity columns `ENTITY`, `MODEL`, `TERM`, `STATUS`; exact integer entity columns `OBSERVATIONS`; date columns `AS_OF`, `START_DATE`.
- Related reports: [reports02/etf-us/risk/rp-IVV.html](https://stockviz.github.io/reports02/etf-us/risk/rp-IVV.html), [reports02/etf-us/rp-risk.html](https://stockviz.github.io/reports02/etf-us/rp-risk.html).
- Limits: 50 complete-case weeks, intercept, nested configured benchmarks. Rank deficiency gives status and NULL coefficients. This new analytical view is related to ETF reports, not a reproduced legacy report model.

```json
{
  "name": "query_dashboard_dataset",
  "arguments": {
    "dataset_name": "DASHBOARD_ETF_REGRESSION",
    "limit": 2
  }
}
```

<a id="dataset-DASHBOARD_ETF_RETURNS"></a>
#### `DASHBOARD_ETF_RETURNS`

Selected-period eligible ETF price, return, wealth change, and drawdown inputs.

- Grain and analytical keys: ENTITY, AS_OF, FREQUENCY.
- Units: PRICE retains price units; RETURN, CUM_RETURN, and DRAWDOWN are decimal fractions.
- Columns: `ENTITY`, `AS_OF`, `FREQUENCY`, `PRICE`, `RETURN`, `CUM_RETURN`, `DRAWDOWN`.
- Code-schema filter candidates: textual entity columns `ENTITY`, `FREQUENCY`; exact integer entity columns none; date columns `AS_OF`.
- Related reports: [reports02/etf-us/risk/rp-IVV.html](https://stockviz.github.io/reports02/etf-us/risk/rp-IVV.html), [reports02/etf-us/rp-country.html](https://stockviz.github.io/reports02/etf-us/rp-country.html), [reports02/etf-us/rp-risk.html](https://stockviz.github.io/reports02/etf-us/rp-risk.html), [reports02/etf-us/rp-sector.html](https://stockviz.github.io/reports02/etf-us/rp-sector.html).
- Limits: Default W, with D/M/Y loader opt-ins; no filling. Universe is latest bounded CAPM intersected with latest metadata, applied backward. Country/sector heatmaps and legacy price-row horizons are not materialized.

```json
{
  "name": "query_dashboard_dataset",
  "arguments": {
    "dataset_name": "DASHBOARD_ETF_RETURNS",
    "limit": 2
  }
}
```

<a id="dataset-DASHBOARD_ETF_RISK"></a>
#### `DASHBOARD_ETF_RISK`

Whole-selected-window generic ETF risk summary.

- Grain and analytical keys: ENTITY, START_DATE, AS_OF.
- Units: CUM_RETURN, ANN_RETURN, VOLATILITY, and MAX_DRAWDOWN are decimal fractions; OBSERVATIONS is a count.
- Columns: `ENTITY`, `START_DATE`, `AS_OF`, `OBSERVATIONS`, `CUM_RETURN`, `ANN_RETURN`, `VOLATILITY`, `MAX_DRAWDOWN`.
- Code-schema filter candidates: textual entity columns `ENTITY`; exact integer entity columns `OBSERVATIONS`; date columns `START_DATE`, `AS_OF`.
- Related reports: [reports02/etf-us/risk/rp-IVV.html](https://stockviz.github.io/reports02/etf-us/risk/rp-IVV.html), [reports02/etf-us/rp-risk.html](https://stockviz.github.io/reports02/etf-us/rp-risk.html).
- Limits: Daily calculations use sample SD and default annualization 252. Not stored EQ_CAPM, report peer scores, or exact sampled-weekly drawdown.

```json
{
  "name": "query_dashboard_dataset",
  "arguments": {
    "dataset_name": "DASHBOARD_ETF_RISK",
    "limit": 2
  }
}
```

<a id="dataset-DASHBOARD_FF_DEFS"></a>
#### `DASHBOARD_FF_DEFS`

Literal Fama-French industry definitions.

- Grain and analytical keys: ID.
- Units: DEF is text.
- Columns: `ID`, `DEF`.
- Code-schema filter candidates: textual entity columns `ID`, `DEF`; exact integer entity columns none; date columns none.
- Related reports: [reports02/etf-us/rp-fama-french-factors.html](https://stockviz.github.io/reports02/etf-us/rp-fama-french-factors.html), [reports02/etf-us/rp-fama-french-industry.html](https://stockviz.github.io/reports02/etf-us/rp-fama-french-industry.html), [reports02/etf-us/rp-fama-french-regression.html](https://stockviz.github.io/reports02/etf-us/rp-fama-french-regression.html).
- Limits: Reference descriptions are not factor model formulas or a historical definition vintage.

```json
{
  "name": "query_dashboard_dataset",
  "arguments": {
    "dataset_name": "DASHBOARD_FF_DEFS",
    "limit": 2
  }
}
```

<a id="dataset-DASHBOARD_FF_REGRESSION"></a>
#### `DASHBOARD_FF_REGRESSION`

Latest stored Fama-French six-factor snapshots for report industries and eligible US ETFs.

- Grain and analytical keys: KEY_ID, KEY_TYPE, TIME_STAMP.
- Units: INTERCEPT is daily alpha times 100; MKT_RF/SMB/HML/RMW/CMA/MOM are betas times 100; R_SQD is a fraction; RESIDUAL_CUMRET/RESIDUAL_SD are percent.
- Columns: `KEY_ID`, `KEY_TYPE`, `TIME_STAMP`, `INTERCEPT`, `MKT_RF`, `SMB`, `HML`, `RMW`, `CMA`, `MOM`, `R_SQD`, `RESIDUAL_CUMRET`, `RESIDUAL_SD`.
- Code-schema filter candidates: textual entity columns `KEY_ID`, `KEY_TYPE`; exact integer entity columns none; date columns `TIME_STAMP`.
- Related reports: [reports02/etf-us/rp-fama-french-regression.html](https://stockviz.github.io/reports02/etf-us/rp-fama-french-regression.html).
- Limits: Divide copied betas by 100 before interpreting exposures. No fresh OLS or rolling exposure series is computed. Upstream date can be factor maximum rather than final aligned regression date, and old snapshots may have been deleted upstream.

```json
{
  "name": "query_dashboard_dataset",
  "arguments": {
    "dataset_name": "DASHBOARD_FF_REGRESSION",
    "limit": 2
  }
}
```

<a id="dataset-DASHBOARD_FF_RETURNS"></a>
#### `DASHBOARD_FF_RETURNS`

Native Fama-French return observations across four source families.

- Grain and analytical keys: FAMILY, KEY_ID, RET_TYPE, AS_OF.
- Units: RET_PERCENT is raw percent; RETURN=RET_PERCENT/100 except -99.99/-999 sentinels become NULL.
- Columns: `FAMILY`, `KEY_ID`, `RET_TYPE`, `AS_OF`, `RET_PERCENT`, `RETURN`.
- Code-schema filter candidates: textual entity columns `FAMILY`, `KEY_ID`, `RET_TYPE`; exact integer entity columns none; date columns `AS_OF`.
- Related reports: [reports02/etf-us/rp-fama-french-factors.html](https://stockviz.github.io/reports02/etf-us/rp-fama-french-factors.html), [reports02/etf-us/rp-fama-french-industry.html](https://stockviz.github.io/reports02/etf-us/rp-fama-french-industry.html).
- Limits: All return types remain; choose deliberately. No seasonal paths, annual heatmaps, or size-relative comparisons are implied.

```json
{
  "name": "query_dashboard_dataset",
  "arguments": {
    "dataset_name": "DASHBOARD_FF_RETURNS",
    "limit": 2
  }
}
```

<a id="dataset-DASHBOARD_INDEX_MEMBERSHIP"></a>
#### `DASHBOARD_INDEX_MEMBERSHIP`

Report index membership snapshots with explicit current/history roles.

- Grain and analytical keys: MEMBERSHIP_KIND, INDEX_NAME, MEMBERSHIP_DATE, SYMBOL.
- Units: CAP_WEIGHT retains native weight convention; INDUSTRY is text.
- Columns: `MEMBERSHIP_KIND`, `INDEX_NAME`, `MEMBERSHIP_DATE`, `SYMBOL`, `INDUSTRY`, `CAP_WEIGHT`.
- Code-schema filter candidates: textual entity columns `MEMBERSHIP_KIND`, `INDEX_NAME`, `SYMBOL`, `INDUSTRY`; exact integer entity columns none; date columns `MEMBERSHIP_DATE`.
- Related reports: [reports01/eq/52wk-IN.html](https://stockviz.github.io/reports01/eq/52wk-IN.html), [reports01/eq/ath-IN.html](https://stockviz.github.io/reports01/eq/ath-IN.html), [reports01/eq/drawdowns-IN.html](https://stockviz.github.io/reports01/eq/drawdowns-IN.html), [reports01/eq/results-IN.html](https://stockviz.github.io/reports01/eq/results-IN.html), [reports01/eq/streaks-IN.html](https://stockviz.github.io/reports01/eq/streaks-IN.html), [reports01/index/analysis/rp-NIFTY50.html](https://stockviz.github.io/reports01/index/analysis/rp-NIFTY50.html), [reports01/index/rp-IN.html](https://stockviz.github.io/reports01/index/rp-IN.html).
- Limits: CURRENT is latest snapshot <= cutoff; HISTORY is latest available history snapshot per index inside display window, not the full archive or reconstructed historical membership.

```json
{
  "name": "query_dashboard_dataset",
  "arguments": {
    "dataset_name": "DASHBOARD_INDEX_MEMBERSHIP",
    "limit": 2
  }
}
```

<a id="dataset-DASHBOARD_INDEX_RETURNS"></a>
#### `DASHBOARD_INDEX_RETURNS`

Selected-period benchmark index curves for equity and MF comparisons.

- Grain and analytical keys: ENTITY, AS_OF, FREQUENCY.
- Units: PRICE is index level; RETURN, CUM_RETURN, and DRAWDOWN are decimal fractions.
- Columns: `ENTITY`, `AS_OF`, `FREQUENCY`, `PRICE`, `RETURN`, `CUM_RETURN`, `DRAWDOWN`.
- Code-schema filter candidates: textual entity columns `ENTITY`, `FREQUENCY`; exact integer entity columns none; date columns `AS_OF`.
- Related reports: [reports03/mf/analysis/rp-118269.html](https://stockviz.github.io/reports03/mf/analysis/rp-118269.html), [reports03/mf/rp-IN.html](https://stockviz.github.io/reports03/mf/rp-IN.html).
- Limits: Default W; D/M/Y require opt-in. Observation endpoints are actual, initial return NULL, and no fill occurs. These benchmarks do not reconstruct full report-aligned comparisons by themselves.

```json
{
  "name": "query_dashboard_dataset",
  "arguments": {
    "dataset_name": "DASHBOARD_INDEX_RETURNS",
    "limit": 2
  }
}
```

<a id="dataset-DASHBOARD_INDEX_RISK"></a>
#### `DASHBOARD_INDEX_RISK`

Latest stored index risk metric observations.

- Grain and analytical keys: ENTITY, OBSERVED_DATE, METRIC_ID.
- Units: VALUE retains source INDEX_CAPM units and upstream formula.
- Columns: `ENTITY`, `OBSERVED_DATE`, `METRIC_ID`, `VALUE`.
- Code-schema filter candidates: textual entity columns `ENTITY`, `METRIC_ID`; exact integer entity columns none; date columns `OBSERVED_DATE`.
- Related reports: [reports01/index/risk/rp-NIFTY50TR.html](https://stockviz.github.io/reports01/index/risk/rp-NIFTY50TR.html), [reports01/index/rp-risk.html](https://stockviz.github.io/reports01/index/rp-risk.html).
- Limits: Not the generic MARKET_RISK calculation; labels alone do not define formulas, ranks, or annualization.

```json
{
  "name": "query_dashboard_dataset",
  "arguments": {
    "dataset_name": "DASHBOARD_INDEX_RISK",
    "limit": 2
  }
}
```

<a id="dataset-DASHBOARD_INDUSTRY_FUNDAMENTALS"></a>
#### `DASHBOARD_INDUSTRY_FUNDAMENTALS`

Latest report bank/industry fundamental items and book-value multiple input.

- Grain and analytical keys: INDUSTRY, SYMBOL, PERIOD_END, PERIOD_TYPE, ITEM_KEY, consolidation/audit variant.
- Units: ITEM_VAL retains key-specific source units; BV_MULTIPLE is (price/ABVPS)*(XBRL_FACE_VALUE/current_FACE_VALUE), a multiple.
- Columns: `INDUSTRY`, `SYMBOL`, `MEMBERSHIP_DATE`, `PERIOD_END`, `PERIOD_TYPE`, `IS_CONSOLIDATED`, `IS_AUDITED`, `ITEM_KEY`, `ITEM_VAL`, `PRICE_DATE`.
- Code-schema filter candidates: textual entity columns `INDUSTRY`, `SYMBOL`, `PERIOD_TYPE`, `ITEM_KEY`; exact integer entity columns `IS_CONSOLIDATED`, `IS_AUDITED`; date columns `MEMBERSHIP_DATE`, `PERIOD_END`, `PRICE_DATE`.
- Related reports: [reports01/index/industry/rp-23Wheelers.html](https://stockviz.github.io/reports01/index/industry/rp-23Wheelers.html).
- Limits: Ten bank keys plus BV_MULTIPLE; prefers standalone per symbol/latest period, correcting the legacy global consolidation minimum. PERIOD_END is not public availability time.

```json
{
  "name": "query_dashboard_dataset",
  "arguments": {
    "dataset_name": "DASHBOARD_INDUSTRY_FUNDAMENTALS",
    "limit": 2
  }
}
```

<a id="dataset-DASHBOARD_INDUSTRY_MEMBERS"></a>
#### `DASHBOARD_INDUSTRY_MEMBERS`

Latest industry constituent prices, market caps, and available-cap weights.

- Grain and analytical keys: INDUSTRY, SYMBOL, MEMBERSHIP_DATE; PRICE_DATE dates the market snapshot.
- Units: PX_CLOSE and FACE_VALUE retain quotation units; FF_MKT_CAP_CR/MKT_CAP_CR are INR crore; FREE_FLOAT_WEIGHT/CAP_WEIGHT are fractions.
- Columns: `INDUSTRY`, `SYMBOL`, `MEMBERSHIP_DATE`, `PRICE_DATE`, `PX_CLOSE`, `FACE_VALUE`, `FF_MKT_CAP_CR`, `MKT_CAP_CR`, `FREE_FLOAT_WEIGHT`, `CAP_WEIGHT`.
- Code-schema filter candidates: textual entity columns `INDUSTRY`, `SYMBOL`; exact integer entity columns none; date columns `MEMBERSHIP_DATE`, `PRICE_DATE`.
- Related reports: [reports01/index/industry/rp-23Wheelers.html](https://stockviz.github.io/reports01/index/industry/rp-23Wheelers.html).
- Limits: Uses latest industry per symbol and global latest price/misc date. Missing prices/caps remain NULL; available denominators do not prove full membership coverage.

```json
{
  "name": "query_dashboard_dataset",
  "arguments": {
    "dataset_name": "DASHBOARD_INDUSTRY_MEMBERS",
    "limit": 2
  }
}
```

<a id="dataset-DASHBOARD_INDUSTRY_NARRATIVES"></a>
#### `DASHBOARD_INDUSTRY_NARRATIVES`

Latest industry prompt summaries and source references.

- Grain and analytical keys: ENTITY, AS_OF, source prompt/snapshot occurrence.
- Units: CONTENT_JSON retains INDUSTRY, AS_OF, PROMPT, SUMMARY, and SOURCES.
- Columns: `ENTITY`, `AS_OF`, `CONTENT_JSON`.
- Code-schema filter candidates: textual entity columns `ENTITY`, `CONTENT_JSON`; exact integer entity columns none; date columns `AS_OF`.
- Related reports: [reports01/index/industry/rp-23Wheelers.html](https://stockviz.github.io/reports01/index/industry/rp-23Wheelers.html).
- Limits: Tied latest snapshots are retained. Missing optional SQLite source is unavailable rather than evidence of no commentary.

```json
{
  "name": "query_dashboard_dataset",
  "arguments": {
    "dataset_name": "DASHBOARD_INDUSTRY_NARRATIVES",
    "limit": 2
  }
}
```

<a id="dataset-DASHBOARD_INDUSTRY_STATISTICS"></a>
#### `DASHBOARD_INDUSTRY_STATISTICS`

Industry financial share statistics for report EBIT/revenue items.

- Grain and analytical keys: INDUSTRY, SYMBOL, PERIOD_END, FIN, ITEM_KEY; UPDATE_DATE dates selected revision.
- Units: VALUE retains source SHARE_PCT, in percent.
- Columns: `INDUSTRY`, `SYMBOL`, `PERIOD_END`, `UPDATE_DATE`, `FIN`, `ITEM_KEY`, `VALUE`.
- Code-schema filter candidates: textual entity columns `INDUSTRY`, `SYMBOL`, `FIN`, `ITEM_KEY`; exact integer entity columns none; date columns `PERIOD_END`, `UPDATE_DATE`.
- Related reports: [reports01/index/industry/rp-23Wheelers.html](https://stockviz.github.io/reports01/index/industry/rp-23Wheelers.html).
- Limits: Latest update <= cutoff independently per key; FIN definitions remain separate. UPDATE_DATE loses time-of-day precision, and period end is not publication time.

```json
{
  "name": "query_dashboard_dataset",
  "arguments": {
    "dataset_name": "DASHBOARD_INDUSTRY_STATISTICS",
    "limit": 2
  }
}
```

<a id="dataset-DASHBOARD_MARKET_DISTRIBUTION"></a>
#### `DASHBOARD_MARKET_DISTRIBUTION`

Whole-window daily-return distribution by market family and weighting.

- Grain and analytical keys: FAMILY, ENTITY, WEIGHTING, OBSERVED_DATE.
- Units: MEAN_PCT, SD_PCT, Q05_PCT, MEDIAN_PCT, and Q95_PCT are daily return percentages; SAMPLE_COUNT a count.
- Columns: `FAMILY`, `ENTITY`, `WEIGHTING`, `OBSERVED_DATE`, `SAMPLE_COUNT`, `MEAN_PCT`, `SD_PCT`, `Q05_PCT`, `MEDIAN_PCT`, `Q95_PCT`.
- Code-schema filter candidates: textual entity columns `FAMILY`, `ENTITY`, `WEIGHTING`; exact integer entity columns `SAMPLE_COUNT`; date columns `OBSERVED_DATE`.
- Related reports: [reports01/index/industry/rp-23Wheelers.html](https://stockviz.github.io/reports01/index/industry/rp-23Wheelers.html), [reports01/index/risk/rp-NIFTY50TR.html](https://stockviz.github.io/reports01/index/risk/rp-NIFTY50TR.html), [reports01/index/rp-industry.html](https://stockviz.github.io/reports01/index/rp-industry.html), [reports01/index/rp-risk.html](https://stockviz.github.io/reports01/index/rp-risk.html), [reports01/index/rp-syn.html](https://stockviz.github.io/reports01/index/rp-syn.html), [reports01/macro/rp-bnd.html](https://stockviz.github.io/reports01/macro/rp-bnd.html), [reports01/macro/rp-cmdy.html](https://stockviz.github.io/reports01/macro/rp-cmdy.html), [reports01/macro/rp-cur.html](https://stockviz.github.io/reports01/macro/rp-cur.html).
- Limits: Not legacy distributions of SMA scenario metrics or multi-year annual rolling returns.

```json
{
  "name": "query_dashboard_dataset",
  "arguments": {
    "dataset_name": "DASHBOARD_MARKET_DISTRIBUTION",
    "limit": 2
  }
}
```

<a id="dataset-DASHBOARD_MARKET_HORIZON"></a>
#### `DASHBOARD_MARKET_HORIZON`

Trailing observed-session return by market family and weighting.

- Grain and analytical keys: FAMILY, ENTITY, WEIGHTING, OBSERVED_DATE, HORIZON_SESSIONS.
- Units: RETURN_PCT=100*(price[t]/price[t-h]-1); HORIZON_SESSIONS counts intervals.
- Columns: `FAMILY`, `ENTITY`, `WEIGHTING`, `OBSERVED_DATE`, `START_DATE`, `HORIZON_SESSIONS`, `RETURN_PCT`.
- Code-schema filter candidates: textual entity columns `FAMILY`, `ENTITY`, `WEIGHTING`; exact integer entity columns `HORIZON_SESSIONS`; date columns `OBSERVED_DATE`, `START_DATE`.
- Related reports: [reports01/index/industry/rp-23Wheelers.html](https://stockviz.github.io/reports01/index/industry/rp-23Wheelers.html), [reports01/index/risk/rp-NIFTY50TR.html](https://stockviz.github.io/reports01/index/risk/rp-NIFTY50TR.html), [reports01/index/rp-industry.html](https://stockviz.github.io/reports01/index/rp-industry.html), [reports01/index/rp-risk.html](https://stockviz.github.io/reports01/index/rp-risk.html), [reports01/index/rp-syn.html](https://stockviz.github.io/reports01/index/rp-syn.html), [reports01/macro/rp-bnd.html](https://stockviz.github.io/reports01/macro/rp-bnd.html), [reports01/macro/rp-cmdy.html](https://stockviz.github.io/reports01/macro/rp-cmdy.html), [reports01/macro/rp-cur.html](https://stockviz.github.io/reports01/macro/rp-cur.html).
- Limits: Requires h+1 observations; defaults 1/5/20/60/120/252/756/1260/2520 differ from legacy 5/10/20/50/100/200 price-row tables.

```json
{
  "name": "query_dashboard_dataset",
  "arguments": {
    "dataset_name": "DASHBOARD_MARKET_HORIZON",
    "limit": 2
  }
}
```

<a id="dataset-DASHBOARD_MARKET_RISK"></a>
#### `DASHBOARD_MARKET_RISK`

Whole-selected-window return/risk summary by market family and weighting.

- Grain and analytical keys: FAMILY, ENTITY, WEIGHTING, START_DATE, OBSERVED_DATE.
- Units: ANNUALIZED_RETURN_PCT, ANNUALIZED_VOL_PCT, DOWNSIDE_DEV_PCT, MAX_DRAWDOWN_PCT are percentages; SHARPE_ZERO_RF dimensionless.
- Columns: `FAMILY`, `ENTITY`, `WEIGHTING`, `OBSERVED_DATE`, `START_DATE`, `SAMPLE_COUNT`, `ANNUALIZED_RETURN_PCT`, `ANNUALIZED_VOL_PCT`, `DOWNSIDE_DEV_PCT`, `MAX_DRAWDOWN_PCT`, `SHARPE_ZERO_RF`.
- Code-schema filter candidates: textual entity columns `FAMILY`, `ENTITY`, `WEIGHTING`; exact integer entity columns `SAMPLE_COUNT`; date columns `OBSERVED_DATE`, `START_DATE`.
- Related reports: [reports01/index/industry/rp-23Wheelers.html](https://stockviz.github.io/reports01/index/industry/rp-23Wheelers.html), [reports01/index/risk/rp-NIFTY50TR.html](https://stockviz.github.io/reports01/index/risk/rp-NIFTY50TR.html), [reports01/index/rp-industry.html](https://stockviz.github.io/reports01/index/rp-industry.html), [reports01/index/rp-risk.html](https://stockviz.github.io/reports01/index/rp-risk.html), [reports01/index/rp-syn.html](https://stockviz.github.io/reports01/index/rp-syn.html), [reports01/macro/rp-bnd.html](https://stockviz.github.io/reports01/macro/rp-bnd.html), [reports01/macro/rp-cmdy.html](https://stockviz.github.io/reports01/macro/rp-cmdy.html), [reports01/macro/rp-cur.html](https://stockviz.github.io/reports01/macro/rp-cur.html).
- Limits: 252-session annualization, sample SD, zero risk-free Sharpe, and initial wealth peak 1. Missing returns drop from summary, not fill with zero; not rolling risk or legacy rank/UPR output.

```json
{
  "name": "query_dashboard_dataset",
  "arguments": {
    "dataset_name": "DASHBOARD_MARKET_RISK",
    "limit": 2
  }
}
```

<a id="dataset-DASHBOARD_MARKET_SERIES"></a>
#### `DASHBOARD_MARKET_SERIES`

Market levels and daily-return inputs across index, industry, synthetic, and macro families.

- Grain and analytical keys: FAMILY, ENTITY, WEIGHTING, OBSERVED_DATE.
- Units: LEVEL follows UNIT and source quotations; DAILY_RETURN is decimal. Stored-return industry/synthetic series compound to growth of 1.
- Columns: `FAMILY`, `ENTITY`, `WEIGHTING`, `OBSERVED_DATE`, `LEVEL`, `DAILY_RETURN`, `UNIT`.
- Code-schema filter candidates: textual entity columns `FAMILY`, `ENTITY`, `WEIGHTING`, `UNIT`; exact integer entity columns none; date columns `OBSERVED_DATE`.
- Related reports: [reports01/index/industry/rp-23Wheelers.html](https://stockviz.github.io/reports01/index/industry/rp-23Wheelers.html), [reports01/index/risk/rp-NIFTY50TR.html](https://stockviz.github.io/reports01/index/risk/rp-NIFTY50TR.html), [reports01/index/rp-industry.html](https://stockviz.github.io/reports01/index/rp-industry.html), [reports01/index/rp-risk.html](https://stockviz.github.io/reports01/index/rp-risk.html), [reports01/index/rp-syn.html](https://stockviz.github.io/reports01/index/rp-syn.html), [reports01/macro/rp-bnd.html](https://stockviz.github.io/reports01/macro/rp-bnd.html), [reports01/macro/rp-cmdy.html](https://stockviz.github.io/reports01/macro/rp-cmdy.html), [reports01/macro/rp-cur.html](https://stockviz.github.io/reports01/macro/rp-cur.html).
- Limits: First stored return can affect synthetic level; missing stored returns stop the cumulative path. FX quote direction needs upstream verification; MCX expiry_series=0 has roll jumps. Yield-level returns are not bond total returns or basis-point changes.

```json
{
  "name": "query_dashboard_dataset",
  "arguments": {
    "dataset_name": "DASHBOARD_MARKET_SERIES",
    "limit": 2
  }
}
```

<a id="dataset-DASHBOARD_MARKET_SMA"></a>
#### `DASHBOARD_MARKET_SMA`

Full-window SMA, price gap, and lagged long/cash return by market family.

- Grain and analytical keys: FAMILY, ENTITY, WEIGHTING, OBSERVED_DATE, WINDOW_SESSIONS.
- Units: SMA has level units; GAP_PCT=100*(price/SMA-1); STRATEGY_RETURN is decimal.
- Columns: `FAMILY`, `ENTITY`, `WEIGHTING`, `OBSERVED_DATE`, `WINDOW_SESSIONS`, `SMA`, `GAP_PCT`, `STRATEGY_RETURN`.
- Code-schema filter candidates: textual entity columns `FAMILY`, `ENTITY`, `WEIGHTING`; exact integer entity columns `WINDOW_SESSIONS`; date columns `OBSERVED_DATE`.
- Related reports: [reports01/index/industry/rp-23Wheelers.html](https://stockviz.github.io/reports01/index/industry/rp-23Wheelers.html), [reports01/index/risk/rp-NIFTY50TR.html](https://stockviz.github.io/reports01/index/risk/rp-NIFTY50TR.html), [reports01/index/rp-industry.html](https://stockviz.github.io/reports01/index/rp-industry.html), [reports01/index/rp-risk.html](https://stockviz.github.io/reports01/index/rp-risk.html), [reports01/index/rp-syn.html](https://stockviz.github.io/reports01/index/rp-syn.html), [reports01/macro/rp-bnd.html](https://stockviz.github.io/reports01/macro/rp-bnd.html), [reports01/macro/rp-cmdy.html](https://stockviz.github.io/reports01/macro/rp-cmdy.html), [reports01/macro/rp-cur.html](https://stockviz.github.io/reports01/macro/rp-cur.html).
- Limits: Uses prior observed price>SMA signal, cash earns zero, no fees. Full observed window required; no aggregate upside-potential ratio (UPR) is stored.

```json
{
  "name": "query_dashboard_dataset",
  "arguments": {
    "dataset_name": "DASHBOARD_MARKET_SMA",
    "limit": 2
  }
}
```

<a id="dataset-DASHBOARD_METRIC_DICTIONARY"></a>
#### `DASHBOARD_METRIC_DICTIONARY`

Literal report-family metric labels from metric_map.csv.

- Grain and analytical keys: REPORT_FAMILY, METRIC_ID.
- Units: DESCRIPTION is text.
- Columns: `REPORT_FAMILY`, `METRIC_ID`, `DESCRIPTION`.
- Code-schema filter candidates: textual entity columns `REPORT_FAMILY`, `METRIC_ID`, `DESCRIPTION`; exact integer entity columns none; date columns none.
- Related reports: [reports01/index/industry/rp-23Wheelers.html](https://stockviz.github.io/reports01/index/industry/rp-23Wheelers.html), [reports01/index/rp-industry.html](https://stockviz.github.io/reports01/index/rp-industry.html), [reports01/index/rp-risk.html](https://stockviz.github.io/reports01/index/rp-risk.html), [reports02/etf-us/rp-risk.html](https://stockviz.github.io/reports02/etf-us/rp-risk.html), [reports03/mf/analysis/rp-118269.html](https://stockviz.github.io/reports03/mf/analysis/rp-118269.html), [reports03/mf/rp-IN.html](https://stockviz.github.io/reports03/mf/rp-IN.html).
- Limits: No inferred formulas, scaling, or ranks. Missing optional source files produce quality warnings; references have no historical vintage.

```json
{
  "name": "query_dashboard_dataset",
  "arguments": {
    "dataset_name": "DASHBOARD_METRIC_DICTIONARY",
    "limit": 2
  }
}
```

<a id="dataset-DASHBOARD_MF_CAPM"></a>
#### `DASHBOARD_MF_CAPM`

Latest report-relevant stored metrics for eligible direct-growth funds.

- Grain and analytical keys: SCHEME_CODE, ID, AS_OF; START_DATE retains metric source window.
- Units: VAL retains upstream units and formulas.
- Columns: `SCHEME_CODE`, `ID`, `START_DATE`, `AS_OF`, `VAL`.
- Code-schema filter candidates: textual entity columns `ID`; exact integer entity columns `SCHEME_CODE`; date columns `START_DATE`, `AS_OF`.
- Related reports: [reports03/mf/analysis/rp-118269.html](https://stockviz.github.io/reports03/mf/analysis/rp-118269.html).
- Limits: No inferred reciprocal-beta transform, peer ranks, normalized radar axes, or composite scores. Eligibility is name-based large/midcap, not every AMFI category.

```json
{
  "name": "query_dashboard_dataset",
  "arguments": {
    "dataset_name": "DASHBOARD_MF_CAPM",
    "limit": 2
  }
}
```

<a id="dataset-DASHBOARD_MF_COHORT"></a>
#### `DASHBOARD_MF_COHORT`

Candidate direct-growth large/midcap cohorts with explicit rejection reasons.

- Grain and analytical keys: COHORT, SCHEME_CODE.
- Units: ELIGIBLE is an indicator; dates describe source coverage; SCHEME_NAME and EXCLUSION_REASON are text.
- Columns: `COHORT`, `SCHEME_CODE`, `SCHEME_NAME`, `FIRST_NAV_DATE`, `LAST_NAV_DATE`, `SOURCE_AS_OF`, `WINDOW_START`, `ELIGIBLE`, `EXCLUSION_REASON`.
- Code-schema filter candidates: textual entity columns `COHORT`, `SCHEME_NAME`, `EXCLUSION_REASON`; exact integer entity columns `SCHEME_CODE`, `ELIGIBLE`; date columns `FIRST_NAV_DATE`, `LAST_NAV_DATE`, `SOURCE_AS_OF`, `WINDOW_START`.
- Related reports: [reports03/mf/analysis/rp-118269.html](https://stockviz.github.io/reports03/mf/analysis/rp-118269.html), [reports03/mf/rp-IN.html](https://stockviz.github.io/reports03/mf/rp-IN.html).
- Limits: Historical name matching over cutoff minus 1825 days; candidate must start <= window+180 days and end >= bounded global NAV max minus five days. Lexicographic MAX name is not latest official name; renamed funds can appear in both cohorts.

```json
{
  "name": "query_dashboard_dataset",
  "arguments": {
    "dataset_name": "DASHBOARD_MF_COHORT",
    "limit": 2
  }
}
```

<a id="dataset-DASHBOARD_MF_REGRESSION"></a>
#### `DASHBOARD_MF_REGRESSION`

Rolling weekly nested-benchmark fund OLS coefficients and fit statistics.

- Grain and analytical keys: ENTITY, MODEL, AS_OF, TERM; START_DATE and OBSERVATIONS describe the window.
- Units: Unscaled intercept decimal return/week, beta dimensionless; R_SQUARED/ADJ_R_SQUARED fractions; EXCESS_CUM_RETURN decimal wealth difference.
- Columns: `ENTITY`, `MODEL`, `AS_OF`, `START_DATE`, `OBSERVATIONS`, `TERM`, `COEFFICIENT`, `R_SQUARED`, `ADJ_R_SQUARED`, `EXCESS_CUM_RETURN`, `STATUS`.
- Code-schema filter candidates: textual entity columns `ENTITY`, `MODEL`, `TERM`, `STATUS`; exact integer entity columns `OBSERVATIONS`; date columns `AS_OF`, `START_DATE`.
- Related reports: [reports03/mf/analysis/rp-118269.html](https://stockviz.github.io/reports03/mf/analysis/rp-118269.html), [reports03/mf/rp-IN.html](https://stockviz.github.io/reports03/mf/rp-IN.html).
- Limits: 50 complete-case weekly endpoints with intercept; date gaps can span more than 50 calendar weeks. Not MF master monthly full-shared-history multivariate models, peer ranks, or radar transforms.

```json
{
  "name": "query_dashboard_dataset",
  "arguments": {
    "dataset_name": "DASHBOARD_MF_REGRESSION",
    "limit": 2
  }
}
```

<a id="dataset-DASHBOARD_MF_RETURNS"></a>
#### `DASHBOARD_MF_RETURNS`

Selected-period fund NAV, return, wealth change, and drawdown curves.

- Grain and analytical keys: ENTITY, AS_OF, FREQUENCY.
- Units: PRICE is NAV; RETURN, CUM_RETURN, and DRAWDOWN are decimal fractions.
- Columns: `ENTITY`, `AS_OF`, `FREQUENCY`, `PRICE`, `RETURN`, `CUM_RETURN`, `DRAWDOWN`.
- Code-schema filter candidates: textual entity columns `ENTITY`, `FREQUENCY`; exact integer entity columns none; date columns `AS_OF`.
- Related reports: [reports03/mf/analysis/rp-118269.html](https://stockviz.github.io/reports03/mf/analysis/rp-118269.html), [reports03/mf/rp-IN.html](https://stockviz.github.io/reports03/mf/rp-IN.html).
- Limits: Default W; D/M/Y require loader opt-ins. Current cutoff name-selected eligible cohort applies backward; it is not a historical investable universe. Weekly drawdown is not daily drawdown.

```json
{
  "name": "query_dashboard_dataset",
  "arguments": {
    "dataset_name": "DASHBOARD_MF_RETURNS",
    "limit": 2
  }
}
```

<a id="dataset-DASHBOARD_OPTION_IV"></a>
#### `DASHBOARD_OPTION_IV`

Report-selected near-ATM live-expiry implied-volatility quotes.

- Grain and analytical keys: ENTITY, OBSERVED_DATE, EXPIRY, OPTION_TYPE, STRIKE.
- Units: IV_PCT is annualized percent converted from source decimal IV; STRIKE retains index-point quotation.
- Columns: `ENTITY`, `OBSERVED_DATE`, `EXPIRY`, `OPTION_TYPE`, `STRIKE`, `IV_PCT`.
- Code-schema filter candidates: textual entity columns `ENTITY`, `OPTION_TYPE`; exact integer entity columns none; date columns `OBSERVED_DATE`, `EXPIRY`.
- Related reports: [reports01/index/rp-vol-NIFTY.html](https://stockviz.github.io/reports01/index/rp-vol-NIFTY.html).
- Limits: Latest report-selected quotes, not a complete surface or model recalibration.

```json
{
  "name": "query_dashboard_dataset",
  "arguments": {
    "dataset_name": "DASHBOARD_OPTION_IV",
    "limit": 2
  }
}
```

<a id="dataset-DASHBOARD_OPTION_POSITIONING"></a>
#### `DASHBOARD_OPTION_POSITIONING`

Open interest and OI-weighted strike/spot gap for nearest strictly future expiry.

- Grain and analytical keys: ENTITY, OBSERVED_DATE, EXPIRY, OPTION_TYPE (or ALL).
- Units: OPEN_INTEREST retains native contracts/quantity convention; STRIKE_SPOT_GAP_PCT is percent.
- Columns: `ENTITY`, `OBSERVED_DATE`, `EXPIRY`, `OPTION_TYPE`, `OPEN_INTEREST`, `STRIKE_SPOT_GAP_PCT`.
- Code-schema filter candidates: textual entity columns `ENTITY`, `OPTION_TYPE`; exact integer entity columns none; date columns `OBSERVED_DATE`, `EXPIRY`.
- Related reports: [reports01/index/rp-vol-NIFTY.html](https://stockviz.github.io/reports01/index/rp-vol-NIFTY.html).
- Limits: Gap is 100*sum(OI*(strike/spot-1))/sum(OI); zero total OI yields NULL, not invented zero. No complete option-chain reconstruction.

```json
{
  "name": "query_dashboard_dataset",
  "arguments": {
    "dataset_name": "DASHBOARD_OPTION_POSITIONING",
    "limit": 2
  }
}
```

<a id="dataset-DASHBOARD_PMS_AUM"></a>
#### `DASHBOARD_PMS_AUM`

Discretionary manager-level monthly AUM summaries.

- Grain and analytical keys: ID, AS_OF month-end.
- Units: AUM_INR_CR is INR crore.
- Columns: `ID`, `AS_OF`, `AUM_INR_CR`.
- Code-schema filter candidates: textual entity columns none; exact integer entity columns `ID`; date columns `AS_OF`.
- Related reports: [reports03/pms/analysis/rp-PMS.INP000000187.html](https://stockviz.github.io/reports03/pms/analysis/rp-PMS.INP000000187.html), [reports03/pms/rp-IN.html](https://stockviz.github.io/reports03/pms/rp-IN.html).
- Limits: Not strategy AUM, strategy count, latest-two-month mean, growth, annualized return, Sharpe, or information ratio. Join manager names separately through PMS_META.ID.

```json
{
  "name": "query_dashboard_dataset",
  "arguments": {
    "dataset_name": "DASHBOARD_PMS_AUM",
    "limit": 2
  }
}
```

<a id="dataset-DASHBOARD_PMS_META"></a>
#### `DASHBOARD_PMS_META`

Undated manager names and SEBI registration references for report-eligible PMS managers.

- Grain and analytical keys: ID.
- Units: SEBI_ID and PMS_NAME are identifiers/text.
- Columns: `ID`, `SEBI_ID`, `PMS_NAME`.
- Code-schema filter candidates: textual entity columns `SEBI_ID`, `PMS_NAME`; exact integer entity columns `ID`; date columns none.
- Related reports: [reports03/pms/analysis/rp-PMS.INP000000187.html](https://stockviz.github.io/reports03/pms/analysis/rp-PMS.INP000000187.html), [reports03/pms/rp-IN.html](https://stockviz.github.io/reports03/pms/rp-IN.html).
- Limits: Eligibility requires at least twelve complete months in display window and source activity in cutoff year or prior year. Metadata can be current state, not historical identity vintage.

```json
{
  "name": "query_dashboard_dataset",
  "arguments": {
    "dataset_name": "DASHBOARD_PMS_META",
    "limit": 2
  }
}
```

<a id="dataset-DASHBOARD_PMS_MONTHLY"></a>
#### `DASHBOARD_PMS_MONTHLY`

Normalized manager/strategy monthly returns and AUM across PMS source JSON eras.

- Grain and analytical keys: ID, AS_OF month-end, STRATEGY, source occurrence; canonical keys can conflict.
- Units: RETURN is a decimal fraction, AUM_INR_CR INR crore; SOURCE_STRATEGY preserves original naming; FORMAT identifies source era.
- Columns: `ID`, `AS_OF`, `STRATEGY`, `SOURCE_STRATEGY`, `ASSET_CLASS`, `RETURN`, `AUM_INR_CR`, `FORMAT`.
- Code-schema filter candidates: textual entity columns `STRATEGY`, `SOURCE_STRATEGY`, `ASSET_CLASS`, `FORMAT`; exact integer entity columns `ID`; date columns `AS_OF`.
- Related reports: [reports03/pms/analysis/rp-PMS.INP000000187.html](https://stockviz.github.io/reports03/pms/analysis/rp-PMS.INP000000187.html), [reports03/pms/rp-IN.html](https://stockviz.github.io/reports03/pms/rp-IN.html).
- Limits: Aliases are case-insensitive regex mappings and can be current state. Flat-format ASSET_CLASS stays NULL; exact duplicates collapse but conflicting canonical rows survive with partial quality. Excludes partial current month; do not sum overlapping/conflicting strategy AUM.

```json
{
  "name": "query_dashboard_dataset",
  "arguments": {
    "dataset_name": "DASHBOARD_PMS_MONTHLY",
    "limit": 2
  }
}
```

<a id="dataset-DASHBOARD_REALIZED_VOL"></a>
#### `DASHBOARD_REALIZED_VOL`

Rolling OHLC realized-volatility estimators by observation frequency.

- Grain and analytical keys: ENTITY, OBSERVED_DATE, FREQUENCY, WINDOW_SESSIONS, ESTIMATOR.
- Units: ANNUALIZED_VOL_PCT is percent; WINDOW_SESSIONS counts bars at selected frequency.
- Columns: `ENTITY`, `OBSERVED_DATE`, `FREQUENCY`, `WINDOW_SESSIONS`, `ESTIMATOR`, `ANNUALIZED_VOL_PCT`.
- Code-schema filter candidates: textual entity columns `ENTITY`, `FREQUENCY`, `ESTIMATOR`; exact integer entity columns `WINDOW_SESSIONS`; date columns `OBSERVED_DATE`.
- Related reports: [reports01/index/rp-vol-NIFTY.html](https://stockviz.github.io/reports01/index/rp-vol-NIFTY.html).
- Limits: CLOSE/PARKINSON/GARMAN_KLASS/ROGERS_SATCHELL/GK_YZ/YANG_ZHANG use 252/52/12 annualization for D/W/M. Partial bucket date is last actual observation. Legacy TTR default/order parity is not certified.

```json
{
  "name": "query_dashboard_dataset",
  "arguments": {
    "dataset_name": "DASHBOARD_REALIZED_VOL",
    "limit": 2
  }
}
```

<a id="dataset-DASHBOARD_VALUATION"></a>
#### `DASHBOARD_VALUATION`

Index/entity PE or PB history with report-visibility flag.

- Grain and analytical keys: ENTITY, OBSERVED_DATE, METRIC.
- Units: VALUE is a raw valuation multiple; REPORT_VISIBLE is an indicator.
- Columns: `ENTITY`, `OBSERVED_DATE`, `METRIC`, `VALUE`, `REPORT_VISIBLE`.
- Code-schema filter candidates: textual entity columns `ENTITY`, `METRIC`; exact integer entity columns `REPORT_VISIBLE`; date columns `OBSERVED_DATE`.
- Related reports: [reports01/index/rp-valuations.html](https://stockviz.github.io/reports01/index/rp-valuations.html).
- Limits: Preserves outliers; visibility records the report's [-10,50] clip rather than deleting observations.

```json
{
  "name": "query_dashboard_dataset",
  "arguments": {
    "dataset_name": "DASHBOARD_VALUATION",
    "limit": 2
  }
}
```

<a id="dataset-DASHBOARD_VIX"></a>
#### `DASHBOARD_VIX`

VIX close and rolling one-standard-deviation bands.

- Grain and analytical keys: OBSERVED_DATE.
- Units: VIX, MEAN, LOWER_BAND, UPPER_BAND are VIX level units.
- Columns: `OBSERVED_DATE`, `VIX`, `MEAN`, `LOWER_BAND`, `UPPER_BAND`.
- Code-schema filter candidates: textual entity columns none; exact integer entity columns none; date columns `OBSERVED_DATE`.
- Related reports: [reports01/index/rp-vol-NIFTY.html](https://stockviz.github.io/reports01/index/rp-vol-NIFTY.html).
- Limits: Default 50-observation mean and sample SD; not a probability interval or a forecast.

```json
{
  "name": "query_dashboard_dataset",
  "arguments": {
    "dataset_name": "DASHBOARD_VIX",
    "limit": 2
  }
}
```

<a id="dataset-DASHBOARD_VIX_FORWARD_SAMPLE"></a>
#### `DASHBOARD_VIX_FORWARD_SAMPLE`

Historical future VIX levels after anchors near latest VIX.

- Grain and analytical keys: ANCHOR_DATE, OBSERVED_DATE, FORWARD_SESSIONS.
- Units: VIX is a level; FORWARD_SESSIONS counts 1..10 future observations.
- Columns: `ANCHOR_DATE`, `OBSERVED_DATE`, `FORWARD_SESSIONS`, `VIX`.
- Code-schema filter candidates: textual entity columns none; exact integer entity columns `FORWARD_SESSIONS`; date columns `ANCHOR_DATE`, `OBSERVED_DATE`.
- Related reports: [reports01/index/rp-vol-NIFTY.html](https://stockviz.github.io/reports01/index/rp-vol-NIFTY.html).
- Limits: Anchors lie strictly within +/-1% of latest available VIX. Samples overlap and near-end anchors have fewer outcomes; neither independent draws nor forecast probabilities.

```json
{
  "name": "query_dashboard_dataset",
  "arguments": {
    "dataset_name": "DASHBOARD_VIX_FORWARD_SAMPLE",
    "limit": 2
  }
}
```

<a id="dataset-DASHBOARD_YIELD_CURVE"></a>
#### `DASHBOARD_YIELD_CURVE`

Regional yield observations and same-date spreads to shortest available tenor.

- Grain and analytical keys: REGION, OBSERVED_DATE, MATURITY_YEARS.
- Units: MATURITY_YEARS is fractional years; YIELD_PCT annual percent; SPREAD_TO_SHORT_PCT_POINTS percentage points.
- Columns: `REGION`, `OBSERVED_DATE`, `MATURITY_YEARS`, `YIELD_PCT`, `SPREAD_TO_SHORT_PCT_POINTS`.
- Code-schema filter candidates: textual entity columns `REGION`; exact integer entity columns none; date columns `OBSERVED_DATE`.
- Related reports: [reports01/macro/rp-bnd.html](https://stockviz.github.io/reports01/macro/rp-bnd.html).
- Limits: Does not impose legacy complete-case tenor selections or yearly-lag curve snapshots. Yield-level percentage returns elsewhere are not yield changes in basis points or bond total returns.

```json
{
  "name": "query_dashboard_dataset",
  "arguments": {
    "dataset_name": "DASHBOARD_YIELD_CURVE",
    "limit": 2
  }
}
```

### Missing inputs, quality, and parity limits

Optional SQLite narratives and CSV references need accessible configured source files. Equity summaries, broker timelines, broker narratives, and industry summaries can be unavailable independently. `quality=unavailable` and warnings are evidence of a missing input; an empty result is not proof that no report narrative exists. Dated narratives retain malformed source dates in `CONTENT_JSON` with `AS_OF=NULL`, `invalid_source_date_count`, and partial quality. Undated narratives and CSV definitions are current-state references, not historical snapshots.

The catalog and query metadata, when reachable, determine what is actually published. The lineage describes code-level contracts and earlier bounded probes; those are not current deployment, freshness, row-count, or all-history validation. This documentation task did not read native databases, authenticate, execute report producers, or run loaders. The live MCP catalog could not be read because the connection closed on both attempts. No dataset response or financial result was synthesized.

Several report calculations remain absent or deliberately different:

- Shared fan-chart eligibility/filling/highlighting and unavailable external plotting-helper behavior are not materialized. Pixel-perfect HTML, images, and cached RData are outside these datasets.
- Market horizons use return intervals rather than the legacy number of price rows. Whole-window risk/daily-return distributions do not reproduce rolling annual-return or SMA-scenario distributions. Generic lagged SMA facts do not include report UPR scores or all strategy/ranking outputs.
- Current cohort/snapshot facts are not complete historical constituent archives. ETF holdings changes, exact country/sector heatmaps, and report freshness gates are not emitted merely by exposing prices and metadata. The CME helper is defined but unused by the audited commodity report.
- Stored CAPM metrics require upstream formula/unit verification. Fama-French copied betas are scaled by 100. Generic ETF weekly regressions do not reproduce a legacy report model, and MF weekly regressions do not reproduce the master report's monthly full-history models, reciprocal-beta radar, or peer ranks.
- Equity financials/financing facts do not include every legacy fallback, corporate-action annotation, consolidation convention, or historical financing regime adjustment. The supplemental industry standalone preference intentionally corrects a legacy global-selection issue rather than claiming numerical identity.
- PMS facts omit report strategy counts, selection/leaderboard logic, benchmark/composite paths, annualized return, Sharpe, and IR. Conflicting canonical keys remain auditable, so client calculations must address conflicts explicitly.

### Link-check results and unresolved mappings

All 55 dataset contracts have at least one source-traced, existing rendered report page. All 36 distinct report URLs linked here returned HTTP GET `200` in bounded checks on October 27, 2026; none returned a broken/unavailable status. Requests read at most 1024 response bytes with an 18-second timeout and six workers. This verifies route availability, not report recency, embedded assets, chart contents, or financial correctness.

No selected Rmd-to-rendered-page mapping is unresolved. Dynamic families use existing representative pages rather than invented template URLs; their complete page inventories were not link-checked. R helpers have no invented HTML routes, and R producers are traced to their actual Rmd/render targets. Remaining unresolved matters are live catalog availability/publication/filter advertisement, upstream metric/model definitions, unavailable optional-source configurations, external helper behavior, and numerical/model parity. `report-map.json` records these boundaries, exact source associations, per-dataset gaps, and each URL check.


<a id="exporting-with-mcp-consumer"></a>
## Exporting with mcp-consumer

The remote service returns bounded JSON pages. If you need a CSV without manually
passing pages through a model, use mcp-consumer 0.3.0 or later with your own private
configuration:

```sh
stockviz-mcp-consumer --config config.json dashboard-datasets --search PMS
stockviz-mcp-consumer --config config.json dashboard-query --dataset-name DASHBOARD_PMS_MONTHLY --page-size 2
stockviz-mcp-consumer --config config.json dashboard --dataset-name DASHBOARD_PMS_MONTHLY --date-column AS_OF --start 2025-01-01 --end 2025-12-31 --page-size 200 --output pms-2025.csv
```

The local stdio extension also exposes `download_dashboard_dataset`. That is a
consumer helper, not a thirty-first tool on the remote service. It follows remote
pages internally, verifies one publication generation, and returns file metadata
rather than raw rows or cursors. It refuses an existing destination and retains
clearly named partial files if an export fails. Account quotas and unavailable
sources still apply; a large export can fail before completion.

CSV represents both SQL NULL and an empty string as a blank cell. Use the JSON
query tool when that distinction matters. The exporter preserves numeric text and
does not escape text as spreadsheet formulas; import untrusted narrative columns
as text in a spreadsheet.

<a id="verification-and-scope"></a>
## Verification and scope

The tool argument reference follows the deployed `tools/list` catalog captured on October 27, 2026 (UTC). Dataset
names, filter columns, units, and report mappings follow the dashboard producer
schemas, data dictionary, source/report lineage, and report pages. The checks
validate documentation coverage and request structure; they do not execute every
protected example, prove that every source is populated, or establish numerical
parity with every chart on the reports website.

Use `get_data_quality` for the service's publication overview, each AMFI discovery
response for its own source coverage, and dashboard discovery/query metadata for
the particular report materialization. A fresh tool catalog does not imply fresh
financial observations.
