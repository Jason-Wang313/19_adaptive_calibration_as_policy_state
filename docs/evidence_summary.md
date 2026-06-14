# Evidence Summary

## V3 Full-Scale Run

- Entry point: `python experiments\full_scale_calibration_state.py`
- Output directory: `results/full_scale/`
- Progress: `stage=complete`, `plot_failures=0`
- Total deterministic batch-row summaries: 1,681
- Total simulated episodes: 14,614
- Family rows: A=224, B=135, C=288, D=344, E=162, F=144, G=240, H=144

## Headline Results

- CSC main success: 0.997
- Frozen-start main success: 0.951
- Windowed SysID main success: 1.000
- Windowed estimator-family success: 0.998
- Low-excitation CSC success: 0.901
- High-noise CSC success: 1.000
- Condition-aware fallback success: 0.979
- CSC recovery-family success: 0.986
- CSC planning-family tail error: 0.3668
- Shuffled calibration-state success: 0.653

## Interpretation

The evidence supports the policy-state interface claim: calibration drift can
be decision-relevant, and structured current calibration state should be exposed
to the policy under drift.

The evidence does not support RLS-specific dominance. Windowed SysID is a strong
calibration-state baseline and reaches 1.000 main success. The final claim is
therefore intentionally narrow: calibration as policy state, not a universal
online-calibration algorithm.
