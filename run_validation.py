"""Baseline validation report generator."""
from src.experiments import run_repeated
from src.metrics_v2 import summarize_runs

if __name__ == "__main__":
    rows = run_repeated(n_runs=100, completeness=1.0, missingness="complete")
    print(summarize_runs(rows))
