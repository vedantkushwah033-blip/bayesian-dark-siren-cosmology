"""Baseline low-redshift cosmology utilities for the dark-siren simulation."""

import numpy as np

C_KM_S = 299792.458


def hubble_distance(z, H0):
    """Approximate luminosity distance in Mpc using d_L ~= c z / H0."""
    z = np.asarray(z, dtype=float)
    return C_KM_S * z / H0
