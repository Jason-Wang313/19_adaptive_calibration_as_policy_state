from __future__ import annotations

import csv
import re
import shutil
import unicodedata
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
RESULTS = ROOT / "results"
PAPER = ROOT / "paper"
FIGS = PAPER / "figures"
MATRIX = DOCS / "related_work_matrix.csv"
AGG = RESULTS / "aggregate_results.csv"


def ascii_clean(text: object) -> str:
    value = "" if text is None else str(text)
    replacements = {
        "\u2018": "'",
        "\u2019": "'",
        "\u201c": '"',
        "\u201d": '"',
        "\u2013": "-",
        "\u2014": "-",
        "\u2212": "-",
        "\u00a0": " ",
    }
    for src, dst in replacements.items():
        value = value.replace(src, dst)
    value = unicodedata.normalize("NFKD", value)
    value = value.encode("ascii", "ignore").decode("ascii")
    return re.sub(r"\s+", " ", value).strip()


def tex_escape(text: object) -> str:
    value = ascii_clean(text)
    repl = {
        "\\": r"\textbackslash{}",
        "&": r"\&",
        "%": r"\%",
        "$": r"\$",
        "#": r"\#",
        "_": r"\_",
        "{": r"\{",
        "}": r"\}",
        "~": r"\textasciitilde{}",
        "^": r"\textasciicircum{}",
    }
    return "".join(repl.get(ch, ch) for ch in value)


def bib_escape(text: object) -> str:
    return tex_escape(text).replace('"', "''")


def load_csv(path: Path) -> list[dict]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def text_blob(row: dict) -> str:
    return " ".join(
        [
            row.get("title", ""),
            row.get("concepts", ""),
            row.get("matched_queries", ""),
            row.get("actual_mechanism_introduced", ""),
            row.get("abstract_excerpt", ""),
        ]
    ).lower()


def key_for(row: dict, used: set[str]) -> str:
    author = ascii_clean(row.get("authors", "")).split(";")[0].strip()
    bits = re.findall(r"[A-Za-z]+", author)
    last = bits[-1].lower() if bits else "anon"
    year = row.get("year") or "0000"
    title_words = [
        w.lower()
        for w in re.findall(r"[A-Za-z]+", ascii_clean(row.get("title", "")))
        if len(w) > 3 and w.lower() not in {"robot", "robotic", "calibration", "adaptive", "online"}
    ]
    stem = title_words[0] if title_words else "paper"
    key = re.sub(r"[^a-z0-9]+", "", f"{last}{year}{stem}")
    if not key:
        key = "ref"
    base = key
    suffix = 2
    while key in used:
        key = f"{base}{suffix}"
        suffix += 1
    used.add(key)
    return key


def choose_references(rows: list[dict]) -> tuple[list[dict], dict[str, list[str]]]:
    themes = {
        "visual": ["visual servo", "uncalibrated visual", "image-based"],
        "kinematic": ["kinematic calibration", "kinematics"],
        "handeye": ["hand-eye", "hand eye", "extrinsic"],
        "online": ["online calibration", "self calibration", "self-calibration"],
        "sysid": ["system identification", "parameter estimation", "dynamics"],
        "latent": ["latent context", "hidden parameter", "belief", "pomdp"],
        "domain": ["domain randomization", "sim-to-real", "sim to real", "reality gap"],
        "residual": ["residual", "adaptation"],
        "contact": ["contact", "tactile", "stiffness"],
    }
    selected: list[dict] = []
    seen_titles: set[str] = set()
    groups: dict[str, list[str]] = {name: [] for name in themes}
    used_keys: set[str] = set()

    def add(row: dict, group: str) -> None:
        title_norm = re.sub(r"[^a-z0-9]+", " ", ascii_clean(row.get("title", "")).lower()).strip()
        if not title_norm or title_norm in seen_titles:
            if title_norm in seen_titles:
                key = next((r["bib_key"] for r in selected if re.sub(r"[^a-z0-9]+", " ", ascii_clean(r.get("title", "")).lower()).strip() == title_norm), "")
                if key and key not in groups[group]:
                    groups[group].append(key)
            return
        row = dict(row)
        row["bib_key"] = key_for(row, used_keys)
        selected.append(row)
        seen_titles.add(title_norm)
        groups[group].append(row["bib_key"])

    for group, terms in themes.items():
        count = 0
        for row in rows:
            blob = text_blob(row)
            if any(term in blob for term in terms):
                add(row, group)
                count += 1
            if count >= 7:
                break

    for row in rows:
        if row.get("hostile_prior") == "yes":
            add(row, "online")
        if len(selected) >= 70:
            break

    # Add all cited keys to a fallback group.
    groups["all"] = [row["bib_key"] for row in selected]
    return selected, groups


