# Pilot Results: Missing-Host and Catalogue-Incompleteness Controls

## Validation status

The validation workflow completed successfully. Unit tests, the 1,000-run calibration, missing-host pilot, paired incompleteness pilot, and known-host diagnostic all completed successfully.

## Main findings

The 1,000-run complete-catalogue control with true H0 = 70 km/s/Mpc gave median bias +1.986 km/s/Mpc, mean bias +1.259, median RMSE 6.190, mean 68% posterior width 22.372, 68% coverage 94.4%, and 95% coverage 99.9%. The control is reproducible but not perfectly nominally calibrated, so incompleteness effects should be interpreted relative to it.

The known-host diagnostic gave median bias +1.475, mean bias +1.616, mean 68% width 17.045, and 68% coverage 74.9%. This confirms that the simplified low-redshift distance model itself contributes to baseline calibration error.

The 200-run random-missingness pilot showed little change across 100%, 90%, 70%, and 50% catalogue completeness: median bias stayed around +1.7 km/s/Mpc and 68% coverage stayed around 93–95%.

The 300-run paired missing-host pilot compared naive catalogue-only inference with an oracle missing-host-aware model for random, faint, redshift-dependent, and sky-dependent missingness at 90%, 70%, and 50% completeness. The oracle model is a validation control using the hidden simulated population; it is not presented as a realistic survey correction.

The clearest mechanism-specific effect in this baseline is redshift-dependent incompleteness. Naive median bias changed from about +1.31 at 90% completeness to +0.97 at 70% and +0.68 at 50%, while posterior width increased from about 22.42 to 22.82 km/s/Mpc. Random, faint, and sky mechanisms produced much smaller changes in this configuration.

## Next experiment

Proceed to the planned host-generation × inference-weighting matrix. The key scientific comparison is matched versus deliberately mismatched assumptions about host weighting, under each incompleteness mechanism and completeness level.

Do not introduce an arbitrary selection-function denominator beta(H0). A defensible beta(H0) requires a consistent event/galaxy selection model and should be added only after the baseline model is validated.

## GP pilot result (3,600 paired runs)

The GP extension completed successfully. The pilot contains 300 paired simulations for each of 12 mechanism/completeness conditions, comparing uniform catalogue weighting with the current GP-smoothed redshift-density weighting.

The result is a **negative control result rather than a GP improvement**. Across all 3,600 paired runs, the GP posterior was narrower on average by 1.980 km/s/Mpc in 68% interval width, but its mean median-bias increased by 1.310 km/s/Mpc relative to the naive weighting. Overall 68% coverage decreased from 95.61% to 92.83% (a 2.78 percentage-point decrease).

The effect was present for all four missingness mechanisms. At 50% completeness, the GP bias increase was +1.377, +1.363, +1.064, and +1.469 km/s/Mpc for faint, random, redshift-dependent, and sky-dependent missingness respectively. The corresponding reductions in 68% width were 1.970, 1.997, 1.458, and 2.034 km/s/Mpc.

This does **not** show that Gaussian processes are intrinsically unsuitable for dark-siren inference. It shows that this particular lightweight implementation—an RBF GP fitted to binned log redshift counts and then used to reweight the already observed galaxies—does not recover the missing-host information in the present simulation. It tends to concentrate probability on reconstructed density peaks, narrowing the posterior without enough reduction in systematic error.

Accordingly, the GP pilot should be reported as a falsification/diagnostic experiment, not as a successful method. No claim of GP-based improvement should be made from this implementation.

The current scientific stopping point is therefore the baseline incompleteness/host-weighting matrix plus the documented GP negative result. A substantially different GP model would require a proper intensity/selection formulation and should be treated as a future extension rather than added solely to obtain a positive result.
