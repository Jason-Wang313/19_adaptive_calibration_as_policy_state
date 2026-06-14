# Child Status

## Current Stage
Submission hardening v3 complete.

## Latest Actions
- Added `README.md` and `requirements.txt`.
- Wrote `docs/final_audit.md`.
- Committed repository contents.
- Created public GitHub repo `Jason-Wang313/19_adaptive_calibration_as_policy_state`.
- Pushed local `master` to `origin/master`.
- Patched final audit/status to record push success.
- Added and reran the v2 Windowed SysID hostile baseline.
- Regenerated the paper source and rebuilt the PDF.
- Copied the v2 PDF to `C:\Users\wangz\Downloads\19.pdf`.
- Removed tracked `paper/main.pdf`.
- Added `docs/full_scale_execution_plan.md`.
- Added and ran `experiments/full_scale_calibration_state.py`.
- Generated `results/full_scale/` with eight v3 experiment families, 1,681 deterministic batch-row summaries, 14,614 episodes, generated tables, figures, metadata, and progress audit.
- Expanded `paper/main.tex` into a 25-page v3 manuscript.
- Copied final v3 PDF to `C:\Users\wangz\Downloads\19.pdf`.
- Final v3 PDF is 25 pages and 433568 bytes.
- Final v3 PDF SHA256 is `A315127510349C88F29DDB15C40C0B0E916EB979227D809666210A9E773B4EB4`.

## Commands Run
- `git add -A; ... git commit -m "Add adaptive calibration policy-state paper"; ...; exit 0`
- `git remote -v; exit 0`
- `gh repo view Jason-Wang313/19_adaptive_calibration_as_policy_state --json nameWithOwner,url,visibility; ...; exit 0`
- `gh repo create 19_adaptive_calibration_as_policy_state --public --source=. --remote=origin --push; ...; exit 0`
- `apply_patch` updated `docs/final_audit.md` and rewrote `child_status.md`.
- `python experiments\run_calibration_state_sim.py`
- `python scripts\write_paper.py`
- `python experiments\full_scale_calibration_state.py`

## Build Commands Completed
- `python scripts\synthesize_literature.py ...; exit 0`
- `python experiments\check_formal_claim.py ...; exit 0`
- `python experiments\run_calibration_state_sim.py ...; exit 0`
- `python scripts\write_paper.py ...; exit 0`
- Direct `pdflatex` / `bibtex` / `pdflatex` / `pdflatex`, all exit 0.
- Copied `paper\main.pdf` to `C:\Users\wangz\Downloads\19.pdf`; final v3 PDF is 433568 bytes.
- `pdftotext C:\Users\wangz\Downloads\19.pdf - | rg "Submission-hardening version: v3|1,681|14,614|0\.997|1\.000|0\.653|Final Audit"`
- `Get-FileHash C:\Users\wangz\Downloads\19.pdf -Algorithm SHA256`

## Failures
- `gh repo view Jason-Wang313/19_adaptive_calibration_as_policy_state` initially failed because the repo did not exist yet.

## Recovery Steps
- Created the missing public repo with `gh repo create ... --public --source=. --remote=origin --push`.
- Reused cached literature collection because it exceeds required coverage and avoids unnecessary recollection.

Exit code: 0
End time: 2026-06-11 16:13:27 +01:00
PDF exists: True
Desktop copy exists: False
