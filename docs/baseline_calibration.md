# Baseline calibration report

Generated from GitHub Actions run #8 (commit `b9277e7`).

## Purpose

Before studying catalogue incompleteness, the simulation is checked under a complete catalogue and a correctly specified host model. A second control fixes the host identity so that host-mixture uncertainty can be separated from the basic distance-to-(H_0) inference.

These results are calibration diagnostics, not scientific conclusions about real dark-siren analyses.

## Complete catalogue, unknown host

Configuration:

- 1,000 independent mock universes
- (H_0=70) km/s/Mpc
- 500 galaxies per universe
- complete catalogue
- uniform host generation
- uniform inference weighting
- 15% fractional GW distance uncertainty
- low-redshift (d_L \approx cz/H_0) model

Measured results:

| Metric | Value |
|---|---:|
| Median bias | +1.986 km/s/Mpc |
| Mean bias | +1.259 km/s/Mpc |
| Median RMSE | 6.190 km/s/Mpc |
| Mean RMSE | 4.822 km/s/Mpc |
| Mean 68% interval width | 22.372 km/s/Mpc |
| Mean 95% interval width | 35.820 km/s/Mpc |
| 68% coverage | 94.4% |
| 95% coverage | 99.9% |
| 68% coverage MC SE | 0.0073 |
| 95% coverage MC SE | 0.0010 |
| Median-pull mean | 0.143 |
| Median-pull SD | 0.670 |
| Mean-pull mean | 0.080 |
| Mean-pull SD | 0.547 |

## Known-host control

The same 1,000-run calibration was repeated with the true host supplied as the sole candidate. This isolates the distance-to-(H_0) part of the model from the dark-siren host-mixture ambiguity.

Measured results:

| Metric | Value |
|---|---:|
| Median bias | +1.475 km/s/Mpc |
| Mean bias | +1.616 km/s/Mpc |
| Median RMSE | 7.177 km/s/Mpc |
| Mean RMSE | 6.455 km/s/Mpc |
| Mean 68% interval width | 17.045 km/s/Mpc |
| Mean 95% interval width | 29.958 km/s/Mpc |
| 68% coverage | 74.9% |
| 95% coverage | 98.6% |
| 68% coverage MC SE | 0.0137 |
| 95% coverage MC SE | 0.0037 |
| Median-pull mean | 0.200 |
| Median-pull SD | 1.041 |
| Mean-pull mean | 0.214 |
| Mean-pull SD | 0.934 |

## Interpretation

The known-host control already shows a modest positive estimator bias and non-nominal interval coverage. The complete-catalogue dark-siren mixture produces substantially broader posteriors and still higher coverage.

Therefore the baseline is **operationally validated as a reproducible simulation**, but it is **not perfectly calibrated in the strict statistical sense**. The incompleteness study must retain the complete-catalogue case as its internal control and report changes relative to that control.

We should not describe the baseline as an exactly calibrated 68%/95% posterior until a later model refinement achieves that property.

## Next stage

The next experiment should be a small pilot at 90%, 70%, and 50% completeness using:

- uniform host generation
- uniform inference weighting
- random missingness
- the same seeds across completeness levels
- naive catalogue-only inference

Only after inspecting this pilot should the full host-weighting × missingness matrix be launched.

The oracle missing-host model remains a separate validation control and should not be mixed into the naive results.
