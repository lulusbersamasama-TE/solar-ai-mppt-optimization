# Preliminary Results (prior local full run)

All figures below were reported from the earlier local project execution with the user-provided datasets. Rerun all notebooks after downloading the derived files to confirm; **GitHub CI has not validated these figures**.

## Forecasting — five-minute GHI horizon, chronological test
| Model | MAE (W/m²) | RMSE (W/m²) | R² |
|---|---:|---:|---:|
| Persistence | 53.062 | 116.346 | 0.829 |
| Linear regression | 58.500 | 108.103 | 0.852 |
| Random forest | 49.824 | 102.149 | 0.868 |

## GMPP voltage — grouped holdout
| Model | MAE (V) | RMSE (V) | R² |
|---|---:|---:|---:|
| Linear regression | 3.315 | 4.211 | 0.355 |
| Random forest | 0.301 | 1.072 | 0.958 |

## Static PV test curves: equal-step simulated control
| Controller | Numerical tracking efficiency | Final ≥98% GMPP hit |
|---|---:|---:|
| P&O | 94.86% | 45.00% |
| AI linear | 93.25% | 20.83% |
| AI random forest | 98.50% | 96.67% |

## Weather-linked synthetic scenarios
| Controller | Numerical tracking efficiency |
|---|---:|
| P&O | 94.51% |
| AI + persistence | 98.85% |
| AI + RF forecast | 98.81% |
| Future-GHI oracle (diagnostic only) | 98.94% |

The RF weather model did **not** improve the integrated numerical MPPT efficiency over persistence. Six-string irradiance input to AI is privileged relative to P&O. This is not converter-level real-world testing.
