# Experiment Rigor Checklist

- [x] Formal ambiguity check: `python experiments/check_formal_claim.py`.
- [x] Main simulation entry point: `python experiments/run_calibration_state_sim.py`.
- [x] Main rollout count: 14,400 rollouts across four drift modes and six controllers.
- [x] V2 hostile baseline: 2,400 Windowed SysID rollouts.
- [x] Baselines include nominal offline, robust low gain, privileged frozen-start calibration, residual bias, Windowed SysID, CSC, and oracle.
- [x] Metrics include success rate, final error, path efficiency, command use, calibration error, and standard error for success.
- [x] Machine-readable outputs: episode CSV, aggregate CSV, Windowed SysID CSV, progress JSON.
- [x] Figures regenerate from the experiment script.
- [ ] Real-robot or high-fidelity visual-servoing validation.
- [ ] Learned recurrent-policy baseline.
- [ ] Explicit observability or excitation stress beyond the current drift modes.

Decision: rigorous enough for workshop-only / strong-revise positioning; not enough for deployment or main-track claims.
