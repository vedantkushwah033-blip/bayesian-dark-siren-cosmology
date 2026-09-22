"""Generate figures only from an executed summary matrix."""
from src.figures import plot_bias_vs_completeness, plot_coverage_vs_completeness

if __name__ == "__main__":
    plot_bias_vs_completeness()
    plot_coverage_vs_completeness()
    print("Figures written to results/figures/")
