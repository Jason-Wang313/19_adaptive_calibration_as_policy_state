# Reproducibility Checklist

- [x] Python dependencies are listed in `requirements.txt`.
- [x] Formal check source is `experiments/check_formal_claim.py`.
- [x] Simulation source is `experiments/run_calibration_state_sim.py`.
- [x] Paper generator is `scripts/write_paper.py`.
- [x] Main outputs are `results/aggregate_results.csv`, `results/episode_results.csv`, and `results/calibration_state_evidence.md`.
- [x] V2 baseline outputs are `results/windowed_context_baseline.csv` and `results/windowed_context_table.tex`.
- [x] Paper source is `paper/main.tex`.
- [x] Canonical batch PDF path is `C:/Users/wangz/Downloads/19.pdf`.
- [x] `paper/main.pdf` is removed from git tracking after the canonical PDF copy is verified.
- [ ] The long simulation took roughly 15 minutes locally; future runs should expect a multi-minute runtime.

Recommended verification commands:

```powershell
python experiments\check_formal_claim.py
python experiments\run_calibration_state_sim.py
python scripts\write_paper.py
cd paper
pdflatex -interaction=nonstopmode -halt-on-error main.tex
bibtex main
pdflatex -interaction=nonstopmode -halt-on-error main.tex
pdflatex -interaction=nonstopmode -halt-on-error main.tex
```
