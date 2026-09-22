# Final Research Report

## Bayesian Simulation Study of Galaxy-Catalogue Incompleteness and Host-Galaxy Weighting in Dark-Siren H0 Inference

### Abstract

This project studies how incomplete galaxy catalogues and assumptions about the host-galaxy population affect Bayesian inference of the Hubble constant, H0, from dark-siren gravitational-wave events. The study uses controlled synthetic universes so that the injected H0 and the hidden host are known for validation while the inference calculation receives only the information available to the simulated observer.

The baseline model uses the pedagogical low-redshift relation d_L ≈ cz/H0 and a Gaussian luminosity-distance measurement. Catalogue completeness is varied from 100% to 50%, with random, faint-galaxy, redshift-dependent, and sky-dependent missingness. Host galaxies are generated using uniform, luminosity-weighted, or mass-proxy-weighted populations, while the inference weighting can match or deliberately mismatch the generating model.

The completed experiment matrix contains 15,300 runs across 153 conditions. The main result is that simple host-weight mismatch does not create a large universal degradation in this baseline model. Redshift-dependent incompleteness produces the clearest mechanism-specific change, but its effect is conditional on the toy setup. A 3,600-run Gaussian-process pilot was also completed. The current lightweight GP reconstruction narrowed posterior intervals but increased bias and reduced 68% coverage, so it is reported as a negative diagnostic result rather than as a successful correction.

---

## 1. Research question

> When the host galaxy of a gravitational-wave event is unknown, how do incomplete galaxy catalogues and different assumptions about host-galaxy weighting affect Bayesian inference of H0?

The purpose is not to reproduce the full LVK analysis pipeline. It is to isolate catalogue incompleteness and host-prior assumptions in a transparent, reproducible simulation.

---

## 2. Simulation design

The experiment proceeds in the following order:

1. Generate a complete synthetic galaxy population.
2. Assign redshifts using a low-redshift volume-weighted distribution.
3. Compute luminosity distances using d_L ≈ cz/H0.
4. Assign luminosity and mass proxies.
5. Draw a hidden host from a specified host-population model.
6. Generate a noisy gravitational-wave distance measurement.
7. Apply a catalogue-selection mechanism.
8. Perform Bayesian H0 inference using the observed catalogue.
9. Optionally include an uncatalogued-host contribution in the oracle validation model.
10. Repeat across independent mock universes.
11. Measure bias, RMSE, posterior width, coverage, pull statistics, and host retention.

The hidden host is never passed to the inference calculation.

### Experimental factors

**Completeness:** 100%, 90%, 70%, 50%.

**Missingness mechanisms:** complete, random, faint-galaxy, redshift-dependent, sky-dependent.

**Host-generation models:** uniform, luminosity-weighted, mass-proxy-weighted.

**Inference weighting:** uniform, luminosity-weighted, mass-proxy-weighted.

The selection mechanisms enforce the same requested catalogue size at a given completeness level, allowing missingness patterns to be compared at fixed nominal completeness.

---

## 3. Baseline calibration

The 1,000-run complete-catalogue control used H0,true = 70 km/s/Mpc.

| Diagnostic | Result |
|---|---:|
| Median bias | +1.986 km/s/Mpc |
| Mean bias | +1.259 km/s/Mpc |
| Median RMSE | 6.190 km/s/Mpc |
| Mean 68% width | 22.372 km/s/Mpc |
| Mean 95% width | 35.820 km/s/Mpc |
| 68% coverage | 94.4% |
| 95% coverage | 99.9% |
| 68% coverage MC SE | 0.0073 |
| 95% coverage MC SE | 0.0010 |
| Median-pull mean | 0.143 |
| Median-pull SD | 0.670 |

The complete case is therefore reproducible but not perfectly nominally calibrated. The 68% interval is somewhat conservative and the 95% interval is also broader in coverage than its nominal level.

A separate known-host diagnostic gave 68% coverage of 74.9% and mean 68% width of 17.045 km/s/Mpc. This demonstrates that part of the calibration behaviour comes from the simplified distance likelihood/model itself rather than from catalogue incompleteness alone.

The study therefore treats the complete-catalogue control as the reference point rather than forcing artificial calibration.

A dedicated 2,000-run posterior-coverage calibration was subsequently reproduced from the repository calibration script with the same seed sequence and inference implementation. The empirical coverage curve was 87.45% (50% nominal), 94.35% (68%), 97.35% (80%), 99.05% (90%), and 99.85% (95%), with Monte Carlo standard errors of 0.0074, 0.0052, 0.0036, 0.0022, and 0.0009 respectively. The result confirms conservative posterior coverage in this synthetic baseline and strengthens the earlier 1,000-run calibration. It is a calibration diagnostic for this model, not a claim about a realistic dark-siren analysis.

