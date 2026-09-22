"""Run a nominal-vs-empirical coverage calibration experiment."""

import numpy as np
import pandas as pd

from src.simulations_v2 import simulate_galaxy_catalogue, choose_host, simulate_gw_event
from src.bayesian_inference import posterior_h0, posterior_summary


def _quantile(grid, posterior, q):
    cdf = np.concatenate(
        [[0.0], np.cumsum((posterior[1:] + posterior[:-1]) * np.diff(grid) / 2)]
    )
    cdf /= cdf[-1]
    return float(np.interp(q, cdf, grid))


def run(n_runs=2000, seed=2026, n_galaxies=500, h0_true=70.0):
    grid = np.linspace(50.0, 90.0, 1601)
    levels = (0.50, 0.68, 0.80, 0.90, 0.95)
    counts = {level: 0 for level in levels}

    for r in range(n_runs):
        s = seed + r
        cat = simulate_galaxy_catalogue(
            n_galaxies=n_galaxies, H0_true=h0_true, seed=s
        )
        host = choose_host(cat, weighting="uniform", seed=s + 100000)
        gw = simulate_gw_event(cat["true_distance_mpc"][host], seed=s + 200000)
        posterior = posterior_h0(
            grid,
            cat["redshift"],
            gw["observed_distance_mpc"],
            gw["sigma_mpc"],
        )

        for level in levels:
            alpha = (1.0 - level) / 2.0
            lower = _quantile(grid, posterior, alpha)
            upper = _quantile(grid, posterior, 1.0 - alpha)
            counts[level] += int(lower <= h0_true <= upper)

    rows = []
    for level in levels:
        coverage = counts[level] / n_runs
        se = np.sqrt(coverage * (1.0 - coverage) / n_runs)
        rows.append(
            {
                "nominal_coverage": level,
                "empirical_coverage": coverage,
                "coverage_se": se,
                "n": n_runs,
            }
        )
    return pd.DataFrame(rows)


if __name__ == "__main__":
    df = run()
    df.to_csv("results/calibration_curve.csv", index=False)
    print(df.to_string(index=False))
