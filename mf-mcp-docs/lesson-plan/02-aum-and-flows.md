# Lesson 2: Follow the money

[Previous lesson](01-evidence-and-discovery.md) | [Course overview](README.md) | [Next lesson](03-nav-and-fund-comparisons.md)

## Question and outcomes

A fund gets larger. Did investors add money, did its investments appreciate, or did its identity change? Size alone cannot tell you.

After this lesson, you can distinguish fund houses, underlying funds, and plans; choose between raw-plan and consolidated AUM; and compare asset growth with reported flows without confusing the two.

Prerequisite: lesson 1 and available AMFI metadata. Allow about 60 minutes.

## Concepts to learn

Assets under management (AUM) measure assets at a date; average AUM averages assets over a reporting period. Neither is an investment return. Subscriptions are money entering; redemptions are money leaving; reported net flows describe their net movement. Asset values also change with investment performance, distributions, mergers, and other changes. Average AUM differences are especially unsuitable for reconstructing cash flows.

A fund house manages multiple underlying funds. An underlying fund can have Direct and Regular plans and Growth or distribution options. A raw-plan ranking does not rank consolidated underlying funds. Canonical consolidation uses a versioned name heuristic, not an authoritative merger history.

The sources also use different units: monthly category monetary statistics use INR crore; raw scheme/fund-house average AUM uses INR lakh. Inspect the returned units instead of assuming a common scale. Sum compatible flows across observed reporting periods when appropriate; never sum monthly AUM snapshots into an annual asset total.

## Guided lab

1. Revisit `get_amfi_datasets`. Choose an available scheme-AUM report and a bounded monthly-statistics window. Record actual source dates; do not assume matching publication schedules.
2. Use `get_amfi_aum_ranking` for an underlying-fund or category ranking at one report. Set an explicit date selector and inspect consolidation/classification warnings.
3. Use `get_amfi_aum_growth` with explicit cutoffs to examine asset change. Record the resolved baseline and endpoint dates, which can precede your cutoffs.
4. Separately use `query_amfi_flows` at category granularity for an available bounded period. Preserve source section, category group, and exact category identity. Check missing-month coverage.
5. Write an observation about size and another about flows. Do not say which fund performed best: you have not measured NAV performance.

Paste this prompt:

```text
Use AMFI discovery to choose a category and a short covered date window. Inspect
the current schemas first. Retrieve a consolidated AUM ranking, AUM growth with
explicit start/end cutoffs, and separately reported category flows for a covered
window. Explain whether the source dates and category identities match. Show
resolved reports, units, consolidation method, and missing coverage. Follow all
pages needed for claims about a whole result, or label a bounded top-N preview.
Do not infer fund inflows from AUM growth or fund returns from either measure.
```

For a category-history extension, use `get_amfi_category_aum_history`. It always groups by category and can return short pages while more data remains. Follow `has_more`, not page length.

## Independent exercise

Critique these claims using your saved evidence:

1. "This fund's average assets rose most, so it delivered the best return."
2. "Adding every monthly AUM number gives annual inflows."
3. "A category flow ranking identifies the fund that attracted the most money."
4. "The historical category was known at that time because the report date is old."

For each, name the mistaken inference and the data you would need to support a narrower claim. `query_amfi_flows` documents fund-level flows as a `data_gap`; a schema accepting `granularity=fund` does not make those flows available.

## Completion check

Submit a two-part comparison: AUM evidence and flow evidence. Include requested/resolved dates, source identities, units, warnings, and a paragraph on why the two parts are not a return ranking.

You pass when you distinguish exact `period` from an `as_of` cutoff, explain latest-classification bias in historical AUM queries, and avoid adding overlapping category totals. If using `get_amfi_category_aum`, note that changes are `compare_period minus period`, not the reverse.

Optional programming task: use decimal arithmetic to normalize monetary units and label every column with its unit. Preserve null values and verify conversions with code.

## Reading

Read [consolidated rankings](../samples/mcp-service-tool-samples.md#tool-get_amfi_aum_ranking), [AUM growth](../samples/mcp-service-tool-samples.md#tool-get_amfi_aum_growth), [category history](../samples/mcp-service-tool-samples.md#tool-get_amfi_category_aum_history), and [reported flows](../samples/mcp-service-tool-samples.md#tool-query_amfi_flows). Compare their grain with [raw scheme AUM](../samples/mcp-service-tool-samples.md#tool-get_amfi_scheme_aum).
