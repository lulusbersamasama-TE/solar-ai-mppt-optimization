# Verification protocol — Solar AI–MPPT

This protocol maps each course requirement to falsifiable numerical evidence. **Run Notebooks 01 → 02 → 03 → 04**, with the derived data in `data/`. Do not report any Notebook 04 numbers before a successful full rerun.

## Research questions, hypotheses and primary estimands

| RQ | Null claim to test | Metric / evidence | Caution |
|---|---|---|---|
| RQ1: Is 5-min irradiance prediction more accurate than persistence? | RF forecast does not improve RMSE over persistence on chronological test | 01 model table + 04 rapid-transition conditional RMSE | A smaller overall RMSE may conceal poorer extreme-event performance |
| RQ2: Do better V_GMPP predictions produce more PV power? | RF six-section does not reduce exact numerical power loss on held-out P–V curves vs linear/mean-irradiance baselines | 02 regression metrics + 04 per-curve power loss and 1-feature ablation | Global PV peaks can jump non-continuously |
| RQ3: Is AI's numerical tracking advantage robust to P&O tuning? | AI-RF gains vanish after choosing P&O initialization/step **only on validation** | 03 original scenario + 04 validation grid, fair-timing test, paired episode bootstrap | AI has six irradiance sensors; P&O only terminal power |
| RQ4: Does RF weather forecasting itself improve MPPT versus persistence? | AI + RF forecast does not exceed AI + persistence | 03 synthetic linked episodes + 04 paired episode bootstrap | If CI includes zero, cannot claim robust improvement; oracle is diagnostic |

## Mathematical justification

1. PV power from sampled I–V: `P(V)=V I(V)`. `P*=max_{V in grid} P(V)`. `V*=argmax P(V)`.
2. Exact numerical voltage-choice loss: `L_P(Vhat) = 100(P* - P(Vhat))/P*`. Regression RMSE is not an energy metric.
3. For an isolated differentiable local maximum, `P'(V*)=0`, `P''(V*)<0`. For small `e=Vhat-V*`, `P(V*)-P(V*+e) ≈ -(1/2)P''(V*)e²`. This approximation **fails** when a global optimum moves between shading-induced peaks.
4. Per-iteration numerical MPPT efficiency: `100 * Σ_{episodes,k} P_tracker / Σ_{episodes,k} P*_episode`. **Not converter efficiency nor joules**, unless a consistent step duration and dynamics are supplied.
5. Paired bootstrap: resample *entire held-out curves/episodes* (not 30 serial steps); for every resample compute `100 * Σ(P_AI-P_PO)/ΣP*`; report percentile interval of 2000 replicates. If zero lies within the interval, do not claim a reliable positive numerical gap under this sample.
6. Spatial irradiance information ablation: compare same RF architecture trained on `(G1,...,G6)` versus `mean(G1,...,G6)`, using the same held-out curves; describes informational benefit, **not** full sensor parity with P&O.

## Verification matrix for the 10% rubric component

| Check | Notebook | Evidence | Acceptance / report |
|---|---|---|---|
| Dataset integrity | 01, 02, 04 | Raw counts, timestamp duplicate counts, sections, I–V labels | Report anomalies and exclusions; no silent leakage |
| Chronological split | 01 | Target time t+5, 15-min purges | No overlapping input/output windows at split boundaries |
| Group split | 02, 04 | GroupShuffleSplit by first five sections | No group appears in both train and test |
| Electrical consistency | 02, 03, 04 | `Vmp·Imp≈Pmax`, power-grid deviation, boundary maxima | Quantify finite grid error; investigate boundary maxima if found |
| ML comparison | 01, 02 | Persistence/linear/RF on untouched test | Include validation and test, MAE/RMSE/R² and operational metric |
| Rapid GHI transients | 04 | Conditional RMSE on top 10% `|G(t+5)-G(t)|` | Explicitly state any performance deterioration |
| Model power cost | 04 | Per-curve `L_P`, 98%-P hit fraction, 95th percentile loss | Explain significant voltage outliers |
| P&O sensitivity | 04 | Validation-only V0×step search, test result | Never choose hyperparameters from test |
| Fair controller timing | 04 | Both trackers observe starting voltage before updates | Distinguish from earlier Notebook 03 first-sample asymmetry |
| Increment of forecasting | 03, 04 | AI forecast minus AI persistence, paired episode CI | No claim if negative or not robust |
| Split/seed robustness | 04 | Three fresh group-based split retrainings | Report mean, standard deviation, individual values |
| Team provenance | GitHub | Individual commits/issues/PRs and peer reflections | Separate personal accounts; a shared account cannot prove 3 people's work |

