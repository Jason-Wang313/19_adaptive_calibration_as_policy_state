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
The strongest evidence is the v3 full-scale synthetic suite:
- Full-scale runner: `python experiments\full_scale_calibration_state.py`.
- Progress audit: `results/full_scale/progress.json` reports `stage=complete`, zero plot failures, 1,681 deterministic batch-row summaries, and 14,614 episodes.
- Main suite: CSC success 0.997, frozen-start calibration success 0.951, Windowed SysID success 1.000, oracle success 1.000.
- Main final error: CSC 0.0020, Windowed SysID 0.0037, oracle 0.0015.
- Estimator/interface ablations: RLS and Windowed SysID variants are strong, while matrix-not-policy, scalar context, and shuffled matrix controls are weaker.
- Negative controls: shuffled state 0.653, scalar context 0.694, matrix-not-policy 0.792, CSC 1.000, oracle 1.000.
- Recovery family: CSC success 0.986 under drift-event stress.

## 9. Biggest weaknesses
The evidence is simulation-only and uses a local linear calibration abstraction. The estimator is hand-designed RLS rather than a learned recurrent policy. The v2 baseline shows that a different online system-identification estimator can recover much of the same benefit, narrowing the contribution to the calibration-state interface. The paper still does not compare against strong end-to-end recurrent neural policies that may infer an equivalent latent state. The literature sweep is broad and hostile but automated. CSC may fail when calibration is unobservable from task residuals, changes too quickly, or becomes ill-conditioned.

## 10. Paper-readiness judgment
V3 synthetic mechanism submission-ready under a narrow calibration-as-policy-state claim. The paper now has a 25-page manuscript, eight experiment families, strong baselines, negative controls, and explicit boundaries. It still does not support deployment-ready robot calibration, real-robot safety, or RLS-specific dominance.

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
- Full-scale v3 simulation completed with 1,681 deterministic batch rows and 14,614 episodes.
- Paper expanded with fresh v3 results.
- Direct `pdflatex`, `bibtex`, `pdflatex`, `pdflatex` build succeeded.
- Final v3 PDF copied to `C:/Users/wangz/Downloads/19.pdf` and is 433,568 bytes.
- Final v3 PDF SHA256 is `95CCDC986E46AE1EBA511A169CC3450DEFF76D0F214BF214C6AF05C83D9D604E`.
- VLA-style link markers: 53 link annotations; pages `[(2, 43), (3, 10)]`; colors green = 53, red = 0, cyan = 0; all borders `(0, 0, 1)`.
- Visual link-page render check: pages 2 and 3 show green citation/URL boxes matching the visible VLA-v4 role model; no cyan boxes appear. No red internal-reference link annotations are present in the final PDF inventory.
- PDF text extraction verified the visible `Submission-hardening version: v3` note, 1,681, 14,614, 0.997, 1.000, 0.653, and final audit text.
- Local `paper/main.pdf` was removed after the canonical Downloads copy was verified.
- Public GitHub repository created and pushed at `https://github.com/Jason-Wang313/19_adaptive_calibration_as_policy_state`.
- Submission-hardening v3 docs, code, results, and manuscript updates are part of the v3 hardening pass.

## Orchestrator Desktop Copy

Checked: 2026-06-11 16:13:28 +01:00
Downloads PDF: C:/Users/wangz/Downloads/19.pdf
Result: copy script exit 0 log C:\Users\wangz\robotics_60_paper_batch\logs\desktop_copy_19_20260611_161327.log
V2 cleanup removed the Desktop copy; it is not canonical.
