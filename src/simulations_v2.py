"""Controlled dark-siren mock-universe generation."""

import numpy as np
from .cosmology import hubble_distance


def simulate_galaxy_catalogue(n_galaxies=500, H0_true=70.0, z_min=0.005, z_max=0.08, seed=42):
    rng = np.random.default_rng(seed)
    z = rng.uniform(z_min, z_max, n_galaxies)
    distance = hubble_distance(z, H0_true)
    luminosity = 10 ** rng.uniform(9.0, 11.5, n_galaxies)
    mass_proxy = luminosity * 10 ** rng.normal(0.0, 0.25, n_galaxies)
    ra = rng.uniform(0.0, 360.0, n_galaxies)
    return {
        "galaxy_id": np.arange(n_galaxies),
        "redshift": z,
        "true_distance_mpc": distance,
        "luminosity_proxy": luminosity,
        "mass_proxy": mass_proxy,
        "ra_deg": ra,
    }


def choose_host(catalogue, weighting="uniform", seed=7):
    rng = np.random.default_rng(seed)
    if weighting == "uniform":
        w = np.ones(len(catalogue["redshift"]))
    elif weighting == "luminosity":
        w = catalogue["luminosity_proxy"]
    elif weighting == "mass":
        w = catalogue["mass_proxy"]
    else:
        raise ValueError("Unknown host weighting.")
    w = w / w.sum()
    return int(rng.choice(len(w), p=w))


def simulate_gw_event(true_distance_mpc, fractional_distance_error=0.15, seed=123):
    rng = np.random.default_rng(seed)
    sigma = fractional_distance_error * true_distance_mpc
    observed = rng.normal(true_distance_mpc, sigma)
    return {"observed_distance_mpc": observed, "sigma_mpc": sigma}
