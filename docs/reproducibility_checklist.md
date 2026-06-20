# Reproducibility Checklist

- [x] Python dependencies are listed in `requirements.txt`.
- [x] Formal check source is `experiments/check_formal_claim.py`.
- [x] Simulation source is `experiments/run_calibration_state_sim.py`.
- [x] Full-scale v3 source is `experiments/full_scale_calibration_state.py`.
- [x] Paper generator is `scripts/write_paper.py`.
- [x] Main outputs are `results/aggregate_results.csv`, `results/episode_results.csv`, and `results/calibration_state_evidence.md`.
- [x] V2 baseline outputs are `results/windowed_context_baseline.csv` and `results/windowed_context_table.tex`.
- [x] V3 outputs are in `results/full_scale/`.
- [x] V3 `progress.json` reports `stage=complete` and zero plot failures.
- [x] V3 `metadata.json` reports 1,681 seed rows and 14,614 episodes.
- [x] Paper source is `paper/main.tex`.
- [x] Canonical batch PDF path is `C:/Users/wangz/Downloads/19.pdf`.
- [x] Final PDF page count: 25.
- [x] Final PDF bytes: 433,568.
- [x] Final PDF SHA256: `95CCDC986E46AE1EBA511A169CC3450DEFF76D0F214BF214C6AF05C83D9D604E`.
- [x] VLA-style boxed links: 53 annotations; pages `[(2, 43), (3, 10)]`; colors green = 53, red = 0, cyan = 0; all borders `(0, 0, 1)`.
- [x] `paper/main.pdf` is removed from git tracking after the canonical PDF copy is verified.
- [ ] The long simulation took roughly 15 minutes locally; future runs should expect a multi-minute runtime.

Recommended verification commands:

```powershell
python experiments\check_formal_claim.py
python experiments\run_calibration_state_sim.py
python experiments\full_scale_calibration_state.py
python scripts\write_paper.py
cd paper
pdflatex -interaction=nonstopmode -halt-on-error main.tex
bibtex main
pdflatex -interaction=nonstopmode -halt-on-error main.tex
pdflatex -interaction=nonstopmode -halt-on-error main.tex
pdftotext main.pdf - | rg "Submission-hardening version: v3|1,681|14,614|0\.997|1\.000|0\.653|Artifact-To-Claim"
```
