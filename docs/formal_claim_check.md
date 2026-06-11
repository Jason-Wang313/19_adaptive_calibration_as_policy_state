# Formal Claim Check

## Ambiguity Instance
Consider the one-step linear observation dynamics `y_{t+1}=y_t+F_c u_t` with current observation `y_t=0` and goal displacement `g=(1,0)`. The hidden calibration map is either `F_1=I` or a 90-degree rotation `F_2`.

A policy that sees only `(y_t,g)` must choose the same action under both hidden maps. A calibration-state policy that also sees `c` may choose `F_c^{-1}g`.

## Numerical Verification
- Best same-action memoryless command under a uniform prior: `(0.500, -0.500)`.
- Squared error under `F_1`: 0.500.
- Squared error under `F_2`: 0.500.
- Expected squared error of the best memoryless same-action command: 0.500.
- Expected squared error with calibration-state action selection: 0.000.

## Adversarial Check
- This does not prove CSC is globally stable.
- This does not prove calibration is observable; it assumes the hidden map is known to the calibration-state policy for the one-step separation.
- The claim is only that omitting calibration state can create an irreducible action ambiguity at the same observation-goal pair.
- The simulation then tests whether an online residual-based estimate can recover enough of that state during longer rollouts.
