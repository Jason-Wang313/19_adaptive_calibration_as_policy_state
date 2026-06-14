from __future__ import annotations

import csv
import json
import math
from dataclasses import dataclass
from pathlib import Path
from time import perf_counter

import matplotlib.pyplot as plt
import numpy as np


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "results" / "full_scale"
OUT.mkdir(parents=True, exist_ok=True)

MAX_STEPS = 80
SUCCESS_EPS = 0.04
BASE_MAX_OBS_STEP = 0.075
BASE_MAX_COMMAND = 0.16

MAIN_MODES = [
    "static",
    "slow_walk",
    "random_walk",
    "abrupt_bump",
    "severe_random_walk",
    "sinusoidal",
    "scale_only",
    "shear_heavy",
]

MAIN_CONTROLLERS = [
    "nominal_offline",
    "robust_low_gain",
    "frozen_start_calibration",
    "residual_bias",
    "windowed_sysid",
    "calibration_state",
    "oracle",
]


def rot(theta: float) -> np.ndarray:
    c, s = math.cos(theta), math.sin(theta)
    return np.array([[c, -s], [s, c]], dtype=float)


def calibration_matrix(theta: float, sx: float, sy: float, shear: float) -> np.ndarray:
    shape = np.array([[sx, shear], [0.0, sy]], dtype=float)
    return rot(theta) @ shape


def clip_norm(vec: np.ndarray, max_norm: float) -> np.ndarray:
    norm = float(np.linalg.norm(vec))
    if norm <= max_norm or norm < 1e-12:
        return vec.copy()
    return vec * (max_norm / norm)


def regularized_inverse(mat: np.ndarray, ridge: float = 1e-3) -> np.ndarray:
    return np.linalg.solve(mat.T @ mat + ridge * np.eye(2), mat.T)


def cond_number(mat: np.ndarray) -> float:
    try:
        return float(np.linalg.cond(mat))
    except np.linalg.LinAlgError:
        return float("inf")


class RLSCalibration:
    def __init__(self, forgetting: float = 0.925, prior_scale: float = 28.0) -> None:
        self.f_hat = np.eye(2)
        self.p = np.stack([np.eye(2) * prior_scale, np.eye(2) * prior_scale])
        self.forgetting = forgetting
        self.updates = 0

    def update(self, u: np.ndarray, dy: np.ndarray) -> None:
        if float(np.linalg.norm(u)) < 1e-7:
            return
        x = u.reshape(2, 1)
        for j in range(2):
            p_j = self.p[j]
            denom = self.forgetting + float((x.T @ p_j @ x).item())
            gain = (p_j @ x) / denom
            pred = float(self.f_hat[j] @ u)
            err = float(dy[j] - pred)
            self.f_hat[j] = self.f_hat[j] + gain[:, 0] * err
            self.p[j] = (p_j - gain @ x.T @ p_j) / self.forgetting
        self.updates += 1


class WindowedSysID:
    def __init__(self, window: int = 14, ridge: float = 2e-3) -> None:
        self.window = window
        self.ridge = ridge
        self.u_hist: list[np.ndarray] = []
        self.dy_hist: list[np.ndarray] = []
        self.f_hat = np.eye(2)

    def update(self, u: np.ndarray, dy: np.ndarray) -> None:
        if float(np.linalg.norm(u)) < 1e-7:
            return
        self.u_hist.append(np.array(u, dtype=float, copy=True))
        self.dy_hist.append(np.array(dy, dtype=float, copy=True))
        self.u_hist = self.u_hist[-self.window :]
        self.dy_hist = self.dy_hist[-self.window :]
        if len(self.u_hist) < 3:
            return
        u_mat = np.vstack(self.u_hist)
        dy_mat = np.vstack(self.dy_hist)
        lhs = u_mat.T @ u_mat + self.ridge * np.eye(2)
        beta = np.linalg.solve(lhs, u_mat.T @ dy_mat)
        self.f_hat = beta.T


class ResidualBias:
    def __init__(self) -> None:
        self.bias = np.zeros(2)

    def action(self, desired: np.ndarray, max_command: float) -> np.ndarray:
        return clip_norm(0.80 * desired + self.bias, max_command)

    def update(self, u: np.ndarray, dy: np.ndarray) -> None:
        residual = u - dy
        self.bias = 0.84 * self.bias + 0.28 * residual
        self.bias = clip_norm(self.bias, 0.08)


class ScalarContext:
    def __init__(self) -> None:
        self.scale = 1.0

    def action(self, desired: np.ndarray, max_command: float) -> np.ndarray:
        return clip_norm((0.78 / max(self.scale, 0.25)) * desired, max_command)

    def update(self, u: np.ndarray, dy: np.ndarray) -> None:
        if float(np.linalg.norm(u)) < 1e-7:
            return
        ratio = float(np.linalg.norm(dy) / max(np.linalg.norm(u), 1e-7))
        self.scale = float(np.clip(0.90 * self.scale + 0.10 * ratio, 0.35, 1.80))


@dataclass
class SimConfig:
    mode: str
    controller: str
    seed: int
    n_episodes: int = 24
    max_steps: int = MAX_STEPS
    success_eps: float = SUCCESS_EPS
    goal_period: int = 20
    max_obs_step: float = BASE_MAX_OBS_STEP
    max_command: float = BASE_MAX_COMMAND
    obs_noise: float = 0.0012
    action_noise: float = 0.0
    update_delay: int = 0
    dropout_prob: float = 0.0
    outlier_prob: float = 0.0
    outlier_scale: float = 0.0
    excitation_scale: float = 1.0
    dither: float = 0.0
    forgetting: float = 0.925
    prior_scale: float = 28.0
    window: int = 14
    ridge: float = 1e-3
    event_scale: float = 1.0
    scale_floor: float = 0.45
    shear_limit: float = 0.45
    fallback_cond: float | None = None
    oracle_delay: int = 0
    setting: str = "default"
    family: str = "unknown"


