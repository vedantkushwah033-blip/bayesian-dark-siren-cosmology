"""Compare catalogue-only and GP-redshift-density weighting.

The pilot is intentionally small and reproducible. It compares the baseline
uniform candidate weighting against a GP-smoothed redshift-density weighting
for the four incompleteness mechanisms.
"""

import pandas as pd
from src.experiments import run_repeated
from src.gp_reconstruction import gp_redshift_weights
from src.bayesian_inference import posterior_h0, posterior_summary
import numpy as np


def run_gp_repeated(n_runs=300, completeness=0.7, mechanism="redshift", seed=2026):
    rows = []
    grid = np.linspace(50.0, 90.0, 1601)

    for r in range(n_runs):
        s = seed + r
        # Reuse the exact simulation/masking logic through the baseline runner
        # for the naive control, then independently reconstruct the same model
        # below so the paired random seed is preserved.
        from src.simulations_v2 import simulate_galaxy_catalogue, choose_host, simulate_gw_event
        from src.completeness import random_missing_mask, faint_missing_mask, redshift_dependent_mask, sky_region_mask

        cat = simulate_galaxy_catalogue(n_galaxies=500, H0_true=70.0, seed=s)
        host = choose_host(cat, weighting="uniform", seed=s + 100000)
        gw = simulate_gw_event(cat["true_distance_mpc"][host], seed=s + 200000)

        if mechanism == "random":
            mask = random_missing_mask(500, completeness, s + 300000)
        elif mechanism == "faint":
            mask = faint_missing_mask(cat["luminosity_proxy"], completeness)
        elif mechanism == "redshift":
            mask = redshift_dependent_mask(cat["redshift"], completeness, s + 300000)
        elif mechanism == "sky":
            mask = sky_region_mask(cat["ra_deg"], completeness, seed=s + 300000)
        else:
            raise ValueError("Unknown mechanism.")

        z_obs = cat["redshift"][mask]

        p_naive = posterior_h0(
            grid, z_obs, gw["observed_distance_mpc"], gw["sigma_mpc"],
            weights=np.ones(len(z_obs))
        )
        gp_w = gp_redshift_weights(z_obs)
        p_gp = posterior_h0(
            grid, z_obs, gw["observed_distance_mpc"], gw["sigma_mpc"],
            weights=gp_w
        )
        n = posterior_summary(grid, p_naive)
        g = posterior_summary(grid, p_gp)

        rows.append({
            "run": r, "mechanism": mechanism, "completeness": completeness,
            "naive_median": n["median"], "gp_median": g["median"],
            "naive_bias": n["median"] - 70.0, "gp_bias": g["median"] - 70.0,
            "naive_width_68": n["upper_68"] - n["lower_68"],
            "gp_width_68": g["upper_68"] - g["lower_68"],
            "naive_covered_68": n["lower_68"] <= 70.0 <= n["upper_68"],
            "gp_covered_68": g["lower_68"] <= 70.0 <= g["upper_68"],
        })
    return rows


def main():
    all_rows = []
    for mechanism in ("random", "faint", "redshift", "sky"):
        for completeness in (0.9, 0.7, 0.5):
            all_rows.extend(run_gp_repeated(300, completeness, mechanism))
    df = pd.DataFrame(all_rows)
    df.to_csv("results/gp_pilot.csv", index=False)
    summary = (
        df.groupby(["mechanism", "completeness"])
        .agg(
            naive_bias=("naive_bias", "mean"),
            gp_bias=("gp_bias", "mean"),
            naive_width_68=("naive_width_68", "mean"),
            gp_width_68=("gp_width_68", "mean"),
            naive_coverage_68=("naive_covered_68", "mean"),
            gp_coverage_68=("gp_covered_68", "mean"),
        )
        .reset_index()
    )
    summary.to_csv("results/gp_pilot_summary.csv", index=False)
    print(summary.to_string(index=False))


if __name__ == "__main__":
    main()
