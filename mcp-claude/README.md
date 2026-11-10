# StockViz connector for Claude

StockViz gives Claude read-only access to Indian mutual-fund and market research: AMFI AUM and category flows, fund NAVs, index and equity history, published strategies and backtests, and dashboard datasets.

It cannot place trades, move money, or access your personal portfolio. Published model portfolios are research portfolios, not your brokerage holdings. Data may be delayed or incomplete; this is not investment advice.

## Connect

1. In Claude, open Settings > Connectors and add a custom connector (the wording and availability depend on your plan and organization).
2. Name it StockViz and use `https://mutual-fund-mcp.stockviz.workers.dev/mcp`.
3. Connect and complete the StockViz Auth0 sign-in. Use your own email/password account. This is separate from the stockviz.biz website login. The service automatically approves a successful new sign-in, subject to explicit account blocks and quotas.
4. Grant the research connection. The required tool scope is `research:read`; you do not need administrator credentials or a manually shared API token.
5. Ask: "Use StockViz to show data quality and the available research strategies."

The server uses remote Streamable HTTP MCP, OAuth authorization code with PKCE and dynamic public-client registration. Discovery can work before sign-in; data tools require authentication. Choose sign-in when the server asks if Claude offers lazy authentication. Do not interpret discovery alone as a successful login.

Email/password is the documented acceptance path. Google and GitHub sign-ins are not claimed as verified for this submission. If login fails, disconnect and reconnect; contact support if a fresh login still fails. Never send support a token or password.

## Example requests

- Which mid-cap funds had the largest average AUM in the last available AMFI report? Consolidate plan variants and report the source date and units.
- Compare NAV-based performance for two Direct Growth plans over a specified date window. Discover exact scheme codes first.
- Show the full-window drawdown and performance of NIFTY 50 using stored index observations.
- Explain a published StockViz strategy and its linked backtest, including assumptions and source dates.
- Discover the available dashboard datasets and show a small dated sample from a selected dataset.

Start with `get_data_quality`, `get_amfi_datasets`, `list_strategies`, or `list_dashboard_datasets`. Some broad catalogs can be slow. Use narrow search/date filters and bounded pages. Follow returned cursors unchanged until `has_more` is false when you need a complete download; a first page is not a full history. Account limits apply even to read-only operations.

AUM growth is not fund return or net inflow. AMFI plan consolidation uses disclosed name heuristics; current classifications may not be point-in-time. Raw equity history is not adjusted total-return data. Preserve source dates, units, coverage and warnings in any analysis. Backtests do not guarantee future returns.

See the [full tool guide and dashboard recipes](../mf-mcp-docs/samples/mcp-service-tool-samples.md) and [research lesson plan](../mf-mcp-docs/lesson-plan/README.md).

## Privacy and support

The [connector privacy notice](privacy-policy.md) describes identity and operational data used by this service. Support and privacy requests: info@stockviz.biz. Do not include account passwords, OAuth tokens, or personal financial records in your request.

## Directory submission package

This checkout is preparation material, not a submitted or approved directory listing.

- [Portal answers and release gates](submission.md)
- [Reviewer setup and acceptance](reviewer-guide.md)
- `listing.json`: copyable listing fields, with unresolved owner decisions kept separate.
- `smoke-test-plan.json`: one acceptance entry per discovered tool; examples require discovery substitutions and are not execution evidence.
- `assets/stockviz-icon.png`: square PNG derived from the existing StockViz marketing logo.
- `evidence/live-readiness.json`: timestamped public production checks, not authenticated tool acceptance.

Run the non-mutating public preflight from this directory:

```sh
python3 -m unittest discover -s tests -v
python3 scripts/check_readiness.py --output evidence/live-readiness.json
```

The checker deliberately exits nonzero when the live endpoint fails a requirement. It does not authenticate, create accounts, register OAuth clients, call protected data successfully, deploy, or submit. Its anonymous call only checks the authentication challenge. A green result is not proof that every tool works in Claude.

The initial 2026-11-10 directory-preparation release exposed 29 titled read-only tools. `explain_signal` was retired because archived decision-time inputs are unavailable; reconnect clients to refresh discovery. That initial Worker suite passed 1,083 tests across 51 files. The current reviewer-fix suite passes 1,142 tests across 53 files and typecheck; all 135 public checks still pass. See the release evidence below for the current version and targeted protected-call results.

The reviewer regression release fixes NAV name-search timeouts, queues small concurrent bursts without raising backend caps, and returns actionable errors for unknown research IDs. Protected production tests passed all three reported searches, two eight-call bursts, seven unknown-ID cases and complete searched pagination reconciled to native data. See [targeted remediation evidence](evidence/reviewer-remediation.json); this is separate from the original directory acceptance checklist.

The privacy notice is owner-approved. A reviewer account and authenticated every-tool Inspector/Claude acceptance are still required before submission; neither is available yet. See submission.md for the remaining launch steps.
