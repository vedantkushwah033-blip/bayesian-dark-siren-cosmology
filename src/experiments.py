"""Repeated-universe experiments for dark-siren H0 inference."""
import numpy as np
from .simulations_v2 import simulate_galaxy_catalogue, choose_host, simulate_gw_event
from .bayesian_inference import posterior_h0, posterior_summary
from .completeness import random_missing_mask, faint_missing_mask, redshift_dependent_mask, sky_region_mask
from .metrics import summarize_runs

def run_repeated(n_runs=100, n_galaxies=500, H0_true=70.0, completeness=1.0, missingness="complete", host_generation="uniform", seed=2026):
    estimates=[]; lows=[]; highs=[]
    H0_grid=np.linspace(50,90,1601)
    for r in range(n_runs):
        base_seed=seed+r
        cat=simulate_galaxy_catalogue(n_galaxies=n_galaxies,H0_true=H0_true,seed=base_seed)
        host=choose_host(cat, weighting=host_generation, seed=base_seed+100000)
        gw=simulate_gw_event(cat["true_distance_mpc"][host],seed=base_seed+200000)
        if missingness=="complete": mask=np.ones(n_galaxies,dtype=bool)
        elif missingness=="random": mask=random_missing_mask(n_galaxies,completeness,seed=base_seed+300000)
        elif missingness=="faint": mask=faint_missing_mask(cat["luminosity_proxy"],completeness)
        elif missingness=="redshift": mask=redshift_dependent_mask(cat["redshift"],completeness,seed=base_seed+300000)
        elif missingness=="sky": mask=sky_region_mask(cat["ra_deg"],completeness,seed=base_seed+300000)
        else: raise ValueError("Unknown missingness mechanism")
        # For the first calibration stage, keep runs where the hidden host remains observed.
        if not mask[host]:
            continue
        weights=np.ones(mask.sum())
        if host_generation=="luminosity": weights=cat["luminosity_proxy"][mask]
        elif host_generation=="mass": weights=cat["mass_proxy"][mask]
        post=posterior_h0(H0_grid,cat["redshift"][mask],gw["observed_distance_mpc"],gw["sigma_mpc"],weights=weights)
        s=posterior_summary(H0_grid,post)
        estimates.append(s["median"]); lows.append(s["lower_68"]); highs.append(s["upper_68"])
    return summarize_runs(estimates,lows,highs,H0_true)
