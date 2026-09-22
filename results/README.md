# Results

This directory contains the reproducibility entry point for generated numerical results.

The latest executed full experiment matrix was produced by GitHub Actions run `35758311087` at commit `a13e72f78276fa7e0b291fad278710aeb6014a15`.

The archived `full-experiment-matrix` artifact contains:

- `experiment_matrix.csv` — 15,300 raw simulation runs.
- `summary_matrix.csv` — 153 summarized experimental conditions.
- `figures/` — 12 publication figures generated from the matrix.

The matrix covers 3 host-generation models, 3 inference-weighting models, 5 missingness conditions, and 4 catalogue-completeness levels, with 100 runs per condition.

The generated CSVs and figures are intentionally retained as GitHub Actions artifacts rather than committed to the repository. See `docs/reproducibility.md` for the commands that regenerate them.

The GP extension is executed separately by the GP Pilot workflow and is not mixed into the full-matrix artifact.
