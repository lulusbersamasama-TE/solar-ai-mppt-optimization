# Dataset setup

This folder intentionally contains no raw datasets. Obtain the original datasets from the course group's shared archive (and confirm source licensing/attribution).

Place exactly these **derived files** here before running:
- `srrl_weather_compact.csv.gz`: expected columns `timestamp, ghi, dhi, dni, temperature_c, rh_pct, zenith_deg, ghi_extraterrestrial`; timestamp must be parsable and ordered by observation time.
- `pv_database_summary_extract.csv`: expected `Curve, Section_1_Wm2,...,Section_6_Wm2, Vmp_V, Imp_A, Pmax_W`; one row per PV curve.
- `pv_iv_curves_0p1V.npz`: arrays `voltage` (415 values), `current` (14400 x 415), `curve_id` (IDs 1 through 14400), produced by downsampling *actual supplied I-V curves*, not by fabricating electric readings.

These three files are included in the previously prepared *starter/completed* project ZIP in this conversation. Extract its `data` folder locally or upload to Google Drive/Colab (do not upload the raw datasets to this public GitHub repository without checking licensing).

The irradiance observations and I-V sweeps come from **different systems**. Joining them is explicitly a synthetic scenario, not a measured field trajectory.
