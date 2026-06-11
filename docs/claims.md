# Claims

## Supported By Formal Argument
- Hidden calibration can be decision-relevant: in a linear action-observation system, two hidden calibration maps can produce the same current observation and goal but require different optimal actions.
- A memoryless policy that omits calibration state cannot be simultaneously optimal for both hidden maps at that shared observation-goal pair.

## Supported By Runnable Evidence If Experiments Pass
- In the 2D drift-control testbed, explicit calibration-state control should improve success, final error, and path efficiency over offline calibration, robust low-gain control, and a simple residual-bias adapter.
- The advantage should be largest under abrupt or random-walk drift and smaller under static mild miscalibration.

## Boundary Claims
- CSC helps only when the hidden calibration map is at least locally observable from recent transitions.
- CSC is not a replacement for hand-eye calibration, kinematic calibration, or visual servoing; it changes how their outputs enter the policy loop.
- CSC does not prove that all robot adaptation should be physically factorized, only that calibration drift is a strong case where factorization matters.

## Unsupported Claims To Avoid
- Do not claim real-robot validation.
- Do not claim superiority over all recurrent learned policies.
- Do not claim novelty for online calibration itself.
- Do not claim global observability or stability beyond the simplified setting.
