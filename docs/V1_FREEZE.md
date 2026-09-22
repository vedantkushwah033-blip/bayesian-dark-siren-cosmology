# Version 1 Research Freeze

## Project
Bayesian Simulation Study of Galaxy-Catalogue Incompleteness and Host-Galaxy Weighting in Dark-Siren H0 Inference

## Freeze point
Commit: a726eae6018c021b79dd2a7fb245a2dd63d6d1c4

## Validated scope
- 15,300 simulations
- 153 experimental conditions
- 100 independent runs per condition
- 3 host-generation models
- 3 inference-weighting models
- 4 completeness levels: 100%, 90%, 70%, 50%
- Complete + 4 incomplete-catalogue mechanisms
- Dedicated 2,000-run posterior coverage calibration
- 3,600-run lightweight GP diagnostic
- Oracle missing-host validation/control
- CI validation passing

## Scientific interpretation
This is a controlled synthetic simulation study, not a real LVK H0 measurement and not a universal prediction of dark-siren bias.

The baseline uses the low-redshift approximation d_L approximately cz/H0. No arbitrary beta(H0) selection correction is introduced without an explicit selection model.

Within this simulation, redshift-dependent missingness produced the clearest mechanism-specific changes. Aggregate RMSE and coverage were comparatively similar between matched and mismatched host-weighting assumptions.

The 2,000-run calibration study showed conservative baseline posterior coverage: 50%, 68%, 80%, 90%, and 95% nominal intervals achieved 87.45%, 94.35%, 97.35%, 99.05%, and 99.85% empirical coverage, respectively.

The lightweight GP diagnostic narrowed intervals but increased mean median bias and reduced 68% coverage. This is a negative diagnostic for the specific implementation, not evidence that Gaussian processes generally fail in cosmology.

## Version 2 boundary
Do not add the following to Version 1 merely for complexity:
- explicit event/survey selection and a consistent beta(H0) treatment
- full cosmological distance-redshift relation
- redshift measurement uncertainty
- peculiar velocities
- clustered galaxy populations
- intensity-based missing-host likelihood

These are future extensions requiring a new validation cycle.

## Reproducibility
The generated full-matrix CSVs and figures are retained as GitHub Actions artifacts rather than committed to the repository. Artifact-level facts are authoritative for the executed matrix.

## Freeze rule
Changes to scientific methodology or headline numerical claims should create a new version rather than silently modifying this Version 1 package.