---

## 4. Catalogue incompleteness

A 200-run random-missingness pilot showed little change across 100%, 90%, 70%, and 50% completeness. Median bias remained near +1.7 km/s/Mpc and 68% coverage remained roughly 93–95%.

The larger 15,300-run matrix allowed the missingness mechanism and host-weight assumptions to vary simultaneously.

The clearest mechanism-specific behaviour appeared for redshift-dependent missingness. In the paired missing-host pilot, naive median bias changed from approximately +1.31 km/s/Mpc at 90% completeness to +0.97 at 70% and +0.68 at 50%, while the mean 68% posterior width increased from approximately 22.42 to 22.82 km/s/Mpc.

This does not mean that redshift-dependent incompleteness universally improves or worsens H0 inference. The direction and magnitude arise from the particular simulated redshift distribution, distance uncertainty, catalogue size, and selection rule.

---

## 5. Host-weighting misspecification

The complete-catalogue portion of the 15,300-run matrix showed no large universal penalty from changing the assumed host weighting.

For the 100% complete case, mean bias by generating host model and inference model was:

| True host population | Luminosity inference | Mass inference | Uniform inference |
|---|---:|---:|---:|
| Luminosity | 1.154 | 1.324 | 1.519 |
| Mass | 0.720 | 1.674 | 0.740 |
| Uniform | 1.402 | 1.091 | 1.091 |

Across incomplete conditions, the mean absolute median bias was approximately 1.66 km/s/Mpc for matched host/inference assumptions and 1.74 km/s/Mpc for mismatched assumptions. Mean median-RMSE was approximately 6.16 km/s/Mpc for matched and 6.16 km/s/Mpc for mismatched conditions. Mean 68% coverage was approximately 94.0% for matched and 94.3% for mismatched conditions.

Thus, under the present baseline assumptions, host-weight mismatch is not a dominant universal failure mode. This is a useful negative result rather than evidence that host weighting is irrelevant in realistic analyses.

---

## 6. Missing-host-aware oracle test

The project includes an explicit uncatalogued-host component in a controlled oracle experiment.

The oracle model receives information from the hidden synthetic population that a real incomplete survey would not possess. It therefore should not be described as a realistic survey correction.

Its purpose is narrower: it tests whether explicitly accounting for the missing population can recover information lost by simply conditioning on the observed catalogue.

In the 300-run paired pilot, the oracle model largely reconstructed the complete-population behaviour under the corresponding simplified assumptions. The result is therefore useful as a validation control, not as a deployable inference method.

---

## 7. Gaussian-process extension

### Motivation

The GP extension was designed to test whether structure in the observed redshift distribution could provide a better weighting scheme than uniform catalogue weighting.

The implemented method fits a lightweight RBF Gaussian process to binned log redshift counts and converts the reconstructed density into positive candidate weights. It is explicitly a density-field reconstruction control, not a full Poisson-process GP model or a realistic survey-selection model.

### Experiment

The GP pilot contains 3,600 paired simulations:

- 4 missingness mechanisms
- 3 completeness levels
- 300 paired runs per condition

The same simulated universe is used for the naive and GP comparisons.

### Result

The GP pilot did not improve the baseline inference.

Across all 3,600 paired runs:

| Metric | Naive | GP |
|---|---:|---:|
| Mean median bias | 1.593 | 2.903 km/s/Mpc |
| Mean 68% width | 22.482 | 20.501 km/s/Mpc |
| 68% coverage | 95.61% | 92.83% |

Relative to naive weighting, the GP:

- increased mean median bias by 1.310 km/s/Mpc;
- reduced mean 68% interval width by 1.980 km/s/Mpc;
- reduced 68% coverage by 2.78 percentage points.

At 50% completeness, the increase in GP bias was approximately:

- faint: +1.377 km/s/Mpc
- random: +1.363 km/s/Mpc
- redshift-dependent: +1.064 km/s/Mpc
- sky-dependent: +1.469 km/s/Mpc

The corresponding reductions in 68% width were approximately 1.970, 1.997, 1.458, and 2.034 km/s/Mpc respectively.

### Interpretation

The current GP implementation concentrates probability around reconstructed redshift-density structure. In this simulation, that concentration narrows the posterior without sufficiently reducing systematic error. The result is therefore narrower but less well calibrated.

