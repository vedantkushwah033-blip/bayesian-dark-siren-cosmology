# Professor-Facing Presentation — Dark-Siren Cosmology

## Slide 1 — Title

**Bayesian Simulation Study of Galaxy-Catalogue Incompleteness and Host-Galaxy Weighting in Dark-Siren H₀ Inference**

Vedant Kushwaha  
B.Sc.–M.Sc. Applied Statistics, Delhi Technological University

**Research question:** When the host galaxy is unknown, how do catalogue incompleteness and host-galaxy assumptions affect Bayesian inference of H₀?

---

## Slide 2 — Motivation

- Dark-siren inference uses gravitational-wave luminosity distance together with candidate-galaxy information.
- The true host is not supplied to ordinary inference.
- Real catalogues can be incomplete, and missing galaxies need not be missing randomly.
- This project isolates these effects in a controlled synthetic experiment.

**Important scope:** this is a simulation study, not a real LVK H₀ measurement.

---

## Slide 3 — Simulation design

- **15,300 simulations**
- **153 experimental conditions**
- **100 independent runs per condition**
- Completeness: **100%, 90%, 70%, 50%**
- Missingness: complete, random, faint-galaxy, redshift-dependent, sky-footprint
- Host generation: uniform, luminosity-weighted, mass-proxy-weighted
- Inference weighting: independently varied across the same three models
- Baseline distance relation: **d_L ≈ cz/H₀**

This design separates catalogue incompleteness from host-prior misspecification.

---

## Slide 4 — Main findings

- Random incompleteness produced relatively small changes in the baseline simulation.
- Redshift-dependent missingness produced the clearest mechanism-specific changes.
- Matched and mismatched host-weight assumptions showed similar aggregate RMSE and coverage across incomplete conditions.
- Therefore, the baseline does not support treating simple host-weight mismatch as a universal dominant failure mode.

**Interpretation:** conclusions are conditional on the synthetic population and inference model.

---

## Slide 5 — Statistical validation

A dedicated **2,000-run coverage calibration** was independently reproduced from the repository's calibration script.

| Nominal coverage | Empirical coverage |
|---:|---:|
| 50% | 87.45% |
| 68% | **94.35%** |
| 80% | 97.35% |
| 90% | 99.05% |
| 95% | 99.85% |

**Key point:** the baseline posterior intervals are conservative in this synthetic model.

This calibration prevents treating nominal Bayesian coverage as automatically validated.

---

## Slide 6 — GP diagnostic

A separate **3,600-run** pilot tested lightweight RBF Gaussian-process redshift-density reconstruction.

| Metric | Naive | GP |
|---|---:|---:|
| Mean median bias | 1.593 | 2.903 km/s/Mpc |
| Mean 68% width | 22.482 | 20.501 km/s/Mpc |
| 68% coverage | 95.61% | 92.83% |

The GP produced narrower intervals but higher bias and lower coverage.

**Interpretation:** this is a negative diagnostic for the tested reconstruction/reweighting strategy, not a claim that Gaussian processes generally fail.

---

## Slide 7 — Conclusion and Version 2

### Current conclusion

The simulation framework separates:
1. catalogue completeness,
2. missingness mechanism,
3. host-population assumptions,
4. inference weighting,
5. density reconstruction.

The strongest mechanism-specific effect in the current baseline comes from redshift-dependent missingness.

### Version 2

A substantially more realistic model would add:

- explicit event and survey selection;
- full cosmological distance-redshift relation;
- redshift uncertainty and peculiar velocities;
- clustered/physically motivated galaxy populations;
- an intensity-based missing-host likelihood.

Only after that would more sophisticated density-reconstruction methods be evaluated.

### Repository

https://github.com/vedantkushwah033-blip/bayesian-dark-siren-cosmology
