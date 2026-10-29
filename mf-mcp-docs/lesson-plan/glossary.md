# Market and research glossary

[Course overview](README.md)

These explanations support the lessons. For a tool's precise calculation, use its advertised schema and the source reference rather than inferring a formula from a label.

| Term | Working meaning | Common mistake |
| --- | --- | --- |
| AMFI | Association of Mutual Funds in India; a source of mutual-fund reporting data used here. | Assuming every AMFI dataset measures the same population or dates. |
| Fund house / AMC | Organization managing multiple investment funds. | Calling a fund-house asset total one investment fund's size. |
| Underlying fund | Investment fund whose plan/option variants may be consolidated for AUM analysis. | Treating a heuristic canonical name as an authoritative merger identity. |
| Scheme code | Identifier for the specific stored mutual-fund scheme/plan/option. | Guessing a code from a generic fund name. |
| Direct / Regular | Different mutual-fund plan arrangements, commonly with different expenses. | Comparing them as identical series. |
| Growth / IDCW | Growth retains gains in the option; IDCW involves income distribution cum capital withdrawal. | Treating raw distribution-option NAV change as total investor return. |
| NAV | Net asset value per unit. | Equating a high unit NAV with an expensive valuation. |
| AUM / average AUM | Assets under management / their average over a reporting period. | Calling asset growth a return or net inflow. |
| Subscription / redemption | Money entering / leaving a fund or category under the source definition. | Calling gross subscriptions net inflows. |
| Net flow | Reported net investor money movement. | Reconstructing it from average AUM differences. |
| Folio | Mutual-fund account record. | Counting folios as unique people. |
| Lakh / crore | Indian monetary/counting units; preserve the dataset's stated scale. | Mixing lakh-denominated and crore-denominated amounts. |
| Index | Basket summarized under a defined methodology. | Assuming its reported performance is a cost-free investable product. |
| Price return / total return | Price movement / return including distributions under the series methodology. | Replacing a missing total-return series with price return without disclosure. |
| Benchmark | Reference used to interpret performance. | Selecting it after seeing which reference makes the result look best. |
| CAGR | Annualized compounded endpoint growth under the stated time convention. | Treating it as the return earned every year. |
| Volatility | Dispersion of returns under a stated frequency and estimator. | Interpreting it as maximum possible loss. |
| Sharpe ratio | Excess return relative to volatility, under explicit frequency and risk-free conventions. | Comparing ratios computed with different methods as identical measurements. |
| Drawdown | Decline from a running or selected-window peak, depending on the metric. | Calling window drawdown a lifetime risk limit. |
| Current / maximum drawdown | Endpoint distance below the window peak / deepest observed peak-to-trough loss. | Using one as a synonym for the other. |
| PMS | Portfolio Management Services; manager and strategy facts have different grains. | Adding overlapping strategy AUM to claim manager assets. |
| Backtest / model portfolio | Historical rules-based study / published model allocation. | Calling either your executed account history. |
| Factor / momentum | A systematic attribute / tendency to rank or select using prior performance. | Inferring exact rules from the strategy's name. |
| Alpha / beta | Model-dependent intercept / sensitivity to a benchmark or factor. | Assuming labels establish causality, skill, or scaling. |
| Grain / key | Meaning of one row / fields used to identify its analytical entity. | Treating a paging ID as an economic key or rank. |
| Cursor | Opaque continuation returned by a tool. | Editing it or changing filters between pages. |
| NULL / zero | Missing observation / observed numeric value. | Converting missing values to zero. |
| Coverage / freshness | Observations present / how recent source observations or publication are. | Equating a fresh catalog with complete data. |
| Point-in-time | Data known and usable at a historical decision time. | Treating an old period end or latest classification as proof of historical availability. |
| Look-ahead / survivorship bias | Using future information / analyzing only surviving or selected instruments. | Applying today's eligible universe backward as a historical selection test. |
| Holdout / overfitting | Later data reserved from selection / rules fitted too closely to observed history. | Tuning repeatedly after inspecting the supposed holdout. |
| Parity | Matching a defined output or method, not merely sharing some inputs. | Claiming report reproduction because related source facts are accessible. |

For the lakh-to-crore conversion used by this service, see the [AUM tool reference](../samples/mcp-service-tool-samples.md#tool-get_amfi_aum_ranking) and verify conversions with code in your exercise.
