# Final Audit

## 1. Chosen thesis
Calibration drift should be represented as policy state: a robot policy should carry an online estimate of the current action-observation calibration map and condition each control action on that estimate, rather than treating calibration as offline preprocessing or as generic robustness noise.

## 2. Field assumption broken
The broken assumption is that calibration can be estimated outside the policy loop and then held fixed, or safely absorbed by feedback/robustness, during embodied task execution.

## 3. New central mechanism
Calibration-State Control (CSC): a low-dimensional recurrent state estimates the local action-to-observation Jacobian with forgetting, exposes the estimate and its conditioning to the policy, and computes task actions through the current calibration state. The policy interface changes from `pi(observation, goal)` to `pi(observation, goal, calibration_state)`.

## 4. Genuine novelty
Online calibration, hand-eye calibration, uncalibrated visual servoing, system identification, and latent-context adaptation are not claimed as new. The novelty is the policy-state interface claim: calibration is treated as a decision-relevant hidden state that must remain inside the policy input/action computation when drift continues during rollout. The formal ambiguity example shows why this is not merely an implementation detail.

## 5. Closest hostile prior work
Closest hostile classes:
- Data-driven and uncalibrated visual servoing, especially `Data-Driven Model Predictive Control for Uncalibrated Visual Servoing` (2023).
- Calibration-free hand-eye/eye-in-hand coordination, including Su (2003) and adaptive differential visual feedback work.
- Online kinematic calibration and online parameter-estimation/control methods.
- Latent-context and Bayesian robot adaptation methods that infer hidden physical parameters.

These make online estimation and adaptation less novel, but they leave open the narrower policy-interface claim defended here.

## 6. Literature coverage
`docs/related_work_matrix.csv` contains 6,710 entries from a broad OpenAlex sweep. The generated coverage marks 300 serious-skim papers, 225 structured deep-read papers, and 100 hostile priors. Important prior rows include problem claimed, mechanism introduced, hidden assumptions, fixed variables, ignored failure modes, novelty threat, and remaining opening. The sweep is automated from metadata/abstracts and should guide human review, not replace final manual bibliography review.

## 7. Proof/formal-claim status
There is one modest formal claim. In a one-step linear action-observation system, two hidden calibration maps can yield the same observation-goal pair but require different optimal actions. A memoryless policy omitting calibration state must choose the same action and cannot be optimal for both, while a calibration-state policy can. `docs/formal_claim_check.md` verifies the arithmetic: best same-action expected squared error is 0.5, calibration-state expected squared error is 0.0. No global stability, observability, or real-robot theorem is claimed.

## 8. Strongest evidence
The strongest evidence is the reproducible 14,400-rollout 2D hidden-calibration drift simulation plus a 2,400-rollout v2 Windowed SysID baseline. CSC nearly matches oracle calibration under moving drift and beats the privileged frozen-start calibration baseline when calibration changes during the rollout:
- Abrupt bumps: CSC 0.962 success vs. frozen-start 0.538.
- Severe random walk: CSC 0.977 success vs. frozen-start 0.898.
- Random walk: CSC 0.970 success vs. frozen-start 0.947.
- Static: CSC 0.970 success vs. frozen-start 0.973, correctly showing little benefit when a known calibration remains fixed.
- Windowed SysID: 0.867 success under abrupt bumps and 0.948 under severe random walk, showing a strong online system-identification baseline recovers much of the benefit but does not erase CSC in the hardest drift modes.

## 9. Biggest weaknesses
The evidence is simulation-only and uses a local linear calibration abstraction. The estimator is hand-designed RLS rather than a learned recurrent policy. The v2 baseline shows that a different online system-identification estimator can recover much of the same benefit, narrowing the contribution to the calibration-state interface. The paper still does not compare against strong end-to-end recurrent neural policies that may infer an equivalent latent state. The literature sweep is broad and hostile but automated. CSC may fail when calibration is unobservable from task residuals, changes too quickly, or becomes ill-conditioned.

## 10. Paper-readiness judgment
Workshop-only / strong-revise. The mechanism and falsification target are clear enough for a focused workshop paper, and the v2 baseline makes the estimator boundary more honest. A main-conference submission would need real-robot evidence, stronger learned-policy baselines, and deeper manual treatment of the closest visual-servoing and online-calibration priors.

## 11. Exact Downloads PDF path
`C:/Users/wangz/Downloads/19.pdf`

## 12. GitHub URL
`https://github.com/Jason-Wang313/19_adaptive_calibration_as_policy_state`

## 13. Visible Desktop PDF copy status
Absent after v2 hardening cleanup. The canonical PDF is only `C:/Users/wangz/Downloads/19.pdf`.

## Verification summary
- Literature synthesis rerun from the cached 6,710-row matrix.
- Formal ambiguity check rerun.
- Full simulation rerun with 14,400 main rollouts and the 2,400-rollout Windowed SysID baseline.
- Paper regenerated from fresh results.
- Direct `pdflatex`, `bibtex`, `pdflatex`, `pdflatex` build succeeded.
- Final v2 PDF copied to `C:/Users/wangz/Downloads/19.pdf` and is 228,400 bytes.
- PDF text extraction verified the visible `Submission-hardening version: v2` note and Windowed SysID table.
- Tracked `paper/main.pdf` was removed after the canonical Downloads copy was verified.
- Public GitHub repository created and pushed at `https://github.com/Jason-Wang313/19_adaptive_calibration_as_policy_state`.
- Submission-hardening v2 is committed and pushed on `origin/master`.

## Orchestrator Desktop Copy

Checked: 2026-06-11 16:13:28 +01:00
Downloads PDF: C:/Users/wangz/Downloads/19.pdf
Result: copy script exit 0 log C:\Users\wangz\robotics_60_paper_batch\logs\desktop_copy_19_20260611_161327.log
V2 cleanup removed the Desktop copy; it is not canonical.
