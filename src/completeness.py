"""Catalogue incompleteness mechanisms for controlled experiments."""
import numpy as np

def random_missing_mask(n, completeness, seed=None):
    rng=np.random.default_rng(seed)
    return rng.random(n) < completeness

def faint_missing_mask(luminosity, completeness):
    luminosity=np.asarray(luminosity,float)
    threshold=np.quantile(luminosity,1-completeness)
    return luminosity >= threshold

def redshift_dependent_mask(redshift, completeness, seed=None):
    rng=np.random.default_rng(seed)
    z=np.asarray(redshift,float)
    x=(z-z.min())/(z.max()-z.min()+1e-12)
    p=1-x
    p=np.clip(p,0,1)
    p*=completeness/p.mean()
    p=np.clip(p,0,1)
    return rng.random(len(z)) < p

def sky_region_mask(ra, completeness, sky_fraction=0.25, seed=None):
    rng=np.random.default_rng(seed)
    ra=np.asarray(ra)%360
    start=rng.uniform(0,360)
    blocked=((ra-start)%360) < 360*sky_fraction
    keep=~blocked
    if keep.mean() <= completeness:
        return keep
    return keep & (rng.random(len(ra)) < completeness/keep.mean())
