# StockViz MCP connector privacy notice

Effective date: 2026-11-10.

## Scope and contact

SAS DATA ANALYTICS PVT. LTD., operating as StockViz, provides the remote MCP research connector at https://mutual-fund-mcp.stockviz.workers.dev/mcp. This notice covers that connector, not all services on stockviz.biz, your broker, or your use of Claude.

Contact info@stockviz.biz for support, privacy questions, or a request about your account data. Do not send passwords, access tokens, refresh tokens, or personal financial records by email.

## Information processed

When you sign in, the connector processes the identity-provider issuer, subject identifier, provider, email address and email-verification status when supplied. Application records include account creation and activity, first and most recent successful sign-in, most recent successful tool use, approval or block status, access policy, quotas and policy revisions. Provider identifiers distinguish accounts; the service does not need your brokerage account or personal holdings for research access.

OAuth processing includes client identifiers, callback addresses, requested scopes, PKCE challenges, short-lived authorization state and codes, signed access tokens and refresh-token families. The application stores refresh-token hashes and family metadata rather than the raw refresh token in its refresh-grant database. Your client retains the credentials it needs to maintain your connection.

Tool requests contain arguments needed for your question, such as fund codes, equity symbols, index or dataset names, dates, search filters and pagination cursors. The connector processes those arguments to query research data and returns results to Claude. Access control and monitoring use account identifiers, operation categories, counts, volume, timing, failures and quota or administrator-audit information.

Optional diagnostic tracing can record NAV request filters, timestamps, client class and cursor metadata, including allowlisted public cursor fields. Infrastructure logs may include request URLs, query strings and operational metadata. Application diagnostic restrictions do not mean that infrastructure logs are empty or that every query parameter is redacted.

The connector's tools do not request your complete Claude conversation, Claude memory, chat history or local files. Claude may include information from your prompt in tool arguments. Avoid putting personal or confidential information into research filters. This notice does not describe Anthropic's separate handling of your conversations.

## Purposes and storage

StockViz uses identity and operational information to authenticate users, enforce permissions and quotas, prevent abuse, diagnose failures and support the connection. Research publications are separate from your personal investment accounts. The connector does not execute trades, transfer financial assets or manage your personal portfolio.

Application infrastructure includes Cloudflare Workers, D1, Durable Objects, R2 and Hyperdrive. Auth0 supplies the current user sign-in flow. Research reads use a StockViz-operated MariaDB mirror alongside published research storage. Infrastructure providers may process information outside your country; their processing locations, subprocessors and safeguards are described in their own notices and terms.

## Sharing and providers

Claude receives the research results requested through the connector. Auth0 and Cloudflare process identity, requests or operational information as needed to provide their services. A selected social identity provider handles its own authentication if you choose an available social sign-in.

The connector does not send your identity to a broker to answer research queries. StockViz may disclose information when required by law, to address abuse or security incidents, or to respond to a request you authorize. This research service does not require the sale of personal information or advertising profiles to answer your questions.

Relevant provider notices:

- https://www.anthropic.com/legal/privacy
- https://www.cloudflare.com/privacypolicy/
- https://www.okta.com/privacy-policy/

## Retention and deletion requests

The current application settings retain account usage aggregates for 30 days and service usage aggregates for 90 days, subject to asynchronous cleanup. OAuth access tokens have a 24-hour validity period and refresh grants have a 30-day absolute lifetime. Credential expiration prevents further use but does not itself delete database rows, audit records, logs or backups.

Account identity, access policy, administrator audit, expired or revoked token-family and replay-protection records do not currently have a fixed automatic deletion schedule. Infrastructure logs and backups have separate provider-managed lifecycles. Contact info@stockviz.biz to request access, correction or deletion of account information. StockViz will assess the request and explain any records retained for security, legal obligations or backup lifecycle reasons. This notice does not promise that all copies are erased immediately or within the usage-aggregate retention window.

Disconnecting the connector in Claude stops that connection's use; it is not an account-record deletion request. You may also request that StockViz block further service access for your identity.

## Security and changes

The application uses HTTPS, scoped OAuth credentials and access controls. Explicit administrator blocks and quotas still apply after sign-in. Do not share another person's OAuth cache or put tokens in URLs, public issues or repository files. No internet service can guarantee absolute security.

StockViz may update this notice as the service changes. The effective date above identifies the published version; contact the privacy address if you need clarification about a change.
