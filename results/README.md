# Results

This directory contains the reproducibility entry point for generated numerical results.

The latest verified full experiment matrix contains:

- `experiment_matrix.csv` — 15,300 raw simulation runs.
- `summary_matrix.csv` — 153 summarized experimental conditions.
- `figures/` — 12 publication figures generated from the matrix.

The matrix covers 3 host-generation models, 3 inference-weighting models, 5 missingness conditions, and 4 catalogue-completeness levels, with 100 runs per condition.

The generated CSVs and figures are intentionally retained as GitHub Actions artifacts rather than committed to the repository. The repository audit verifies the artifact contents and dimensions; stale workflow run identifiers are intentionally not repeated here because the numerical artifact is the authoritative record. See `docs/reproducibility.md` for the commands that regenerate them.

The GP extension is executed separately by the GP Pilot workflow and is not mixed into the full-matrix artifact.

For professor-facing presentation, the strongest existing outputs are the completeness/missingness comparison, host-weighting comparison, coverage calibration, and GP diagnostic. These should be surfaced from the archived artifacts rather than recreated from summary numbers.
