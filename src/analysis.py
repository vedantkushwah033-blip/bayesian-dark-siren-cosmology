"""Aggregate raw simulation rows into publication-ready summary tables."""
from collections import defaultdict
import numpy as np


def summarize_matrix(rows):
    groups = defaultdict(list)
    for row in rows:
        key = (
            row["host_generation"],
            row["inference_weighting"],
            row["missingness"],
            row["target_completeness"],
        )
        groups[key].append(row)

    summaries = []
    for key, group in sorted(groups.items(), key=str):
        h0_values = np.asarray(
            [r.get("H0_true", 70.0) for r in group], float
        )
        if not np.allclose(h0_values, h0_values[0]):
            raise ValueError("A summary group contains inconsistent H0_true values.")
        h0 = float(h0_values[0])

        med = np.array([r["median"] for r in group], float)
        mean = np.array([r["mean"] for r in group], float)
        lo68 = np.array([r["lower_68"] for r in group], float)
        hi68 = np.array([r["upper_68"] for r in group], float)
        lo95 = np.array([r["lower_95"] for r in group], float)
        hi95 = np.array([r["upper_95"] for r in group], float)
        c68 = np.mean((lo68 <= h0) & (h0 <= hi68))
        c95 = np.mean((lo95 <= h0) & (h0 <= hi95))

        pull_median = np.asarray(
            [r.get("pull_median", r.get("pull", (r["median"] - h0) / max(r["posterior_sd"], 1e-12)))
             for r in group],
            float,
        )
        pull_mean = np.asarray(
            [r.get("pull_mean", (r["mean"] - h0) / max(r["posterior_sd"], 1e-12))
             for r in group],
            float,
        )

        summaries.append({
            "host_generation": key[0],
            "inference_weighting": key[1],
            "missingness": key[2],
            "completeness": key[3],
            "H0_true": h0,
            "n": len(group),
            "median_bias": float(np.mean(med - h0)),
            "mean_bias": float(np.mean(mean - h0)),
            "rmse_median": float(np.sqrt(np.mean((med - h0) ** 2))),
            "rmse_mean": float(np.sqrt(np.mean((mean - h0) ** 2))),
            "mean_width_68": float(np.mean(hi68 - lo68)),
            "mean_width_95": float(np.mean(hi95 - lo95)),
            "coverage_68": float(c68),
            "coverage_95": float(c95),
            "coverage_68_se": float(np.sqrt(c68 * (1-c68) / len(group))),
            "coverage_95_se": float(np.sqrt(c95 * (1-c95) / len(group))),
            "pull_median_mean": float(np.mean(pull_median)),
            "pull_median_sd": float(np.std(pull_median, ddof=1)) if len(group) > 1 else float("nan"),
            "pull_mean_mean": float(np.mean(pull_mean)),
            "pull_mean_sd": float(np.std(pull_mean, ddof=1)) if len(group) > 1 else float("nan"),
            "host_observed_fraction": float(np.mean([r["host_observed"] for r in group])),
        })
    return summaries
