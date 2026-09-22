"""Baseline calibration diagnostics.

Compares the full catalogue mixture against a known-host control to identify
whether calibration differences arise from host ambiguity or the simplified
distance-to-H0 likelihood itself.
"""
import numpy as np
from src.simulations_v2 import simulate_galaxy_catalogue, choose_host, simulate_gw_event
from src.bayesian_inference import posterior_h0, posterior_summary
from src.metrics_v2 import summarize_runs


def run_known_host(n_runs=1000, H0_true=70.0, seed=2026):
    rows = []
    grid = np.linspace(50.0, 90.0, 1601)
    for r in range(n_runs):
        s = seed + r
        cat = simulate_galaxy_catalogue(n_galaxies=500, H0_true=H0_true, seed=s)
        host = choose_host(cat, weighting="uniform", seed=s + 100000)
        gw = simulate_gw_event(cat["true_distance_mpc"][host], seed=s + 200000)
        z = np.array([cat["redshift"][host]])
        posterior = posterior_h0(
            grid,
            z,
            gw["observed_distance_mpc"],
            gw["sigma_mpc"],
            weights=np.array([1.0]),
        )
        summary = posterior_summary(grid, posterior)
        rows.append({
            "H0_true": H0_true,
            "median": summary["median"],
            "mean": summary["mean"],
            "posterior_sd": summary["posterior_sd"],
            "lower_68": summary["lower_68"],
            "upper_68": summary["upper_68"],
            "lower_95": summary["lower_95"],
            "upper_95": summary["upper_95"],
            "pull_median": (summary["median"] - H0_true) / max(summary["posterior_sd"], 1e-12),
            "pull_mean": (summary["mean"] - H0_true) / max(summary["posterior_sd"], 1e-12),
            "host_observed": True,
        })
    return rows


if __name__ == "__main__":
    print(summarize_runs(run_known_host()))
