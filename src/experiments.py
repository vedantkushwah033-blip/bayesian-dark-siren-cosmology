"""Controlled experiment matrix for dark-siren catalogue incompleteness."""

import numpy as np
from .simulations_v2 import simulate_galaxy_catalogue, choose_host, simulate_gw_event
from .bayesian_inference import posterior_h0, posterior_summary
from .completeness import (
    random_missing_mask,
    faint_missing_mask,
    redshift_dependent_mask,
    sky_region_mask,
)


def _weights(cat, mode):
    if mode == "uniform":
        return np.ones(len(cat["redshift"]))
    if mode == "luminosity":
        return np.asarray(cat["luminosity_proxy"], float)
    if mode == "mass":
        return np.asarray(cat["mass_proxy"], float)
    raise ValueError("Unknown weighting mode.")


def _mask(cat, completeness, mechanism, seed):
    n = len(cat["redshift"])
    if mechanism == "complete":
        return np.ones(n, dtype=bool)
    if mechanism == "random":
        return random_missing_mask(n, completeness, seed)
    if mechanism == "faint":
        return faint_missing_mask(cat["luminosity_proxy"], completeness)
    if mechanism == "redshift":
        return redshift_dependent_mask(cat["redshift"], completeness, seed)
    if mechanism == "sky":
        return sky_region_mask(cat["ra_deg"], completeness, seed=seed)
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
    """Run independent mock universes and return per-run diagnostics.

    The missing-host component is intentionally an oracle term: it uses the
    known hidden population from the simulation. This is a validation control,
    not a claim about what a real survey can observe.
    """
    if inference_weighting is None:
        inference_weighting = host_generation

    rows = []
    grid = np.linspace(50.0, 90.0, 1601)

    for r in range(n_runs):
        s = seed + r
        cat = simulate_galaxy_catalogue(
            n_galaxies=n_galaxies, H0_true=H0_true, seed=s
        )
        true_weights = _weights(cat, host_generation)
        host = choose_host(cat, weighting=host_generation, seed=s + 100000)
        gw = simulate_gw_event(
            cat["true_distance_mpc"][host],
            seed=s + 200000,
        )
        mask = _mask(cat, completeness, missingness, s + 300000)

        hidden = ~mask
        observed_weights = _weights(cat, inference_weighting)[mask]
        if observed_weights.size == 0:
            continue

        missing_weight = 0.0
        missing_z = None
        missing_w = None
        if include_missing_host_term and missingness != "complete" and hidden.any():
            missing_weight = float(true_weights[hidden].sum() / true_weights.sum())
            missing_z = cat["redshift"][hidden]
            missing_w = true_weights[hidden]

        posterior = posterior_h0(
            grid,
            cat["redshift"][mask],
            gw["observed_distance_mpc"],
            gw["sigma_mpc"],
            weights=observed_weights,
            missing_weight=missing_weight,
            missing_redshifts=missing_z,
            missing_weights=missing_w,
        )
        summary = posterior_summary(grid, posterior)

        rows.append(
            {
                "run": r,
                "H0_true": float(H0_true),
                "host_generation": host_generation,
                "inference_weighting": inference_weighting,
                "missingness": missingness,
                "target_completeness": completeness,
                "realized_completeness": float(mask.mean()),
                "host_observed": bool(mask[host]),
                "host_redshift": float(cat["redshift"][host]),
                "missing_host_prior_mass": float(missing_weight),
                "median": float(summary["median"]),
                "mean": float(summary["mean"]),
                "posterior_sd": float(summary["posterior_sd"]),
                "lower_68": float(summary["lower_68"]),
                "upper_68": float(summary["upper_68"]),
                "lower_95": float(summary["lower_95"]),
                "upper_95": float(summary["upper_95"]),
                "width_68": float(summary["upper_68"] - summary["lower_68"]),
                "width_95": float(summary["upper_95"] - summary["lower_95"]),
                "pull_median": float(
                    (summary["median"] - H0_true)
                    / max(summary["posterior_sd"], 1e-12)
                ),
                "pull_mean": float(
                    (summary["mean"] - H0_true)
                    / max(summary["posterior_sd"], 1e-12)
                ),
            }
        )

    if not rows:
        raise ValueError("No valid simulation runs.")
    return rows


def run_experiment_grid(
    completeness_levels=(1.0, 0.9, 0.7, 0.5),
    mechanisms=("complete", "random", "faint", "redshift", "sky"),
    host_models=("uniform", "luminosity", "mass"),
    n_runs=100,
    n_galaxies=500,
    H0_true=70.0,
    include_missing_host_term=False,
    seed=2026,
):
    """Run the planned host-weighting × completeness × selection matrix."""
    results = []
    counter = 0
    for host_model in host_models:
        for inference_model in host_models:
            for mechanism in mechanisms:
                for completeness in completeness_levels:
                    if mechanism == "complete" and completeness != 1.0:
                        continue
                    rows = run_repeated(
                        n_runs=n_runs,
                        n_galaxies=n_galaxies,
                        H0_true=H0_true,
                        completeness=completeness,
                        missingness=mechanism,
                        host_generation=host_model,
                        inference_weighting=inference_model,
                        include_missing_host_term=include_missing_host_term,
                        seed=seed + counter * 1000000,
                    )
                    results.extend(rows)
                    counter += 1
    return results
