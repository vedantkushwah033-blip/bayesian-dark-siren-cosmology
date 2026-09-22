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
        med = np.array([r["median"] for r in group], float)
        mean = np.array([r["mean"] for r in group], float)
        lo68 = np.array([r["lower_68"] for r in group], float)
        hi68 = np.array([r["upper_68"] for r in group], float)
        lo95 = np.array([r["lower_95"] for r in group], float)
        hi95 = np.array([r["upper_95"] for r in group], float)
        h0 = 70.0
        c68 = np.mean((lo68 <= h0) & (h0 <= hi68))
        c95 = np.mean((lo95 <= h0) & (h0 <= hi95))
        summaries.append({
            "host_generation": key[0],
            "inference_weighting": key[1],
            "missingness": key[2],
            "completeness": key[3],
            "n": len(group),
            "median_bias": float(np.mean(med - h0)),
            "mean_bias": float(np.mean(mean - h0)),
            "rmse": float(np.sqrt(np.mean((med - h0) ** 2))),
            "mean_width_68": float(np.mean(hi68 - lo68)),
            "mean_width_95": float(np.mean(hi95 - lo95)),
            "coverage_68": float(c68),
            "coverage_95": float(c95),
            "coverage_68_se": float(np.sqrt(c68 * (1-c68) / len(group))),
            "coverage_95_se": float(np.sqrt(c95 * (1-c95) / len(group))),
            "mean_pull": float(np.mean([r["pull"] for r in group])),
            "sd_pull": float(np.std([r["pull"] for r in group], ddof=1)) if len(group) > 1 else float("nan"),
            "host_observed_fraction": float(np.mean([r["host_observed"] for r in group])),
        })
    return summaries
