# Adaptive Calibration as Policy State

This repository contains the paper-19 child-agent output for **Adaptive Calibration as Policy State**. The thesis is that calibration drift should be represented as a recurrent policy state rather than treated only as offline preprocessing or generic robustness noise.

## Main Artifacts
- `paper/main.tex`: anonymous ICLR-style manuscript.
- `paper/main.pdf`: compiled paper.
- `docs/related_work_matrix.csv`: 6,710-paper landscape matrix with 300 serious skims, 225 structured deep reads, and 100 hostile priors.
- `docs/literature_map.md`, `docs/hostile_prior_work.md`, `docs/novelty_boundary_map.md`, `docs/novelty_decision.md`: novelty and literature analysis.
- `results/aggregate_results.csv`, `results/calibration_state_evidence.md`: simulation evidence summary.
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

## Evidence Scope
The empirical evidence is simulation-only: a deterministic 2D hidden calibration drift testbed with 14,400 rollouts. The strongest supported claim is that explicit calibration state helps when the hidden action-observation map changes during a rollout and remains locally observable from recent residuals. The repo does not claim real-robot validation or dominance over all learned recurrent policies.
