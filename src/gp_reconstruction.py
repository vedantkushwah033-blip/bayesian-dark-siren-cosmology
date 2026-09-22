"""Lightweight Gaussian-process reconstruction of the 1D galaxy redshift density.

This is a deliberately transparent extension of the baseline simulation. It fits
a GP to log-smoothed redshift counts and converts the reconstructed intensity
into non-negative candidate weights. It is a density-field reconstruction
control, not a full Poisson-process GP model.
"""

import numpy as np
from scipy.linalg import cho_factor, cho_solve


def _rbf(x1, x2, length_scale):
    d = (np.asarray(x1)[:, None] - np.asarray(x2)[None, :]) / length_scale
    return np.exp(-0.5 * d * d)


def reconstruct_redshift_density(
    observed_redshifts,
    target_redshifts,
    z_min=0.01,
    z_max=0.12,
    n_bins=30,
    length_scale=0.015,
    noise_floor=0.08,
):
    """Return GP-reconstructed positive density weights at target redshifts.

    The observed catalogue is binned in redshift. A GP with an RBF kernel is
    fitted to log(count + 0.5), with a simple count-dependent noise estimate.
    The exponentiated GP mean is normalized before being evaluated at targets.
    """
    observed = np.asarray(observed_redshifts, dtype=float)
    target = np.asarray(target_redshifts, dtype=float)
    if observed.size == 0 or target.size == 0:
        raise ValueError("Observed and target redshift arrays must be non-empty.")
    if not (z_min < z_max and n_bins >= 5 and length_scale > 0):
        raise ValueError("Invalid GP reconstruction settings.")

    edges = np.linspace(z_min, z_max, n_bins + 1)
    centers = 0.5 * (edges[:-1] + edges[1:])
    counts, _ = np.histogram(observed, bins=edges)

    y = np.log(counts.astype(float) + 0.5)
    # A conservative heteroscedastic noise approximation on log counts.
    noise = np.maximum(1.0 / (counts.astype(float) + 0.5), noise_floor)

    K = _rbf(centers, centers, length_scale)
    K[np.diag_indices_from(K)] += noise
    c, lower = cho_factor(K, lower=True, check_finite=False)

    K_star = _rbf(target, centers, length_scale)
    mean = K_star @ cho_solve((c, lower), y, check_finite=False)
    density = np.exp(np.clip(mean, -20.0, 20.0))

    # Keep the reconstruction tied to the observed support.
    density = np.maximum(density, 1e-12)
    return density / np.sum(density)


def gp_redshift_weights(
    observed_redshifts,
    length_scale=0.015,
    n_bins=30,
    z_min=0.01,
    z_max=0.12,
):
    """Build normalized GP-derived weights for observed candidate galaxies."""
    return reconstruct_redshift_density(
        observed_redshifts,
        observed_redshifts,
        z_min=z_min,
        z_max=z_max,
        n_bins=n_bins,
        length_scale=length_scale,
    )
