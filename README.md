# Bayesian Dark-Siren Cosmology

## A controlled simulation study of galaxy-catalogue incompleteness and host-galaxy assumptions

This project asks a practical question in gravitational-wave cosmology:

> **When the galaxy that hosted a gravitational-wave event is not identified, how much can the galaxy catalogue and our assumptions about the host population affect the inferred Hubble constant, H₀?**

The project is deliberately simulation-first. We create a known mock universe, hide the true host from the inference code, introduce controlled catalogue incompleteness, and then ask how well the Bayesian analysis recovers the injected H₀.

The goal is not to claim a new precision cosmology method. The goal is to make the effect of catalogue assumptions measurable, reproducible, and easy to audit.

## Why this matters

A dark siren is a gravitational-wave event whose host galaxy is not uniquely identified. The gravitational-wave signal provides a luminosity-distance measurement, while possible host galaxies provide redshift information. The inference therefore depends on a population of candidate galaxies rather than one known host.

That makes catalogue construction part of the statistical problem.

Two catalogues can contain the same fraction of the underlying galaxies and still behave differently if the missing galaxies are preferentially faint, distant, or located outside the observed sky footprint. Host-galaxy weighting can introduce another layer of model dependence.

This study keeps those effects separate.

## Research design

The simulation proceeds in this order:

1. Generate a complete synthetic galaxy population.
2. Assign each galaxy a redshift and distance using the low-redshift baseline relation.
3. Assign simple luminosity and mass proxies.
4. Draw a hidden host from a specified host-population model.
5. Generate a noisy gravitational-wave distance measurement.
6. Apply a catalogue-selection mechanism to the same underlying universe.
7. Perform Bayesian H₀ inference using only the observed catalogue.
8. Optionally include an explicit uncatalogued-host component.
9. Repeat the experiment across independent mock universes.
10. Measure bias, RMSE, posterior width, coverage, and pull behaviour.

The hidden host is used only for validation. It is never supplied to the inference calculation.

## Experimental factors

### Catalogue completeness

- 100%
- 90%
- 70%
- 50%

### Missingness mechanisms

- Complete catalogue
- Random missingness
- Faint-galaxy selection
- Redshift-dependent selection
- Sky-footprint selection

### Host-population models

- Uniform
- Luminosity weighted
- Mass-proxy weighted

### Inference assumptions

The host-generation model and inference weighting are allowed to match or deliberately disagree. This lets the study distinguish catalogue incompleteness from host-prior misspecification.

## Baseline cosmology

The first-stage simulation uses

**d_L ≈ c z / H₀**

as a low-redshift approximation.

This is a controlled baseline, not a replacement for the full cosmological distance-redshift relation. More realistic effects will only be introduced after the baseline has been validated.

## Missing-host model

When catalogue galaxies are omitted, the project can include a separate uncatalogued-host likelihood contribution.

Schematically,

**L(H₀) = L_catalogue(H₀) + L_missing(H₀)**

where the missing component is represented in the simulation by the redshift distribution and host-population weight of galaxies absent from the observed catalogue.

This is an **oracle validation model** because the simulation knows the underlying population. It is not being presented as a complete real-survey selection model.

## Validation

Each simulation records:

- posterior mean and median
- 68% credible interval
- 95% credible interval
- posterior width
- H₀ bias
- RMSE
- 68% coverage
- 95% coverage
- Monte-Carlo uncertainty on coverage
- pull
- whether the hidden host was observed

The 100% complete, correctly specified experiment is the calibration control. A dedicated 2,000-run coverage calibration gives empirical coverage of 94.35% for nominal 68% intervals, confirming that the baseline posterior intervals are conservative in this synthetic setup.

## What would count as a meaningful result?

We will not describe a catalogue as simply “good” or “bad”.

Instead, results will be stated conditionally, for example:

> Under the simulated redshift distribution, host population, GW distance uncertainty, and missingness mechanism used here, reducing catalogue completeness changed the recovered H₀ bias and posterior coverage by the measured amounts.

This avoids turning one simulation setup into a universal claim about dark-siren cosmology.

## Current status

The repository contains the mock-universe generator, Bayesian inference model, catalogue-selection mechanisms, repeated-universe experiment framework, validation metrics, regression tests, publication-figure pipeline, and a lightweight GP redshift-density pilot.

The main 15,300-run experiment matrix and the 3,600-run GP pilot have now been executed. The GP pilot produced a negative result: its current redshift-density reweighting narrowed posteriors but increased bias and reduced 68% coverage. The final interpretation therefore treats the GP extension as a diagnostic/falsification experiment rather than a successful correction.

## Current empirical conclusion

Within this controlled low-redshift simulation, catalogue incompleteness and simple host-weighting misspecification do not produce a single universal failure mode. The strongest mechanism-specific changes occur for redshift-dependent missingness, while the full host-weighting matrix shows only modest average differences between matched and mismatched assumptions. The lightweight GP reconstruction does not recover the missing information: across 3,600 paired runs it increases mean median-bias by about 1.31 km/s/Mpc, reduces mean 68% interval width by about 1.98 km/s/Mpc, and lowers 68% coverage by about 2.78 percentage points.

These statements are conditional on the simulation assumptions and should not be interpreted as claims about real LVK catalogues or detector data.

## Reproducibility

The simulation uses explicit random seeds. The raw experiment output is intended to be generated by:

    python run_experiment_matrix.py

The analysis should be run only after the simulation output exists. No numerical result should be inserted into the paper or README unless it comes from an actual executed run.

## Scope and limitations

This is an undergraduate simulation study. It does not claim to reproduce the full LVK analysis pipeline.

Important effects intentionally left for later stages include detailed detector selection, peculiar velocities, redshift measurement uncertainty, realistic sky localization, galaxy clustering, survey-specific selection functions, and full cosmological distance-redshift modelling.

Those omissions are part of the staged design rather than hidden assumptions.
