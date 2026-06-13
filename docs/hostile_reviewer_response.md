# Hostile Reviewer Response

## Likely Rejection Point

"The paper claims novelty for an online calibration estimator, but online system identification and visual servoing already estimate these maps."

## Response

The v2 manuscript narrows the claim. It does not claim online calibration, RLS, or system identification as novel. The contribution is the policy-state interface: calibration drift is a decision-relevant state variable that should remain inside the action computation when it changes during rollout.

The new Windowed SysID baseline is intentionally hostile. It estimates the local action-observation map from the most recent 14 transitions and uses the same inverse-control interface. It recovers much of the benefit, reaching 0.867 success under abrupt bumps and 0.948 under severe random walk. CSC remains stronger in those modes at 0.962 and 0.977, but the honest conclusion is that the state interface matters more than the specific estimator.

## What The Paper Still Cannot Claim

- Real-robot validation.
- Superiority over trained recurrent neural policies.
- Novelty for online calibration, visual servoing, or system identification.
- Global observability or stability.

## Honest Position

Workshop-only / strong-revise: useful mechanism and falsification target, but not main-track without hardware or strong learned-policy comparisons.
