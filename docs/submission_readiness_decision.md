# Submission Readiness Decision

Decision: v3 synthetic mechanism submission-ready under a narrow claim.

## Why This Is Now Submission-Ready Under The Narrow Claim

- The manuscript is now a 25-page full-scale artifact.
- The v3 runner completed eight experiment families with 1,681 deterministic batch-row summaries and 14,614 episodes.
- The paper includes main comparison, estimator/interface ablations, observability stress, noise/latency/outlier stress, conditioning/fallback, drift recovery, planning/control utility, and negative controls.
- Windowed SysID reaches 1.000 main success, so the claim is calibration as policy state rather than RLS-specific novelty.
- Negative controls are explicit: shuffled state, scalar context, and matrix-not-policy are weaker than structured calibration-state controllers.

## Remaining Limits

- The formal ambiguity check is clean and reproducible.
- Evidence is still simulation-only and locally linear.
- No real robot or high-fidelity visual-servoing task is included.
- No trained recurrent neural policy baseline is included.
- The strongest novelty is the policy-state interface, not a new online calibration algorithm.

## Required Next Work For Main-Track Strength

- Add real robot or photorealistic/higher-fidelity visual-servoing validation.
- Compare against an end-to-end recurrent policy trained across calibration drift.
- Stress observability, excitation, and ill-conditioning explicitly.
- Manually deepen treatment of visual-servoing, online calibration, and system-identification priors.
