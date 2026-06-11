# Novelty Decision

## Decision
Proceed with **Calibration-State Control (CSC)**.

## Chosen Thesis
Calibration drift should be represented as policy state: a robot policy should carry an online estimate of the current action-observation calibration map and condition each control action on that estimate, instead of treating calibration as offline preprocessing or as generic robustness noise.

## New Central Mechanism
Calibration-State Control (CSC): a low-dimensional recurrent state estimates the local action-to-observation Jacobian with forgetting, exposes that estimate and its conditioning to the policy, and computes task actions through the current calibration state. The policy interface changes from pi(observation, goal) to pi(observation, goal, calibration_state).

## Why Not The Weaker Alternatives
- Bigger model: the contribution is a changed state variable and control interface, not model capacity.
- Better data: the testbed uses the same rollouts for all methods; the difference is whether calibration is represented.
- New benchmark only: the simulation is evidence for a mechanism, not the contribution by itself.
- Add uncertainty: uncertainty is not the core; the core is a calibration-state channel that changes the action map.
- Add active learning: no separate information-gathering policy is claimed.
- Add verifier: no post-hoc checker is used.
- Combine modules: the estimator/controller coupling is defined around one physical hidden state, not a loose pipeline.
- LLM planner/RL: neither is used.

## Minimum Defensible Claim
For control systems where observation changes are governed by a hidden, slowly drifting action-observation calibration map, a policy that receives only current observation and goal is missing a decision-relevant state variable. An explicit calibration-state interface can reduce final error and path inefficiency when the map is observable from recent action-observation residuals.

## Unsupported Or Future Claims
- No claim yet that CSC outperforms end-to-end recurrent neural policies on real robots.
- No claim yet that the estimator is globally identifiable under arbitrary robot tasks.
- No claim yet that calibration state is sufficient for all sim-to-real mismatch.
