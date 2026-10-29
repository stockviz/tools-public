# Lesson 7: Make research reproducible

[Previous lesson](06-dashboard-research.md) | [Course overview](README.md) | [Next lesson](08-capstone.md)

## Question and outcomes

Your agent produced a table. Can you trace the rows, repeat the calculation, and detect an incomplete download?

After this lesson, you can distinguish remote pages from local complete exports, preserve a research manifest, and verify calculations against their inputs.

Prerequisite: complete one earlier data lab. Allow about 60 minutes. The local downloader track needs Python 3.11 or later on Linux/macOS and a private workspace. You can instead use your agent's supported complete-page retrieval with saved evidence; do not claim a local export you did not run.

## Concepts to learn

A remote history tool returns a bounded page. `format=csv` adds inline CSV for that page; it does not create a complete local history file. The optional consumer follows pages in code and reports completed file metadata. Its local `download_*` tools are not remote service tools.

The downloader does not proxy the separate remote AUM analytics tools. Save their responses through your own agent/workspace workflow when permitted. Do not invent an AUM CLI command.

## Guided lab: choose an evidence route

### Route A: local downloader

1. Follow the [consumer installation and sign-in instructions](../../mf-mcp-consumer/README.md#install) in a clean private working directory. Use your own OAuth cache. The ZIP's outer `mcp-consumer` directory is the project root; its inner `mcp_consumer` directory is the Python package.
2. Sign in under the OS account that runs the consumer. Keep one operation at a time against a shared OAuth cache because rotating refresh credentials are single-use. Do not share caches.
3. Choose one already discovered index, NAV plan, equity pair, or dashboard dataset and a short covered window. Use a new filename. For dashboard filters, inspect the published schema first.
4. Run the export using the documented CLI or local tool. Let code handle pagination rather than asking the model to transcribe every row or cursor.
5. Inspect the completion metadata and open the actual file with your analysis tool. Verify row count, actual dates, identity, and SHA-256 with code. A checksum detects file changes; it does not certify financial truth.
6. Save the request, schema/units, warnings, and publication metadata beside the analysis, excluding credentials and sensitive local details from any shared copy.

From the installed outer project directory, these are discovery/preview commands, not complete exports:

```sh
.venv/bin/stockviz-mcp-consumer --config config.json dashboard-datasets --search PMS --page-size 20
.venv/bin/stockviz-mcp-consumer --config config.json dashboard-query --dataset-name DASHBOARD_PMS_MONTHLY --page-size 2
```

For the actual export, use the documented `dashboard`, `nav`, `index`, or `equity` command with your discovered identifiers and chosen window. The [consumer guide](../../mf-mcp-consumer/README.md#download-a-csv) gives the syntax. For a local agent extension, use this prompt after replacing the bracketed placeholders with discovered values:

```text
Use the LOCAL StockViz CSV downloader's download_index_history tool for
index_name [EXACT_DISCOVERED_NAME], start [COVERED_START], end [COVERED_END],
and filename [NEW_CSV_BASENAME]. Let the tool handle all pages. Return completed
path, row/page counts, actual coverage, SHA-256, and warnings, not copied rows.
Then use a separate analysis tool to open and verify the saved file. If export
fails, report the failure and partial path; do not analyze it as complete.
```

Local tool filenames are confined new basenames, not arbitrary absolute paths. Keep remote and local extensions distinct when both advertise dashboard discovery/query tools.

### Route B: saved remote evidence

1. Choose a small bounded query from an earlier lesson and inspect its current pagination contract.
2. Save every successful page through your agent's file/analysis facilities, keeping filters and limit unchanged. Retain counts, actual dates, source warnings, and publication metadata.
3. Verify completion programmatically using the tool's actual continuation fields. If a continuation fails or publication changes, restart; do not stitch the attempts together.
4. Create an input manifest and run one calculation from the complete saved rows. Label this as saved MCP evidence, not a consumer-verified export.

For a nonpaginated metrics tool, save its full returned response and calculation conventions instead. That supports a metric citation, not a claim that you independently reproduced the underlying history.

## Independent exercise

Ask the agent to reproduce one modest result, such as endpoint NAV change or a manager's AUM change between two valid observed reports. Freeze the inputs before calculating. Verify that the file really contains the cited identities and dates, and document missing/conflicting rows.

Your manifest should contain:

- Research question, source tool, exact nonsecret arguments, and retrieval timestamp.
- Requested and actual coverage, source/publication dates, units, and grain.
- Completion status, page/row counts where applicable, file path, and checksum.
- Warnings, exclusions, calculation method, script/tool used, and result location.

CSV blanks cannot distinguish SQL NULL from empty text. Preserve bounded JSON evidence if that distinction matters. Numeric text needs deliberate parsing; untrusted narrative fields must be imported as text, not executed as spreadsheet formulas.

## Completion check

Submit a verified evidence bundle and one reproducible calculation, or a clearly labeled blocked export specification if you lack local access. The blocked specification is useful partial work, not a completed export lab.

You pass the practical lab only with a real completed file or saved response, actual verification output, and a result traceable to it. Failed exports retain partial files and never count as complete. Existing files are not overwritten; choose a new name. Do not repeatedly retry quotas or timeouts, and do not bypass account limits.

## Reading

Read the [consumer guide](../../mf-mcp-consumer/README.md), especially authentication, partial-file handling, privacy, and integrity, and [remote versus local dashboard export](../samples/mcp-service-tool-samples.md#exporting-with-mcp-consumer).
