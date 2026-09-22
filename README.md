# Bayesian Dark-Siren Cosmology

A Bayesian simulation study of galaxy-catalogue incompleteness and host-galaxy weighting in dark-siren H0 inference.

## Research question

When the host galaxy of a gravitational-wave event is unknown, how do incomplete galaxy catalogues and different assumptions about host-galaxy weighting affect Bayesian inference of the Hubble constant H0?

## Current model

The first stage uses a deliberately simplified low-redshift relation:

**d_L approximately equals c z / H0**

The simulation creates a fixed underlying synthetic galaxy universe, chooses a hidden host, generates a noisy gravitational-wave luminosity-distance measurement, and infers H0 from a mixture over candidate host galaxies.

## Experimental design

- Complete catalogue baseline: 100%
- Catalogue completeness: 90%, 70%, 50%
- Planned missingness mechanisms: random, faint-galaxy, redshift-dependent, and sky-region/footprint missingness
- Planned host weighting: uniform, luminosity proxy, and mass proxy
- Planned evaluation: bias, posterior width, RMSE, and 68%/95% coverage over repeated simulations

## Important methodological distinction

The underlying universe is kept fixed when catalogue incompleteness is introduced. We distinguish:

1. **Catalogue-only inference:** omitted galaxies are ignored.
2. **Oracle-complete validation:** omitted galaxies are retained in the likelihood only as a simulation control.
3. **Host-weight mismatch experiments:** the population model used to generate the hidden host can deliberately differ from the weighting model used during inference.

These are separate experiments and will not be conflated.

## Scope

This is a controlled simulation study, not a claim of precision cosmological constraints from current LIGO-Virgo-KAGRA data. The baseline is intentionally simplified; more realistic selection effects and cosmological distance-redshift relations will be added only after baseline validation succeeds.
