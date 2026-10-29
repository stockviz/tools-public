# Assessment and facilitator guide

[Course overview](README.md) | [Capstone](08-capstone.md)

Use this guide for peer review or self-assessment. It gives expected reasoning, not fabricated answer tables. Actual financial answers depend on the publications and windows the learner retrieves.

## Facilitation

Before a session, confirm each learner can discover tools and authenticate independently. Do not distribute shared OAuth caches. Check the source availability needed for the lesson; if unavailable, use the documented alternate activity or record a blocked practical lab.

Ask the learner to predict which source they need before allowing the agent to choose one. After retrieval, ask them to explain one warning in their own words. An agent-written answer is not evidence that the learner understands it.

Keep programming optional except where a numerical claim needs real arithmetic or completeness verification. An agent can write and execute that code; the learner should still explain the inputs, output, and checks. Review one small result closely instead of collecting many unexamined tables.

## Expected reasoning by lesson

| Lesson | Evidence of understanding | Correction if missing |
| --- | --- | --- |
| 1 | Separates discovery, permission, source availability, and actual coverage. | Ask which successful step would still leave a protected financial query unanswered. |
| 2 | Distinguishes fund house, underlying fund, plan, average assets, flows, and returns; discloses classification bias. | Ask what else besides investor deposits changes asset values, and why average assets are not endpoint wealth. |
| 3 | Resolves exact Direct Growth codes; checks actual common dates and metric conventions. | Ask whether a larger NAV or a different inception date makes a comparison fair. |
| 4 | Preserves price/total-return convention and symbol/series; explains drawdown window and alignment. | Ask why a tool's return winner need not have the best Sharpe or lowest loss. |
| 5 | Traces strategy ID to explicit run ID, preserves unknown rules/costs, and accepts archived-signal gaps. | Ask what decision-time evidence would be needed to explain an old trade. |
| 6 | Inspects live schema, grain, units, filtering semantics, generation, and conflicts. | Ask whether a substring match is equality, and whether one row per strategy means one unique observation. |
| 7 | Produces real completed evidence and verification output, with secrets excluded. | Ask whether inline CSV is a whole export and what would prove the last page was reached. |
| 8 | Makes a narrow supported claim another learner can trace. | Ask the learner to remove every sentence whose evidence they cannot identify. |

## Answer notes for the claim exercises

In lesson 2, none of the four claims is supported as written. AUM growth is not NAV performance; asset snapshots cannot be summed as flows; category flows do not identify fund flows; and latest classification can postdate a historical report. Fund-level flows are documented as unavailable, so a narrower honest answer may be the only answer possible.

In lesson 4, `get_index_metrics` chooses its winner by full-window total return, not safety. Its matching-date requirements can refuse a comparison. That refusal is evidence of an unmet input condition, not evidence that an index is inferior.

In lesson 5, `compare_strategies.comparable` does not certify matching methodologies. `explain_signal` cannot supply missing archived inputs by narrating what happened afterward. A useful audit can conclude that a claim remains untestable.

In lesson 6, monthly PMS returns are neither stored annualized returns nor Sharpe. Manager and strategy AUM are not interchangeable. Exact report output can depend on additional cached paths, gates, and transformations absent from the fact tables.

## Capstone rubric

Mark each criterion `ready`, `revise`, or `blocked`. Use written reasons rather than a decorative score. Every criterion must be ready for full completion; a declared source blocker is honest partial work, not a failing fabricated result.

| Criterion | Ready when |
| --- | --- |
| Question | Population, measurement, and window-selection rule are explicit and answerable. |
| Source fit | Tools match the financial quantity and row grain; identifiers came from discovery. |
| Data integrity | Status, actual coverage, pagination/completion, publication generation where available, missing values, and conflicts are checked. |
| Method | Arithmetic ran in an explicit tool; units, annualization, return convention, and risk-free assumption are stated where relevant. |
| Interpretation | Observations are separate from causal/predictive claims; size is not return, and return is not safety. |
| Limitations | Biases and missing inputs that affect this exact question are named, not hidden in a generic disclaimer. |
| Reproduction | Saved inputs or full metric responses, nonsecret arguments, manifest, and calculation output support each material figure. |
| Communication | A financially curious nonexpert can understand the answer and its uncertainty without buying anything. |

## Stop-and-correct conditions

Do not approve a result that contains invented data, partial pages described as complete, credentials in shared work, silent series substitutions, missing values converted to zero, or performance claims from the wrong financial quantity. Correct the evidence and rerun affected calculations before polishing the prose.

Do not require the learner to prove unavailable market history. Require them to identify the missing evidence, state which conclusion it blocks, and propose a feasible next check instead.
