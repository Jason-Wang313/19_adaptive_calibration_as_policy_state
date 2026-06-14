# Hostile Reviewer Response

## Likely Rejection Point

"The paper claims novelty for an online calibration estimator, but online system identification and visual servoing already estimate these maps."

## Response

The v3 manuscript narrows the claim. It does not claim online calibration, RLS, or system identification as novel. The contribution is the policy-state interface: calibration drift is a decision-relevant state variable that should remain inside the action computation when it changes during rollout.

The Windowed SysID baseline is intentionally hostile. In the v3 main suite it reaches 1.000 success, while RLS-based CSC reaches 0.997 success and lower final error. The honest conclusion is that structured calibration state matters more than the specific estimator.

## What The Paper Still Cannot Claim

- Real-robot validation.
- Superiority over trained recurrent neural policies.
- Novelty for online calibration, visual servoing, or system identification.
- Global observability or stability.

## Honest Position

V3 synthetic mechanism submission-ready under the narrow policy-state claim: useful mechanism, formal ambiguity, full-scale simulation, strong baselines, and negative controls. It is still not a real-robot or learned-recurrent-policy dominance claim.
