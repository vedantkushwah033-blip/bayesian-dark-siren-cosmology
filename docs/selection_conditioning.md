# Selection conditioning in the baseline model

The baseline experiment is a conditional, single-event simulation. It conditions on the existence of the simulated gravitational-wave event and does not model the H0-dependent probability that an event is detected by a gravitational-wave search.

Therefore, the baseline posterior is **not** a detector-selection-complete population likelihood and is not intended to produce a real LVK cosmological measurement.

A beta(H0)-type selection normalization is intentionally deferred. Introducing such a factor without a consistent model for gravitational-wave detection, source population, galaxy-survey selection, and the corresponding observed-data likelihood would add an arbitrary correction rather than improve the model.

A future selection-aware version should introduce the event-detection model and galaxy-survey selection jointly, then evaluate the corresponding normalization consistently across the H0 grid.

This conditioning choice is part of the stated scope of Version 1, not an omitted hidden assumption.
