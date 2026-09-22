"""Bayesian H0 inference for the simplified dark-siren mixture model."""
import numpy as np
from scipy.stats import norm

C_KM_S = 299792.458

def posterior_h0(H0_grid, redshifts, gw_distance, gw_sigma, weights=None, missing_weight=0.0, missing_redshifts=None, missing_weights=None, prior_min=50.0, prior_max=90.0):
    """Compute a normalized H0 posterior with an optional missing-host component."""
    H0_grid = np.asarray(H0_grid, dtype=float)
    redshifts = np.asarray(redshifts, dtype=float)
    if redshifts.size == 0:
        raise ValueError("At least one catalogued redshift is required.")
    weights = np.ones(redshifts.size) if weights is None else np.asarray(weights, dtype=float)
    if weights.size != redshifts.size or np.any(weights < 0) or weights.sum() <= 0:
        raise ValueError("Invalid catalogue weights.")
    if not 0.0 <= missing_weight < 1.0:
        raise ValueError("missing_weight must be in [0, 1).")
    weights = weights / weights.sum() * (1.0 - missing_weight)
    if missing_weight > 0:
        if missing_redshifts is None:
            raise ValueError("missing_redshifts are required when missing_weight > 0.")
        missing_redshifts = np.asarray(missing_redshifts, dtype=float)
        missing_weights = np.ones(missing_redshifts.size) if missing_weights is None else np.asarray(missing_weights, dtype=float)
        if missing_redshifts.size == 0 or missing_weights.size != missing_redshifts.size or np.any(missing_weights < 0) or missing_weights.sum() <= 0:
            raise ValueError("Invalid missing-host support or weights.")
        missing_weights = missing_weights / missing_weights.sum()
    else:
        missing_redshifts = np.array([])
        missing_weights = np.array([])
    posterior = np.zeros_like(H0_grid)
    valid_prior = (H0_grid >= prior_min) & (H0_grid <= prior_max)
    for j, H0 in enumerate(H0_grid):
        d = C_KM_S * redshifts / H0
        like = np.sum(weights * norm.pdf(gw_distance, loc=d, scale=gw_sigma))
        if missing_weight > 0:
            dm = C_KM_S * missing_redshifts / H0
            like += missing_weight * np.sum(missing_weights * norm.pdf(gw_distance, loc=dm, scale=gw_sigma))
        posterior[j] = like
    posterior[~valid_prior] = 0.0
    area = np.trapezoid(posterior, H0_grid)
    if not np.isfinite(area) or area <= 0:
        raise ValueError("Posterior normalization failed.")
    return posterior / area

def posterior_summary(H0_grid, posterior):
    """Return posterior mean, median, central 68% and central 95% intervals."""
    H0_grid = np.asarray(H0_grid, dtype=float)
    posterior = np.asarray(posterior, dtype=float)
    mean = np.trapezoid(H0_grid * posterior, H0_grid)
    variance = np.trapezoid((H0_grid - mean) ** 2 * posterior, H0_grid)
    posterior_sd = np.sqrt(max(variance, 0.0))
    cdf = np.concatenate([[0.0], np.cumsum((posterior[1:] + posterior[:-1]) * np.diff(H0_grid) / 2)])
    cdf = cdf / cdf[-1]
    return {"mean": mean, "median": np.interp(0.5, cdf, H0_grid), "posterior_sd": posterior_sd, "lower_68": np.interp(0.16, cdf, H0_grid), "upper_68": np.interp(0.84, cdf, H0_grid), "lower_95": np.interp(0.025, cdf, H0_grid), "upper_95": np.interp(0.975, cdf, H0_grid)}