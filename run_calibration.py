"""Extended baseline calibration run.

This is a higher-statistics check of the complete-catalogue null experiment.
It is deliberately separate from the 100-run smoke/validation run.
"""
from src.experiments import run_repeated
from src.metrics_v2 import summarize_runs

if __name__ == "__main__":
    rows = run_repeated(
        n_runs=1000,
        completeness=1.0,
        missingness="complete",
        seed=2026,
    )
    print(summarize_runs(rows))
