# MCP history CSV downloader

This directory contains `mcp-consumer-share.zip`, a source-only distribution of
a local downloader for compatible NAV, index and raw equity MCP history tools. It saves all
pages to a CSV without asking a language model to copy rows or pagination tokens.

## Install

Use Python 3.11 or later on Linux/macOS (POSIX). Install on the same machine
and under the same OS account that will run Goose and own the CSV files. In a
terminal, start in the directory containing the downloaded ZIP:

```sh
unzip mcp-consumer-share.zip
cd mcp-consumer
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.lock.txt
.venv/bin/python -m pip install -e .
```

The ZIP has one outer project folder, `mcp-consumer/` (hyphen). Its child
`mcp_consumer/` (underscore) is the Python package, not the installation root.
Run the remaining terminal commands from the outer folder, which contains
`pyproject.toml` and `config.json`. If you already extracted the ZIP, open that
folder rather than extracting again. The ZIP deliberately excludes `.venv`;
installation creates `.venv/bin/stockviz-mcp-consumer`. Use this same environment
for login and Goose. Do not point Goose at a virtual environment from another
machine or a directory you later move.

The included `config.json` is ready to use:

```json
{
  "server_url": "https://mutual-fund-mcp.stockviz.workers.dev/mcp",
  "output_dir": "./exports"
}
```

You do not need to copy or edit configuration before login. OAuth state uses your
own per-user home directory, not a shared cache. Relative output paths resolve
beside the config file. To use another compatible endpoint, edit `server_url` or
pass `--url`. Standard SDK OAuth client registration is used by default.

The server must expose compatible `get_nav_history`, `get_index_history`,
`get_equity_history` and `list_equities`
tools and grant `research:read`. StockViz PortfolioManagerMf supports standard
OAuth client registration.

## Sign in

Sign in with the included config:

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

Run `login` first on this machine under the OS account that runs Goose. From
the outer `mcp-consumer/` project folder, generate a command with absolute paths
and the quoting Goose needs, including when your installation path has spaces:

```sh
GOOSE_COMMAND="$(.venv/bin/python - <<'PY'
from pathlib import Path
import shlex

root = Path.cwd().resolve()
executable = root / ".venv/bin/stockviz-mcp-consumer"
config = root / "config.json"
if not executable.is_file() or not config.is_file():
    raise SystemExit("Run this from the installed project root after pip install -e .")
print(shlex.join([str(executable), "--config", str(config), "serve"]))
PY
)"
printf '%s\n' "$GOOSE_COMMAND"
goose session --with-extension "$GOOSE_COMMAND"
```

The last line starts a Goose CLI session with the local extension. For a
persistent setup, run `goose configure` → `Add Extension` → `Command-line
Extension`. Paste the **entire printed line**, including its quotes, into the
command field. In Goose Desktop, add a custom STDIO extension and paste that
same line into **Command**. Set the timeout to **300 seconds** initially and
leave environment variables empty. Longer or queued downloads may need a larger
timeout. Do not enter the remote HTTP MCP URL for this local downloader.

Goose does not expand placeholders, `~`, or shell variables in a pasted Command.
Paste the printed absolute command, not `$GOOSE_COMMAND` or the generator above.
Keep its quotes: an unquoted path containing spaces can produce "Failed to start
extension" or "No such file or directory". If a file is missing, check that you
installed from the outer project folder and that both the executable and
`config.json` still exist at the printed paths. After moving the project,
recreate `.venv` with the install steps and generate the command again.

Running the printed `serve` command manually normally stays quiet while waiting
for MCP messages on stdin; this is not a hung download. Press Ctrl-C to stop it,
then let Goose launch it. The configured `output_dir` resolves beside
`config.json`, independent of Goose's working directory; the default is the
project's `exports/`. Do not put OAuth tokens in Goose's settings.

The extension exposes
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

The ZIP includes only a generated public config, never the publisher's local
configuration, credentials, virtual environments, exports, logs or caches. Do not
distribute your configured working directory.
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

The builder generates `config.json` from fixed public defaults without reading the
publisher's local config. The bundle never includes OAuth credentials or state.

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
