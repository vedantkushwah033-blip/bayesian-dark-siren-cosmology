"""Controlled catalogue-selection mechanisms.

Each mechanism acts on one fixed underlying universe. Completeness is an
experimental parameter, not a change to the true galaxy population.
"""
import numpy as np


def _validate_completeness(completeness):
    if not 0.0 < completeness <= 1.0:
        raise ValueError("completeness must be in (0, 1].")


def random_missing_mask(n, completeness, seed=None):
    _validate_completeness(completeness)
    n_keep = int(round(n * completeness))
    rng = np.random.default_rng(seed)
    mask = np.zeros(n, dtype=bool)
    mask[rng.choice(n, size=n_keep, replace=False)] = True
    return mask


def faint_missing_mask(luminosity, completeness):
    _validate_completeness(completeness)
    luminosity = np.asarray(luminosity, float)
    n_keep = int(round(len(luminosity) * completeness))
    order = np.argsort(luminosity)[::-1]
    mask = np.zeros(len(luminosity), dtype=bool)
    mask[order[:n_keep]] = True
    return mask


def redshift_dependent_mask(redshift, completeness, seed=None):
    _validate_completeness(completeness)
    rng = np.random.default_rng(seed)
    z = np.asarray(redshift, float)
    n_keep = int(round(len(z) * completeness))
    score = 1.0 / (z + 1e-9)
    score = score / score.sum()
    keep = rng.choice(len(z), size=n_keep, replace=False, p=score)
    mask = np.zeros(len(z), dtype=bool)
    mask[keep] = True
    return mask


def sky_region_mask(ra, completeness, sky_fraction=0.25, seed=None):
    """Create sky-dependent missingness at any requested completeness.

    A contiguous sky patch is made less observable, but exact catalogue size
    is still enforced. This separates sky topology from raw catalogue size.
    """
    _validate_completeness(completeness)
    if not 0.0 <= sky_fraction < 1.0:
        raise ValueError("sky_fraction must be in [0, 1).")
    rng = np.random.default_rng(seed)
    ra = np.asarray(ra, float) % 360.0
    n_keep = int(round(len(ra) * completeness))

    start = rng.uniform(0.0, 360.0)
    blocked = ((ra - start) % 360.0) < 360.0 * sky_fraction

    # Give galaxies inside the footprint gap a lower detection score, while
    # retaining a non-zero chance of selection. Sampling with these scores
    # permits 90%, 70%, and 50% completeness without changing n_keep.
    score = np.where(blocked, 0.15, 1.0).astype(float)
    score /= score.sum()
    keep = rng.choice(len(ra), size=n_keep, replace=False, p=score)

    mask = np.zeros(len(ra), dtype=bool)
    mask[keep] = True
    return mask
