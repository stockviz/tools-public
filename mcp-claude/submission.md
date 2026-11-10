# Directory submission worksheet

Reference requirements checked on 2026-11-10:

- https://claude.com/docs/connectors/building/submission
- https://claude.com/docs/connectors/building/review-criteria
- https://claude.com/docs/connectors/building/authentication
- https://claude.com/docs/connectors/building/testing

Open https://claude.ai/directory/manage > Submit new > MCP connector. This is a remote connector, not a local MCPB extension, plugin or MCP App. This package does not accept directory terms or submit on the owner's behalf.

## Current release status

The owner approved the privacy notice, removal of `explain_signal`, production deployment and public documentation publication. The release candidate has 29 read-only tools with titles. Check evidence/release-status.json for the verified deployment and publication state; plans are not deployment evidence.

Two launch requirements remain blocked: no dedicated reviewer identity exists, and there is no signed-in Claude session available for authenticated acceptance. Do not confirm the portal's every-tool testing checkbox until the tests are actually complete. Public Inspector discovery and a passing public readiness probe do not satisfy these requirements.

## Portal fields

### Connection

Universal URL: https://mutual-fund-mcp.stockviz.workers.dev/mcp

StockViz operates this Cloudflare Worker and its research API. All users use the same URL. The hostname contains StockViz but uses workers.dev; no custom-domain or per-customer URL migration is part of this release.

### Tools

The portal syncs the catalog from the live server, not listing.json. The release exposes 29 read-only tools; each must have a title, readOnlyHint true and destructiveHint false. Names must be at most 64 characters. `explain_signal` is retired because exact archived decision-time inputs are unavailable. Clients must refresh discovery; do not replace it with a fabricated explanation.

No trading, financial-transfer or private-account tools are exposed. Login, quota and operational telemetry records are service-side writes, not financial transactions.

### Listing

Copy the name, one-liner and detail-card description from listing.json. Proposed permanent slug: `stockviz`; check its availability before publishing. Suggested category: Finance, if offered by the portal; use the portal's actual category choices.

Documentation URL:
https://github.com/stockviz/tools-public/blob/main/mcp-claude/README.md

Privacy policy URL:
https://github.com/stockviz/tools-public/blob/main/mcp-claude/privacy-policy.md

Support: info@stockviz.biz.
Icon: assets/stockviz-icon.png, a 1024 x 1024 PNG from the existing StockViz marketing logo. Carousel screenshots are not required because this connector does not provide an interactive MCP App.

### Use cases

Read Indian fund AUM and reported category flows; compare NAV and index performance; inspect published strategy/model research; query bounded public dashboard datasets. Users need their own StockViz MCP Auth0 sign-in. Automatic enrollment does not remove quotas or administrator blocks. The optional local CSV downloader is not required.

### Company

Display name: StockViz.
Legal operator: SAS DATA ANALYTICS PVT. LTD.
Website: https://stockviz.biz/.
Support/privacy contact: info@stockviz.biz.

The owner approved the privacy/legal/data-rights confirmation in the preparation conversation. The person submitting must enter the primary review contact and accept the portal's terms and acknowledgments themselves. Do not infer a personal contact address or sign for the owner.

### Authentication

Choose OAuth sign-in with Dynamic Client Registration (`oauth_dcr`), public client, authorization code with S256 PKCE. Do not enter Auth0's upstream client secret into Claude. The MCP Worker is Claude's downstream authorization server; Auth0 supplies upstream user sign-in.

Public initialize/tools/list do not grant data access. All data tools require `research:read`. Select "Required when the server asks" for discovery-before-sign-in behavior, then verify that Claude actually starts sign-in on the protected 401 challenge. This is not an anonymous public-data connector. Static service headers are not required. CIMD and Anthropic-held client credentials are not claimed.

Endpoints:
- `/.well-known/oauth-authorization-server`
- `/.well-known/oauth-protected-resource`
- `/authorize`
- `/oauth/register`
- `/oauth/token`

Claude callback: https://claude.ai/api/mcp/auth_callback.

Email/password is the documented login path. Google/GitHub are outside the claimed acceptance scope. Verify fresh sign-in, state/callback handling, code exchange, protected access and refresh in the actual Claude client; public metadata alone proves none of these. Do not request administrator scopes or disclose ingestion credentials.

### Data handling

The research API is operated by StockViz; underlying market and fund datasets are derived from external sources. The owner approved the requested data-rights confirmation. The tools do not request health data, execute financial transfers, generate AI media or inspect Claude memory/history/files. The submitter must answer the sponsored-content field accurately for the actual published datasets.

The approved privacy notice discloses identity, operational usage, optional query diagnostics, infrastructure logging, service providers and retention limitations. Read it before completing the portal's data-handling fields. Credential expiry is not record deletion.

### Test & launch

Follow reviewer-guide.md. Create a dedicated, non-admin Auth0 email/password reviewer identity and validate access to populated shared research data. Enter credentials only in the portal's private reviewer fields. Never commit its password, OAuth credentials or account IDs. Supply every sign-in step, any MFA requirement, account expiry and quota information privately.

No reviewer account is currently available. A link to self-registration is not a substitute for the requested test credentials. Do not disable authentication, reuse an administrator account, mint a signed token or grant unapproved quota exemptions to bypass this gate.

Exercise all 29 tools in MCP Inspector and in a Claude custom-connector conversation. Record actual identifiers, dates, warnings and sanitized evidence. smoke-test-plan.json remains an unexecuted checklist until those results exist. `data_gap` and `unavailable` are not populated-data success.

### Compliance and submission

The owner must review and acknowledge all seven portal statements: directory guidelines, first-party API usage, financial transactions, AI media generation, prompt injection, conversation data collection and public documentation. Privacy approval is not acceptance of Anthropic's directory terms.

After reviewer access and authenticated tool acceptance pass, an eligible paid Claude account can submit. Review status and directory acceptance belong to Anthropic. A deployed connector and public documentation do not by themselves prove submission readiness.
