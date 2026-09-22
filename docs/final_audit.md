# Final Audit Checklist

## Scope

This checklist records the final repository audit for the baseline dark-siren simulation study.

## Verified from repository source and executed outputs

- The validated simulation is `src/simulations_v2.py`.
- The old baseline notebook has been migrated to `simulations_v2`.
- The main matrix workflow runs simulation, analysis, and publication-figure generation in sequence.
- The validation workflow runs the complete test suite before baseline/calibration diagnostics.
- The GP pilot is a separate workflow and produces `gp_pilot.csv` and `gp_pilot_summary.csv`.
- The final report explicitly describes the GP model as a lightweight density-reconstruction diagnostic rather than a full survey-selection model.
- The executed full matrix contains **15,300 runs across 153 conditions**.
- The executed GP pilot contains **3,600 paired runs**.
- The latest Full Experiment Matrix workflow completed successfully at run `35758311087`.
- The latest Validation workflow completed successfully at run `35758311024`.
- The full-matrix artifact was inspected and contains the raw matrix, summary matrix, and publication figures.
- No arbitrary `beta(H0)` selection denominator is introduced.

## Scientific consistency checks

- Results are conditional on the simplified low-redshift cosmology and Gaussian distance model.
- The complete-catalogue case is treated as a calibration reference rather than assumed to have nominal coverage.
- The hidden host is not supplied to ordinary inference.
- The oracle missing-host model is explicitly labelled a validation control.
- GP posterior narrowing is not treated as improvement without considering bias and coverage.
- Future work calls for a consistent selection/intensity model before introducing a realistic `beta(H0)` normalization.

## Execution verification

The execution checks are now complete for the current release candidate:

- Full Experiment Matrix: **PASS**
- Validation workflow: **PASS**
- Full-matrix artifact inspection: **PASS**
- Raw matrix integrity: **15,300 rows, no missing values**
- Summary integrity: **153 conditions, no missing values**
- Publication figures in artifact: **12**

The numerical outputs referenced by the final report are therefore tied to an executed workflow artifact rather than only repository source code.

## Release rule

Do not change the scientific conclusions merely to obtain a more favourable result. Preserve the executed simulation outputs as the numerical record and treat later methodological extensions as separate experiments.