## Crucial limitations / reviewer answers

- **No physical converter model.** Results measure controller reference-voltage selection on static I–V sweeps; no inductor current, PWM, switching frequency, sensor noise, losses, or seconds-to-settle.
- **Information asymmetry.** RF sees six irradiance section values; P&O doesn't. Claims of algorithmic superiority under equal hardware and sensing are unsupported.
- **Synthetic join.** SRRL GHI and six-section PV sweeps are from different systems; hourly/daylight environment does not supply a measured partial shading trajectory for that PV module.
- **PV domain coverage.** Few fully uniform irradiation cases; forecast-linked test conditioned on high GHI and nearest withheld curves. Report matching error and sample count.
- **Potential P&O first-step asymmetry in Notebook 03.** The original AI logs power **after** its first one-step adjustment while P&O logs power **before** its first update. Notebook 04 corrects this alignment for sensitivity/fair comparison; do not pool metrics from the two timing conventions.
- **Static end-step behavior is not stability.** RF's zero end-of-episode voltage movement follows a constant target; it is not verified converter oscillation elimination.
- **Per-curve bootstrap interval is not field deployment confidence.** It does not account for meteorological site transfer, device aging, nor hardware dynamics.
- **Negative results are valuable.** If a better forecasting RMSE does not improve AI MPPT relative to persistence, report the null/negative finding and plausible, testable explanations.

## Reproducibility checklist

- [ ] Notebook 01 runs from clean Colab CPU, test forecasts saved.
- [ ] Notebook 02 runs from clean Colab CPU, splits and models saved.
- [ ] Notebook 03 runs from clean Colab CPU, static and synthetic outputs saved.
- [ ] Notebook 04 runs from clean Colab CPU, all required `verification_*` files present.
- [ ] Use consistent six-section feature names; do not hide sklearn warnings.
- [ ] Note Colab Python/scikit-learn version, full vs `SOLAR_FAST` status, and timestamp of runs.
- [ ] Attach graphics/tables from `outputs/` to the report (not raw datasets to public Git).
- [ ] Add GitHub commit/PR links in each person's actual contribution record.
- [ ] Explicitly separate **verified** findings from hypotheses and methodological limitations.

## Reporting outline

**Analysis:** First report weather forecast overall + rapid subset; then GMPP voltage accuracy + exact curve-based power loss; spatial-input ablation; numerical tracking and validation-tuned P&O; incremental forecast comparison with CI and caveats.

**Verification Check:** Show a compact table with dataset/physics tests, split tests, repeated group splits, validation tuning, paired bootstrap, and command `Run all` success screenshots.

**Individual peer/Git:** Use `docs/INDIVIDUAL_REFLECTION_TEMPLATE.md` independently for each team member. Never invent contributions.
## GitHub CI scope

The PR workflow checks notebook Python syntax and calls Notebook 04's exact `static_controller_run` function on a toy concave P–V curve to verify identical starting measurements, P&O reversal, reference-voltage tracking and 1-V step bounds. **Passing CI does not imply the numerical results on real derived data are correct.** Colab Notebook 04 is still mandatory for the real-dataset Verification Check.
