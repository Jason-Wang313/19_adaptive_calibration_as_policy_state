# Adaptive Calibration as Policy State

This repository contains the paper-19 child-agent output for **Adaptive Calibration as Policy State**. The thesis is that calibration drift should be represented as a recurrent policy state rather than treated only as offline preprocessing or generic robustness noise.

## Main Artifacts
- `paper/main.tex`: anonymous ICLR-style manuscript.
- `C:/Users/wangz/Downloads/19.pdf`: canonical compiled paper for the batch.
- `docs/related_work_matrix.csv`: 6,710-paper landscape matrix with 300 serious skims, 225 structured deep reads, and 100 hostile priors.
- `docs/literature_map.md`, `docs/hostile_prior_work.md`, `docs/novelty_boundary_map.md`, `docs/novelty_decision.md`: novelty and literature analysis.
- `results/aggregate_results.csv`, `results/windowed_context_baseline.csv`, `results/calibration_state_evidence.md`: compact v2 simulation evidence summary and hostile baseline.
- `experiments/full_scale_calibration_state.py`: v3 full-scale evidence runner.
- `results/full_scale/`: v3 CSV summaries, generated tables, figures, metadata, and progress audit.
- `docs/final_audit.md`: final readiness audit.

## Reproduce
Install Python dependencies:

```powershell
python -m pip install -r requirements.txt
```

Regenerate literature-derived docs from the cached matrix:

```powershell
python scripts\synthesize_literature.py
```

Run the formal ambiguity check:

```powershell
python experiments\check_formal_claim.py
```

Run the calibration-drift simulation:

```powershell
python experiments\run_calibration_state_sim.py
```

Run the full-scale v3 suite:

```powershell
python experiments\full_scale_calibration_state.py
```

Regenerate the paper source and references:

```powershell
python scripts\write_paper.py
```

Build the paper from `paper/`:

```powershell
pdflatex -interaction=nonstopmode -halt-on-error main.tex
bibtex main
pdflatex -interaction=nonstopmode -halt-on-error main.tex
pdflatex -interaction=nonstopmode -halt-on-error main.tex
```

The local build creates `paper/main.pdf`; the hardened repo removes that build
artifact from git after copying the canonical PDF to Downloads.

## Evidence Scope
The empirical evidence is simulation-only. The v3 full-scale suite contains
1,681 deterministic batch-row summaries and 14,614 simulated episodes across
eight experiment families. CSC reaches 0.997 main success, frozen-start
calibration reaches 0.951, Windowed SysID reaches 1.000, and shuffled
calibration state reaches 0.653 in the negative-control family.

The strongest supported claim is that calibration drift is decision-relevant
policy state when the hidden action-observation map changes during rollout and
remains locally observable. The repo does not claim real-robot validation,
RLS-specific novelty, or dominance over all learned recurrent policies.
