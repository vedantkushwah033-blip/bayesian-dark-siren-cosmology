"""Small paired pilot for catalogue incompleteness.

Uses the same seed sequence at 100%, 90%, 70%, and 50% completeness so the
first-stage comparison is driven by catalogue completeness rather than a
different set of mock universes.
"""
from src.experiments import run_repeated
from src.metrics_v2 import summarize_runs

if __name__ == "__main__":
    for completeness in (1.0, 0.9, 0.7, 0.5):
        rows = run_repeated(
            n_runs=200,
            completeness=completeness,
            missingness="random" if completeness < 1.0 else "complete",
            host_generation="uniform",
            inference_weighting="uniform",
            include_missing_host_term=False,
            seed=9000,
        )
        summary = summarize_runs(rows)
        print(f"COMPLETENESS={completeness:.1f}")
        print(summary)
