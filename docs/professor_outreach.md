# Professor Outreach — Research Email Framework

## Purpose

This document is a starting framework for contacting researchers whose current work directly overlaps with dark-siren cosmology, gravitational-wave cosmology, galaxy catalogues, Bayesian inference, or related statistical methodology.

The email should be customized for each researcher. Do not send a mass-produced generic email.

## Subject

Undergraduate research inquiry — dark-siren cosmology and Bayesian inference

## Email draft

Dear Professor [Surname],

My name is Vedant Kushwaha, and I am a first-year B.Sc.–M.Sc. Applied Statistics student at Delhi Technological University.

I am currently working on a reproducible simulation study of galaxy-catalogue incompleteness and host-galaxy weighting in dark-siren inference of the Hubble constant, H₀.

In the project, I built a Bayesian simulation framework in which the true gravitational-wave host is hidden from the inference model and catalogue incompleteness is introduced through controlled random, faint-galaxy, redshift-dependent, and sky-dependent mechanisms. The completed experiment matrix contains 15,300 simulations across 153 conditions.

I also tested a lightweight Gaussian-process redshift-density reconstruction in a separate 3,600-run experiment. It narrowed posterior intervals but increased bias and reduced coverage, so I have treated that result as a negative diagnostic rather than presenting it as a successful method.

I was particularly interested in your work on [SPECIFIC PAPER / RESEARCH TOPIC]. The connection I see with my current project is [ONE SPECIFIC CONNECTION].

I am now interested in developing the simulation toward a more realistic selection/intensity model for dark-siren inference. If you think this direction overlaps with your group's research, I would be grateful for any advice on how an undergraduate student could develop the work further. If there is an appropriate research opportunity or project for which my background could be relevant, I would also be very interested in learning about it.

Project: https://github.com/vedantkushwah033-blip/bayesian-dark-siren-cosmology

Thank you for your time.

Best regards,  
Vedant Kushwaha  
B.Sc.–M.Sc. Applied Statistics  
Delhi Technological University

## Project snapshot for outreach

Use the following compact factual summary when adapting the email:

- 15,300 simulations across 153 host-weighting/incompleteness conditions.
- 3,600 paired runs for a lightweight GP density-reconstruction diagnostic.
- Baseline nominal 68% posterior coverage: 94.35% in an independent 2,000-run calibration reproduction.
- The GP pilot narrowed intervals but increased mean median bias from 1.593 to 2.903 km/s/Mpc and reduced 68% coverage from 95.61% to 92.83%.
- The project is explicitly a controlled synthetic study, not a real LVK H0 measurement.
- The next proposed extension is an explicit event/galaxy selection and intensity model, followed by realistic redshift, peculiar-velocity, clustering, and cosmological modelling.

Avoid describing the GP result as a failure of Gaussian processes generally. Describe it as a negative result for the specific lightweight reconstruction-and-reweighting implementation used here.

## Personalization rule

Before sending an email:

1. Read the professor's current faculty/research page.
2. Read at least one recent paper relevant to the proposed connection.
3. Mention one specific research topic or paper.
4. Explain the connection in one or two sentences.
5. Ask for advice or a research opportunity rather than demanding a position.
6. Keep the message concise.
