# Paper19 VLA Highlight Hardening Plan

Date: 2026-06-20

## Objective

Make `C:/Users/wangz/Downloads/19.pdf` explicitly match the visible VLA-v4
role model's boxed-link behavior while preserving the final 25-page adaptive
calibration-as-policy-state paper:

- citation links use green one-point boxes;
- internal figure/table/section links use red one-point boxes when present;
- URL links use green one-point boxes;
- the final PDF is rebuilt, copied to Downloads, visually checked, and leaves
  no local `paper/main.pdf`.

## Plan-Start Evidence

Baseline artifact:

- Canonical PDF: `C:/Users/wangz/Downloads/19.pdf`
- Pages: 25
- Size: 433,568 bytes
- SHA256: `A315127510349C88F29DDB15C40C0B0E916EB979227D809666210A9E773B4EB4`
- Local `paper/main.pdf`: absent
- Repository state: clean against `origin/master`

Baseline link inventory from the current Downloads PDF:

- Link pages: `[(2, 43), (3, 10)]`
- Annotation colors: green = 53, red = 0, cyan = 0
- Border widths: `(0, 0, 1)` for all 53 link annotations

Source finding:

- `paper/main.tex` is the active manuscript source.
- The preamble loads plain `\usepackage{hyperref}` but does not explicitly
  lock `citebordercolor`, `linkbordercolor`, `urlbordercolor`, or
  `pdfborder`.
- The current PDF has green citation boxes and no cyan, but no red internal
  link annotations appear in the PDF inventory. The target is to make the
  VLA-style behavior explicit and verify the final output from the rebuilt PDF.
- There is no dedicated build script in `scripts/`; use the documented manual
  `pdflatex`, `bibtex`, and repeated `pdflatex` sequence from `paper/`, then
  copy `paper/main.pdf` to Downloads and remove the local PDF.

## Role-Model Target

Install the same explicit hyperref policy as the visible VLA-v4 role model:

```tex
\usepackage{hyperref}
\hypersetup{
  colorlinks=false,
  pdfborder={0 0 1},
  citebordercolor={0 1 0},
  linkbordercolor={1 0 0},
  urlbordercolor={0 1 0}
}
```

## Execution Plan

1. Add the VLA `\hypersetup` block immediately after `\usepackage{hyperref}`
   in `paper/main.tex`.
2. Rebuild manually from `paper/` with `pdflatex`, `bibtex`, and repeated
   `pdflatex` passes.
3. If the log asks for another pass for cross-references, run the final
   canonical pass before recording metadata.
4. Copy the rebuilt `paper/main.pdf` to `C:/Users/wangz/Downloads/19.pdf`.
5. Remove local `paper/main.pdf` after export.
6. Recompute page count, byte size, SHA256, annotation colors, border widths,
   and link pages from the final Downloads PDF.
7. Render every page that contains link annotations into
   `tmp/pdfs/paper19_after`.
8. Visually inspect rendered affected pages:
   - green citation and URL boxes are crisp and aligned;
   - red internal-reference boxes are crisp and aligned if present;
   - no cyan boxes appear;
   - layout, figures, tables, headers, and page count remain stable.
9. Update README/status/audit/version/validation metadata with the new hash and
   VLA-style boxed-link inventory.
10. Validate build logs, JSON metadata, diff hygiene, final PDF hash, and
    absence of local `paper/main.pdf`.
11. Remove Paper19 temp renders, leaving only the shared role-model render
    directory.
12. Stage only Paper19 source and metadata files, commit, push, and verify a
    clean repository before moving to Paper18.

## Non-Goals

- Do not alter experiment results, claims, figures, tables, bibliography
  content, or page count.
- Do not add or remove citations, references, or URLs merely to change link
  counts.
- Do not leave intermediate PDFs or render folders behind.

## Completion Evidence

Final artifact after hardening:

- Canonical PDF: `C:/Users/wangz/Downloads/19.pdf`
- Pages: 25
- Size: 433,568 bytes
- SHA256: `95CCDC986E46AE1EBA511A169CC3450DEFF76D0F214BF214C6AF05C83D9D604E`
- Local `paper/main.pdf`: absent after export

Final link inventory:

- Link pages: `[(2, 43), (3, 10)]`
- Annotation colors: green = 53, red = 0, cyan = 0
- Border widths: `(0, 0, 1)` for all 53 link annotations

Visual check:

- Rendered affected pages 2 and 3 from the final Downloads PDF.
- Spot-checked page 2 at high detail.
- Green citation and URL boxes are crisp and aligned; no cyan boxes are
  visible. No red internal-reference link annotations are present in the final
  PDF inventory.
