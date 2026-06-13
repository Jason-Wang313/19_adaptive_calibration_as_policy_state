# Submission Readiness Decision

Decision: workshop-only / strong-revise.

## Why Not Submit-Ready

- Evidence is simulation-only and locally linear.
- No real robot or high-fidelity visual-servoing task is included.
- No trained recurrent neural policy baseline is included.
- The strongest novelty is the policy-state interface, not a new online calibration algorithm.

## Why Not Kill

- The formal ambiguity check is clean and reproducible.
- CSC beats frozen-start calibration exactly when calibration changes during rollout.
- The v2 Windowed SysID baseline strengthens the paper by showing a serious estimator baseline while preserving a gap under abrupt and severe drift.

## Required Next Work For Main-Track Strength

- Add real robot or photorealistic/higher-fidelity visual-servoing validation.
- Compare against an end-to-end recurrent policy trained across calibration drift.
- Stress observability, excitation, and ill-conditioning explicitly.
- Manually deepen treatment of visual-servoing, online calibration, and system-identification priors.
