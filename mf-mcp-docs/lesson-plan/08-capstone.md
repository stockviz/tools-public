# Lesson 8: Complete a research memo

[Previous lesson](07-reproducible-exports.md) | [Course overview](README.md) | [Assessment guide](assessment-guide.md)

## Assignment

Write a research memo for a curious friend who understands agents but does not know the financial terms. Answer one narrow question using StockViz evidence. Allow about 90 minutes after the earlier labs; narrow the scope if data collection exceeds your access or time budget.

Choose one project:

- Fund comparison: how do two verified Direct Growth plans compare on return and drawdown over a preselected shared covered window? Include a sensitivity window and explain why fund size does not settle the question.
- Assets and flows: what do consolidated category AUM and separately reported category flows say about a covered period? Preserve source identities and explain why neither establishes a fund's investment return.
- Strategy audit: what is supported by a strategy definition and its explicitly linked backtest, and what remains unknown about historical execution? Include a preselected common subwindow if coverage permits.
- Dashboard investigation: what can you establish about one PMS manager's assets and strategy observations, or one other documented report family? Trace each claim to a published dataset and distinguish it from exact report reproduction.

A missing source is a legitimate finding. It does not justify changing the question silently or fabricating results. Record any agreed scope change before continuing.

## Working sequence

1. Write your question, population, measurement, and window-selection rule before retrieving performance results. Note what could make the question unanswerable.
2. Discover schemas and identifiers, then inspect source-specific availability and quality. List the exact calls needed; avoid broad downloads unrelated to the question.
3. Retrieve bounded evidence completely where the claim requires complete rows. Save a manifest and calculation inputs using lesson 7.
4. Run calculations in code or another explicit analysis tool. Preserve the actual dates, units, missing values, and calculation conventions.
5. Write the memo, then ask the agent to argue against its strongest claim. Check the objections yourself against the evidence.
6. Give a second learner the memo and manifest. Ask them to trace one figure and one caveat without reading your chat history. Revise any unsupported claim.

Paste this review prompt after drafting:

```text
Review this research memo as a skeptical reader. For each material claim, identify
its exact saved evidence and calculation. Flag mismatched units/windows, partial
pagination, current-cohort or latest-classification bias, unsupported total-return
assumptions, missing cost/execution evidence, and recommendations that go beyond
the data. Distinguish an interpretation from an observation. Do not fill gaps with
plausible values. Return specific corrections, then help me verify them against
the actual files or responses.
```

## Memo structure

Aim for 600–1,000 words plus evidence tables. This is a suggested writing target, not a reason to pad a short answer.

1. Question and short answer: say what you found and how limited the answer is.
2. Data and method: give exact identities, requested/observed dates, units, grain, coverage, and conventions.
3. Findings: include a compact table and at most one necessary chart, each with source references and actual observation dates.
4. Interpretation: explain the result in ordinary language. Separate descriptive comparison from prediction or causal explanation.
5. Limitations: state missing coverage, biases, costs, and unavailable inputs that affect your particular conclusion.
6. Reproduction: identify the manifest, saved responses/exports, and calculation code or analysis instructions.
7. Next question: propose one additional piece of evidence that would change or strengthen your answer.

Do not include account credentials or private holdings. These are public research facts, not personal investment advice.

## Acceptance criteria

Your submission contains the memo, an evidence manifest, and the saved inputs/calculation output supporting its material numerical claims. A chart without underlying provenance is insufficient.

You pass when a reviewer can trace the claims, verify completeness where required, distinguish source facts from your calculations, and see an honest boundary around what you do not know. Use the [assessment rubric](assessment-guide.md) for a more detailed review. If authentication or a publication blocks a required step, submit the blocker and an execution-ready specification; label the project incomplete rather than presenting a simulated result.
