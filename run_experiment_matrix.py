"""Run the full planned simulation matrix.

This script writes raw per-run diagnostics to CSV. It is intentionally kept
separate from the analysis code so the simulation design remains reproducible.
"""
import csv
from src.experiments import run_experiment_grid

if __name__ == "__main__":
    rows = run_experiment_grid(n_runs=100)
    fields = sorted(rows[0])
    with open("results/experiment_matrix.csv", "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)
    print(f"Wrote {len(rows)} simulation rows to results/experiment_matrix.csv")
