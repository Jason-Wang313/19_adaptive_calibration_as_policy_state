# Calibration-State Evidence

Episodes per mode/controller: 600. Maximum steps: 80. Success threshold: 0.04.

## Aggregate Results

| Mode | Controller | Success | Mean final error | Path efficiency | Mean calibration error |
| --- | --- | ---: | ---: | ---: | ---: |
| abrupt_bump | calibration_state | 0.962 | 0.0017 | 0.928 | 0.369 |
| abrupt_bump | frozen_start_calibration | 0.538 | 0.1069 | 0.802 | 0.986 |
| abrupt_bump | nominal_offline | 0.478 | 0.1159 | 0.820 | 1.000 |
| abrupt_bump | oracle | 0.967 | 0.0015 | 0.973 | 0.007 |
| abrupt_bump | residual_bias | 0.362 | 0.0864 | 0.772 | 1.000 |
| abrupt_bump | robust_low_gain | 0.145 | 0.2855 | 0.996 | 1.000 |
| random_walk | calibration_state | 0.970 | 0.0020 | 0.967 | 0.144 |
| random_walk | frozen_start_calibration | 0.947 | 0.0028 | 0.962 | 0.242 |
| random_walk | nominal_offline | 0.875 | 0.0084 | 0.942 | 0.370 |
| random_walk | oracle | 0.973 | 0.0020 | 0.974 | 0.026 |
| random_walk | residual_bias | 0.790 | 0.0180 | 0.963 | 0.370 |
| random_walk | robust_low_gain | 0.250 | 0.1825 | 1.000 | 0.370 |
| severe_random_walk | calibration_state | 0.977 | 0.0017 | 0.950 | 0.283 |
| severe_random_walk | frozen_start_calibration | 0.898 | 0.0086 | 0.928 | 0.502 |
| severe_random_walk | nominal_offline | 0.750 | 0.0347 | 0.876 | 0.700 |
| severe_random_walk | oracle | 0.978 | 0.0016 | 0.973 | 0.058 |
| severe_random_walk | residual_bias | 0.648 | 0.0371 | 0.891 | 0.700 |
| severe_random_walk | robust_low_gain | 0.218 | 0.2067 | 0.999 | 0.700 |
| static | calibration_state | 0.970 | 0.0017 | 0.967 | 0.025 |
| static | frozen_start_calibration | 0.973 | 0.0017 | 0.974 | 0.000 |
| static | nominal_offline | 0.922 | 0.0045 | 0.936 | 0.358 |
| static | oracle | 0.973 | 0.0017 | 0.974 | 0.000 |
| static | residual_bias | 0.835 | 0.0161 | 0.962 | 0.358 |
| static | robust_low_gain | 0.240 | 0.1684 | 1.000 | 0.358 |

## CSC Advantage Over Strongest Non-Oracle Baseline

| Mode | Best non-oracle baseline | Baseline success | CSC success | CSC final-error change |
| --- | --- | ---: | ---: | ---: |
| static | frozen_start_calibration | 0.973 | 0.970 | -0.0000 |
| random_walk | frozen_start_calibration | 0.947 | 0.970 | -0.0008 |
| abrupt_bump | frozen_start_calibration | 0.538 | 0.962 | -0.1053 |
| severe_random_walk | frozen_start_calibration | 0.898 | 0.977 | -0.0069 |

## Interpretation
- The frozen-start baseline is intentionally privileged: it knows the initial calibration matrix but cannot update after drift.
- CSC is expected to beat frozen-start most clearly when the calibration map changes during the rollout.
- If CSC fails in a mode, that is evidence that the drift is too fast, poorly conditioned, or insufficiently observable from task residuals.