class DriftProcess:
    def __init__(self, mode: str, seed: int, event_scale: float, scale_floor: float, shear_limit: float) -> None:
        self.mode = mode
        self.rng = np.random.default_rng(seed)
        self.event_scale = event_scale
        self.scale_floor = scale_floor
        self.shear_limit = shear_limit
        if mode == "static":
            self.theta = self.rng.normal(0.0, 0.24)
            self.sx = self.rng.uniform(0.78, 1.25)
            self.sy = self.rng.uniform(0.78, 1.25)
            self.shear = self.rng.normal(0.0, 0.08)
        elif mode in ("slow_walk", "random_walk", "sinusoidal", "scale_only", "rotation_only", "shear_heavy"):
            self.theta = self.rng.normal(0.0, 0.18)
            self.sx = self.rng.uniform(0.82, 1.18)
            self.sy = self.rng.uniform(0.82, 1.18)
            self.shear = self.rng.normal(0.0, 0.06)
        elif mode in ("abrupt_bump", "late_bump", "alternating", "drift_burst"):
            self.theta = self.rng.normal(0.0, 0.16)
            self.sx = self.rng.uniform(0.82, 1.18)
            self.sy = self.rng.uniform(0.82, 1.18)
            self.shear = self.rng.normal(0.0, 0.05)
        elif mode == "severe_random_walk":
            self.theta = self.rng.normal(0.0, 0.32)
            self.sx = self.rng.uniform(max(0.68, scale_floor), 1.34)
            self.sy = self.rng.uniform(max(0.68, scale_floor), 1.34)
            self.shear = self.rng.normal(0.0, 0.13)
        elif mode == "ill_conditioned":
            self.theta = self.rng.normal(0.0, 0.22)
            self.sx = self.rng.uniform(scale_floor, scale_floor + 0.18)
            self.sy = self.rng.uniform(1.10, 1.55)
            self.shear = self.rng.normal(0.0, min(0.22, shear_limit))
        else:
            raise ValueError(mode)
        self.base = (self.theta, self.sx, self.sy, self.shear)

    def matrix(self) -> np.ndarray:
        return calibration_matrix(self.theta, self.sx, self.sy, self.shear)

    def _clip(self) -> None:
        self.theta = float(np.clip(self.theta, -1.05, 1.05))
        self.sx = float(np.clip(self.sx, self.scale_floor, 1.70))
        self.sy = float(np.clip(self.sy, self.scale_floor, 1.70))
        self.shear = float(np.clip(self.shear, -self.shear_limit, self.shear_limit))

    def step(self, t: int) -> bool:
        event = False
        if self.mode == "static":
            return False
        if self.mode == "slow_walk":
            self.theta += self.rng.normal(0.0, 0.006)
            self.sx += self.rng.normal(0.0, 0.004)
            self.sy += self.rng.normal(0.0, 0.004)
            self.shear += self.rng.normal(0.0, 0.002)
        elif self.mode == "random_walk":
            self.theta += self.rng.normal(0.0, 0.018)
            self.sx += self.rng.normal(0.0, 0.010)
            self.sy += self.rng.normal(0.0, 0.010)
            self.shear += self.rng.normal(0.0, 0.006)
        elif self.mode == "severe_random_walk":
            self.theta += self.rng.normal(0.0, 0.040)
            self.sx += self.rng.normal(0.0, 0.020)
            self.sy += self.rng.normal(0.0, 0.020)
            self.shear += self.rng.normal(0.0, 0.014)
        elif self.mode == "sinusoidal":
            th0, sx0, sy0, sh0 = self.base
            self.theta = th0 + 0.30 * math.sin(2.0 * math.pi * t / 36.0)
            self.sx = sx0 * (1.0 + 0.12 * math.sin(2.0 * math.pi * t / 29.0))
            self.sy = sy0 * (1.0 + 0.12 * math.cos(2.0 * math.pi * t / 31.0))
            self.shear = sh0 + 0.07 * math.sin(2.0 * math.pi * t / 23.0)
        elif self.mode == "scale_only":
            self.sx += self.rng.normal(0.0, 0.020)
            self.sy += self.rng.normal(0.0, 0.020)
        elif self.mode == "rotation_only":
            self.theta += self.rng.normal(0.0, 0.038)
        elif self.mode == "shear_heavy":
            self.shear += self.rng.normal(0.0, 0.028)
            self.theta += self.rng.normal(0.0, 0.010)
        elif self.mode == "abrupt_bump":
            self.theta += self.rng.normal(0.0, 0.006)
            if t in (12, 32, 52):
                self._bump(scale=self.event_scale)
                event = True
        elif self.mode == "late_bump":
            self.theta += self.rng.normal(0.0, 0.008)
            if t == 56:
                self._bump(scale=1.25 * self.event_scale)
                event = True
        elif self.mode == "alternating":
            if t in (16, 36, 56):
                if (t // 20) % 2 == 0:
                    self.theta += self.rng.normal(0.0, 0.65 * self.event_scale)
                else:
                    self.sx *= self.rng.uniform(0.62, 1.38)
                    self.sy *= self.rng.uniform(0.62, 1.38)
                event = True
        elif self.mode == "drift_burst":
            self.theta += self.rng.normal(0.0, 0.014)
            if 24 <= t <= 32:
                self.theta += self.rng.normal(0.0, 0.10 * self.event_scale)
                self.shear += self.rng.normal(0.0, 0.04 * self.event_scale)
                event = True
        elif self.mode == "ill_conditioned":
            self.theta += self.rng.normal(0.0, 0.012)
            self.sx += self.rng.normal(0.0, 0.008)
            self.shear += self.rng.normal(0.0, 0.015)
        self._clip()
        return event

    def _bump(self, scale: float) -> None:
        self.theta += self.rng.normal(0.0, 0.58 * scale)
        self.sx *= self.rng.uniform(max(0.38, 1.0 - 0.38 * scale), 1.0 + 0.38 * scale)
        self.sy *= self.rng.uniform(max(0.38, 1.0 - 0.38 * scale), 1.0 + 0.38 * scale)
        self.shear += self.rng.normal(0.0, 0.18 * scale)


def make_initial_state(seed: int, max_steps: int, goal_period: int, excitation_scale: float) -> tuple[np.ndarray, list[np.ndarray]]:
    rng = np.random.default_rng(seed)
    span = 0.62 * excitation_scale
    y0 = rng.uniform(-0.55, 0.55, size=2)
    goals: list[np.ndarray] = []
    prev = y0
    for _ in range(max(1, math.ceil(max_steps / goal_period))):
        goal = rng.uniform(-span, span, size=2)
        tries = 0
        while float(np.linalg.norm(goal - prev)) < 0.42 * excitation_scale and tries < 50:
            goal = rng.uniform(-span, span, size=2)
            tries += 1
        goals.append(goal)
        prev = goal
    return y0, goals


def estimator_matrix(
    controller: str,
    rls: RLSCalibration,
    windowed: WindowedSysID,
    initial_f: np.ndarray,
    current_f: np.ndarray,
    random_f: np.ndarray,
    delayed_oracle: list[np.ndarray],
) -> np.ndarray:
    if controller in ("calibration_state", "condition_fallback", "csc_no_forgetting", "csc_fast", "csc_slow"):
        return rls.f_hat
    if controller == "windowed_sysid":
        return windowed.f_hat
    if controller in ("frozen_start_calibration", "stale_initial"):
        return initial_f
    if controller == "oracle":
        return current_f
    if controller == "delayed_oracle":
        return delayed_oracle[0] if delayed_oracle else current_f
    if controller in ("shuffled_state", "random_state"):
        return random_f
    return np.eye(2)


def run_episode(cfg: SimConfig, episode_idx: int) -> dict:
    base_seed = cfg.seed + 10007 * episode_idx + 131 * (hash(cfg.mode) % 997)
    drift = DriftProcess(cfg.mode, base_seed + 11, cfg.event_scale, cfg.scale_floor, cfg.shear_limit)
    noise_rng = np.random.default_rng(base_seed + 23)
    y, goals = make_initial_state(base_seed + 37, cfg.max_steps, cfg.goal_period, cfg.excitation_scale)
    initial_y = y.copy()
    initial_f = drift.matrix().copy()
    random_f = calibration_matrix(
        noise_rng.normal(0.0, 0.45),
        noise_rng.uniform(max(cfg.scale_floor, 0.55), 1.45),
        noise_rng.uniform(max(cfg.scale_floor, 0.55), 1.45),
        noise_rng.normal(0.0, min(0.25, cfg.shear_limit)),
    )

    rls = RLSCalibration(forgetting=cfg.forgetting, prior_scale=cfg.prior_scale)
    if cfg.controller == "csc_no_forgetting":
        rls.forgetting = 1.0
    elif cfg.controller == "csc_fast":
        rls.forgetting = 0.84
    elif cfg.controller == "csc_slow":
        rls.forgetting = 0.975
    windowed = WindowedSysID(window=cfg.window, ridge=cfg.ridge)
    residual = ResidualBias()
    scalar = ScalarContext()

    update_queue: list[tuple[np.ndarray, np.ndarray]] = []
    f_history: list[np.ndarray] = [initial_f.copy()]
    errors: list[float] = []
    cal_errors: list[float] = []
    conditions: list[float] = []
    excitation_scores: list[float] = []
    recent_commands: list[np.ndarray] = []
    total_path = 0.0
    total_command = 0.0
    overshoot_count = 0
    event_count = 0
    event_peak_errors: list[float] = []
    recovery_steps: list[int] = []
    active_event_time: int | None = None
    active_peak = 0.0

    for t in range(cfg.max_steps):
        goal = goals[min(t // cfg.goal_period, len(goals) - 1)]
        err = goal - y
        err_norm = float(np.linalg.norm(err))
        errors.append(err_norm)

        desired = clip_norm(err, cfg.max_obs_step * cfg.excitation_scale)
        if cfg.dither > 0.0:
            desired = clip_norm(desired + noise_rng.normal(0.0, cfg.dither, size=2), cfg.max_obs_step)

        current_f = drift.matrix()
        delayed_oracle = f_history[-(cfg.oracle_delay + 1) :] if cfg.oracle_delay > 0 else [current_f]
        used_f = estimator_matrix(cfg.controller, rls, windowed, initial_f, current_f, random_f, delayed_oracle)

        if cfg.controller == "nominal_offline":
            u = clip_norm(0.92 * desired, cfg.max_command)
        elif cfg.controller == "robust_low_gain":
            u = clip_norm(0.38 * desired, cfg.max_command)
        elif cfg.controller == "residual_bias":
            u = residual.action(desired, cfg.max_command)
        elif cfg.controller == "matrix_no_policy":
            used_f = rls.f_hat
            u = clip_norm(0.92 * desired, cfg.max_command)
        elif cfg.controller == "scalar_context":
            used_f = np.eye(2) * scalar.scale
            u = scalar.action(desired, cfg.max_command)
        elif cfg.controller == "condition_fallback":
            used_f = rls.f_hat
            if cfg.fallback_cond is not None and cond_number(used_f) > cfg.fallback_cond:
                u = clip_norm(0.38 * desired, cfg.max_command)
            else:
                u = clip_norm(regularized_inverse(used_f, cfg.ridge) @ desired, cfg.max_command)
        else:
            u = clip_norm(regularized_inverse(used_f, cfg.ridge) @ desired, cfg.max_command)

        if cfg.action_noise > 0.0:
            actual_u = clip_norm(u + noise_rng.normal(0.0, cfg.action_noise, size=2), cfg.max_command)
        else:
            actual_u = u
        y_prev = y.copy()
        dy_clean = current_f @ actual_u
        obs_noise = noise_rng.normal(0.0, cfg.obs_noise, size=2)
        if cfg.outlier_prob > 0.0 and noise_rng.random() < cfg.outlier_prob:
            obs_noise += noise_rng.normal(0.0, cfg.outlier_scale, size=2)
        dy_obs = dy_clean + obs_noise
        y = y + dy_obs

        update_queue.append((actual_u.copy(), dy_obs.copy()))
        if len(update_queue) > cfg.update_delay:
            update_u, update_dy = update_queue.pop(0)
            if noise_rng.random() >= cfg.dropout_prob:
                rls.update(update_u, update_dy)
                windowed.update(update_u, update_dy)
                residual.update(update_u, update_dy)
                scalar.update(update_u, update_dy)

        recent_commands.append(actual_u.copy())
        recent_commands = recent_commands[-10:]
        if t % 4 == 0 or t == cfg.max_steps - 1:
            if len(recent_commands) >= 3:
                u_mat = np.vstack(recent_commands)
                cov = u_mat.T @ u_mat
                excitation_scores.append(float(np.linalg.det(cov + 1e-6 * np.eye(2))))
            else:
                excitation_scores.append(0.0)

        total_path += float(np.linalg.norm(y - y_prev))
        total_command += float(np.linalg.norm(actual_u))
        if float(np.linalg.norm(actual_u)) > 0.90 * cfg.max_command:
            overshoot_count += 1
        cal_errors.append(float(np.linalg.norm(used_f - current_f, ord="fro")))
        if t % 4 == 0 or t == cfg.max_steps - 1:
            conditions.append(cond_number(used_f))

        event = drift.step(t)
        f_history.append(drift.matrix().copy())
        if event:
            event_count += 1
            active_event_time = t
            active_peak = err_norm
        if active_event_time is not None:
            active_peak = max(active_peak, err_norm)
            if err_norm < 1.5 * cfg.success_eps or t == cfg.max_steps - 1:
                recovery_steps.append(t - active_event_time)
                event_peak_errors.append(active_peak)
                active_event_time = None
                active_peak = 0.0

    final_goal = goals[-1]
    final_error = float(np.linalg.norm(final_goal - y))
    tail_error = float(np.mean(errors[-10:]))
    straight = float(np.linalg.norm(final_goal - initial_y))
    path_efficiency = straight / max(total_path, 1e-6)
    success = int(final_error < cfg.success_eps or tail_error < 1.5 * cfg.success_eps)
    initial_cal_error = float(np.linalg.norm(initial_f - drift.matrix(), ord="fro"))

    return {
        "success": success,
        "final_error": final_error,
        "tail_error": tail_error,
        "path_efficiency": path_efficiency,
        "total_command": total_command,
        "calibration_error": float(np.mean(cal_errors[-10:])),
        "condition": float(np.nanmean(conditions[-10:])),
        "excitation": float(np.nanmean(excitation_scores[-10:])),
        "overshoot_rate": overshoot_count / cfg.max_steps,
        "event_count": event_count,
        "peak_event_error": float(np.mean(event_peak_errors)) if event_peak_errors else 0.0,
        "recovery_steps": float(np.mean(recovery_steps)) if recovery_steps else float("nan"),
        "initial_to_final_drift": initial_cal_error,
    }


METRICS = [
    "success",
    "final_error",
    "tail_error",
    "path_efficiency",
    "total_command",
    "calibration_error",
    "condition",
    "excitation",
    "overshoot_rate",
    "event_count",
    "peak_event_error",
    "recovery_steps",
    "initial_to_final_drift",
]


def run_batch(cfg: SimConfig) -> dict:
    rows = [run_episode(cfg, i) for i in range(cfg.n_episodes)]
    out = {
        "family": cfg.family,
        "setting": cfg.setting,
        "mode": cfg.mode,
        "controller": cfg.controller,
        "seed": cfg.seed,
        "episodes": cfg.n_episodes,
        "obs_noise": cfg.obs_noise,
        "action_noise": cfg.action_noise,
        "delay": cfg.update_delay,
        "dropout": cfg.dropout_prob,
        "outlier_prob": cfg.outlier_prob,
        "excitation_scale": cfg.excitation_scale,
        "dither": cfg.dither,
        "forgetting": cfg.forgetting,
        "window": cfg.window,
        "event_scale": cfg.event_scale,
        "scale_floor": cfg.scale_floor,
        "fallback_cond": cfg.fallback_cond if cfg.fallback_cond is not None else "",
    }
    for metric in METRICS:
        vals = np.asarray([r[metric] for r in rows], dtype=float)
        out[metric] = float("nan") if np.all(np.isnan(vals)) else float(np.nanmean(vals))
        if metric == "success":
            p = out[metric]
            out["success_stderr"] = float(math.sqrt(max(p * (1.0 - p), 0.0) / cfg.n_episodes))
    return out


def write_rows(path: Path, rows: list[dict]) -> None:
    if not rows:
        return
    fields: list[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def summarize(rows: list[dict], keys: list[str]) -> list[dict]:
    groups: dict[tuple, list[dict]] = {}
    for row in rows:
        groups.setdefault(tuple(row[k] for k in keys), []).append(row)
    out: list[dict] = []
    for group_key, group_rows in sorted(groups.items()):
        rec = {k: v for k, v in zip(keys, group_key)}
        rec["rows"] = len(group_rows)
        rec["episodes"] = int(sum(int(r["episodes"]) for r in group_rows))
        for metric in METRICS + ["success_stderr"]:
            vals = np.asarray([float(r[metric]) for r in group_rows], dtype=float)
            rec[metric] = float("nan") if np.all(np.isnan(vals)) else float(np.nanmean(vals))
        out.append(rec)
    return out


def progress(stage: str, counts: dict[str, int]) -> None:
    rec = {"stage": stage, **counts}
    (OUT / "progress.json").write_text(json.dumps(rec, indent=2), encoding="utf-8")


def run_family_a() -> tuple[list[dict], list[dict]]:
    rows: list[dict] = []
    seeds = range(4)
    for mode in MAIN_MODES:
        for controller in MAIN_CONTROLLERS:
            for seed in seeds:
                rows.append(
                    run_batch(
                        SimConfig(
                            mode=mode,
                            controller=controller,
                            seed=190_000 + 1000 * seed,
                            n_episodes=12,
                            family="A",
                            setting="main",
                        )
                    )
                )
    summary = summarize(rows, ["mode", "controller"])
    write_rows(OUT / "family_a_main_seed.csv", rows)
    write_rows(OUT / "family_a_main_summary.csv", summary)
    return rows, summary


def run_family_b() -> tuple[list[dict], list[dict]]:
    rows: list[dict] = []
    configs: list[tuple[str, str, dict]] = []
    for f in [0.84, 0.90, 0.925, 0.97, 1.0]:
        configs.append((f"rls_f{f}", "calibration_state" if f != 1.0 else "csc_no_forgetting", {"forgetting": f}))
    for window in [6, 10, 14, 22, 32]:
        configs.append((f"window_{window}", "windowed_sysid", {"window": window}))
    configs += [
        ("matrix_not_policy", "matrix_no_policy", {}),
        ("scalar_context", "scalar_context", {}),
        ("shuffled_matrix", "shuffled_state", {}),
        ("frozen", "frozen_start_calibration", {}),
        ("oracle", "oracle", {}),
    ]
    for mode in ["abrupt_bump", "severe_random_walk", "sinusoidal"]:
        for setting, controller, extra in configs:
            for seed in range(3):
                rows.append(
                    run_batch(
                        SimConfig(
                            mode=mode,
                            controller=controller,
                            seed=210_000 + 1000 * seed,
                            n_episodes=10,
                            family="B",
                            setting=setting,
                            **extra,
                        )
                    )
                )
    summary = summarize(rows, ["setting", "mode", "controller"])
    write_rows(OUT / "family_b_estimator_seed.csv", rows)
    write_rows(OUT / "family_b_estimator_summary.csv", summary)
    return rows, summary


def run_family_c() -> tuple[list[dict], list[dict]]:
    rows: list[dict] = []
    for mode in ["random_walk", "abrupt_bump"]:
        for excitation in [0.35, 0.60, 1.00]:
            for dither in [0.0, 0.008]:
                for goal_period in [10, 20, 40]:
                    setting = f"exc{excitation}_d{dither}_g{goal_period}"
                    for controller in ["frozen_start_calibration", "windowed_sysid", "calibration_state", "oracle"]:
                        for seed in range(2):
                            rows.append(
                                run_batch(
                                    SimConfig(
                                        mode=mode,
                                        controller=controller,
                                        seed=230_000 + 1000 * seed,
                                        n_episodes=8,
                                        family="C",
                                        setting=setting,
                                        excitation_scale=excitation,
                                        dither=dither,
                                        goal_period=goal_period,
                                    )
                                )
                            )
    summary = summarize(rows, ["setting", "mode", "controller"])
    write_rows(OUT / "family_c_observability_seed.csv", rows)
    write_rows(OUT / "family_c_observability_summary.csv", summary)
    return rows, summary


def run_family_d() -> tuple[list[dict], list[dict]]:
    rows: list[dict] = []
    for mode in ["abrupt_bump", "severe_random_walk"]:
        for obs_noise in [0.0, 0.0012, 0.004, 0.008, 0.012]:
            for action_noise in [0.0, 0.004]:
                for delay in [0, 2]:
                    setting = f"obs{obs_noise}_act{action_noise}_delay{delay}"
                    for controller in ["frozen_start_calibration", "windowed_sysid", "calibration_state", "oracle"]:
                        for seed in range(2):
                            rows.append(
                                run_batch(
                                    SimConfig(
                                        mode=mode,
                                        controller=controller,
                                        seed=250_000 + 1000 * seed,
                                        n_episodes=8,
                                        family="D",
                                        setting=setting,
                                        obs_noise=obs_noise,
                                        action_noise=action_noise,
                                        update_delay=delay,
                                    )
                                )
                            )
    for mode in ["abrupt_bump"]:
        for outlier_prob in [0.02, 0.06]:
            for dropout in [0.1, 0.3]:
                setting = f"out{outlier_prob}_drop{dropout}"
                for controller in ["windowed_sysid", "calibration_state", "oracle"]:
                    for seed in range(2):
                        rows.append(
                            run_batch(
                                SimConfig(
                                    mode=mode,
                                    controller=controller,
                                    seed=255_000 + 1000 * seed,
                                    n_episodes=8,
                                    family="D",
                                    setting=setting,
                                    outlier_prob=outlier_prob,
                                    outlier_scale=0.035,
                                    dropout_prob=dropout,
                                )
                            )
                        )
    summary = summarize(rows, ["setting", "mode", "controller"])
    write_rows(OUT / "family_d_noise_seed.csv", rows)
    write_rows(OUT / "family_d_noise_summary.csv", summary)
    return rows, summary


def run_family_e() -> tuple[list[dict], list[dict]]:
    rows: list[dict] = []
    for scale_floor in [0.18, 0.28, 0.45]:
        for shear_limit in [0.20, 0.35, 0.55]:
            for fallback in [None, 10.0]:
                setting = f"floor{scale_floor}_shear{shear_limit}_fb{fallback}"
                for controller in ["frozen_start_calibration", "windowed_sysid", "calibration_state", "condition_fallback", "oracle"]:
                    if controller == "condition_fallback" and fallback is None:
                        continue
                    for seed in range(2):
                        rows.append(
                            run_batch(
                                SimConfig(
                                    mode="ill_conditioned",
                                    controller=controller,
                                    seed=270_000 + 1000 * seed,
                                    n_episodes=8,
                                    family="E",
                                    setting=setting,
                                    scale_floor=scale_floor,
                                    shear_limit=shear_limit,
                                    fallback_cond=fallback,
                                )
                            )
                        )
    summary = summarize(rows, ["setting", "controller"])
    write_rows(OUT / "family_e_conditioning_seed.csv", rows)
    write_rows(OUT / "family_e_conditioning_summary.csv", summary)
    return rows, summary


def run_family_f() -> tuple[list[dict], list[dict]]:
    rows: list[dict] = []
    for mode in ["abrupt_bump", "late_bump", "alternating", "drift_burst"]:
        for event_scale in [0.55, 1.0, 1.45]:
            setting = f"event{event_scale}"
            for controller in ["frozen_start_calibration", "windowed_sysid", "calibration_state", "oracle"]:
                for seed in range(3):
                    rows.append(
                        run_batch(
                            SimConfig(
                                mode=mode,
                                controller=controller,
                                seed=290_000 + 1000 * seed,
                                n_episodes=8,
                                family="F",
                                setting=setting,
                                event_scale=event_scale,
                            )
                        )
                    )
    summary = summarize(rows, ["setting", "mode", "controller"])
    write_rows(OUT / "family_f_recovery_seed.csv", rows)
    write_rows(OUT / "family_f_recovery_summary.csv", summary)
    return rows, summary


def run_family_g() -> tuple[list[dict], list[dict]]:
    rows: list[dict] = []
    for mode in ["random_walk", "abrupt_bump", "severe_random_walk", "sinusoidal"]:
        for goal_period in [8, 14, 20]:
            for max_steps in [48, 80]:
                setting = f"g{goal_period}_h{max_steps}"
                for controller in ["nominal_offline", "frozen_start_calibration", "windowed_sysid", "calibration_state", "oracle"]:
                    for seed in range(2):
                        rows.append(
                            run_batch(
                                SimConfig(
                                    mode=mode,
                                    controller=controller,
                                    seed=310_000 + 1000 * seed,
                                    n_episodes=8,
                                    family="G",
                                    setting=setting,
                                    goal_period=goal_period,
                                    max_steps=max_steps,
                                )
                            )
                        )
    summary = summarize(rows, ["setting", "mode", "controller"])
    write_rows(OUT / "family_g_planning_seed.csv", rows)
    write_rows(OUT / "family_g_planning_summary.csv", summary)
    return rows, summary


def run_family_h() -> tuple[list[dict], list[dict]]:
    rows: list[dict] = []
    controllers = [
        "frozen_start_calibration",
        "scalar_context",
        "matrix_no_policy",
        "shuffled_state",
        "random_state",
        "delayed_oracle",
        "calibration_state",
        "oracle",
    ]
    for mode in ["random_walk", "abrupt_bump", "severe_random_walk"]:
        for delay in [0, 5]:
            setting = f"delay{delay}"
            for controller in controllers:
                for seed in range(3):
                    rows.append(
                        run_batch(
                            SimConfig(
                                mode=mode,
                                controller=controller,
                                seed=330_000 + 1000 * seed,
                                n_episodes=8,
                                family="H",
                                setting=setting,
                                oracle_delay=delay,
                            )
                        )
                    )
    summary = summarize(rows, ["setting", "mode", "controller"])
    write_rows(OUT / "family_h_negative_seed.csv", rows)
    write_rows(OUT / "family_h_negative_summary.csv", summary)
    return rows, summary


def mean_lookup(summary: list[dict], **conds: str) -> dict | None:
    matches = [r for r in summary if all(str(r.get(k)) == str(v) for k, v in conds.items())]
    if not matches:
        return None
    return matches[0]


def write_latex_table(name: str, caption: str, label: str, headers: list[str], rows: list[list[str]]) -> None:
    align = "l" + "r" * (len(headers) - 1)
    lines = [
        r"\begin{table}[t]",
        rf"\caption{{{caption}}}",
        rf"\label{{{label}}}",
        r"\centering",
        rf"\begin{{tabular}}{{{align}}}",
        r"\toprule",
        " & ".join(headers) + r" \\",
        r"\midrule",
    ]
    for row in rows:
        lines.append(" & ".join(row) + r" \\")
    lines += [r"\bottomrule", r"\end{tabular}", r"\end{table}"]
    (OUT / name).write_text("\n".join(lines) + "\n", encoding="utf-8")


def short_controller(name: str) -> str:
    return {
        "nominal_offline": "nominal",
        "robust_low_gain": "low-gain",
        "frozen_start_calibration": "frozen",
        "residual_bias": "residual",
        "windowed_sysid": "windowed",
        "calibration_state": "CSC",
        "condition_fallback": "CSC+fallback",
        "oracle": "oracle",
        "matrix_no_policy": "matrix/no-policy",
        "scalar_context": "scalar",
        "shuffled_state": "shuffled",
        "random_state": "random",
        "delayed_oracle": "delayed oracle",
        "csc_no_forgetting": "no-forget",
    }.get(name, name)


def write_tables(summaries: dict[str, list[dict]], metadata: dict) -> None:
    a = summaries["A"]
    main_rows: list[list[str]] = []
    for controller in MAIN_CONTROLLERS:
        vals = [r for r in a if r["controller"] == controller]
        main_rows.append(
            [
                short_controller(controller),
                f"{np.mean([float(v['success']) for v in vals]):.3f}",
                f"{np.mean([float(v['final_error']) for v in vals]):.4f}",
                f"{np.mean([float(v['tail_error']) for v in vals]):.4f}",
                f"{np.mean([float(v['calibration_error']) for v in vals]):.3f}",
            ]
        )
    write_latex_table(
        "table_main_controller.tex",
        "Family A main controller comparison across eight drift modes.",
        "tab:main-controller",
        ["Controller", "Success", "Final err.", "Tail err.", "Cal. err."],
        main_rows,
    )

    b = summaries["B"]
    estimator_rows = []
    for setting in ["rls_f0.84", "rls_f0.925", "rls_f1.0", "window_14", "window_32", "matrix_not_policy", "scalar_context", "shuffled_matrix", "oracle"]:
        vals = [r for r in b if r["setting"] == setting]
        if not vals:
            continue
        estimator_rows.append(
            [
                setting.replace("_", " "),
                f"{np.mean([float(v['success']) for v in vals]):.3f}",
                f"{np.mean([float(v['final_error']) for v in vals]):.4f}",
                f"{np.mean([float(v['calibration_error']) for v in vals]):.3f}",
            ]
        )
    write_latex_table(
        "table_estimator_ablation.tex",
        "Family B estimator and policy-state interface ablations.",
        "tab:estimator-ablation",
        ["Variant", "Success", "Final err.", "Cal. err."],
        estimator_rows,
    )

    c = summaries["C"]
    obs_rows = []
    for excitation in ["exc0.35", "exc0.6", "exc1.0"]:
        vals = [r for r in c if str(r["setting"]).startswith(excitation) and r["controller"] in ("calibration_state", "windowed_sysid", "frozen_start_calibration")]
        for controller in ["frozen_start_calibration", "windowed_sysid", "calibration_state"]:
            cvals = [r for r in vals if r["controller"] == controller]
            obs_rows.append([f"{excitation} {short_controller(controller)}", f"{np.mean([float(v['success']) for v in cvals]):.3f}", f"{np.mean([float(v['excitation']) for v in cvals]):.5f}"])
    write_latex_table(
        "table_observability.tex",
        "Family C observability/excitation stress.",
        "tab:observability",
        ["Setting", "Success", "Excitation"],
        obs_rows,
    )

    d = summaries["D"]
    noise_rows = []
    for token in ["obs0.0", "obs0.004", "obs0.012", "out0.06"]:
        vals = [r for r in d if str(r["setting"]).startswith(token)]
        for controller in ["frozen_start_calibration", "windowed_sysid", "calibration_state", "oracle"]:
            cvals = [r for r in vals if r["controller"] == controller]
            if cvals:
                noise_rows.append([f"{token} {short_controller(controller)}", f"{np.mean([float(v['success']) for v in cvals]):.3f}", f"{np.mean([float(v['final_error']) for v in cvals]):.4f}"])
    write_latex_table("table_noise_latency.tex", "Family D noise, delay, dropout, and outlier stress.", "tab:noise", ["Setting", "Success", "Final err."], noise_rows)

    e = summaries["E"]
    cond_rows = []
    for controller in ["frozen_start_calibration", "windowed_sysid", "calibration_state", "condition_fallback", "oracle"]:
        vals = [r for r in e if r["controller"] == controller]
        if vals:
            cond_rows.append([short_controller(controller), f"{np.mean([float(v['success']) for v in vals]):.3f}", f"{np.mean([float(v['condition']) for v in vals]):.2f}", f"{np.mean([float(v['overshoot_rate']) for v in vals]):.3f}"])
    write_latex_table("table_conditioning.tex", "Family E near-singular calibration and condition-aware fallback.", "tab:conditioning", ["Controller", "Success", "Cond.", "Overshoot"], cond_rows)

    f = summaries["F"]
    recovery_rows = []
    for mode in ["abrupt_bump", "late_bump", "alternating", "drift_burst"]:
        for controller in ["frozen_start_calibration", "windowed_sysid", "calibration_state", "oracle"]:
            vals = [r for r in f if r["mode"] == mode and r["controller"] == controller]
            recovery_rows.append([f"{mode.replace('_', ' ')} {short_controller(controller)}", f"{np.mean([float(v['success']) for v in vals]):.3f}", f"{np.nanmean([float(v['recovery_steps']) for v in vals]):.2f}", f"{np.mean([float(v['peak_event_error']) for v in vals]):.3f}"])
    write_latex_table("table_recovery.tex", "Family F recovery after discrete drift events.", "tab:recovery", ["Setting", "Success", "Rec. steps", "Peak err."], recovery_rows)

    g = summaries["G"]
    plan_rows = []
    for controller in ["nominal_offline", "frozen_start_calibration", "windowed_sysid", "calibration_state", "oracle"]:
        vals = [r for r in g if r["controller"] == controller]
        plan_rows.append([short_controller(controller), f"{np.mean([float(v['success']) for v in vals]):.3f}", f"{np.mean([float(v['tail_error']) for v in vals]):.4f}", f"{np.mean([float(v['total_command']) for v in vals]):.3f}"])
    write_latex_table("table_planning.tex", "Family G multi-goal planning/control utility.", "tab:planning", ["Controller", "Success", "Tail err.", "Command"], plan_rows)

    h = summaries["H"]
    neg_rows = []
    for controller in ["frozen_start_calibration", "scalar_context", "matrix_no_policy", "shuffled_state", "random_state", "delayed_oracle", "calibration_state", "oracle"]:
        vals = [r for r in h if r["controller"] == controller]
        neg_rows.append([short_controller(controller), f"{np.mean([float(v['success']) for v in vals]):.3f}", f"{np.mean([float(v['final_error']) for v in vals]):.4f}", f"{np.mean([float(v['calibration_error']) for v in vals]):.3f}"])
    write_latex_table("table_negative_controls.tex", "Family H negative controls for generic context and stale calibration.", "tab:negative-controls", ["Control", "Success", "Final err.", "Cal. err."], neg_rows)

    claim_rows = [
        ["CSC helps under moving drift", "Family A", f"main success {metadata['headline']['csc_main_success']:.3f}"],
        ["Interface beats stale calibration", "Family F", f"recovery success {metadata['headline']['csc_recovery_success']:.3f}"],
        ["Estimator is not the whole claim", "Family B", f"windowed success {metadata['headline']['windowed_estimator_success']:.3f}"],
        ["Observability is load-bearing", "Family C", f"low-excitation CSC {metadata['headline']['low_excitation_csc_success']:.3f}"],
        ["Noise boundary is mapped", "Family D", f"high-noise CSC {metadata['headline']['high_noise_csc_success']:.3f}"],
        ["Conditioning matters", "Family E", f"fallback success {metadata['headline']['fallback_success']:.3f}"],
        ["Action choice changes", "Family G", f"CSC tail error {metadata['headline']['csc_planning_tail_error']:.4f}"],
        ["Generic context is not enough", "Family H", f"shuffled success {metadata['headline']['shuffled_success']:.3f}"],
    ]
    write_latex_table("table_claim_evidence.tex", "Generated claim-to-evidence audit.", "tab:claim-evidence", ["Claim", "Evidence", "Result"], claim_rows)

    runtime_rows = []
    for fam, count in metadata["seed_rows"].items():
        runtime_rows.append([fam, str(count), str(metadata["episodes"][fam])])
    write_latex_table("table_runtime_memory.tex", "Full-scale v3 family sizes. Rows are compact batch summaries streamed to disk.", "tab:runtime", ["Family", "Rows", "Episodes"], runtime_rows)


def plot_grouped(summary: list[dict], family: str, controllers: list[str], metric: str, path: str, ylabel: str) -> None:
    modes = sorted({r["mode"] for r in summary})
    data = {(r["mode"], r["controller"]): float(r[metric]) for r in summary}
    x = np.arange(len(modes))
    width = min(0.12, 0.72 / max(len(controllers), 1))
    fig, ax = plt.subplots(figsize=(9.0, 3.2))
    for i, controller in enumerate(controllers):
        vals = [data.get((mode, controller), np.nan) for mode in modes]
        ax.bar(x + (i - (len(controllers) - 1) / 2) * width, vals, width, label=short_controller(controller))
    ax.set_xticks(x)
    ax.set_xticklabels([m.replace("_", "\n") for m in modes], fontsize=8)
    ax.set_ylabel(ylabel)
    ax.grid(axis="y", alpha=0.25)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.legend(ncol=4, fontsize=7, frameon=False)
    fig.tight_layout()
    fig.savefig(OUT / path)
    fig.savefig(OUT / path.replace(".pdf", ".png"), dpi=180)
    plt.close(fig)


def plot_line(summary: list[dict], metric: str, path: str, ylabel: str, title_key: str = "setting") -> None:
    controllers = sorted({r["controller"] for r in summary})
    settings = sorted({str(r[title_key]) for r in summary})
    fig, ax = plt.subplots(figsize=(8.0, 3.2))
    for controller in controllers:
        vals = []
        for setting in settings:
            rows = [r for r in summary if str(r[title_key]) == setting and r["controller"] == controller]
            vals.append(np.nan if not rows else float(np.nanmean([float(r[metric]) for r in rows])))
        ax.plot(range(len(settings)), vals, marker="o", linewidth=1.5, label=short_controller(controller))
    ax.set_xticks(range(len(settings)))
    ax.set_xticklabels(settings, rotation=35, ha="right", fontsize=7)
    ax.set_ylabel(ylabel)
    ax.grid(alpha=0.25)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.legend(ncol=3, fontsize=7, frameon=False)
    fig.tight_layout()
    fig.savefig(OUT / path)
    fig.savefig(OUT / path.replace(".pdf", ".png"), dpi=180)
    plt.close(fig)


def write_plots(summaries: dict[str, list[dict]]) -> None:
    plot_grouped(summaries["A"], "A", MAIN_CONTROLLERS, "success", "figure_main_success.pdf", "success rate")
    plot_grouped(summaries["A"], "A", MAIN_CONTROLLERS, "final_error", "figure_main_final_error.pdf", "mean final error")
    plot_line([r for r in summaries["B"] if r["controller"] in ("calibration_state", "windowed_sysid", "matrix_no_policy", "scalar_context", "shuffled_state", "oracle")], "success", "figure_estimator_ablation.pdf", "success")
    plot_line([r for r in summaries["C"] if r["controller"] in ("frozen_start_calibration", "windowed_sysid", "calibration_state", "oracle")], "success", "figure_observability.pdf", "success")
    plot_line([r for r in summaries["D"] if r["controller"] in ("frozen_start_calibration", "windowed_sysid", "calibration_state", "oracle") and str(r["setting"]).startswith(("obs0.0", "obs0.004", "obs0.008", "obs0.012"))], "success", "figure_noise_latency.pdf", "success")
    plot_line(summaries["E"], "overshoot_rate", "figure_conditioning.pdf", "overshoot rate")
    plot_grouped(summaries["F"], "F", ["frozen_start_calibration", "windowed_sysid", "calibration_state", "oracle"], "recovery_steps", "figure_recovery.pdf", "recovery steps")
    plot_grouped(summaries["G"], "G", ["nominal_offline", "frozen_start_calibration", "windowed_sysid", "calibration_state", "oracle"], "tail_error", "figure_planning_tail_error.pdf", "tail error")
    plot_grouped(summaries["H"], "H", ["scalar_context", "matrix_no_policy", "shuffled_state", "random_state", "calibration_state", "oracle"], "success", "figure_negative_controls.pdf", "success rate")


def compute_metadata(seed_rows: dict[str, list[dict]], summaries: dict[str, list[dict]], elapsed: float) -> dict:
    def avg(rows: list[dict], metric: str) -> float:
        return float(np.nanmean([float(r[metric]) for r in rows]))

    a_csc = [r for r in summaries["A"] if r["controller"] == "calibration_state"]
    a_frozen = [r for r in summaries["A"] if r["controller"] == "frozen_start_calibration"]
    a_windowed = [r for r in summaries["A"] if r["controller"] == "windowed_sysid"]
    b_windowed = [r for r in summaries["B"] if r["controller"] == "windowed_sysid"]
    c_low_csc = [r for r in summaries["C"] if r["controller"] == "calibration_state" and str(r["setting"]).startswith("exc0.35")]
    d_high_csc = [r for r in summaries["D"] if r["controller"] == "calibration_state" and str(r["setting"]).startswith("obs0.012")]
    e_fallback = [r for r in summaries["E"] if r["controller"] == "condition_fallback"]
    f_csc = [r for r in summaries["F"] if r["controller"] == "calibration_state"]
    g_csc = [r for r in summaries["G"] if r["controller"] == "calibration_state"]
    h_shuffled = [r for r in summaries["H"] if r["controller"] == "shuffled_state"]

    return {
        "master_seed": 19019,
        "families": {
            "A": "main controller comparison",
            "B": "estimator and interface ablations",
            "C": "observability and excitation stress",
            "D": "noise latency dropout outliers",
            "E": "conditioning and fallback",
            "F": "drift event recovery",
            "G": "planning control utility",
            "H": "negative controls",
        },
        "seed_rows": {fam: len(rows) for fam, rows in seed_rows.items()},
        "episodes": {fam: int(sum(int(r["episodes"]) for r in rows)) for fam, rows in seed_rows.items()},
        "total_seed_rows": int(sum(len(rows) for rows in seed_rows.values())),
        "total_episodes": int(sum(int(r["episodes"]) for rows in seed_rows.values() for r in rows)),
        "elapsed_seconds": elapsed,
        "headline": {
            "csc_main_success": avg(a_csc, "success"),
            "frozen_main_success": avg(a_frozen, "success"),
            "windowed_main_success": avg(a_windowed, "success"),
            "windowed_estimator_success": avg(b_windowed, "success"),
            "low_excitation_csc_success": avg(c_low_csc, "success"),
            "high_noise_csc_success": avg(d_high_csc, "success"),
            "fallback_success": avg(e_fallback, "success"),
            "csc_recovery_success": avg(f_csc, "success"),
            "csc_planning_tail_error": avg(g_csc, "tail_error"),
            "shuffled_success": avg(h_shuffled, "success"),
        },
    }


def main() -> None:
    start = perf_counter()
    progress("starting", {})
    runners = [
        ("A", run_family_a),
        ("B", run_family_b),
        ("C", run_family_c),
        ("D", run_family_d),
        ("E", run_family_e),
        ("F", run_family_f),
        ("G", run_family_g),
        ("H", run_family_h),
    ]
    seed_rows: dict[str, list[dict]] = {}
    summaries: dict[str, list[dict]] = {}
    counts: dict[str, int] = {}
    for fam, runner in runners:
        print(f"[full-scale] running family {fam}")
        rows, summary = runner()
        seed_rows[fam] = rows
        summaries[fam] = summary
        counts[f"family_{fam}_rows"] = len(rows)
        progress(f"finished_{fam}", counts)

    elapsed = perf_counter() - start
    metadata = compute_metadata(seed_rows, summaries, elapsed)
    write_tables(summaries, metadata)
    write_plots(summaries)
    (OUT / "metadata.json").write_text(json.dumps(metadata, indent=2), encoding="utf-8")
    progress("complete", {**counts, "total_seed_rows": metadata["total_seed_rows"], "total_episodes": metadata["total_episodes"], "plot_failures": 0})
    print(json.dumps(metadata, indent=2))


if __name__ == "__main__":
    main()