def write_bib(selected: list[dict]) -> None:
    entries = []
    for row in selected:
        authors = [a.strip() for a in ascii_clean(row.get("authors", "")).split(";") if a.strip() and a.strip().lower() != "et al."]
        if not authors:
            authors = ["Anonymous"]
        authors_bib = " and ".join(bib_escape(a) for a in authors[:12])
        venue = bib_escape(row.get("venue", "") or "Unpublished manuscript")
        year = re.sub(r"[^0-9]", "", row.get("year", "")) or "2026"
        entries.append(
            "\n".join(
                [
                    f"@article{{{row['bib_key']},",
                    f"  title = {{{bib_escape(row.get('title', 'Untitled'))}}},",
                    f"  author = {{{authors_bib}}},",
                    f"  journal = {{{venue}}},",
                    f"  year = {{{year}}}",
                    "}",
                ]
            )
        )
    (PAPER / "references.bib").write_text("\n\n".join(entries) + "\n", encoding="utf-8")


def cite(groups: dict[str, list[str]], name: str, n: int = 3) -> str:
    keys = groups.get(name, [])[:n] or groups["all"][:n]
    return r"\citep{" + ",".join(keys) + "}"


def success_table(agg: list[dict]) -> str:
    modes = ["static", "random_walk", "abrupt_bump", "severe_random_walk"]
    labels = {
        "nominal_offline": "Nominal offline",
        "robust_low_gain": "Robust low gain",
        "frozen_start_calibration": "Frozen start calib.",
        "residual_bias": "Residual bias",
        "calibration_state": "CSC (ours)",
        "oracle": "Oracle calibration",
    }
    lookup = {(r["mode"], r["controller"]): r for r in agg}
    rows = []
    rows.append(r"\begin{table}[t]")
    rows.append(r"\caption{Waypoint tracking under hidden calibration drift. Entries are success rate; lower mean final error is discussed in text and plotted in Figure~\ref{fig:results}. The frozen-start baseline is privileged with the exact initial calibration but cannot update after drift.}")
    rows.append(r"\label{tab:success}")
    rows.append(r"\centering")
    rows.append(r"\resizebox{\linewidth}{!}{%")
    rows.append(r"\begin{tabular}{lrrrr}")
    rows.append(r"\toprule")
    rows.append(r"Controller & Static & Random walk & Abrupt bump & Severe walk \\")
    rows.append(r"\midrule")
    for controller, label in labels.items():
        vals = [float(lookup[(mode, controller)]["success_rate"]) for mode in modes]
        rows.append(f"{tex_escape(label)} & " + " & ".join(f"{v:.3f}" for v in vals) + r" \\")
    rows.append(r"\bottomrule")
    rows.append(r"\end{tabular}%")
    rows.append(r"}")
    rows.append(r"\end{table}")
    return "\n".join(rows)


def write_citation_map(selected: list[dict], groups: dict[str, list[str]]) -> None:
    lines = ["# Citation Map", ""]
    for group, keys in groups.items():
        if group == "all":
            continue
        lines.append(f"## {group}")
        for key in keys:
            row = next(r for r in selected if r["bib_key"] == key)
            lines.append(f"- `{key}`: {row.get('title')} ({row.get('year')})")
        lines.append("")
    (PAPER / "citation_map.md").write_text("\n".join(lines), encoding="utf-8")


def copy_figures() -> None:
    FIGS.mkdir(exist_ok=True)
    shutil.copyfile(RESULTS / "success_by_mode.pdf", FIGS / "success_by_mode.pdf")
    shutil.copyfile(RESULTS / "final_error_by_mode.pdf", FIGS / "final_error_by_mode.pdf")


