"""Simulation metrics for repeated dark-siren experiments."""
import numpy as np

def summarize_runs(estimates, lower, upper, true_h0):
    estimates=np.asarray(estimates,float); lower=np.asarray(lower,float); upper=np.asarray(upper,float)
    err=estimates-true_h0
    return {
        "n": int(len(estimates)),
        "mean_estimate": float(np.mean(estimates)),
        "bias": float(np.mean(err)),
        "relative_bias": float(np.mean(err)/true_h0),
        "rmse": float(np.sqrt(np.mean(err**2))),
        "mean_interval_width": float(np.mean(upper-lower)),
        "coverage_68": float(np.mean((lower<=true_h0)&(true_h0<=upper))),
    }
