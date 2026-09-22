# Research Summary — Dark-Siren Cosmology

**Student:** Vedant Kushwaha  
**Institution:** Delhi Technological University (DTU)  
**Program:** B.Sc.–M.Sc. Applied Statistics  
**Project:** Bayesian Simulation Study of Galaxy-Catalogue Incompleteness and Host-Galaxy Weighting in Dark-Siren H₀ Inference

## Research question

When the host galaxy of a gravitational-wave event is unknown, how do incomplete galaxy catalogues and assumptions about the host-galaxy population affect Bayesian inference of the Hubble constant, H₀?

## What I built

I developed a reproducible simulation framework that:

1. generates complete synthetic galaxy populations;
2. assigns low-redshift distances using d_L ≈ cz/H₀;
3. generates uniform, luminosity-weighted, and mass-proxy-weighted host populations;
4. hides the true host from ordinary inference;
5. injects controlled catalogue incompleteness;
6. performs Bayesian H₀ inference from the available catalogue;
7. repeats the experiment across independent mock universes;
8. measures bias, RMSE, posterior width, coverage, pull, and host retention.

The study compares 100%, 90%, 70%, and 50% catalogue completeness and complete, random, faint-galaxy, redshift-dependent, and sky-dependent missingness.

## Main computational study

The completed matrix contains **15,300 simulations across 153 experimental conditions**, with 100 independent runs per condition.

The study also varies host-generation and inference weighting independently:

- uniform;
- luminosity weighted;
- mass-proxy weighted.

This separates catalogue incompleteness from host-prior misspecification.

## Main findings

The complete-catalogue control is reproducible but not perfectly nominally calibrated, so incomplete cases are interpreted relative to the same baseline rather than against an idealized benchmark.

Random incompleteness alone produced relatively small changes in the baseline simulation. Redshift-dependent missingness produced the clearest mechanism-specific changes.

Across incomplete conditions, matched and mismatched host-weight assumptions showed similar aggregate RMSE and coverage in this baseline model. Therefore, the simulation does not support a claim that simple host-weight mismatch is a universal dominant failure mode.

## Negative GP result

A separate **3,600-run** GP pilot tested lightweight redshift-density reconstruction.

The GP narrowed posterior intervals but did not improve inference:

| Metric | Naive | GP |
|---|---:|---:|
| Mean median bias | 1.593 | 2.903 km/s/Mpc |
| Mean 68% width | 22.482 | 20.501 km/s/Mpc |
| 68% coverage | 95.61% | 92.83% |

The result is reported as a diagnostic/falsification result, not as a successful method. It illustrates that narrower posterior intervals are not automatically better if systematic uncertainty is not recovered.

## Current research direction

The next scientifically motivated extension is to move from the controlled baseline toward:

- a full cosmological distance-redshift relation;
- physically motivated galaxy-host populations;
- realistic redshift and peculiar-velocity uncertainty;
- explicit survey selection;
- an intensity-based missing-host likelihood;
- and only then more sophisticated density-reconstruction methods.

## Scope

This is an undergraduate simulation study, not a reproduction of the full LVK analysis pipeline. The conclusions are conditional on the stated simulation assumptions.

## Reproducibility

The complete source code, tests, experiment workflows, analysis scripts, figures, and methodological documentation are available in the project repository.

**GitHub:** https://github.com/vedantkushwah033-blip/bayesian-dark-siren-cosmology
