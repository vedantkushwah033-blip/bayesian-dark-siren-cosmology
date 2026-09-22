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
