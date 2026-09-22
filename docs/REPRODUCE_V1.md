# Reproduce Version 1

## Environment
1. Clone the repository.
2. Use Python 3.12.
3. Install dependencies with:
   pip install -r requirements.txt

## Checks
Run:
- pytest -q
- python run_validation.py
- python run_calibration.py
- python run_calibration_curve.py

## Main experiment
The full matrix is computationally larger and is intended to run through the GitHub Actions workflow. The verified Version 1 matrix contains 15,300 raw runs across 153 conditions.

## Expected scientific reference
Independent reproduction of the 2,000-run calibration from repository source gives:
- 50% nominal: 87.45% empirical coverage
- 68% nominal: 94.35%
- 80% nominal: 97.35%
- 90% nominal: 99.05%
- 95% nominal: 99.85%

## Important scope
Do not interpret the synthetic study as a real LVK H0 measurement. Do not add a beta(H0) selection factor without an explicit event/survey selection model. The lightweight GP experiment is a diagnostic, not a general test of Gaussian processes.

## Executed evidence
The full experiment matrix and figures are retained as GitHub Actions artifacts. The repository documentation records the verified artifact-level run facts.
