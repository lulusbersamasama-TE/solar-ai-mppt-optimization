# Results and Discussion — Evidence-based report scaffold

> This is a **template**. Baseline figures below come from saved notebook outputs on `main`; values marked `[Notebook 04: pending run]` must NOT be published until recomputed from the uploaded derived data.

## RQ1 — Short-horizon irradiance forecasting

On the 225,225 chronologically held-out windows with a five-minute target horizon, persistence gave RMSE **116.346 W/m²**, linear regression **108.103 W/m²**, and random forest **102.149 W/m²**. The relative RF RMSE reduction versus persistence is **12.20%**. Test MAE was **49.824 W/m²** and R² **0.868** for RF.

**Verification beyond aggregate:** Top-decile absolute 5-min GHI change threshold: **[pending] W/m²**, rapid-subset RF RMSE: **[pending]**, persistence RMSE: **[pending]**. Cite `verification_transient_weather_metrics.csv`.

**Interpretation:** Explain the failure modes during abrupt irradiance changes using an actual held-out plot, without claiming perfect weather transient anticipation.

## RQ2 — Spatial irradiance to GMPP voltage, and PV energy cost

On 2,160 group-disjoint held-out curves, RF V_GMPP RMSE **1.072 V**, MAE **0.301 V**, R² **0.958**, with **94.630%** of predictions within ±1 V. Linear regression RMSE was **4.211 V**.

**Electrical validation:** `P(V)=V I(V)`; `V*=argmax_V P(V)`; exact `power-loss(Vhat)=100·[P(V*)-P(Vhat)]/P(V*)`.

PV full-resolution Pmax versus 0.1-V sampled sweep: previously observed median absolute deviation **0.001535 W**, maximum **0.398265 W**. Recheck `verification_integrity.csv` and boundary-maxima fraction in Notebook 04.

**New verification to insert:** RF mean power loss **[pending]%**, p95 power loss **[pending]%**, >98%-GMPP hit **[pending]%**; compare with linear and RF-mean-irradiance ablation **[pending]**. Cite `verification_voltage_power_loss_summary.csv` and `verification_spatial_sensor_ablation.csv`.

**Interpretation:** A small voltage error does not imply a fixed power loss on a multiple-peak curve. Explain isolated-peak Taylor approximation and its failure across global peak switches.

## RQ3 — Numerical tracking relative to P&O and sensitivity

**Historical Notebook 03 (not aligned first-step measurement)**:
- P&O efficiency **94.861%**, final ≥98% GMPP hit **45.000%**
- AI linear efficiency **93.250%**, hit **20.833%**
- AI RF efficiency **98.497%**, hit **96.667%**

**Important correction:** Notebook 03 measures AI power after its first command adjustment but P&O power before its first adjustment. Notebook 04 compares both controllers with measurements **before** each update, so the new numbers are not directly interchangeable with this historic table.

**New verification to insert:** P&O validation-chosen starting voltage **[pending] V**, perturbation **[pending] V**, validation efficiency **[pending]%**; held-out adjusted P&O efficiency **[pending]%**, AI RF at matching start/step **[pending]%**, paired-episode advantage **[pending] percentage points, 95% CI [pending, pending]**. Cite `verification_po_validation_grid.csv`, `verification_static_controller_summary.csv`, `verification_static_paired_bootstrap.csv`.

**Interpretation:** Results support a conditional comparison of control strategies **with different sensing assumptions**, not a causal sensor-parity hardware superiority claim.

## RQ4 — Does forecasting improve MPPT rather than merely GHI RMSE?

**Historical Notebook 03 synthetic test** (75 accepted of 75 candidate episodes; median 6-section curve-matching RMSE **36.573 W/m²**):
- P&O: **94.509%**
- AI + persistence: **98.849%**
- AI + RF forecast: **98.806%**
- AI + actual-future-GHI oracle: **98.939%**

The AI + RF forecast advantage versus AI + persistence was **−0.043 percentage points**, i.e. not a positive gain in the tested scenario. **Do not say forecasting improves numerical MPPT efficiency here.**

**New verification:** Paired episode bootstrap `AI forecast - AI persistence`: **[pending] pp, 95% CI [pending, pending]** based on `verification_forecast_increment_CI.csv`.

**Interpretation:** Environmental forecasting, spatial-shading estimation, chosen reference voltage and tracked power are separate steps. Gains in one component need not propagate to the next; explore whether the V_GMPP references coincide or PV power is locally flat.

## Repeated seeds and model stability

Group-disjoint retrains using three split seeds **7, 42, 2026**: RMSE values **[pending, pending, pending] V**; mean ± SD **[pending] ± [pending] V**. This tests dependence on curve grouping within the same dataset, **not** cross-device or cross-climate generalization.

## Verification and implementation limitations

Explicitly report: no converter state-space dynamics, PWM or physical settling seconds; PV and meteorology came from different systems; fixed simulated section shading and nearest test-only curve matching; P&O does not receive six-section irradiance; model/claim reproducibility depends on saved seeds and split files; only two original near-uniform PV patterns; GitHub syntax + synthetic controller smoke CI is not full original-dataset numerical verification.

## Individual Peer/Git reflection

Each team member independently attaches an evidence table linking real commits/issues/PRs, a verified simulation figure, and a technical reflection. Current shared-account commits do **not** demonstrate separate authorship. Use `docs/INDIVIDUAL_REFLECTION_TEMPLATE.md`.

## Reviewer verdict framework

Only after rerunning Notebook 04, answer:
1. Is RF forecasting robust on the **rapid** transient subset, or only overall?
2. Does six-section RF reduce exact PV power loss relative to linear and mean-G RF?
3. Does tuned P&O close the tracking difference under aligned iteration timing?
4. Is the additional RF **forecasting** effect positive, negative, or statistically unresolved under the paired scenario bootstrap?
5. What remains unknown without sensor-parity and a dynamic converter model?

Never replace missing experimental evidence with inferred or idealized values.