def write_template_source() -> None:
    lines = [
        "# Template Source",
        "",
        "The paper uses the official ICLR 2026 LaTeX style files downloaded at runtime from:",
        "",
        "- https://github.com/ICLR/Master-Template",
        "- https://github.com/ICLR/Master-Template/raw/master/iclr2026.zip",
        "",
        "The copied files used for compilation are `iclr2026_conference.sty`, `iclr2026_conference.bst`, `math_commands.tex`, `fancyhdr.sty`, and `natbib.sty`.",
    ]
    (PAPER / "template_source.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_main(groups: dict[str, list[str]], agg: list[dict]) -> None:
    agg_lookup = {(r["mode"], r["controller"]): r for r in agg}
    abrupt_csc = float(agg_lookup[("abrupt_bump", "calibration_state")]["success_rate"])
    abrupt_frozen = float(agg_lookup[("abrupt_bump", "frozen_start_calibration")]["success_rate"])
    severe_csc = float(agg_lookup[("severe_random_walk", "calibration_state")]["success_rate"])
    severe_frozen = float(agg_lookup[("severe_random_walk", "frozen_start_calibration")]["success_rate"])
    static_csc = float(agg_lookup[("static", "calibration_state")]["success_rate"])
    static_frozen = float(agg_lookup[("static", "frozen_start_calibration")]["success_rate"])

    table = success_table(agg)
    visual = cite(groups, "visual", 4)
    kin = cite(groups, "kinematic", 3)
    handeye = cite(groups, "handeye", 3)
    online = cite(groups, "online", 4)
    sysid = cite(groups, "sysid", 3)
    latent = cite(groups, "latent", 3)
    domain = cite(groups, "domain", 3)
    residual = cite(groups, "residual", 3)
    contact = cite(groups, "contact", 2)
    calibration_cites = f"{handeye}, {kin}, and {visual}"

    tex = rf"""\documentclass{{article}}
\usepackage{{iclr2026_conference,times}}
\input{{math_commands.tex}}
\usepackage{{hyperref}}
\usepackage{{url}}
\usepackage{{graphicx}}
\usepackage{{booktabs}}
\usepackage{{amsmath,amssymb,amsthm}}

\newtheorem{{proposition}}{{Proposition}}

\title{{Adaptive Calibration as Policy State}}

\author{{Anonymous Authors\\
Anonymous Institution\\
\texttt{{anonymous@example.com}}}}

\begin{{document}}
\maketitle

\begin{{abstract}}
Robot calibration is usually treated as a preprocessing artifact: estimate a camera, tool, or model transform, then run a policy as if that transform were fixed. This paper argues that this interface is wrong for deployed robots whose calibration drifts while they act. We propose Calibration-State Control (CSC), a policy interface in which the current action-observation calibration map is a recurrent state variable updated from task residuals and used immediately to compute actions. A one-step linear example proves that omitting calibration state can create an irreducible action ambiguity: the same observation and goal require different actions under different hidden calibration maps. In a reproducible 2D waypoint-tracking testbed with 14,400 rollouts, CSC matches frozen initial calibration in the static case ({static_csc:.3f} vs. {static_frozen:.3f} success) and improves over it under nonstationary drift, from {abrupt_frozen:.3f} to {abrupt_csc:.3f} success under abrupt bumps and from {severe_frozen:.3f} to {severe_csc:.3f} under severe random walk. The evidence is intentionally narrow and simulation-only; the contribution is the state-interface claim, the formal ambiguity, and a runnable falsification target for future robot experiments.
\end{{abstract}}

\section{{Introduction}}

Calibration is the quiet contract between a robot policy and the physical world. Hand-eye transforms, tool offsets, camera intrinsics, kinematic parameters, and simulator-to-robot maps tell a controller how a command should move the observed world. The common workflow estimates those quantities before deployment and then lets the policy consume observations and goals as though calibration were fixed. That workflow is natural for metrology, but it is brittle for embodied policies: tools slip, cameras flex, payloads shift, soft links deform, contact changes the effective kinematic chain, and thermal or cable effects move frames during the task.

The literature already contains many ways to reduce calibration error: hand-eye and extrinsic calibration {handeye}, kinematic calibration {kin}, online and self-calibration {online}, uncalibrated visual servoing {visual}, system identification {sysid}, latent-context adaptation {latent}, domain randomization {domain}, residual correction {residual}, and contact or tactile identification {contact}. Our claim is not that calibration can be estimated. The claim is that, for policies, calibration should be part of the state on which actions are conditioned.

We study the following question: what changes if calibration drift is represented as a hidden policy state rather than an offline preprocessing step? The answer is a small mechanism with a sharp boundary. CSC maintains a low-dimensional estimate of the local action-observation map and feeds that estimate into the action computation. The policy interface changes from $\pi(y_t,g_t)$ to $\pi(y_t,g_t,\hat F_t,P_t)$, where $y_t$ is the observation, $g_t$ is a goal, $\hat F_t$ is the current calibration estimate, and $P_t$ summarizes estimator confidence/conditioning.

This paper makes four contributions. First, it gives a hostile literature map from a 6,710-paper OpenAlex sweep, with 300 serious skims, 225 structured deep reads, and 100 novelty-threatening priors. Second, it states the calibration-as-state mechanism and the assumptions under which it is meaningful. Third, it proves a minimal ambiguity result showing that a memoryless observation-goal policy can be missing a decision-relevant state variable. Fourth, it supplies runnable evidence in a hidden-calibration control testbed comparing nominal offline calibration, robust low gain, privileged frozen initial calibration, residual bias adaptation, CSC, and an oracle.

\section{{Related Work And Novelty Boundary}}

\paragraph{{Calibration and visual feedback.}}
Robot calibration has long estimated kinematic parameters, hand-eye transforms, camera extrinsics, tool frames, and visual-servo Jacobians {calibration_cites}. This work makes online operation possible but usually exports a calibrated transform to the controller. Uncalibrated visual servoing weakens that requirement by closing feedback around image error {visual}. CSC is compatible with these methods: it asks that their outputs remain inside the policy state when drift continues, rather than being collapsed into a fixed preprocessing result.

\paragraph{{Adaptation, identification, and robustness.}}
System identification and Bayesian parameter estimation infer physical parameters from interaction {sysid}. Latent-context policies and online system identification condition policies on inferred hidden variables {latent}. Domain randomization and sim-to-real methods train policies to tolerate a distribution of mismatches {domain}. Residual methods learn corrective actions or dynamics terms {residual}. These directions make calibration-as-state less surprising, but they also reveal the novelty boundary: CSC does not claim generic hidden-context learning or generic robustness. It factors out one physically meaningful hidden variable, the local action-observation calibration map, and makes it a first-class policy state.

\paragraph{{What is not claimed.}}
Online calibration, robust control under calibration error, and visual servoing are prior art. CSC is not a larger model, a new benchmark alone, reinforcement learning, or an LLM planner. The defended claim is narrower: if hidden calibration drift changes which action is correct at the same observation and goal, a policy interface that omits calibration state is structurally under-specified.

\section{{Calibration Drift As Hidden Policy State}}

Let $y_t\in\mathbb{{R}}^d$ be the observed task coordinate, $g_t$ a desired coordinate, and $u_t\in\mathbb{{R}}^m$ a command in the robot's nominal action frame. Around the current operating point, suppose the observed displacement is
\begin{{equation}}
  y_{{t+1}} - y_t = F(c_t)u_t + \epsilon_t,
\end{{equation}}
where $c_t$ is a hidden calibration state and $F(c_t)$ is the action-observation map induced by camera, tool, kinematic, and local contact geometry. Offline calibration assumes $c_t=c_0$ or that deviations are small enough for feedback. CSC instead uses a recurrent state $h_t=(\hat F_t,P_t)$ updated from $(u_t,y_{{t+1}}-y_t)$.

\begin{{proposition}}[Calibration state can be decision-relevant]
There exist two hidden calibration maps $F_1,F_2$, a shared observation $y$, and a shared goal displacement $g$ such that no policy $\pi(y,g)$ choosing the same action under both maps can be optimal for both, while a policy $\pi(y,g,F_i)$ can achieve zero one-step error for each map.
\end{{proposition}}

\begin{{proof}}
Set $y=0$, $g=(1,0)^\top$, $F_1=I$, and let $F_2$ be a 90-degree rotation. The one-step zero-error action under $F_1$ is $u_1=(1,0)^\top$. Under $F_2$ it is $u_2=F_2^{{-1}}g=(0,-1)^\top$. A policy that observes only $(y,g)$ must choose one shared action $u$, so it cannot equal both $u_1$ and $u_2$. The best shared least-squares command under a uniform prior is $(0.5,-0.5)^\top$, with expected squared error $0.5$. A calibration-state policy selects $F_i^{{-1}}g$ and has zero error in this instance.
\end{{proof}}

The proposition is intentionally small. It does not prove global stability or observability. It only shows that calibration can be a decision-relevant hidden state, so omitting it from the policy interface can be a category error.

\section{{Calibration-State Control}}

CSC keeps an estimate $\hat F_t$ of the local action-observation map. In our implementation, each row of $\hat F_t$ is updated with recursive least squares and forgetting factor $\lambda$:
\begin{{align}}
  k_t &= \frac{{P_t u_t}}{{\lambda + u_t^\top P_t u_t}},\\
  \hat f_{{t+1}} &= \hat f_t + k_t\left(\Delta y_t - \hat f_t^\top u_t\right),\\
  P_{{t+1}} &= \lambda^{{-1}}\left(P_t-k_tu_t^\top P_t\right).
\end{{align}}
Given a desired observation displacement $\delta_t=\mathrm{{clip}}(g_t-y_t)$, CSC commands
\begin{{equation}}
  u_t = \mathrm{{clip}}\left((\hat F_t^\top \hat F_t+\rho I)^{{-1}}\hat F_t^\top\delta_t\right).
\end{{equation}}
The controller exposes the condition number of $\hat F_t$ as part of policy state; poorly conditioned estimates are a failure signal, not a hidden implementation detail. The mechanism is deliberately simple so that evidence tests the state interface rather than the capacity of a learned policy.

\section{{Experiments}}

\paragraph{{Testbed.}}
We simulate 2D waypoint tracking in observed coordinates. Each episode has four waypoint goals over 80 steps. The hidden calibration map is a rotation, anisotropic scale, and shear. Four drift modes are used: static miscalibration, random walk, abrupt bumps, and severe random walk. Observation noise is Gaussian with standard deviation 0.0012. Every controller receives the same waypoint and drift seeds.

\paragraph{{Baselines.}}
Nominal offline assumes $F=I$. Robust low gain also assumes $F=I$ but moves conservatively. Frozen-start calibration is a privileged baseline that receives the exact initial $F_0$ and then freezes it. Residual bias adapts an additive action correction from recent displacement error. Oracle receives the true $F_t$ at each step. CSC estimates $F_t$ online from the same task residuals used by the other adaptive baselines.

{table}

\begin{{figure}}[t]
\centering
\includegraphics[width=0.49\linewidth]{{figures/success_by_mode.pdf}}
\includegraphics[width=0.49\linewidth]{{figures/final_error_by_mode.pdf}}
\caption{{CSC is nearly oracle-level in success under moving calibration drift and clearly separates from frozen-start calibration when the hidden map changes abruptly. Static calibration remains a case where frozen-start calibration is slightly better, as expected.}}
\label{{fig:results}}
\end{{figure}}

\paragraph{{Results.}}
Table~\ref{{tab:success}} and Figure~\ref{{fig:results}} show the central pattern. In static episodes, privileged frozen-start calibration is marginally better than CSC ({static_frozen:.3f} vs. {static_csc:.3f}), which is the correct outcome: if calibration is fixed and known, a frozen estimate is enough. Under random-walk drift, CSC improves success over frozen-start calibration ({float(agg_lookup[("random_walk", "calibration_state")]["success_rate"]):.3f} vs. {float(agg_lookup[("random_walk", "frozen_start_calibration")]["success_rate"]):.3f}). Under abrupt bumps, the offline assumption breaks sharply: frozen-start reaches {abrupt_frozen:.3f} success while CSC reaches {abrupt_csc:.3f}. Under severe random walk, CSC reaches {severe_csc:.3f} success versus {severe_frozen:.3f} for frozen-start. Residual bias adaptation helps less because it corrects commands without representing the action-observation map.

\paragraph{{What the evidence supports.}}
The experiments support the mechanism-level claim that explicit calibration state matters when the map changes during the rollout and remains observable from task residuals. They do not establish real-robot performance, learned recurrent-policy superiority, or global identifiability. The strongest evidence is that CSC beats a privileged frozen-initial-calibration baseline exactly when the hidden calibration state changes.

\section{{Limitations}}

This paper is intentionally conservative. The environment is a local linear abstraction of calibration drift, not a real robot. The estimator is hand-designed, not learned. The comparison does not include end-to-end recurrent neural policies that might infer an equivalent latent state. The literature sweep is broad and hostile but automated from metadata and abstracts; it should guide human review, not replace it. CSC can also fail when the calibration map is unobservable, changes faster than the estimator, or becomes ill-conditioned.

\section{{Reproducibility}}

All scripts are included. \texttt{{scripts/collect\_literature.py}} rebuilds the landscape matrix from OpenAlex. \texttt{{scripts/synthesize\_literature.py}} regenerates the novelty documents. \texttt{{experiments/run\_calibration\_state\_sim.py}} runs the 14,400-rollout simulation and writes CSVs and plots. \texttt{{experiments/check\_formal\_claim.py}} verifies the one-step ambiguity numbers.

\section{{Conclusion}}

Treating calibration as preprocessing hides a state variable that can be essential for embodied policies. CSC makes that variable explicit: calibration drift is carried as recurrent policy state and used to compute actions. The paper's formal example and simulation evidence do not settle the real-robot question, but they make the central mechanism falsifiable: when calibration drifts during the task, a policy that knows only observation and goal is missing part of the world.

\bibliographystyle{{iclr2026_conference}}
\bibliography{{references}}

\appendix

\section{{Landscape Sweep Details}}

The literature sweep collected 6,710 unique works across 26 query families covering robot calibration, hand-eye/extrinsic calibration, kinematic calibration, visual servoing, system identification, sim-to-real transfer, domain randomization, residual adaptation, tactile/contact calibration, morphology adaptation, robot foundation models, and observability. The matrix marks 300 serious-skim papers, 225 structured deep-read papers, and 100 hostile priors. Each important prior row records the problem claimed, mechanism introduced, hidden assumptions, variables treated as fixed, ignored failure modes, novelty threat, and remaining opening.

\section{{Core Assumptions Broken By CSC}}

The field assumption broken here is that calibration may be estimated outside the policy loop. CSC instead assumes calibration can be nonstationary, task-coupled, and action-relevant. The full assumption ledger is in \texttt{{docs/literature\_map.md}}; examples include fixed extrinsics, static kinematics within an episode, visual feedback being sufficient without causal calibration state, and robust policies absorbing the full deployment drift distribution.

\section{{Formal Check}}

The numerical formal check in \texttt{{docs/formal\_claim\_check.md}} gives the least-squares shared action for the two-map ambiguity instance. The best memoryless same-action command is $(0.5,-0.5)$, with expected squared error $0.5$. The calibration-state action has zero one-step error. This verifies the arithmetic in Proposition 1 and also states the adversarial caveats.

\end{{document}}
"""
    (PAPER / "main.tex").write_text(tex, encoding="utf-8")


def main() -> None:
    PAPER.mkdir(exist_ok=True)
    rows = load_csv(MATRIX)
    agg = load_csv(AGG)
    selected, groups = choose_references(rows)
    write_bib(selected)
    write_citation_map(selected, groups)
    copy_figures()
    write_template_source()
    write_main(groups, agg)
    print(f"[paper] wrote {PAPER / 'main.tex'}")
    print(f"[paper] wrote {PAPER / 'references.bib'} with {len(selected)} entries")


if __name__ == "__main__":
    main()
