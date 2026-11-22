# Predictive Solar Irradiance Forecasting and Intelligent MPPT Optimization Under Partial Shading

Python / Google Colab project implementing **Data → Baseline → Model → Evaluation → Analysis**.

## Three notebooks

1. `notebooks/01_irradiance_baseline.ipynb`: 5-minute GHI forecasting with chronological train/validation/test and persistence, linear-regression, random-forest baselines.
2. `notebooks/02_gmpp_baseline.ipynb`: six-section irradiance to voltage at global MPP (V_GMPP), with **group-disjoint** train/validation/test and linear-regression and random-forest baselines.
3. `notebooks/03_integrated_mppt_po_simulation.ipynb`: original sampled P–V curves, P&O versus AI reference-voltage tracking; then separate forecast-linked synthetic-shading scenarios.

## Data and getting started

This public repository intentionally **does not contain** the large user-supplied datasets or fitted model artifacts. Read [data/README.md](data/README.md) and copy the three preprocessed files from the provided starter ZIP into `data/`:

- `srrl_weather_compact.csv.gz`
- `pv_database_summary_extract.csv`
- `pv_iv_curves_0p1V.npz`

Then `pip install -r requirements.txt` and run notebook **01 → 02 → 03** from the repository root in Jupyter or Colab. Alternatively, unzip the supplied project archive under `/content/solar_ai_mppt_project/` in Colab. To smoke-test with smaller models, set `SOLAR_FAST=1`; unset for final results. Outputs are written under ignored `outputs/`.

## Scientific interpretation

- Forecast input data are **chronologically split** using a purge; lag and rolling features are computed only from prior observations within consecutive one-minute segments.
- GMPP data are **configuration-group split**, not time-split; individual I–V sweep points are not independent training examples.
- Experimental PV sweeps and SRRL weather originate from **different systems**. Forecast-linked MPPT relies on declared synthetic fixed shading ratios and matching to withheld P–V curves. It is not a measured real-world dynamic PV plant.
- AI voltage-control targets assume access to all six section irradiance estimates; bare P&O does not. It would be incorrect to claim a controlled sensor-parity comparison.
- No converter dynamics, hardware time constant, physical settling time, efficiency losses or actual harvested joules are modeled. MPPT efficiency is an equal-iteration power-sum proxy.
- A better irradiance forecast need not improve MPPT energy. Compare AI+RF forecast to **AI+persistence** before any claim of predictive benefit.

## Team process

Suggested responsibilities: **Member 1** SRRL preprocessing/forecasting; **Member 2** P–V physics and P&O verification; **Member 3** GMPP regression and integrated analysis. Work in feature branches and create reviewable pull requests; refer to issues in commit messages. Each member should review others' code for the peer/Git assessment.

See [EXPERIMENT_RESULTS.md](EXPERIMENT_RESULTS.md) for preliminary results reproduced earlier in the conversation (not GitHub CI-verified).
