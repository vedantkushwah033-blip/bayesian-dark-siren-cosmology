"""Paired comparisons of catalogue-only and missing-host-aware inference."""
from .experiments import run_repeated


def compare_missing_host_models(
    n_runs=100,
    completeness_levels=(0.9, 0.7, 0.5),
    missingness="random",
    host_generation="uniform",
    inference_weighting="uniform",
    n_galaxies=500,
    H0_true=70.0,
    seed=4100,
):
    """Run the same experiment with and without the missing-host term.

    Both analyses receive the same simulated universes through identical seeds,
    making the comparison a paired methodological experiment.
    """
    paired = []
    for i, completeness in enumerate(completeness_levels):
        naive = run_repeated(
            n_runs=n_runs, n_galaxies=n_galaxies, H0_true=H0_true,
            completeness=completeness, missingness=missingness,
            host_generation=host_generation, inference_weighting=inference_weighting,
            include_missing_host_term=False, seed=seed + i * 10000,
        )
        aware = run_repeated(
            n_runs=n_runs, n_galaxies=n_galaxies, H0_true=H0_true,
            completeness=completeness, missingness=missingness,
            host_generation=host_generation, inference_weighting=inference_weighting,
            include_missing_host_term=True, seed=seed + i * 10000,
        )
        for n, a in zip(naive, aware):
            paired.append({
                "completeness": completeness,
                "run": n["run"],
                "naive_median": n["median"],
                "aware_median": a["median"],
                "naive_width_68": n["width_68"],
                "aware_width_68": a["width_68"],
                "naive_host_observed": n["host_observed"],
                "aware_host_observed": a["host_observed"],
                "naive_pull": n["pull_median"],
                "aware_pull": a["pull_median"],
            })
    return paired
