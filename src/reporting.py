"""Research-result formatting helpers.

These functions only summarize values that were actually produced by the
simulation. They do not generate or assume scientific results.
"""
import csv
from pathlib import Path


def write_summary_csv(summaries, path="results/summary_matrix.csv"):
    if not summaries:
        raise ValueError("No summaries supplied.")
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    fields = list(summaries[0].keys())
    with path.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(summaries)


def write_methodology_note(path="results/README.md"):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        "# Results\n\n"
        "This directory is reserved for outputs generated from the committed "
        "simulation code. Numerical results must be produced by an actual "
        "execution of the experiment pipeline; hand-entered or illustrative "
        "values are not considered project results.\n\n"
        "The raw matrix records one row per mock universe. The summary matrix "
        "aggregates those rows by host-generation model, inference weighting, "
        "missingness mechanism, and target catalogue completeness.\n"
    )
