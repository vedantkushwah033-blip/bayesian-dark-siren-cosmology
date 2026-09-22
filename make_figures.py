"""Generate publication-oriented figures from an executed summary matrix."""

from src.figures import (
    plot_bias_vs_completeness,
    plot_coverage_vs_completeness,
    plot_weighting_heatmap,
    plot_mechanism_heatmap,
)


if __name__ == "__main__":
    for mechanism in ("random", "faint", "redshift", "sky"):
        plot_bias_vs_completeness(
            missingness=mechanism,
            output=f"results/figures/bias_vs_completeness_{mechanism}.png",
        )
        plot_coverage_vs_completeness(
            missingness=mechanism,
            output=f"results/figures/coverage_vs_completeness_{mechanism}.png",
        )

    for value_key, filename in (
        ("median_bias", "weighting_median_bias_heatmap.png"),
        ("rmse_mean", "weighting_rmse_heatmap.png"),
        ("coverage_68", "weighting_coverage68_heatmap.png"),
    ):
        plot_weighting_heatmap(
            value_key=value_key,
            output=f"results/figures/{filename}",
        )

    plot_mechanism_heatmap(
        output="results/figures/mechanism_bias_heatmap_50pct.png",
        completeness=0.5,
    )

    print("Figures written to results/figures/")
