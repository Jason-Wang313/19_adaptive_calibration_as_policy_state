# Submission Version Log

## v3 - 2026-06-14

- Added `docs/full_scale_execution_plan.md` before substantive v3 edits.
- Added `experiments/full_scale_calibration_state.py`.
- Generated `results/full_scale/` with eight experiment families, 1,681 deterministic batch-row summaries, 14,614 episodes, generated tables, figures, metadata, and progress audit.
- Expanded `paper/main.tex` into a 25-page v3 manuscript with full-scale experiments, estimator/interface ablations, observability/noise/conditioning/recovery/planning/negative-control analysis, and extended appendices.
- Framed Windowed SysID as a strong calibration-state baseline, narrowing the claim to the policy-state interface.
- Exported final v3 PDF to `C:/Users/wangz/Downloads/19.pdf`; verified 25 pages, 433,568 bytes, SHA256 `A315127510349C88F29DDB15C40C0B0E916EB979227D809666210A9E773B4EB4`.

## v2 - 2026-06-13

- Added a hostile Windowed SysID baseline to `experiments/run_calibration_state_sim.py`.
- Reran the full 14,400-rollout main simulation and added 2,400 Windowed SysID rollouts.
- Generated `results/windowed_context_baseline.csv` and `results/windowed_context_table.tex`.
- Regenerated the manuscript from `scripts/write_paper.py` with visible v2 metadata and the new baseline table.
- Updated claims, reviewer responses, audit notes, and reproducibility documentation.

## v1 - 2026-06-11

- Original generated paper with formal ambiguity check, 14,400-rollout calibration-state simulation, ICLR-style manuscript, and public GitHub repository.
