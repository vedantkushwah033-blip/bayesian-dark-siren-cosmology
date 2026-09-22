"""Repeated mock-universe validation experiments."""

import numpy as np
from .simulations_v2 import simulate_galaxy_catalogue, choose_host, simulate_gw_event
from .bayesian_inference import posterior_h0, posterior_summary
from .completeness import random_missing_mask, faint_missing_mask, redshift_dependent_mask, sky_region_mask


def _host_weights(catalogue, mode):
    if mode == "uniform":
        return np.ones(len(catalogue["redshift"]))
    if mode == "luminosity":
        return catalogue["luminosity_proxy"]
    if mode == "mass":
        return catalogue["mass_proxy"]
    raise ValueError("Unknown host weighting.")


def _mask(catalogue, completeness, mechanism, seed):
    n = len(catalogue["redshift"])
    if mechanism == "complete":
        return np.ones(n, dtype=bool)
    if mechanism == "random":
        return random_missing_mask(n, completeness, seed)
    if mechanism == "faint":
        return faint_missing_mask(catalogue["luminosity_proxy"], completeness)
    if mechanism == "redshift":
        return redshift_dependent_mask(catalogue["redshift"], completeness, seed)
    if mechanism == "sky":
        return sky_region_mask(catalogue["ra_deg"], completeness, seed=seed)
    raise ValueError("Unknown missingness mechanism.")


def run_repeated(
    n_runs=100,
    n_galaxies=500,
    H0_true=70.0,
    completeness=1.0,
    missingness="complete",
    host_generation="uniform",
    inference_weighting=None,
    include_missing_host_term=False,
    seed=2026,
):
    """Run independent universes and return per-run posterior diagnostics."""
    if inference_weighting is None:
        inference_weighting = host_generation

    rows = []
    grid = np.linspace(50.0, 90.0, 1601)

    for r in range(n_runs):
        s = seed + r
        cat = simulate_galaxy_catalogue(n_galaxies=n_galaxies, H0_true=H0_true, seed=s)
        host = choose_host(cat, weighting=host_generation, seed=s + 100000)
        gw = simulate_gw_event(cat["true_distance_mpc"][host], seed=s + 200000)
        mask = _mask(cat, completeness, missingness, s + 300000)

        observed = mask
        hidden = ~mask
        observed_weights = _host_weights(cat, inference_weighting)[observed]
        if observed_weights.size == 0:
            continue

        missing_weight = 0.0
        missing_z = None
        missing_w = None
        if include_missing_host_term and missingness != "complete":
            missing_weight = float(hidden.mean())
            if hidden.any():
                missing_z = cat["redshift"][hidden]
                missing_w = _host_weights(cat, host_generation)[hidden]

        posterior = posterior_h0(
            grid,
            cat["redshift"][observed],
            gw["observed_distance_mpc"],
            gw["sigma_mpc"],
            weights=observed_weights,
            missing_weight=missing_weight,
            missing_redshifts=missing_z,
            missing_weights=missing_w,
        )
        summary = posterior_summary(grid, posterior)
        rows.append({
            "run": r,
            "host_observed": bool(mask[host]),
            "catalogue_completeness": float(mask.mean()),
            "median": summary["median"],
            "mean": summary["mean"],
            "lower_68": summary["lower_68"],
            "upper_68": summary["upper_68"],
            "lower_95": summary["lower_95"],
            "upper_95": summary["upper_95"],
            "posterior_width_68": summary["upper_68"] - summary["lower_68"],
            "posterior_width_95": summary["upper_95"] - summary["lower_95"],
            "pull": (summary["median"] - H0_true) / max((summary["upper_68"] - summary["lower_68"]) / 2.0, 1e-12),
        })

    if not rows:
        raise ValueError("No valid simulation runs.")
    return rows
