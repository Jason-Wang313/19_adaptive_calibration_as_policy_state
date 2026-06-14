# Experiment Rigor Checklist

- [x] Formal ambiguity check: `python experiments/check_formal_claim.py`.
- [x] Main simulation entry point: `python experiments/run_calibration_state_sim.py`.
- [x] Main rollout count: 14,400 rollouts across four drift modes and six controllers.
- [x] V2 hostile baseline: 2,400 Windowed SysID rollouts.
- [x] Baselines include nominal offline, robust low gain, privileged frozen-start calibration, residual bias, Windowed SysID, CSC, and oracle.
- [x] Metrics include success rate, final error, path efficiency, command use, calibration error, and standard error for success.
- [x] Machine-readable outputs: episode CSV, aggregate CSV, Windowed SysID CSV, progress JSON.
- [x] Figures regenerate from the experiment script.
- [x] Full-scale v3 runner: `python experiments/full_scale_calibration_state.py`.
- [x] V3 suite includes eight families: main comparison, estimator/interface ablations, observability/excitation, noise/latency/dropout/outliers, conditioning/fallback, drift-event recovery, planning/control utility, and negative controls.
- [x] V3 generated 1,681 deterministic batch-row summaries and 14,614 simulated episodes.
- [x] V3 generated tables and figures under `results/full_scale/`.
- [x] Strong v3 baselines include Windowed SysID, frozen-start calibration, residual-bias adaptation, negative controls, and oracle calibration.
- [x] V3 reports boundary results: Windowed SysID reaches 1.000 main success, and Family G does not prove planning dominance.
- [ ] Real-robot or high-fidelity visual-servoing validation.
- [ ] Learned recurrent-policy baseline.
- [x] Explicit observability and excitation stress.

Decision: v3 synthetic mechanism submission-ready under a narrow policy-state claim; still not enough for deployment or real-robot claims.
