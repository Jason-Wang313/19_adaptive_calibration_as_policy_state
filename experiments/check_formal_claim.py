from __future__ import annotations

from pathlib import Path

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
DOCS.mkdir(exist_ok=True)
OUT = DOCS / "formal_claim_check.md"


def main() -> None:
    goal = np.array([1.0, 0.0])
    f_identity = np.eye(2)
    f_rot90 = np.array([[0.0, -1.0], [1.0, 0.0]])

    # A memoryless policy receives the same y and goal under both hidden maps, so it
    # must choose the same u. The best same-u action under a uniform prior solves a
    # two-model least-squares problem.
    stacked = np.vstack([f_identity, f_rot90])
    targets = np.concatenate([goal, goal])
    u_memoryless, *_ = np.linalg.lstsq(stacked, targets, rcond=None)
    err_identity = f_identity @ u_memoryless - goal
    err_rot90 = f_rot90 @ u_memoryless - goal
    expected_sq_error = 0.5 * (float(err_identity @ err_identity) + float(err_rot90 @ err_rot90))

    u_state_identity = np.linalg.solve(f_identity, goal)
    u_state_rot90 = np.linalg.solve(f_rot90, goal)
    state_error = 0.5 * (
        float(np.linalg.norm(f_identity @ u_state_identity - goal) ** 2)
        + float(np.linalg.norm(f_rot90 @ u_state_rot90 - goal) ** 2)
    )

    lines = [
        "# Formal Claim Check",
        "",
        "## Ambiguity Instance",
        "Consider the one-step linear observation dynamics `y_{t+1}=y_t+F_c u_t` with current observation `y_t=0` and goal displacement `g=(1,0)`. The hidden calibration map is either `F_1=I` or a 90-degree rotation `F_2`.",
        "",
        "A policy that sees only `(y_t,g)` must choose the same action under both hidden maps. A calibration-state policy that also sees `c` may choose `F_c^{-1}g`.",
        "",
        "## Numerical Verification",
        f"- Best same-action memoryless command under a uniform prior: `({u_memoryless[0]:.3f}, {u_memoryless[1]:.3f})`.",
        f"- Squared error under `F_1`: {float(err_identity @ err_identity):.3f}.",
        f"- Squared error under `F_2`: {float(err_rot90 @ err_rot90):.3f}.",
        f"- Expected squared error of the best memoryless same-action command: {expected_sq_error:.3f}.",
        f"- Expected squared error with calibration-state action selection: {state_error:.3f}.",
        "",
        "## Adversarial Check",
        "- This does not prove CSC is globally stable.",
        "- This does not prove calibration is observable; it assumes the hidden map is known to the calibration-state policy for the one-step separation.",
        "- The claim is only that omitting calibration state can create an irreducible action ambiguity at the same observation-goal pair.",
        "- The simulation then tests whether an online residual-based estimate can recover enough of that state during longer rollouts.",
    ]
    OUT.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"[formal] wrote {OUT}")


if __name__ == "__main__":
    main()
