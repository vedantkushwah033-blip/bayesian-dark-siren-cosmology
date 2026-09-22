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

Therefore the baseline is **operationally validated as a reproducible simulation**, but it is **not perfectly calibrated in the strict statistical sense**. The incompleteness study retains the complete-catalogue case as its internal control and reports changes relative to that control.

A subsequent dedicated 2,000-run coverage calibration, independently reproduced from the repository's current calibration script, found empirical coverage of 94.35% for nominal 68% intervals (with 50%, 80%, 90%, and 95% nominal levels also showing conservative coverage). This confirms that the conservative posterior coverage is a property of the current synthetic baseline rather than an accidental feature of the original 1,000-run sample.

## Follow-on experiments completed

The planned follow-on work has now been executed:

- **15,300-run experiment matrix:** 153 conditions spanning host-generation/inference weighting, completeness, and missingness mechanisms, with 100 independent runs per condition.
- **3,600-run GP pilot:** a lightweight redshift-density reconstruction diagnostic; it narrowed intervals but increased bias and reduced 68% coverage, so it is retained as a negative diagnostic rather than a successful correction.
- **2,000-run coverage calibration:** independent reproduction of the repository calibration script, confirming conservative baseline posterior coverage.
- **Oracle missing-host validation:** retained as a separate control and not mixed with naive catalogue-only results.

The next scientifically motivated stage is Version 2: an explicit event/galaxy selection and intensity model, followed by more realistic redshift, peculiar-velocity, clustering, and cosmological modelling. No arbitrary beta(H_0) selection correction should be introduced before that selection model exists.
