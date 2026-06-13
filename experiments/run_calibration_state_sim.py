from __future__ import annotations

import csv
import json
import math
from dataclasses import dataclass
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np


ROOT = Path(__file__).resolve().parents[1]
RESULTS = ROOT / "results"
DOCS = ROOT / "docs"
RESULTS.mkdir(exist_ok=True)
DOCS.mkdir(exist_ok=True)

EPISODE_CSV = RESULTS / "episode_results.csv"
AGG_CSV = RESULTS / "aggregate_results.csv"
SUMMARY_MD = RESULTS / "calibration_state_evidence.md"
PLOT_SUCCESS = RESULTS / "success_by_mode.pdf"
PLOT_ERROR = RESULTS / "final_error_by_mode.pdf"
PROGRESS = RESULTS / "simulation_progress.json"
WINDOWED_CSV = RESULTS / "windowed_context_baseline.csv"
WINDOWED_TABLE = RESULTS / "windowed_context_table.tex"


MAX_STEPS = 80
N_EPISODES = 600
SUCCESS_EPS = 0.04
GOAL_PERIOD = 20
MAX_OBS_STEP = 0.075
MAX_COMMAND = 0.16
NOISE_STD = 0.0012


MODES = ["static", "random_walk", "abrupt_bump", "severe_random_walk"]
CONTROLLERS = [
    "nominal_offline",
    "robust_low_gain",
    "frozen_start_calibration",
    "residual_bias",
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


@dataclass
class DriftProcess:
    mode: str
    rng: np.random.Generator
    theta: float
    sx: float
    sy: float
    shear: float

    @classmethod
    def create(cls, mode: str, seed: int) -> "DriftProcess":
        rng = np.random.default_rng(seed)
        if mode == "static":
            theta = rng.normal(0.0, 0.24)
            sx = rng.uniform(0.78, 1.25)
            sy = rng.uniform(0.78, 1.25)
            shear = rng.normal(0.0, 0.08)
        elif mode == "random_walk":
            theta = rng.normal(0.0, 0.18)
            sx = rng.uniform(0.82, 1.18)
            sy = rng.uniform(0.82, 1.18)
            shear = rng.normal(0.0, 0.06)
        elif mode == "abrupt_bump":
            theta = rng.normal(0.0, 0.16)
            sx = rng.uniform(0.82, 1.18)
            sy = rng.uniform(0.82, 1.18)
            shear = rng.normal(0.0, 0.05)
        elif mode == "severe_random_walk":
            theta = rng.normal(0.0, 0.32)
            sx = rng.uniform(0.68, 1.34)
            sy = rng.uniform(0.68, 1.34)
            shear = rng.normal(0.0, 0.13)
        else:
            raise ValueError(mode)
        return cls(mode=mode, rng=rng, theta=theta, sx=sx, sy=sy, shear=shear)

    def matrix(self) -> np.ndarray:
        return calibration_matrix(self.theta, self.sx, self.sy, self.shear)

    def step(self, t: int) -> None:
        if self.mode == "static":
            return
        if self.mode == "random_walk":
            self.theta += self.rng.normal(0.0, 0.018)
            self.sx += self.rng.normal(0.0, 0.010)
            self.sy += self.rng.normal(0.0, 0.010)
            self.shear += self.rng.normal(0.0, 0.006)
        elif self.mode == "abrupt_bump":
            self.theta += self.rng.normal(0.0, 0.006)
            if t in (12, 32, 52):
                self.theta += self.rng.normal(0.0, 0.58)
                self.sx *= self.rng.uniform(0.62, 1.38)
                self.sy *= self.rng.uniform(0.62, 1.38)
                self.shear += self.rng.normal(0.0, 0.18)
        elif self.mode == "severe_random_walk":
            self.theta += self.rng.normal(0.0, 0.040)
            self.sx += self.rng.normal(0.0, 0.020)
            self.sy += self.rng.normal(0.0, 0.020)
            self.shear += self.rng.normal(0.0, 0.014)

        self.theta = float(np.clip(self.theta, -0.95, 0.95))
        self.sx = float(np.clip(self.sx, 0.45, 1.65))
        self.sy = float(np.clip(self.sy, 0.45, 1.65))
        self.shear = float(np.clip(self.shear, -0.45, 0.45))


class RLSCalibration:
    def __init__(self, forgetting: float = 0.925, prior_scale: float = 28.0) -> None:
        self.f_hat = np.eye(2)
        self.p = np.stack([np.eye(2) * prior_scale, np.eye(2) * prior_scale])
        self.forgetting = forgetting
        self.updates = 0

    def update(self, u: np.ndarray, dy: np.ndarray) -> None:
        if float(np.linalg.norm(u)) < 1e-6:
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

    def condition(self) -> float:
        try:
            return float(np.linalg.cond(self.f_hat))
        except np.linalg.LinAlgError:
            return float("inf")


class ResidualBias:
    def __init__(self) -> None:
        self.bias = np.zeros(2)

    def action(self, desired: np.ndarray) -> np.ndarray:
        return clip_norm(0.80 * desired + self.bias, MAX_COMMAND)

    def update(self, u: np.ndarray, dy: np.ndarray) -> None:
        residual = u - dy
        self.bias = 0.84 * self.bias + 0.28 * residual
        self.bias = clip_norm(self.bias, 0.08)


class WindowedSysID:
    def __init__(self, window: int = 14, ridge: float = 2e-3) -> None:
        self.window = window
        self.ridge = ridge
        self.u_hist: list[np.ndarray] = []
        self.dy_hist: list[np.ndarray] = []
        self.f_hat = np.eye(2)

    def update(self, u: np.ndarray, dy: np.ndarray) -> None:
        if float(np.linalg.norm(u)) < 1e-6:
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

    def condition(self) -> float:
        try:
            return float(np.linalg.cond(self.f_hat))
        except np.linalg.LinAlgError:
            return float("inf")


def make_initial_state(seed: int) -> tuple[np.ndarray, list[np.ndarray]]:
    rng = np.random.default_rng(seed)
    y0 = rng.uniform(-0.55, 0.55, size=2)
    goals: list[np.ndarray] = []
    prev = y0
    for _ in range(MAX_STEPS // GOAL_PERIOD):
        goal = rng.uniform(-0.62, 0.62, size=2)
        while float(np.linalg.norm(goal - prev)) < 0.42:
            goal = rng.uniform(-0.62, 0.62, size=2)
        goals.append(goal)
        prev = goal
    return y0, goals


def run_episode(mode: str, controller: str, episode_idx: int) -> dict:
    base_seed = 100_000 + 9973 * episode_idx + 101 * MODES.index(mode)
    drift = DriftProcess.create(mode, base_seed + 11)
    noise_rng = np.random.default_rng(base_seed + 23)
    y, goals = make_initial_state(base_seed + 37)
    initial_y = y.copy()
    initial_f = drift.matrix().copy()
    rls = RLSCalibration()
    residual = ResidualBias()
    windowed = WindowedSysID()

    total_path = 0.0
    total_command = 0.0
    max_condition = 1.0
    first_success_step = None
    tracking_errors = []
    calibration_error_trace = []

    for t in range(MAX_STEPS):
        goal = goals[min(t // GOAL_PERIOD, len(goals) - 1)]
        err = goal - y
        err_norm = float(np.linalg.norm(err))
        tracking_errors.append(err_norm)
        if err_norm < SUCCESS_EPS and first_success_step is None:
            first_success_step = t

        desired = clip_norm(err, MAX_OBS_STEP)
        current_f = drift.matrix()

        if controller == "nominal_offline":
            u = clip_norm(0.92 * desired, MAX_COMMAND)
            used_f_hat = np.eye(2)
        elif controller == "robust_low_gain":
            u = clip_norm(0.38 * desired, MAX_COMMAND)
            used_f_hat = np.eye(2)
        elif controller == "frozen_start_calibration":
            used_f_hat = initial_f
            u = clip_norm(regularized_inverse(initial_f, 5e-4) @ desired, MAX_COMMAND)
        elif controller == "residual_bias":
            u = residual.action(desired)
            used_f_hat = np.eye(2)
        elif controller == "calibration_state":
            used_f_hat = rls.f_hat.copy()
            inv_hat = regularized_inverse(used_f_hat, 1e-3)
            u = clip_norm(inv_hat @ desired, MAX_COMMAND)
            max_condition = max(max_condition, rls.condition())
        elif controller == "windowed_sysid":
            used_f_hat = windowed.f_hat.copy()
            inv_hat = regularized_inverse(used_f_hat, 1e-3)
            u = clip_norm(inv_hat @ desired, MAX_COMMAND)
            max_condition = max(max_condition, windowed.condition())
        elif controller == "oracle":
            used_f_hat = current_f
            u = clip_norm(regularized_inverse(current_f, 1e-5) @ desired, MAX_COMMAND)
        else:
            raise ValueError(controller)

        dy = current_f @ u + noise_rng.normal(0.0, NOISE_STD, size=2)
        y = y + dy
        total_path += float(np.linalg.norm(dy))
        total_command += float(np.linalg.norm(u))

        if controller == "calibration_state":
            rls.update(u, dy)
            calibration_error_trace.append(float(np.linalg.norm(rls.f_hat - current_f, ord="fro")))
        elif controller == "windowed_sysid":
            windowed.update(u, dy)
            calibration_error_trace.append(float(np.linalg.norm(windowed.f_hat - current_f, ord="fro")))
        elif controller == "residual_bias":
            residual.update(u, dy)

        drift.step(t)

    final_error = float(np.linalg.norm(goals[-1] - y))
    tail_error = float(np.mean(tracking_errors[-5:])) if tracking_errors else final_error
    success = final_error < SUCCESS_EPS and tail_error < 1.25 * SUCCESS_EPS
    direct_distance = float(np.linalg.norm(goals[0] - initial_y))
    for prev, nxt in zip(goals[:-1], goals[1:]):
        direct_distance += float(np.linalg.norm(nxt - prev))
    path_efficiency = direct_distance / max(total_path, direct_distance, 1e-9)
    initial_error = float(np.linalg.norm(initial_f - np.eye(2), ord="fro"))
    final_f = drift.matrix()
    drift_amount = float(np.linalg.norm(final_f - initial_f, ord="fro"))
    if calibration_error_trace:
        mean_cal_error = float(np.mean(calibration_error_trace[-10:]))
    else:
        mean_cal_error = float(np.linalg.norm(used_f_hat - final_f, ord="fro"))

    return {
        "mode": mode,
        "controller": controller,
        "episode": episode_idx,
        "success": int(success),
        "first_success_step": first_success_step if first_success_step is not None else "",
        "final_error": final_error,
        "tail_error": tail_error,
        "path_efficiency": path_efficiency,
        "total_path": total_path,
        "total_command": total_command,
        "initial_calibration_error": initial_error,
        "drift_amount": drift_amount,
        "mean_recent_calibration_error": mean_cal_error,
        "max_condition": max_condition,
    }


def aggregate(rows: list[dict]) -> list[dict]:
    grouped: dict[tuple[str, str], list[dict]] = {}
    for row in rows:
        grouped.setdefault((row["mode"], row["controller"]), []).append(row)

    out = []
    for (mode, controller), group in sorted(grouped.items()):
        success = np.array([r["success"] for r in group], dtype=float)
        final_error = np.array([r["final_error"] for r in group], dtype=float)
        efficiency = np.array([r["path_efficiency"] for r in group], dtype=float)
        command = np.array([r["total_command"] for r in group], dtype=float)
        cal_error = np.array([r["mean_recent_calibration_error"] for r in group], dtype=float)
        out.append(
            {
                "mode": mode,
                "controller": controller,
                "episodes": len(group),
                "success_rate": float(np.mean(success)),
                "final_error_mean": float(np.mean(final_error)),
                "final_error_median": float(np.median(final_error)),
                "path_efficiency_mean": float(np.mean(efficiency)),
                "total_command_mean": float(np.mean(command)),
                "mean_recent_calibration_error": float(np.mean(cal_error)),
                "success_stderr": float(np.sqrt(np.mean(success) * (1 - np.mean(success)) / len(group))),
            }
        )
    return out


def write_csvs(rows: list[dict], agg: list[dict]) -> None:
    with EPISODE_CSV.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)
    with AGG_CSV.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(agg[0].keys()))
        writer.writeheader()
        writer.writerows(agg)


def plot_bars(agg: list[dict], metric: str, ylabel: str, path: Path) -> None:
    data = {(row["mode"], row["controller"]): row for row in agg}
    x = np.arange(len(MODES))
    width = 0.13
    colors = {
        "nominal_offline": "#777777",
        "robust_low_gain": "#4C78A8",
        "frozen_start_calibration": "#F58518",
        "residual_bias": "#54A24B",
        "calibration_state": "#B279A2",
        "oracle": "#E45756",
    }
    labels = {
        "nominal_offline": "Nominal",
        "robust_low_gain": "Low gain",
        "frozen_start_calibration": "Frozen start",
        "residual_bias": "Residual",
        "calibration_state": "CSC",
        "oracle": "Oracle",
    }
    fig, ax = plt.subplots(figsize=(8.0, 3.0))
    for i, controller in enumerate(CONTROLLERS):
        vals = [float(data[(mode, controller)][metric]) for mode in MODES]
        ax.bar(x + (i - 2.5) * width, vals, width, label=labels[controller], color=colors[controller])
    ax.set_xticks(x)
    ax.set_xticklabels(["static", "walk", "bump", "severe"], fontsize=9)
    ax.set_ylabel(ylabel)
    ax.grid(axis="y", alpha=0.25)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.legend(ncol=3, fontsize=8, frameon=False)
    fig.tight_layout()
    fig.savefig(path)
    plt.close(fig)


def write_summary(agg: list[dict]) -> None:
    lines = [
        "# Calibration-State Evidence",
        "",
        f"Episodes per mode/controller: {N_EPISODES}. Maximum steps: {MAX_STEPS}. Success threshold: {SUCCESS_EPS}.",
        "",
        "## Aggregate Results",
        "",
        "| Mode | Controller | Success | Mean final error | Path efficiency | Mean calibration error |",
        "| --- | --- | ---: | ---: | ---: | ---: |",
    ]
    for row in agg:
        lines.append(
            "| {mode} | {controller} | {success_rate:.3f} | {final_error_mean:.4f} | {path_efficiency_mean:.3f} | {mean_recent_calibration_error:.3f} |".format(
                **row
            )
        )

    by_mode = {mode: {} for mode in MODES}
    for row in agg:
        by_mode[row["mode"]][row["controller"]] = row

    lines += [
        "",
        "## CSC Advantage Over Strongest Non-Oracle Baseline",
        "",
        "| Mode | Best non-oracle baseline | Baseline success | CSC success | CSC final-error change |",
        "| --- | --- | ---: | ---: | ---: |",
    ]
    for mode in MODES:
        baselines = [
            by_mode[mode][c]
            for c in CONTROLLERS
            if c not in ("calibration_state", "oracle")
        ]
        best = max(baselines, key=lambda r: (r["success_rate"], -r["final_error_mean"]))
        csc = by_mode[mode]["calibration_state"]
        change = csc["final_error_mean"] - best["final_error_mean"]
        lines.append(
            f"| {mode} | {best['controller']} | {best['success_rate']:.3f} | {csc['success_rate']:.3f} | {change:.4f} |"
        )

    lines += [
        "",
        "## Interpretation",
        "- The frozen-start baseline is intentionally privileged: it knows the initial calibration matrix but cannot update after drift.",
        "- CSC is expected to beat frozen-start most clearly when the calibration map changes during the rollout.",
        "- If CSC fails in a mode, that is evidence that the drift is too fast, poorly conditioned, or insufficiently observable from task residuals.",
    ]
    SUMMARY_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")


def run_windowed_context_baseline() -> list[dict]:
    rows: list[dict] = []
    total = len(MODES) * N_EPISODES
    done = 0
    for mode in MODES:
        for episode_idx in range(N_EPISODES):
            rows.append(run_episode(mode, "windowed_sysid", episode_idx))
            done += 1
        PROGRESS.write_text(
            json.dumps(
                {
                    "done": done,
                    "total": total,
                    "mode": mode,
                    "controller": "windowed_sysid",
                    "stage": "windowed_context_baseline",
                },
                indent=2,
            ),
            encoding="utf-8",
        )
        print(f"[sim] windowed_sysid / {mode}: {done}/{total}")
    return aggregate(rows)


def write_windowed_context_outputs(agg: list[dict], windowed_agg: list[dict]) -> None:
    combined = {(row["mode"], row["controller"]): row for row in agg}
    for row in windowed_agg:
        combined[(row["mode"], row["controller"])] = row

    with WINDOWED_CSV.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(windowed_agg[0].keys()))
        writer.writeheader()
        writer.writerows(windowed_agg)

    table_lines = [
        r"\begin{table}[t]",
        r"\caption{V2 online system-identification baseline. Windowed SysID fits the local action-observation map from the most recent 14 transitions and feeds the fitted map to the same inverse controller. It is a hostile baseline for the estimator, but it still carries calibration as policy state.}",
        r"\label{tab:windowed-sysid}",
        r"\centering",
        r"\begin{tabular}{lrrrr}",
        r"\toprule",
        r"Mode & Frozen start & Windowed SysID & CSC & Oracle \\",
        r"\midrule",
    ]
    md_lines = [
        "",
        "## V2 Windowed Online System-ID Baseline",
        "",
        "Windowed SysID fits the local action-observation map from the most recent 14 transitions and uses the same inverse-control interface as CSC. This is a stronger hostile baseline than residual-bias correction because it also carries a calibration estimate inside the policy loop.",
        "",
        "| Mode | Frozen start | Windowed SysID | CSC | Oracle |",
        "| --- | ---: | ---: | ---: | ---: |",
    ]
    for mode in MODES:
        frozen = combined[(mode, "frozen_start_calibration")]["success_rate"]
        windowed = combined[(mode, "windowed_sysid")]["success_rate"]
        csc = combined[(mode, "calibration_state")]["success_rate"]
        oracle = combined[(mode, "oracle")]["success_rate"]
        label = mode.replace("_", " ")
        table_lines.append(f"{label} & {frozen:.3f} & {windowed:.3f} & {csc:.3f} & {oracle:.3f} \\\\")
        md_lines.append(f"| {label} | {frozen:.3f} | {windowed:.3f} | {csc:.3f} | {oracle:.3f} |")
    table_lines.extend([r"\bottomrule", r"\end{tabular}", r"\end{table}"])
    WINDOWED_TABLE.write_text("\n".join(table_lines) + "\n", encoding="utf-8")

    existing = SUMMARY_MD.read_text(encoding="utf-8")
    SUMMARY_MD.write_text(existing.rstrip() + "\n" + "\n".join(md_lines) + "\n", encoding="utf-8")


def main() -> None:
    rows: list[dict] = []
    total = len(MODES) * len(CONTROLLERS) * N_EPISODES
    done = 0
    for mode in MODES:
        for controller in CONTROLLERS:
            for episode_idx in range(N_EPISODES):
                rows.append(run_episode(mode, controller, episode_idx))
                done += 1
            PROGRESS.write_text(
                json.dumps(
                    {
                        "done": done,
                        "total": total,
                        "mode": mode,
                        "controller": controller,
                    },
                    indent=2,
                ),
                encoding="utf-8",
            )
            print(f"[sim] {mode} / {controller}: {done}/{total}")

    agg = aggregate(rows)
    write_csvs(rows, agg)
    plot_bars(agg, "success_rate", "success rate", PLOT_SUCCESS)
    plot_bars(agg, "final_error_mean", "mean final error", PLOT_ERROR)
    write_summary(agg)
    windowed_agg = run_windowed_context_baseline()
    write_windowed_context_outputs(agg, windowed_agg)
    print(f"[sim] wrote {EPISODE_CSV}")
    print(f"[sim] wrote {AGG_CSV}")
    print(f"[sim] wrote {WINDOWED_CSV}")
    print(f"[sim] wrote {PLOT_SUCCESS}")
    print(f"[sim] wrote {PLOT_ERROR}")


if __name__ == "__main__":
    main()
