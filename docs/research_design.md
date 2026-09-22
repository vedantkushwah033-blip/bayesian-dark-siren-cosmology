"""Research-design documentation for the controlled simulation study.

The statements below are hypotheses and design choices, not results.
"""

# Research hypotheses

## H1 — Structured incompleteness can matter at fixed nominal completeness

Two catalogues can retain the same fraction of the underlying galaxies while
producing different inference behaviour when the missingness depends on
luminosity, redshift, or sky position.

## H2 — Host-prior misspecification is separable from catalogue incompleteness

If the simulated host population is mass- or luminosity-weighted but the
inference assumes uniform weights, any change in bias or calibration should be
interpreted as model misspecification rather than as a catalogue-selection
effect alone.

## H3 — An uncatalogued-host term should improve calibration in the oracle test

When the simulation supplies the true missing-population redshift support and
host weights, adding that component provides a controlled test of whether
ignoring missing hosts is responsible for changes in posterior calibration.

This is an oracle validation experiment. It is not a claim that a real survey
knows the redshifts of its uncatalogued galaxies.

## H4 — The complete, correctly specified experiment is the calibration control

Before interpreting incomplete-catalogue experiments, the 100% complete case
with matched host generation and inference weighting should be checked for
reasonable recovery of the injected H0 and expected interval coverage.

A small finite-simulation deviation from nominal coverage is not itself proof of
a bug; coverage has Monte-Carlo uncertainty.

# Experimental controls

For every completeness level, the study records the realized catalogue
fraction and whether the hidden host was retained.

For comparisons between missingness mechanisms, the selection functions enforce
the same requested catalogue size. This makes the nominal completeness
comparable while allowing the *pattern* of missingness to differ.

The sky-dependent mechanism uses a contiguous low-observability region with
weighted sampling rather than simply deleting a fixed sky fraction. This keeps
the 90%, 70%, and 50% experiments feasible.

# Statistical reporting

Primary diagnostics are:

- posterior bias of the chosen point estimator
- RMSE
- posterior width
- empirical 68% and 95% coverage
- Monte-Carlo standard error of coverage
- pull distribution
- hidden-host retention fraction

Coverage should be interpreted together with its Monte-Carlo uncertainty.
For N independent trials and measured coverage p, the binomial standard error
is sqrt[p(1-p)/N].

# Scope

The baseline model is intentionally simplified. It does not yet include a
detector-derived selection normalization, realistic sky-localization
likelihoods, peculiar velocities, redshift measurement errors, or a full
cosmological distance-redshift relation.

Those effects should be introduced only after the baseline controls pass.
