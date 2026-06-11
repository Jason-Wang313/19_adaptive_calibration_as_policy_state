# Plan

## Mission
Produce a complete, anonymous ICLR-style robotics paper for paper 19, starting from the seed "Adaptive Calibration as Policy State" but allowing the literature to change the thesis. The run must leave a runnable repository, compiled PDF at `C:/Users/wangz/Downloads/19.pdf`, pushed public GitHub repo `19_adaptive_calibration_as_policy_state` or a documented push failure, and a complete final audit.

## Operating Rules
- Keep work inside `C:\Users\wangz\robotics_60_paper_batch\19_adaptive_calibration_as_policy_state` unless writing the required final PDF to Downloads.
- Update `child_status.md` compactly after each major stage with commands, failures, and recovery steps.
- Use safe non-interactive commands with explicit timeouts for long work.
- Reuse any existing artifacts if present; do not delete useful caches.
- Use direct `pdflatex`/`bibtex` with generous timeouts for the final build.
- Keep claims honest; mark unsupported claims instead of overstating.

## Stages
1. Repository reconnaissance and recovery
   - Inspect existing files, git state, tool availability, and any cached artifacts.
   - Create `docs/`, `scripts/`, `paper/`, `experiments/`, and `results/` as needed.

2. Literature landscape
   - Build `docs/related_work_matrix.csv` with at least 1000 robotics/calibration/adaptation/control/world-model entries.
   - Produce a 1000-paper landscape sweep, 300-paper serious skim, 200-250-paper deep-read subset, and 100-paper hostile prior-work set from cached metadata/abstracts and targeted papers.
   - Save `docs/literature_map.md` and `docs/hostile_prior_work.md`.

3. Novelty selection
   - Define the field box and enumerate at least 20 hidden assumptions.
   - Generate candidate paper directions that break assumptions.
   - Select the strongest direction only after hostile prior-work comparison.
   - Save `docs/novelty_boundary_map.md`, `docs/novelty_decision.md`, `docs/claims.md`, and `docs/reviewer_attacks.md`.

4. Evidence
   - Implement runnable evidence for the selected mechanism.
   - Prefer a compact deterministic simulation with cached outputs: calibration drift as latent policy state, online filtering, and control/planning comparisons.
   - Save scripts, results CSV/JSON, and plots.

5. Paper
   - Obtain or use the latest official ICLR LaTeX template available at runtime; document source/fallback.
   - Write a complete anonymous ICLR-style paper with related work, method, formal claims if defensible, experiments, limitations, and reproducibility notes.
   - Sanitize BibTeX and LaTeX text for pdfLaTeX.

6. Build
   - Compile with direct `pdflatex`, `bibtex`, `pdflatex`, `pdflatex`.
   - Copy only the final PDF to `C:/Users/wangz/Downloads/19.pdf`.
   - If build fails, document logs and recovery in `child_status.md` and `docs/final_audit.md`.

7. Publish
   - Commit all repository artifacts.
   - Create public GitHub repo `19_adaptive_calibration_as_policy_state` and push, or document exact failure.

8. Final audit
   - Write `docs/final_audit.md` answering the required 13 audit questions.
   - Include exact PDF path, GitHub URL or failure, and Desktop-copy status as `pending orchestrator copy` unless the orchestrator has appended a result.
