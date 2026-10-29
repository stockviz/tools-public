# Research financial markets with the StockViz MCP

This course teaches you to use an AI agent to ask financial questions, retrieve StockViz data, and check whether the answer follows from the evidence. You already know how to work with an agent and have written some code. You do not need prior finance training, SQL, or an MCP server implementation.

The course centers on Indian mutual funds and indices, then introduces equity and dashboard research. You finish with a short research memo that another person can reproduce. You do not build a trading bot or receive a list of investments to buy.

## Learning outcomes

By the end, you can:

- Translate a market question into a suitable dataset and sequence of tool calls.
- Distinguish assets under management, investor flows, and investment returns.
- Resolve fund plans, index names, and equity symbol/series pairs without guessing.
- Interpret returns, drawdowns, and risk statistics within their measurement limits.
- Audit a published strategy and explain what its backtest cannot establish.
- Query dashboard data using its published schema and export complete results.
- Write conclusions that separate observations, interpretations, and unanswered questions.

## Before you start

You need an AI agent with remote HTTP MCP support, an account authorized to read the service, and a place to save research notes. A terminal and Python 3.11 or later are needed only for the optional local CSV downloader and coding extensions. A spreadsheet can replace Python for most analysis, provided you handle numeric text and missing values deliberately.

Connect your client's remote MCP integration to:

```text
https://mutual-fund-mcp.stockviz.workers.dev/mcp
```

Follow your client's setup instructions and OAuth browser sign-in. This course does not assume a particular agent or invent client-specific configuration. Protocol initialization and tool discovery are public; protected tool calls require your own token with `research:read`. Never paste credentials, callback codes, or access/refresh tokens into a conversation or lesson file. See the [authentication and request guide](../samples/mcp-service-tool-samples.md#using-the-examples).

The tools are research reads. A published model portfolio is not your private account, and the remote service cannot place orders. The optional downloader writes local files, which is a separate capability.

## Course sequence

Study in order on your own, or use one lesson per group meeting. Times are planning estimates, including exercises, rather than measured completion times.

| Lesson | Main question | Suggested time | Saved work |
| --- | --- | --- | --- |
| [1. Establish the evidence](01-evidence-and-discovery.md) | What can this service actually answer? | 45 minutes | Capability and source-status note |
| [2. Follow the money](02-aum-and-flows.md) | Does a growing fund mean strong returns or new money? | 60 minutes | AUM and flow comparison |
| [3. Compare fund performance](03-nav-and-fund-comparisons.md) | What makes a fund comparison fair? | 75 minutes | Two-plan comparison card |
| [4. Read market risk](04-indices-equities-and-risk.md) | What does a return number leave out? | 60 minutes | Index risk note and raw-price warning |
| [5. Audit a strategy](05-strategies-and-backtests.md) | What does a published backtest prove? | 60 minutes | Strategy audit |
| [6. Investigate a dashboard](06-dashboard-research.md) | Which facts sit behind a report? | 75 minutes | Dataset contract and bounded analysis |
| [7. Make research reproducible](07-reproducible-exports.md) | Can someone repeat your result? | 60 minutes | Evidence bundle or export specification |
| [8. Complete a research memo](08-capstone.md) | What can you defend with the available evidence? | 90 minutes | Memo, evidence log, and peer review |

Use the [glossary](glossary.md) as terms appear. Facilitators and independent learners can use the [assessment guide](assessment-guide.md) to check answers.

## How to use the prompts

Each lesson includes a prompt you can paste into your agent. Prompts name the remote tool's unprefixed name; your client might show a server namespace. If both a remote server and a local downloader expose a similar name, select the extension explicitly.

Before any analysis session, give the agent this instruction:

```text
Use StockViz tools for financial evidence. Discover the current tool schema and
exact identifiers before dependent calls. Show requested and actual source dates,
units, status, coverage, and warnings. Distinguish previews from complete results.
Follow each tool's pagination contract without altering cursors or filters.
Do arithmetic in code or a calculator, not in prose. Preserve missing values.
Do not invent results, silently substitute datasets, or turn research into advice.
If a source is unavailable, state which part of the question cannot be answered.
Do not expose authentication secrets in the research log.
```

Save each exercise in your own workspace, not alongside public documentation if it contains private paths or account information. Record the tool, arguments, requested dates, resolved dates, source/publication metadata, result status, and your conclusion. You need evidence for a claim, not an entire chat transcript.

## When a call fails

A valid request is not a guarantee of data. Distinguish:

- Authentication failure: finish your own sign-in; discovery alone is insufficient.
- Available source with no matches: check identifiers and filters before interpreting emptiness.
- `data_gap`, unavailable, or partial source: retain the warning and limit your conclusion.
- Quota or timeout: narrow the research window or wait according to the service guidance. A smaller page does not bypass account limits.
- Invalid continuation after a publication change: restart that query; do not mix generations.

If access is blocked, you can still complete the conceptual questions and write an execution plan. Label the practical exercise `not executed`, with the blocker. Never replace missing live results with realistic-looking examples. Full course completion requires the practical evidence described in each lesson.

## Sources and scope

The [StockViz tool and dashboard guide](../samples/mcp-service-tool-samples.md) is the primary reference. The [consumer README](../../mf-mcp-consumer/README.md) covers local installation, authentication, exports, and troubleshooting. This course interprets those documents for a learner; it is not a second API specification.

The source guide describes a tool catalog captured on October 27, 2026. Tools and publications can change. In particular, it documents separate `get_amfi_aum_ranking`, `get_amfi_aum_growth`, and `get_amfi_category_aum_history` tools in place of the legacy `query_amfi_analytics` dispatcher. Discover your connected server's schema. If it differs, record the mismatch and use the current contract rather than guessing a replacement request.

The course's prompts and exercises are instructional specifications, not claims of successful live execution. No financial responses or performance figures were generated to write this course. Research is educational, not personalized investment advice; historical results do not promise future returns.
