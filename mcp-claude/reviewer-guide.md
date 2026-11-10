# Reviewer access and test guide

## Connection and identity

Server: https://mutual-fund-mcp.stockviz.workers.dev/mcp
Transport: remote Streamable HTTP MCP.
Authentication: OAuth authorization code with PKCE and dynamic public-client registration. All data tools need `research:read`; public discovery works before login.

Add the server as a Claude custom connector, connect it, and complete the StockViz Auth0 email/password login with the dedicated reviewer identity supplied privately in the submission portal. Do not use the stockviz.biz website account, a Cloudflare service token or administrator credentials. No reviewer account exists yet. The submitter must provision and validate one before submission; this checkout does not contain credentials. Google/GitHub login is not part of the claimed acceptance.

Research data is shared published data rather than a reviewer's personal portfolio. An approved research identity should see populated catalogs subject to quotas. If sign-in succeeds but access is blocked or limited, contact info@stockviz.biz; the submitter must resolve access before submission. Do not work around blocks with another person's tokens.

## Functional acceptance

Use smoke-test-plan.json as a complete tool inventory, checked against the public catalog. Every entry starts `not_run`. The example arguments are templates from existing documentation, not fabricated successful responses. Resolve all discovery-dependent values from actual responses before executing a test. Historical dates must lie within returned coverage.

Recommended order:

1. `get_data_quality`: inspect current publication availability, coverage and warnings.
2. AMFI dataset discovery: resolve actual report dates; exercise AMFI snapshot, classification, consolidated AUM and category-flow tools. Retain INR units and distinguish AUM change from flow.
3. Fund discovery: select an actual plan code for NAV history and metrics; never submit the placeholder scheme code from a template as verified data.
4. Equity/index discovery: resolve exact symbol/series and index names; use a short covered date window for histories and a declared window for metrics.
5. Strategy and backtest discovery: resolve real strategy IDs and run IDs. `explain_signal` has been retired; archived decision-time inputs remain unavailable. Do not invent historical signals. For comparisons, select the IDs required by the current schema.
6. Dashboard discovery: choose an available dataset and advertised schema, then query a small page with supported filters.

For each tool record the client (Inspector and Claude separately), UTC timestamp, arguments with secrets removed, source observation dates, result status, warnings and artifact reference. Update status only after inspecting the result. `isError`, `unavailable`, and `data_gap` do not satisfy populated-data acceptance; an empty page may be legitimate but needs an explanation. Do not claim complete history from a partial page. Check continuation with unchanged filters when present.

Also verify invalid dates/inputs return actionable errors, a fresh connection signs in correctly, and a legitimate expired access grant refreshes without sharing tokens. Do not deliberately manipulate production credentials merely to force an expiry. A read-only annotation describes financial/research actions; the service still writes identity, quota and operational usage records.

Example Claude requests:

- "Use StockViz to list research strategies and data quality."
- "Use the actual published strategy ID to explain its definition, current research allocation and linked backtest."
- "Find two Direct Growth plans, then compare NAV metrics over a date range both cover; retain data warnings."
- "Rank consolidated mid-cap funds by average AUM at an available report date. Show the date and units, and keep this separate from net flows."
- "Discover a StockViz dashboard dataset and show two rows with its provenance and observation dates."

The remote connector does not require the optional local CSV downloader. Do not install a plugin or provide local filesystem access for this review.

## Evidence boundary

The public checker in scripts/check_readiness.py tests reachability, discovery metadata, tool annotations and the anonymous authentication challenge only. It neither signs in nor exercises authenticated data reads. Local fixtures and prior release documents do not replace the current per-tool Inspector/Claude acceptance. Screenshots and successful review claims must come from actual sessions, not generated mockups.
