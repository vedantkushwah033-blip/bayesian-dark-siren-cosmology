"""Synthetic galaxy and gravitational-wave data generation."""

import numpy as np
from .cosmology import hubble_distance


def simulate_galaxy_catalogue(n_galaxies=500, H0_true=70.0, z_min=0.005, z_max=0.08, seed=42):
    """Generate a simple complete synthetic galaxy catalogue."""
    rng = np.random.default_rng(seed)
    z = rng.uniform(z_min, z_max, n_galaxies)
    distance = hubble_distance(z, H0_true)
    return {
        "galaxy_id": np.arange(n_galaxies),
        "redshift": z,
        "true_distance_mpc": distance,
    }


def simulate_gw_event(true_distance_mpc, fractional_distance_error=0.15, seed=123):
    """Generate one noisy GW luminos-distance measurement."""
    rng = np.random.default_rng(seed)
    sigma = fractional_distance_error * true_distance_mpc
    observed = rng.normal(true_distance_mpc, sigma)
    return {"observed_distance_mpc": observed, "sigma_mpc": sigma}
