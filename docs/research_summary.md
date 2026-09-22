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

## Statistical calibration

A dedicated **2,000-run posterior-coverage calibration** independently reproduced from the repository's current calibration script found:

- nominal 50% interval → 87.45% empirical coverage;
- nominal 68% interval → **94.35% empirical coverage**;
- nominal 80% interval → 97.35%;
- nominal 90% interval → 99.05%;
- nominal 95% interval → 99.85%.

This shows that the baseline posterior intervals are conservative in the present synthetic model. The result is a calibration diagnostic for this model, not a claim about real dark-siren analyses.

## Main findings

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

## What the project demonstrates

The central result is methodological: catalogue completeness, missingness mechanism, host-population assumptions, and reconstruction choices can be separated into independently testable simulation controls. The current baseline shows that nominal completeness alone does not determine posterior behaviour; how galaxies are missing can matter.

These conclusions are conditional on the simplified simulation assumptions.

## Current research direction

The next scientifically motivated extension is to move from the controlled baseline toward:

- a full cosmological distance-redshift relation;
- physically motivated galaxy-host populations;
- realistic redshift and peculiar-velocity uncertainty;
- explicit survey selection;
- an intensity-based missing-host likelihood;
- and only then more sophisticated density-reconstruction methods.

## Scope

This is an undergraduate simulation study, not a reproduction of the full LVK analysis pipeline or a real H₀ measurement. The conclusions are conditional on the stated simulation assumptions.

## Reproducibility

The complete source code, tests, experiment workflows, analysis scripts, and methodological documentation are available in the project repository. The main numerical outputs are archived as execution artifacts.

**GitHub:** https://github.com/vedantkushwah033-blip/bayesian-dark-siren-cosmology
