"""Publication-oriented figures from executed experiment summaries.

All plotted values are read from CSV outputs produced by the simulation
pipeline. No scientific result is hard-coded in this module.
"""
from pathlib import Path
import csv
import math
import matplotlib.pyplot as plt


def _rows(path):
    with open(path, newline="") as f:
        return list(csv.DictReader(f))


def _save(fig, output):
    Path(output).parent.mkdir(parents=True, exist_ok=True)
    fig.tight_layout()
    fig.savefig(output, dpi=220, bbox_inches="tight")
    plt.close(fig)


def plot_bias_vs_completeness(
    summary_csv="results/summary_matrix.csv",
    output="results/figures/bias_vs_completeness.png",
    missingness="random",
):
    rows = [r for r in _rows(summary_csv) if r["missingness"] == missingness]
    if not rows:
        raise ValueError("No matching executed results.")
    fig, ax = plt.subplots(figsize=(8, 5))
    for host in sorted({r["host_generation"] for r in rows}):
        for inf in sorted({r["inference_weighting"] for r in rows}):
            sub = sorted(
                [r for r in rows if r["host_generation"] == host and r["inference_weighting"] == inf],
                key=lambda r: float(r["completeness"]),
            )
            if sub:
                ax.plot(
                    [float(r["completeness"]) for r in sub],
                    [float(r["median_bias"]) for r in sub],
                    marker="o",
                    label=f"{host} → {inf}",
                )
    ax.axhline(0, linestyle="--", linewidth=1)
    ax.set_xlabel("Catalogue completeness")
    ax.set_ylabel("Median H₀ bias (km/s/Mpc)")
    ax.set_title(f"H₀ bias under {missingness} catalogue selection")
    ax.legend(fontsize=7, ncol=2)
    _save(fig, output)


def plot_coverage_vs_completeness(
    summary_csv="results/summary_matrix.csv",
    output="results/figures/coverage_vs_completeness.png",
    missingness="random",
):
    rows = [r for r in _rows(summary_csv) if r["missingness"] == missingness]
    if not rows:
        raise ValueError("No matching executed results.")
    fig, ax = plt.subplots(figsize=(8, 5))
    sub = sorted(
        [r for r in rows if r["host_generation"] == "uniform" and r["inference_weighting"] == "uniform"],
        key=lambda r: float(r["completeness"]),
    )
    for level, key in [("68%", "coverage_68"), ("95%", "coverage_95")]:
        if sub:
            ax.plot(
                [float(r["completeness"]) for r in sub],
                [float(r[key]) for r in sub],
                marker="o",
                label=level,
            )
    ax.axhline(0.68, linestyle="--", linewidth=1)
    ax.axhline(0.95, linestyle=":", linewidth=1)
    ax.set_xlabel("Catalogue completeness")
    ax.set_ylabel("Empirical coverage")
    ax.set_title(f"Credible-interval coverage under {missingness} selection")
    ax.set_ylim(0, 1)
    ax.legend()
    _save(fig, output)


def _matrix(rows, host, completeness, value_key):
    sub = [
        r for r in rows
        if r["host_generation"] == host
        and math.isclose(float(r["completeness"]), completeness)
    ]
    models = sorted({r["inference_weighting"] for r in sub})
    values = {(r["host_generation"], r["inference_weighting"]): float(r[value_key]) for r in sub}
    return models, [[values.get((host, inf), float("nan")) for inf in models] for _ in [0]]


def plot_weighting_heatmap(
    summary_csv="results/summary_matrix.csv",
    output="results/figures/weighting_median_bias_heatmap.png",
    completeness=1.0,
    value_key="median_bias",
):
    """Plot the 3×3 host-generation × inference-weighting matrix."""
    rows = _rows(summary_csv)
    models = sorted({r["host_generation"] for r in rows})
    inferences = sorted({r["inference_weighting"] for r in rows})
    data = []
    for host in models:
        row = []
        for inf in inferences:
            matches = [
                r for r in rows
                if r["missingness"] == "complete"
                and math.isclose(float(r["completeness"]), completeness)
                and r["host_generation"] == host
                and r["inference_weighting"] == inf
            ]
            row.append(float(matches[0][value_key]) if matches else float("nan"))
        data.append(row)

    fig, ax = plt.subplots(figsize=(7, 5.5))
    im = ax.imshow(data, aspect="auto")
    ax.set_xticks(range(len(inferences)), inferences)
    ax.set_yticks(range(len(models)), models)
    ax.set_xlabel("Assumed inference weighting")
    ax.set_ylabel("True host-generation model")
    label = {"median_bias": "Median H₀ bias (km/s/Mpc)", "rmse_mean": "Mean RMSE (km/s/Mpc)", "coverage_68": "68% coverage"}.get(value_key, value_key)
    ax.set_title(f"{label} at {completeness:.0%} catalogue completeness")
    for i, row in enumerate(data):
        for j, value in enumerate(row):
            if math.isfinite(value):
                ax.text(j, i, f"{value:.2f}", ha="center", va="center")
    cbar = fig.colorbar(im, ax=ax)
    cbar.set_label(label)
    _save(fig, output)


def plot_mechanism_heatmap(
    summary_csv="results/summary_matrix.csv",
    output="results/figures/mechanism_bias_heatmap_50pct.png",
    completeness=0.5,
    host_generation="uniform",
    inference_weighting="uniform",
):
    """Compare missingness mechanisms at one completeness level."""
    rows = _rows(summary_csv)
    mechanisms = ["complete", "random", "faint", "redshift", "sky"]
    values = []
    for mechanism in mechanisms:
        matches = [
            r for r in rows
            if r["missingness"] == mechanism
            and r["host_generation"] == host_generation
            and r["inference_weighting"] == inference_weighting
            and math.isclose(float(r["completeness"]), completeness)
        ]
        values.append(float(matches[0]["median_bias"]) if matches else float("nan"))

    fig, ax = plt.subplots(figsize=(8, 4.5))
    im = ax.imshow([values], aspect="auto")
    ax.set_xticks(range(len(mechanisms)), mechanisms)
    ax.set_yticks([0], [f"{host_generation} → {inference_weighting}"])
    ax.set_xlabel("Catalogue-selection mechanism")
    ax.set_title(f"Median H₀ bias at {completeness:.0%} completeness")
    for j, value in enumerate(values):
        if math.isfinite(value):
            ax.text(j, 0, f"{value:.2f}", ha="center", va="center")
    cbar = fig.colorbar(im, ax=ax)
    cbar.set_label("Median H₀ bias (km/s/Mpc)")
    _save(fig, output)