This is not evidence that Gaussian processes are intrinsically unsuitable for dark-siren cosmology. It is evidence that this particular lightweight reconstruction-and-reweighting strategy does not recover the missing-host information in the present experiment.

The GP extension should therefore be reported as a falsification/diagnostic experiment, not as a successful method.

---

## 8. Main conclusions

The completed simulation supports five conditional conclusions:

1. **The baseline pipeline is reproducible but its posterior intervals are conservative.** The complete-catalogue 68% coverage is about 94.4%, and the dedicated 2,000-run calibration gives 94.35% coverage for nominal 68% intervals. Later effects should therefore be interpreted relative to the same calibrated control rather than against an idealized zero-bias benchmark.

2. **Random incompleteness alone is weak in this toy setup.** Reducing completeness from 100% to 50% did not produce a large change in the random-missingness pilot.

3. **The topology of missingness matters more than nominal completeness alone.** Redshift-dependent missingness produced clearer changes in posterior behaviour than random, faint, or sky selection in the baseline configuration.

4. **Simple host-weight mismatch is not a catastrophic universal effect here.** Matched and mismatched assumptions produced similar aggregate RMSE and coverage across the full matrix.

5. **The current GP reconstruction does not solve the incompleteness problem.** It narrows posteriors but increases bias and reduces coverage, so it should not be presented as a successful correction.

---

## 9. Limitations

The study intentionally omits several effects required for a realistic dark-siren analysis:

- detector-derived selection effects and a consistent selection-function normalization;
- realistic gravitational-wave sky-localization likelihoods;
- peculiar velocities;
- redshift measurement uncertainty;
- galaxy clustering and environmental correlations;
- realistic survey masks and magnitude limits;
- a full cosmological luminosity-distance/redshift relation;
- a full Poisson-process treatment of the galaxy population;
- a physically calibrated galaxy-host relation using realistic stellar mass or star-formation data.

The GP model is also deliberately simplified. A future GP study should use a proper intensity/selection formulation rather than only reweighting observed galaxies from a smoothed one-dimensional redshift density.

No arbitrary beta(H0) selection denominator should be introduced without a consistent event and galaxy selection model.

---

## 10. Future work

A scientifically defensible next extension would be:

1. replace the pedagogical distance relation with a full cosmological d_L(z, H0, Omega_m, ...) relation;
2. introduce a physically motivated galaxy-host population model;
3. add realistic redshift and peculiar-velocity uncertainty;
4. formulate the survey selection function explicitly;
5. build an intensity-based missing-host likelihood;
6. only then revisit GP or other density-reconstruction methods;
7. compare the resulting method against the already validated baseline controls.

The current project should not add complexity merely to obtain a positive result. The negative GP result is itself part of the scientific record of the simulation.

---

## 11. Reproducibility

The repository contains the simulation code, inference model, selection mechanisms, metrics, tests, experiment workflows, and figure-generation pipeline.

The main experimental outputs were generated through GitHub Actions:

- 15,300-run host-weighting/incompleteness matrix;
- 3,600-run paired GP pilot;
- 1,000-run baseline calibration;
- 2,000-run posterior-coverage calibration;
- known-host diagnostic;
- paired missing-host and incompleteness pilots.

All reported numerical results in this report are taken from executed simulation outputs rather than illustrative values.

---

## 12. Final scientific statement

This project does not claim to solve dark-siren cosmology. It demonstrates a controlled way to measure how catalogue incompleteness and host-population assumptions propagate into Bayesian H0 inference.

The strongest outcome is methodological: the simulation separates catalogue missingness, host-prior misspecification, and reconstruction assumptions into independently testable controls. The GP extension provides a useful negative result by showing that narrower posteriors are not automatically better posteriors when systematic uncertainty is not recovered.


## Appendix A — Reproducibility and interpretation checklist

Before presenting the results as scientific conclusions, verify that every reported number comes from an executed artifact and that the complete-catalogue control is shown alongside incomplete cases. The GP result should be presented as a negative diagnostic: narrower intervals are not automatically better when coverage and bias deteriorate.

The principal claims are conditional on the simulation assumptions. In particular, the low-redshift distance relation, simplified distance uncertainty, synthetic host proxies, and catalogue-selection rules are not substitutes for a real LVK galaxy-catalogue and detector-selection model.

The repository's executed artifacts should be treated as the authoritative numerical record. Future extensions should preserve the existing controls so that added realism can be evaluated against the same baseline rather than replacing it.
