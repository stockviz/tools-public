# MCP history CSV downloader

This directory contains `mcp-consumer-share.zip`, a source-only distribution of
a local downloader for compatible NAV, index and raw equity MCP history tools. It saves all
pages to a CSV without asking a language model to copy rows or pagination tokens.

## Install

Use Python 3.11 or later on Linux or macOS. Extract the ZIP on the machine where
you want the CSV files to live:

```sh
unzip mcp-consumer-share.zip
cd mcp-consumer
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.lock.txt
.venv/bin/python -m pip install -e .
cp config.example.json config.json
```

Edit `config.json` and replace `https://mcp.example.com/mcp` with the MCP endpoint
provided by your operator. Configure your private state and output directories.
Relative paths resolve beside the config file. There is no shared account or
built-in production endpoint.

The server must expose compatible `get_nav_history`, `get_index_history`,
`get_equity_history` and `list_equities`
tools and grant `research:read`. Enable `legacy_registration` only if your
operator confirms that the server needs the legacy public-client adapter.

## Sign in

```sh
.venv/bin/stockviz-mcp-consumer --config config.json login
```

Complete browser authorization using your own account. Each user creates their
own private OAuth cache. Do not copy another person's cache or put credentials
into the config file. If authorization expires and cannot refresh, run login
again.

## Download a CSV

Replace the scheme-code placeholder with an exact code from your server:

```sh
.venv/bin/stockviz-mcp-consumer --config config.json nav \
  --scheme-code '<SCHEME_CODE>' \
  --start 2020-01-01 --end 2025-12-31 \
  --output ./exports/fund.csv
```

For an index, use its exact catalog name:

```sh
.venv/bin/stockviz-mcp-consumer --config config.json index \
  --index-name '<EXACT_INDEX_NAME>' \
  --start 2020-01-01 \
  --output ./exports/index.csv
```

For equities, discover and export an explicit symbol/series pair:

```sh
.venv/bin/stockviz-mcp-consumer --config config.json equities \
  --search RELIANCE --series EQ --page-size 2

.venv/bin/stockviz-mcp-consumer --config config.json equity \
  --symbol RELIANCE --series EQ --start 2026-10-19 --end 2026-10-22 \
  --page-size 2 --output ./exports/reliance-eq.csv
```

The catalog returns one bounded page. Forward `--cursor` literally with unchanged
search, series and page size. Default catalog size is 250; maximum is 1,000.
Broad catalog scans can time out despite a small output limit. Both symbol and
series are mandatory for history; different series are different instruments.
Equity reads share the account's existing remote quotas and retry policy.

Dates are inclusive. Omit the end date for latest available observations. The
program follows every page in code and reports the completed path, row and page
counts, actual dates and SHA-256. It never overwrites an existing file. Failed
exports remain clearly named partial files rather than completed CSVs.

Transient concurrency, page-rate and policy-unavailable errors retry the exact
same page only when the server supplies an explicit valid delay: at most three
attempts per page and 30 seconds of retry waiting across the entire export.
Surfaced SDK HTTP 429 errors use valid `Retry-After` hints under these same bounds.
Long resets (such as 300 seconds), daily quotas, query timeouts and unknown errors
fail without a completed CSV. Safe diagnostics report the recognized category,
retry/reset metadata and retained partial path, not raw SDK messages. Partial
files cannot be resumed; wait or fix the cause before starting a new export.

## Use from Goose

After login, add a command-line/stdio MCP extension to Goose using this command.
Replace `<PROJECT_DIR>` with the absolute path of the extracted project:

```text
<PROJECT_DIR>/.venv/bin/stockviz-mcp-consumer --config <PROJECT_DIR>/config.json serve
```

Start with a tool timeout of 300 seconds. The extension exposes
`download_nav_history`, `download_index_history`, `download_equity_history`
and the read-only catalog tool `list_equities`. Ask Goose to use these local
download tools and return file metadata instead of copying remote tool results.
Goose's shell and the extension must share the filesystem to access the returned
paths.

The extension runs at most two complete downloads at once; additional calls
queue, so allow for queue time in Goose's timeout. Cancellation releases a slot
and never publishes an incomplete export. Independent CLI or server processes
have separate queues and remain limited by the remote server's policy.

## Privacy and integrity

The ZIP excludes deployment configuration, credentials, virtual environments,
exports, logs and caches. Do not distribute your configured working directory.
Runtime reports contain your paths and endpoint; review them before sharing.

The downloader validates counts, identity, dates, sort keys and continuation
progress. It preserves numeric strings and verifies the CSV before publication.
A remote mirror refresh can still change data between pages; the export is not
a guaranteed database snapshot. Raw NAV is not distribution-adjusted.

Equity CSV columns are
`symbol,series,date,open,high,low,close,last,previous_close,total_traded_quantity,total_traded_value,num_transactions`.
Prices and activity are raw stored values, not adjusted prices or total returns.
Nullable fields become empty cells; DOUBLE strings retain database text, not
arbitrary precision. Native SQL integer `num_transactions` values become integer
CSV text without floating-point conversion. Duplicate dates fail closed rather than being deduplicated.
Any failed page prevents a completed export. Ownership does not establish source
freshness. There is no equity summary tool; require all history pages before
calculating a window summary.

The bundle never includes local runtime configuration or OAuth credentials.

See the extracted project's README for the full contract, safety checks,
configuration options and tests.

## Maintainers

Edit the source project, not the generated ZIP or this published README. The
source build runs its tests and privacy scan before publication and leaves the
last good publication untouched when either fails. Identical builds do not
rewrite the public files. After completing a milestone, run
`.venv/bin/python build_share.py` from the source project. It tests, builds and
updates this directory once, then exits. Source edits alone do not publish a
release; no background service is required.
