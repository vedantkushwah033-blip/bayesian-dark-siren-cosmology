# Final Audit Checklist

## Scope

This checklist records the final repository audit for the baseline dark-siren simulation study. It does not replace execution of GitHub Actions.

## Verified from repository source

- The validated simulation is `src/simulations_v2.py`.
- The old baseline notebook has been migrated to `simulations_v2`.
- The main matrix workflow runs simulation, analysis, and publication-figure generation in sequence.
- The validation workflow runs the complete test suite before baseline/calibration diagnostics.
- The GP pilot is a separate workflow and produces `gp_pilot.csv` and `gp_pilot_summary.csv`.
- The final report explicitly describes the GP model as a lightweight density-reconstruction diagnostic rather than a full survey-selection model.
- The final report states the 15,300-run matrix and 3,600-run GP pilot results.
- No arbitrary `beta(H0)` selection denominator is introduced.

## Scientific consistency checks

- Results are conditional on the simplified low-redshift cosmology and Gaussian distance model.
- The complete-catalogue case is treated as a calibration reference rather than assumed to have nominal coverage.
- The hidden host is not supplied to ordinary inference.
- The oracle missing-host model is explicitly labelled a validation control.
- GP posterior narrowing is not treated as improvement without considering bias and coverage.
- Future work calls for a consistent selection/intensity model before introducing a realistic `beta(H0)` normalization.

## Pending execution verification

The repository-side source audit cannot substitute for a successful GitHub Actions run. The final release should therefore be marked verified only after the relevant workflow run completes successfully and its artifacts are inspected.

## Release rule

Do not change the scientific conclusions merely to obtain a more favourable result. Preserve the executed simulation outputs as the numerical record and treat later methodological extensions as separate experiments.
