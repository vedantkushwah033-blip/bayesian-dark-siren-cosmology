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


def plot_gp_comparison(
    gp_csv="results/gp_pilot.csv",
    output="results/figures/gp_bias_width_comparison.png",
):
    """Compare naive and GP bias/width across executed paired runs."""
    rows = _rows(gp_csv)
    mechanisms = ["random", "faint", "redshift", "sky"]
    fig, axes = plt.subplots(1, 2, figsize=(11, 4.5))
    for mechanism in mechanisms:
        sub = [r for r in rows if r["mechanism"] == mechanism]
        if not sub:
            continue
        levels = sorted({float(r["completeness"]) for r in sub}, reverse=True)
        naive_b, gp_b, naive_w, gp_w = [], [], [], []
        for level in levels:
            s = [r for r in sub if math.isclose(float(r["completeness"]), level)]
            naive_b.append(sum(float(r["naive_bias"]) for r in s) / len(s))
            gp_b.append(sum(float(r["gp_bias"]) for r in s) / len(s))
            naive_w.append(sum(float(r["naive_width_68"]) for r in s) / len(s))
            gp_w.append(sum(float(r["gp_width_68"]) for r in s) / len(s))
        axes[0].plot(levels, naive_b, marker="o", linestyle="-", label=f"{mechanism} — naive")
        axes[0].plot(levels, gp_b, marker="o", linestyle="--", label=f"{mechanism} — GP")
        axes[1].plot(levels, naive_w, marker="o", linestyle="-", label=f"{mechanism} — naive")
        axes[1].plot(levels, gp_w, marker="o", linestyle="--", label=f"{mechanism} — GP")
    axes[0].axhline(0, linestyle="--", linewidth=1)
    axes[0].set_xlabel("Catalogue completeness")
    axes[0].set_ylabel("Mean median H₀ bias (km/s/Mpc)")
    axes[0].set_title("Bias: naive vs GP")
    axes[1].set_xlabel("Catalogue completeness")
    axes[1].set_ylabel("Mean 68% posterior width (km/s/Mpc)")
    axes[1].set_title("Posterior width: naive vs GP")
    axes[1].legend(fontsize=7, ncol=2)
    _save(fig, output)


def plot_gp_coverage(
    gp_summary_csv="results/gp_pilot_summary.csv",
    output="results/figures/gp_coverage_comparison.png",
):
    """Compare empirical 68% coverage from the executed GP pilot."""
    rows = _rows(gp_summary_csv)
    fig, ax = plt.subplots(figsize=(8, 5))
    for mechanism in ("random", "faint", "redshift", "sky"):
        sub = sorted(
            [r for r in rows if r["mechanism"] == mechanism],
            key=lambda r: float(r["completeness"]),
        )
        if not sub:
            continue
        x = [float(r["completeness"]) for r in sub]
        ax.plot(x, [float(r["naive_coverage_68"]) for r in sub],
                marker="o", label=f"{mechanism} — naive")
        ax.plot(x, [float(r["gp_coverage_68"]) for r in sub],
                marker="o", linestyle="--", label=f"{mechanism} — GP")
    ax.axhline(0.68, linestyle=":", linewidth=1, label="Nominal 68%")
    ax.set_xlabel("Catalogue completeness")
    ax.set_ylabel("Empirical 68% coverage")
    ax.set_title("Coverage: naive vs GP redshift-density weighting")
    ax.set_ylim(0, 1)
    ax.legend(fontsize=7, ncol=2)
    _save(fig, output)
