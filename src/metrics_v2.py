"""Validation summaries for repeated dark-siren simulations."""
import numpy as np

def summarize_runs(rows, true_h0=70.0):
    med=np.asarray([r["median"] for r in rows],float)
    mean=np.asarray([r["mean"] for r in rows],float)
    lo68=np.asarray([r["lower_68"] for r in rows],float)
    hi68=np.asarray([r["upper_68"] for r in rows],float)
    lo95=np.asarray([r["lower_95"] for r in rows],float)
    hi95=np.asarray([r["upper_95"] for r in rows],float)
    c68=np.mean((lo68<=true_h0)&(true_h0<=hi68))
    c95=np.mean((lo95<=true_h0)&(true_h0<=hi95))
    return {
        "n":len(rows),
        "median_bias":float(np.mean(med-true_h0)),
        "mean_bias":float(np.mean(mean-true_h0)),
        "rmse_median":float(np.sqrt(np.mean((med-true_h0)**2))),
        "mean_width_68":float(np.mean(hi68-lo68)),
        "mean_width_95":float(np.mean(hi95-lo95)),
        "coverage_68":float(c68),
        "coverage_95":float(c95),
        "coverage_68_mc_se":float(np.sqrt(c68*(1-c68)/len(rows))),
        "coverage_95_mc_se":float(np.sqrt(c95*(1-c95)/len(rows))),
        "pull_mean":float(np.mean([r["pull"] for r in rows])),
        "pull_std":float(np.std([r["pull"] for r in rows],ddof=1)) if len(rows)>1 else float("nan"),
    }
