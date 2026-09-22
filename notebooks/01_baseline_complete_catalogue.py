"""Current baseline demonstration for the dark-siren H0 simulation.

This script mirrors the validated v2 simulation rather than the deprecated
prototype generator. It is a lightweight educational demonstration; the
repeated experiment scripts remain the authoritative source for reported
results.
"""

import numpy as np
import matplotlib.pyplot as plt

from src.simulations_v2 import simulate_galaxy_catalogue, choose_host, simulate_gw_event
from src.bayesian_inference import posterior_h0, posterior_summary

H0_TRUE = 70.0
catalogue = simulate_galaxy_catalogue(
    n_galaxies=500,
    H0_true=H0_TRUE,
    seed=42,
)
host_index = choose_host(catalogue, weighting="uniform", seed=100042)
true_distance = catalogue["true_distance_mpc"][host_index]
gw = simulate_gw_event(true_distance_mpc=true_distance, seed=200042)

H0_grid = np.linspace(50, 90, 1601)
posterior = posterior_h0(
    H0_grid,
    catalogue["redshift"],
    gw["observed_distance_mpc"],
    gw["sigma_mpc"],
    weights=np.ones(len(catalogue["redshift"])),
)
summary = posterior_summary(H0_grid, posterior)

print("True H0:", H0_TRUE, "km/s/Mpc")
print("GW observed distance:", round(gw["observed_distance_mpc"], 2), "Mpc")
print("Posterior summary:", summary)

plt.figure(figsize=(8, 5))
plt.plot(H0_grid, posterior)
plt.axvline(H0_TRUE, linestyle="--", label="True H0")
plt.xlabel("H0 (km/s/Mpc)")
plt.ylabel("Posterior density")
plt.title("Baseline dark-siren posterior")
plt.legend()
plt.tight_layout()
plt.show()
