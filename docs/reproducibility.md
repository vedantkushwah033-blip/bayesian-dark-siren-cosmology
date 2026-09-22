# Reproducibility Guide

## Purpose

This document gives the shortest route from a clean checkout to the main simulation outputs. The numerical values in the final report should be traced to executed CSV outputs or archived GitHub Actions artifacts.

## Environment

The project currently declares:

- Python 3.12 in GitHub Actions
- numpy
- pandas
- scipy
- matplotlib
- jupyter
- pytest

Install with:

    python -m pip install -r requirements.txt

For local module imports, run commands from the repository root with:

    PYTHONPATH=. 

## Verification order

Run the lightweight checks first:

    pytest -q

Then run the baseline validation:

    python run_validation.py

Then the calibration:

    python run_calibration.py

The calibration is the primary complete-catalogue reference.

## Main experiment

Generate the full host-weighting/incompleteness matrix:

    python run_experiment_matrix.py

Then summarize it:

    python analyze_results.py

Then generate the main figures:

    python make_figures.py

Expected primary data products are:

- `results/experiment_matrix.csv`
- `results/summary_matrix.csv`
- `results/figures/`

## GP diagnostic

The GP experiment is intentionally separate from the main matrix:

    python run_gp_pilot.py

The GP pilot produces:

- `results/gp_pilot.csv`
- `results/gp_pilot_summary.csv`

The GP result should be interpreted together with bias and coverage, not posterior width alone.

## Important methodological rule

Do not add an arbitrary `beta(H0)` selection denominator to the baseline. A selection correction should be introduced only together with a consistent event-selection and galaxy-selection model.

## Numerical provenance

The repository's executed artifacts are the authoritative numerical record. If a future code change modifies a reported number, regenerate the relevant experiment and update the report from the new artifact rather than editing the number manually.

## Scope

The baseline is a controlled low-redshift simulation. It is not a replacement for an LVK analysis pipeline. In particular, detector selection, realistic sky localization, peculiar velocities, redshift uncertainty, survey masks, clustering, and full cosmological distance-redshift modelling remain future extensions.
