"""Baseline run for the dark-siren H0 simulation.

Run with Python or convert this script into a notebook later.
"""
import os
import sys
sys.path.insert(0, os.path.abspath(".."))

import numpy as np
import matplotlib.pyplot as plt
from src.simulations import simulate_galaxy_catalogue, simulate_gw_event
from src.bayesian_inference import posterior_h0, posterior_summary

H0_TRUE = 70.0
catalogue = simulate_galaxy_catalogue(H0_true=H0_TRUE)
# Use one catalogue galaxy as the hidden true host for the baseline event.
host_index = 137
true_distance = catalogue["true_distance_mpc"][host_index]
gw = simulate_gw_event(true_distance_mpc=true_distance)

H0_grid = np.linspace(50, 90, 1601)
posterior = posterior_h0(
    H0_grid,
    catalogue["redshift"],
    gw["observed_distance_mpc"],
    gw["sigma_mpc"],
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
