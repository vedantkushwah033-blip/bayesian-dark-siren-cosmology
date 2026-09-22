import numpy as np

from src.gp_reconstruction import gp_redshift_weights, reconstruct_redshift_density


def test_gp_weights_are_finite_and_normalized():
    z = np.linspace(0.02, 0.10, 40)
    w = gp_redshift_weights(z)
    assert np.all(np.isfinite(w))
    assert np.all(w > 0)
    assert np.isclose(w.sum(), 1.0)


def test_gp_reconstruction_is_reproducible_and_positive():
    observed = np.array([0.02, 0.021, 0.023, 0.05, 0.052, 0.09])
    target = np.linspace(0.02, 0.09, 20)
    a = reconstruct_redshift_density(observed, target)
    b = reconstruct_redshift_density(observed, target)
    assert np.allclose(a, b)
    assert np.all(a > 0)
    assert np.isclose(a.sum(), 1.0)
