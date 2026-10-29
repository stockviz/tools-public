# Lesson 1: Establish the evidence

[Course overview](README.md) | [Next lesson](02-aum-and-flows.md)

## Question and outcomes

You ask an agent, "How are Indian mutual funds doing?" It could answer with fund size, investor buying, or investment returns. Those are different questions.

After this lesson, you can narrow an open-ended question, inspect source availability, and explain why an authenticated tool response is stronger evidence than an agent's recollection but still needs checking.

Prerequisite: complete the remote connection and OAuth steps in the course overview. Allow about 45 minutes.

## Concepts to learn

MCP lets an agent discover named tools and call them with structured arguments. It does not make the agent a financial expert or guarantee that every underlying source is fresh.

A dataset's _grain_ describes one row: for example, a category in a monthly report or one fund plan on one NAV date. A question about individual funds cannot automatically be answered by a category-level table.

Keep these dates separate: your requested cutoff, an observation date, an ingestion snapshot, and a publication refresh. A recently refreshed mirror can contain old observations. A financial period end does not necessarily tell you when investors first knew the information.

## Guided lab

1. Ask the agent to inspect the connected server's tool names and schemas. Find tools for data quality, AMFI metadata, NAV metrics, index discovery, strategy discovery, and dashboard discovery.
2. Call `get_data_quality` and `get_amfi_datasets`, both with empty arguments. Read each source's status and warnings, not only the top-level status.
3. Choose one question about fund assets and one about investment performance. Identify a suitable tool for each without retrieving a large history.
4. Save a capability note with the question, source, grain, available coverage, units, and unresolved limitations.

Paste this prompt:

```text
Inspect my remote StockViz MCP connection. Call get_data_quality and
get_amfi_datasets with empty arguments. Summarize source-specific availability,
coverage, freshness metadata, and warnings without equating availability with
verified completeness. Then map these questions to tools: category net inflows,
Direct Growth fund performance, index drawdowns, and published strategy rules.
Do not download histories yet. Report schema/documentation mismatches explicitly.
```

These are example `tools/call` parameters, not standalone HTTP request bodies:

```json
{"name":"get_data_quality","arguments":{}}
```

```json
{"name":"get_amfi_datasets","arguments":{}}
```

Use your initialized MCP client to make the calls. The agent usually handles that protocol wrapper.

## Independent exercise

Rewrite "Find the best mutual fund" as two answerable research questions. Give each a population, measurement, date window, and limitation. For example, a comparison of specified Direct Growth plans over a shared observed window is narrower than a claim about every fund.

Then ask the agent to critique your questions. Reject any critique that substitutes a recommendation for a measurable question.

## Completion check

Submit the capability note and your two revised questions. You pass when you can explain:

- Why public discovery does not authorize a protected call.
- Why a source's latest observation can precede the date of your query.
- Why "unavailable" is not the same as a measured zero.
- Which evidence supports one concrete answer, and which evidence is missing.

Optional programming task: represent the note as JSON with explicit `requested_window`, `observed_window`, `units`, `status`, and `warnings` fields. Keep credentials out of it.

## Reading

Read [using the examples](../samples/mcp-service-tool-samples.md#using-the-examples), [pagination and data quality](../samples/mcp-service-tool-samples.md#pagination-and-data-quality), and the references for [AMFI discovery](../samples/mcp-service-tool-samples.md#tool-get_amfi_datasets) and [data quality](../samples/mcp-service-tool-samples.md#tool-get_data_quality).
