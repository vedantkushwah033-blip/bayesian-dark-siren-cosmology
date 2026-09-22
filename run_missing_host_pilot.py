"""Paired pilot: naive versus oracle missing-host-aware inference.

Each seed defines one mock universe and catalogue mask. The two inference
models therefore see the same simulated event and catalogue; only treatment
of the uncatalogued population differs.
"""
from src.experiments import run_repeated
from src.metrics_v2 import summarize_runs

if __name__ == "__main__":
    for mechanism in ("random", "faint", "redshift", "sky"):
        for completeness in (0.9, 0.7, 0.5):
            naive = run_repeated(
                n_runs=300,
                completeness=completeness,
                missingness=mechanism,
                host_generation="uniform",
                inference_weighting="uniform",
                include_missing_host_term=False,
                seed=12000,
            )
            aware = run_repeated(
                n_runs=300,
                completeness=completeness,
                missingness=mechanism,
                host_generation="uniform",
                inference_weighting="uniform",
                include_missing_host_term=True,
                missing_host_weighting="oracle_true",
                seed=12000,
            )
            n = summarize_runs(naive)
            a = summarize_runs(aware)
            print(
                f"MECHANISM={mechanism} COMPLETENESS={completeness:.1f} "
                f"NAIVE_BIAS={n['median_bias']:.6f} "
                f"AWARE_BIAS={a['median_bias']:.6f} "
                f"NAIVE_COV68={n['coverage_68']:.6f} "
                f"AWARE_COV68={a['coverage_68']:.6f} "
                f"NAIVE_WIDTH68={n['mean_width_68']:.6f} "
                f"AWARE_WIDTH68={a['mean_width_68']:.6f} "
                f"NAIVE_HOSTFRAC={n['host_observed_fraction']:.6f} "
                f"AWARE_HOSTFRAC={a['host_observed_fraction']:.6f}"
            )
