# Submission Attack Log

Updated: 2026-06-13 01:51:37 +01:00

## V2 Attack Rounds

1. **"This is just online system identification."** Added Windowed SysID, a hostile baseline that fits the action-observation map from the most recent 14 transitions and uses the same inverse-control interface.
2. **"Residual bias is too weak a baseline."** The v2 baseline is stronger because it carries an explicit calibration map inside the policy loop.
3. **"The RLS estimator may be the whole contribution."** The v2 results narrow the claim: Windowed SysID reaches 0.867 abrupt-bump success and 0.948 severe-random-walk success, so much of the benefit is shared by online calibration-state estimators.
4. **"CSC still needs evidence beyond toy simulation."** The readiness decision stays workshop-only / strong-revise; real robot or higher-fidelity visual-servoing evidence remains required.
5. **"Learned recurrent policies could infer the same state."** This remains unresolved and is explicitly listed as the next major baseline.

## Terminal Assessment

Recoverable baseline weakness was addressed. Remaining weaknesses require new learned-policy or hardware work outside the current local artifact scope.
