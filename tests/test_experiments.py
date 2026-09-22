import numpy as np
from src.experiments import run_repeated
from src.bayesian_inference import posterior_h0


def test_repeated_run_is_reproducible():
    a = run_repeated(n_runs=5, n_galaxies=100, seed=123)
    b = run_repeated(n_runs=5, n_galaxies=100, seed=123)
    assert a == b


def test_missing_host_term_has_unit_total_prior_mass():
    cat_z = np.array([0.01, 0.02, 0.03, 0.04])
    weights = np.array([1.0, 1.0, 1.0])
    missing = np.array([0.05])
    missing_w = np.array([1.0])
    grid = np.linspace(50, 90, 401)
    p = posterior_h0(
        grid,
        cat_z,
        100.0,
        20.0,
        weights=weights,
        missing_weight=0.25,
        missing_redshifts=missing,
        missing_weights=missing_w,
    )
    assert np.isclose(np.trapezoid(p, grid), 1.0, atol=1e-8)


def test_incomplete_run_records_host_status():
    rows = run_repeated(
        n_runs=8,
        n_galaxies=100,
        completeness=0.5,
        missingness="random",
        seed=99,
    )
    assert len(rows) == 8
    assert all("host_observed" in row for row in rows)
    assert all("H0_true" in row for row in rows)
    assert all("pull_mean" in row and "pull_median" in row for row in rows)
    assert all(np.isclose(row["realized_completeness"], 0.5) for row in rows)


def test_all_missingness_mechanisms_hit_requested_size():
    for mechanism in ("random", "faint", "redshift", "sky"):
        rows = run_repeated(
            n_runs=3,
            n_galaxies=100,
            completeness=0.7,
            missingness=mechanism,
            seed=17,
        )
        assert len(rows) == 3
        assert all(np.isclose(r["realized_completeness"], 0.7) for r in rows)



def test_missing_host_weighting_modes_are_distinct_controls():
    inference_rows = run_repeated(
        n_runs=3, n_galaxies=100, completeness=0.7, missingness="random",
        host_generation="luminosity", inference_weighting="uniform",
        include_missing_host_term=True, missing_host_weighting="inference",
        seed=1234,
    )
    oracle_rows = run_repeated(
        n_runs=3, n_galaxies=100, completeness=0.7, missingness="random",
        host_generation="luminosity", inference_weighting="uniform",
        include_missing_host_term=True, missing_host_weighting="oracle_true",
        seed=1234,
    )
    assert all(r["missing_host_weighting"] == "inference" for r in inference_rows)
    assert all(r["missing_host_weighting"] == "oracle_true" for r in oracle_rows)
    assert any(
        not np.isclose(a["missing_host_prior_mass"], b["missing_host_prior_mass"])
        for a, b in zip(inference_rows, oracle_rows)
    )
