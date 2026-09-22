"""Bayesian H0 inference for the baseline dark-siren model."""

import numpy as np
from scipy.stats import norm


def posterior_h0(H0_grid, redshifts, gw_distance, gw_sigma, weights=None, prior_min=50.0, prior_max=90.0):
    """Compute a normalized H0 posterior using a galaxy-host mixture likelihood."""
    H0_grid = np.asarray(H0_grid, dtype=float)
    redshifts = np.asarray(redshifts, dtype=float)
    if weights is None:
        weights = np.ones_like(redshifts) / len(redshifts)
    else:
        weights = np.asarray(weights, dtype=float)
        weights = weights / weights.sum()

    posterior = np.zeros_like(H0_grid)
    valid_prior = (H0_grid >= prior_min) & (H0_grid <= prior_max)
    c = 299792.458
    for j, H0 in enumerate(H0_grid):
        candidate_distances = c * redshifts / H0
        likelihood_per_host = norm.pdf(gw_distance, loc=candidate_distances, scale=gw_sigma)
        posterior[j] = np.sum(weights * likelihood_per_host)
    posterior[~valid_prior] = 0.0
    area = np.trapezoid(posterior, H0_grid)
    if area <= 0:
        raise ValueError("Posterior normalization failed.")
    return posterior / area


def posterior_summary(H0_grid, posterior):
    """Return posterior mean, median and central 68% interval."""
    mean = np.trapezoid(H0_grid * posterior, H0_grid)
    cdf = np.concatenate([[0], np.cumsum((posterior[1:] + posterior[:-1]) * np.diff(H0_grid) / 2)])
    cdf = cdf / cdf[-1]
    median = np.interp(0.5, cdf, H0_grid)
    lo = np.interp(0.16, cdf, H0_grid)
    hi = np.interp(0.84, cdf, H0_grid)
    return {"mean": mean, "median": median, "lower_68": lo, "upper_68": hi}
