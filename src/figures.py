"""Figure generation from executed experiment summaries.

No scientific values are embedded here. Every figure is generated from an
input CSV produced by the simulation pipeline.
"""
from pathlib import Path
import csv
import matplotlib.pyplot as plt


def _rows(path):
    with open(path, newline="") as f:
        return list(csv.DictReader(f))


def plot_bias_vs_completeness(summary_csv="results/summary_matrix.csv",
                              output="results/figures/bias_vs_completeness.png",
                              missingness="random"):
    rows=[r for r in _rows(summary_csv) if r["missingness"] == missingness]
    if not rows:
        raise ValueError("No matching executed results.")
    Path(output).parent.mkdir(parents=True, exist_ok=True)
    plt.figure(figsize=(8,5))
    for host in sorted(set(r["host_generation"] for r in rows)):
        for inf in sorted(set(r["inference_weighting"] for r in rows)):
            sub=[r for r in rows if r["host_generation"]==host and r["inference_weighting"]==inf]
            sub=sorted(sub,key=lambda r:float(r["completeness"]))
            if sub:
                plt.plot([float(r["completeness"]) for r in sub],
                         [float(r["median_bias"]) for r in sub],
                         marker="o", label=f"{host} → {inf}")
    plt.axhline(0, linestyle="--", linewidth=1)
    plt.xlabel("Catalogue completeness")
    plt.ylabel("Median H₀ bias (km/s/Mpc)")
    plt.title(f"H₀ bias under {missingness} catalogue selection")
    plt.legend(fontsize=7)
    plt.tight_layout()
    plt.savefig(output, dpi=180)
    plt.close()


def plot_coverage_vs_completeness(summary_csv="results/summary_matrix.csv",
                                  output="results/figures/coverage_vs_completeness.png",
                                  missingness="random"):
    rows=[r for r in _rows(summary_csv) if r["missingness"] == missingness]
    if not rows:
        raise ValueError("No matching executed results.")
    Path(output).parent.mkdir(parents=True, exist_ok=True)
    plt.figure(figsize=(8,5))
    for level, key in [("68%","coverage_68"),("95%","coverage_95")]:
        sub=[r for r in rows if r["host_generation"]=="uniform" and r["inference_weighting"]=="uniform"]
        sub=sorted(sub,key=lambda r:float(r["completeness"]))
        if sub:
            plt.plot([float(r["completeness"]) for r in sub],
                     [float(r[key]) for r in sub],
                     marker="o", label=level)
    plt.axhline(0.68, linestyle="--", linewidth=1)
    plt.axhline(0.95, linestyle=":", linewidth=1)
    plt.xlabel("Catalogue completeness")
    plt.ylabel("Empirical coverage")
    plt.title(f"Credible-interval coverage under {missingness} selection")
    plt.ylim(0,1)
    plt.legend()
    plt.tight_layout()
    plt.savefig(output, dpi=180)
    plt.close()
