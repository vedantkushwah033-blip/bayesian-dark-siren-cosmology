"""Validation summaries for repeated dark-siren simulations."""
import numpy as np


def summarize_runs(rows, true_h0=70.0):
    """Summarize repeated trials with explicit mean/median pull diagnostics."""
    if not rows:
        raise ValueError("No simulation rows supplied.")

    med = np.asarray([r["median"] for r in rows], float)
    mean = np.asarray([r["mean"] for r in rows], float)
    lo68 = np.asarray([r["lower_68"] for r in rows], float)
    hi68 = np.asarray([r["upper_68"] for r in rows], float)
    lo95 = np.asarray([r["lower_95"] for r in rows], float)
    hi95 = np.asarray([r["upper_95"] for r in rows], float)

    c68 = np.mean((lo68 <= true_h0) & (true_h0 <= hi68))
    c95 = np.mean((lo95 <= true_h0) & (true_h0 <= hi95))

    pull_median = np.asarray(
        [r.get("pull_median", (r["median"] - true_h0) / max(r["posterior_sd"], 1e-12))
         for r in rows],
        float,
    )
    pull_mean = np.asarray(
        [r.get("pull_mean", (r["mean"] - true_h0) / max(r["posterior_sd"], 1e-12))
         for r in rows],
        float,
    )

    return {
        "n": len(rows),
        "median_bias": float(np.mean(med - true_h0)),
        "mean_bias": float(np.mean(mean - true_h0)),
        "rmse_median": float(np.sqrt(np.mean((med - true_h0) ** 2))),
        "rmse_mean": float(np.sqrt(np.mean((mean - true_h0) ** 2))),
        "mean_width_68": float(np.mean(hi68 - lo68)),
        "mean_width_95": float(np.mean(hi95 - lo95)),
        "coverage_68": float(c68),
        "coverage_95": float(c95),
        "coverage_68_mc_se": float(np.sqrt(c68 * (1 - c68) / len(rows))),
        "coverage_95_mc_se": float(np.sqrt(c95 * (1 - c95) / len(rows))),
        "pull_median_mean": float(np.mean(pull_median)),
        "pull_median_sd": float(np.std(pull_median, ddof=1)) if len(rows) > 1 else float("nan"),
        "pull_mean_mean": float(np.mean(pull_mean)),
        "pull_mean_sd": float(np.std(pull_mean, ddof=1)) if len(rows) > 1 else float("nan"),
        "host_observed_fraction": float(np.mean([r["host_observed"] for r in rows])),
    }
