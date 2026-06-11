from __future__ import annotations

import csv
import statistics
from collections import Counter, defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
MATRIX = DOCS / "related_work_matrix.csv"


THESIS = (
    "Calibration drift should be represented as policy state: a robot policy should "
    "carry an online estimate of the current action-observation calibration map and "
    "condition each control action on that estimate, instead of treating calibration "
    "as offline preprocessing or as generic robustness noise."
)

MECHANISM = (
    "Calibration-State Control (CSC): a low-dimensional recurrent state estimates "
    "the local action-to-observation Jacobian with forgetting, exposes that estimate "
    "and its conditioning to the policy, and computes task actions through the current "
    "calibration state. The policy interface changes from pi(observation, goal) to "
    "pi(observation, goal, calibration_state)."
)


ASSUMPTIONS = [
    "A calibration measured before deployment remains valid for the full policy rollout.",
    "Calibration error is small enough to be absorbed by feedback gains.",
    "Calibration drift is independent of the task phase and contact history.",
    "A single robust policy can cover the full calibration-error distribution without knowing the current drift.",
    "Online calibration can be optimized as a separate estimator without changing the control state.",
    "Sensor extrinsics are rigid even under tool changes, payload shifts, heat, and cable motion.",
    "Kinematic parameters are static within an episode.",
    "Dynamics identification and geometric calibration can be separated cleanly.",
    "Visual servo feedback makes explicit geometric state unnecessary.",
    "The robot can execute calibration motions that are independent of the task objective.",
    "Residual policies learn the right correction without representing the physical cause.",
    "Latent-context policies will discover calibration variables without calibration-specific supervision.",
    "Domain randomization support contains the deployment drift.",
    "Calibration uncertainty matters only for planning risk, not for the action itself.",
    "The observation frame and action frame fail independently.",
    "Calibration can be validated from final task success alone.",
    "Estimator convergence is faster than the drift process.",
    "Small action-observation errors stay locally linear around the current pose.",
    "The same calibration state is observable from all useful task trajectories.",
    "Offline benchmarks with fixed camera/robot geometry measure deployment robustness.",
    "End-to-end policies can learn around miscalibration without losing sample efficiency.",
    "The cost of information-gathering motion is negligible.",
    "Calibration is a property of the robot, not of the robot-object-contact system.",
    "A controller's memory should track task state but not metrology state.",
]


DIRECTIONS = [
    (
        "Calibration-State Control",
        "Make calibration a recurrent state variable with a physically interpretable update and use it directly in control.",
        "Breaks the offline-calibration assumption and is testable with a minimal hidden-state control system.",
    ),
    (
        "Task-Embedded Observability",
        "Design task actions whose ordinary residuals also identify calibration drift, without separate calibration routines.",
        "Strong but risks being viewed as active learning unless the mechanism is very specific.",
    ),
    (
        "Calibration-Causal Residuals",
        "Constrain residual policies so corrections factor through explicit calibration causes rather than arbitrary action deltas.",
        "Promising for learning systems but needs a larger learning stack than this paper can honestly validate.",
    ),
    (
        "Drift-Aware Benchmarking",
        "Benchmark policies under nonstationary camera/action map drift.",
        "Useful but forbidden as a benchmark-only contribution and not strong enough alone.",
    ),
]


def load_rows() -> list[dict]:
    with MATRIX.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def md_escape(text: str) -> str:
    return (text or "").replace("|", "\\|").replace("\n", " ").strip()


def short(text: str, limit: int = 220) -> str:
    text = " ".join((text or "").split())
    if len(text) <= limit:
        return text
    return text[: limit - 3].rstrip() + "..."


def top_terms(rows: list[dict], field: str, top_n: int = 12) -> list[tuple[str, int]]:
    counts: Counter[str] = Counter()
    for row in rows:
        for part in row.get(field, "").split(";"):
            item = part.strip()
            if item:
                counts[item] += 1
    return counts.most_common(top_n)


def theme(row: dict) -> str:
    text = f"{row.get('title','')} {row.get('concepts','')} {row.get('actual_mechanism_introduced','')}".lower()
    if "domain randomization" in text or "sim-to-real" in text or "sim to real" in text:
        return "sim-to-real robustness"
    if "hand-eye" in text or "hand eye" in text or "extrinsic" in text:
        return "hand-eye/extrinsic calibration"
    if "kinematic" in text:
        return "kinematic calibration"
    if "visual servo" in text:
        return "visual servoing"
    if "system identification" in text or "dynamics" in text:
        return "system identification"
    if "latent" in text or "context" in text or "hidden" in text or "belief" in text:
        return "hidden-context adaptation"
    if "tactile" in text or "contact" in text:
        return "contact/tactile calibration"
    return "general robot adaptation"


def write_literature_map(rows: list[dict]) -> None:
    serious = [r for r in rows if r.get("serious_skim") == "yes"]
    deep = [r for r in rows if r.get("deep_read") == "yes"]
    hostile = [r for r in rows if r.get("hostile_prior") == "yes"]
    years = [int(r["year"]) for r in rows if r.get("year", "").isdigit() and int(r["year"]) > 0]
    theme_counts = Counter(theme(r) for r in serious)

    lines = [
        "# Literature Map",
        "",
        "## Collection Summary",
        f"- Landscape sweep: {len(rows)} papers in `docs/related_work_matrix.csv`.",
        f"- Serious skim set: {len(serious)} top-ranked papers.",
        f"- Deep-read set: {len(deep)} papers with structured extraction fields.",
        f"- Hostile prior-work set: {len(hostile)} papers selected by novelty-threat score.",
    ]
    if years:
        lines.append(f"- Year range: {min(years)}-{max(years)}, median {statistics.median(years):.0f}.")
    lines += [
        "",
        "## Field Box",
        "The field box is robot calibration under closed-loop embodied policy execution: kinematic, extrinsic, visual-servo, tactile/contact, sim-to-real, and hidden-context adaptation methods that address how model/sensor/action mismatch affects robot behavior.",
        "",
        "## Main Clusters From The Serious Skim",
    ]
    for name, count in theme_counts.most_common():
        lines.append(f"- {name}: {count} papers")

    lines += [
        "",
        "## Hidden Assumptions That May Be False",
    ]
    for i, assumption in enumerate(ASSUMPTIONS, start=1):
        lines.append(f"{i}. {assumption}")

    lines += [
        "",
        "## Candidate Directions That Break Assumptions",
    ]
    for name, core, risk in DIRECTIONS:
        lines.append(f"- **{name}.** {core} {risk}")

    lines += [
        "",
        "## Chosen Direction",
        f"**Thesis.** {THESIS}",
        "",
        f"**Central mechanism.** {MECHANISM}",
        "",
        "## Why This Direction Survived",
        "- It changes the policy state interface, rather than merely adding a larger model, more data, active learning, a verifier, or a benchmark.",
        "- It is directly attacked by online calibration, visual servoing, domain randomization, latent context adaptation, and system identification, so the novelty boundary can be stated sharply.",
        "- It can be tested in a minimal physical-control abstraction where the same observation and goal require different actions under different hidden calibration maps.",
        "- The strongest claim is modest: explicit calibration state can remove an irreducible ambiguity for hidden drift systems when the drift is observable from recent transitions.",
        "",
        "## Repeated Prior-Work Patterns",
    ]
    for field in [
        "hidden_assumptions",
        "variables_treated_as_fixed",
        "failure_modes_ignored",
        "what_it_makes_less_novel",
        "what_it_leaves_open",
    ]:
        lines.append(f"### {field}")
        for term, count in top_terms(serious, field, 10):
            lines.append(f"- {count}: {term}")
        lines.append("")

    lines += [
        "## Important Caveat",
        "The automated sweep uses OpenAlex metadata and abstracts plus rule-based extraction. The deep-read label means structured abstract/metadata review at scale, not full manual PDF reading for every paper. The hostile set is therefore a conservative novelty-threat map to guide claims, not a substitute for final human bibliography review.",
    ]
    (DOCS / "literature_map.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_hostile(rows: list[dict]) -> None:
    hostile = [r for r in rows if r.get("hostile_prior") == "yes"][:100]
    lines = [
        "# Hostile Prior Work",
        "",
        "This set contains the 100 papers that most threaten the novelty of calibration-as-policy-state, selected by calibration/adaptation relevance, hostile keyword overlap, and citation signal.",
        "",
    ]
    for i, row in enumerate(hostile, start=1):
        title = row.get("title", "Untitled")
        year = row.get("year", "")
        authors = row.get("authors", "")
        lines += [
            f"## {i}. {title} ({year})",
            f"- Authors/venue: {short(authors, 180)} / {short(row.get('venue',''), 120)}",
            f"- Problem claimed: {short(row.get('problem_claimed',''), 260)}",
            f"- Actual mechanism introduced: {short(row.get('actual_mechanism_introduced',''), 260)}",
            f"- Hidden assumptions: {short(row.get('hidden_assumptions',''), 300)}",
            f"- Variables treated as fixed: {short(row.get('variables_treated_as_fixed',''), 260)}",
            f"- Failure modes ignored: {short(row.get('failure_modes_ignored',''), 260)}",
            f"- What it makes less novel: {short(row.get('what_it_makes_less_novel',''), 260)}",
            f"- What it leaves open: {short(row.get('what_it_leaves_open',''), 260)}",
            f"- Locator: {row.get('doi') or row.get('url') or row.get('openalex_id')}",
            "",
        ]
    (DOCS / "hostile_prior_work.md").write_text("\n".join(lines), encoding="utf-8")


def write_novelty_boundary(rows: list[dict]) -> None:
    hostile = [r for r in rows if r.get("hostile_prior") == "yes"][:15]
    lines = [
        "# Novelty Boundary Map",
        "",
        "## Not Novel",
        "- Estimating robot-camera extrinsics, hand-eye transforms, tool-center-point offsets, or kinematic parameters.",
        "- Performing online or self-calibration as a separate estimator.",
        "- Robustifying a policy with domain randomization or low feedback gains.",
        "- Inferring generic latent context for robot adaptation.",
        "- Learning residual dynamics or residual actions under model mismatch.",
        "- Using visual servoing to reduce image-space error under calibration noise.",
        "",
        "## Claimed Novel Boundary",
        "- The policy state explicitly includes calibration drift state, not just task state or generic hidden context.",
        "- The calibration state is updated from ordinary task residuals and immediately changes the action map used by the controller.",
        "- The core evidence is not that calibration can be estimated, but that a memoryless policy interface is structurally ambiguous under hidden calibration drift.",
        "- The paper studies when a calibration-state interface beats offline calibration, robust low-gain control, and residual correction at equal task information.",
        "",
        "## Closest Hostile Priors",
    ]
    for row in hostile:
        lines.append(f"- {row.get('title')} ({row.get('year')}): {short(row.get('what_it_makes_less_novel',''), 180)} Leaves open: {short(row.get('what_it_leaves_open',''), 180)}")
    lines += [
        "",
        "## Boundary Conditions",
        "- If calibration drift is unobservable from recent transitions, CSC should not claim recovery; it can only expose uncertainty/conditioning and degrade gracefully.",
        "- If feedback rates are high enough and drift is tiny, visual servoing or robust low-gain control may be sufficient.",
        "- If a learned latent policy reliably discovers the same low-dimensional variable, the novelty shifts from representation to interpretability, sample efficiency, and controllability.",
        "- If deployment drift stays inside the domain-randomized support, explicit state may be unnecessary for success, though it can still improve path efficiency.",
    ]
    (DOCS / "novelty_boundary_map.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_decision() -> None:
    lines = [
        "# Novelty Decision",
        "",
        "## Decision",
        "Proceed with **Calibration-State Control (CSC)**.",
        "",
        "## Chosen Thesis",
        THESIS,
        "",
        "## New Central Mechanism",
        MECHANISM,
        "",
        "## Why Not The Weaker Alternatives",
        "- Bigger model: the contribution is a changed state variable and control interface, not model capacity.",
        "- Better data: the testbed uses the same rollouts for all methods; the difference is whether calibration is represented.",
        "- New benchmark only: the simulation is evidence for a mechanism, not the contribution by itself.",
        "- Add uncertainty: uncertainty is not the core; the core is a calibration-state channel that changes the action map.",
        "- Add active learning: no separate information-gathering policy is claimed.",
        "- Add verifier: no post-hoc checker is used.",
        "- Combine modules: the estimator/controller coupling is defined around one physical hidden state, not a loose pipeline.",
        "- LLM planner/RL: neither is used.",
        "",
        "## Minimum Defensible Claim",
        "For control systems where observation changes are governed by a hidden, slowly drifting action-observation calibration map, a policy that receives only current observation and goal is missing a decision-relevant state variable. An explicit calibration-state interface can reduce final error and path inefficiency when the map is observable from recent action-observation residuals.",
        "",
        "## Unsupported Or Future Claims",
        "- No claim yet that CSC outperforms end-to-end recurrent neural policies on real robots.",
        "- No claim yet that the estimator is globally identifiable under arbitrary robot tasks.",
        "- No claim yet that calibration state is sufficient for all sim-to-real mismatch.",
    ]
    (DOCS / "novelty_decision.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_claims() -> None:
    lines = [
        "# Claims",
        "",
        "## Supported By Formal Argument",
        "- Hidden calibration can be decision-relevant: in a linear action-observation system, two hidden calibration maps can produce the same current observation and goal but require different optimal actions.",
        "- A memoryless policy that omits calibration state cannot be simultaneously optimal for both hidden maps at that shared observation-goal pair.",
        "",
        "## Supported By Runnable Evidence If Experiments Pass",
        "- In the 2D drift-control testbed, explicit calibration-state control should improve success, final error, and path efficiency over offline calibration, robust low-gain control, and a simple residual-bias adapter.",
        "- The advantage should be largest under abrupt or random-walk drift and smaller under static mild miscalibration.",
        "",
        "## Boundary Claims",
        "- CSC helps only when the hidden calibration map is at least locally observable from recent transitions.",
        "- CSC is not a replacement for hand-eye calibration, kinematic calibration, or visual servoing; it changes how their outputs enter the policy loop.",
        "- CSC does not prove that all robot adaptation should be physically factorized, only that calibration drift is a strong case where factorization matters.",
        "",
        "## Unsupported Claims To Avoid",
        "- Do not claim real-robot validation.",
        "- Do not claim superiority over all recurrent learned policies.",
        "- Do not claim novelty for online calibration itself.",
        "- Do not claim global observability or stability beyond the simplified setting.",
    ]
    (DOCS / "claims.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_reviewer_attacks(rows: list[dict]) -> None:
    hostile = [r for r in rows if r.get("hostile_prior") == "yes"][:8]
    lines = [
        "# Reviewer Attacks",
        "",
        "1. **This is just online calibration.**",
        "   Response: the paper must emphasize that online calibration is prior art; the new part is the policy-state interface and the impossibility/evidence that omitting this state creates action ambiguity.",
        "2. **This is just system identification or latent context.**",
        "   Response: CSC is a physical calibration channel with a defined action-observation Jacobian and update rule; generic latent context is a hostile baseline/related class, not the claimed novelty.",
        "3. **Visual servoing already handles calibration error.**",
        "   Response: servoing closes feedback around error but may not represent the hidden action map; experiments should include feedback baselines and state when servoing is sufficient.",
        "4. **The method is a hand-designed estimator, not a learning paper.**",
        "   Response: the paper should be framed as embodied policy-state design; ICLR relevance comes from state representation for robot policies and sim-to-real adaptation.",
        "5. **Toy simulation is too small.**",
        "   Response: the testbed supports the mechanism and formal claim; paper-readiness may be workshop/revise unless larger hardware or learned-policy experiments are added.",
        "6. **Domain randomization can cover this.**",
        "   Response: compare against robust low-gain/randomized-style baselines and claim efficiency/ambiguity, not universal dominance.",
        "7. **The calibration state may be unobservable.**",
        "   Response: explicitly state observability conditions and include failure cases/conditioning diagnostics.",
        "8. **The literature sweep is automated.**",
        "   Response: mark it as broad abstract-level hostile mapping and keep claims conservative.",
        "",
        "## Specific Hostile Papers To Recheck Manually",
    ]
    for row in hostile:
        lines.append(f"- {row.get('title')} ({row.get('year')}): {short(row.get('actual_mechanism_introduced',''), 180)}")
    (DOCS / "reviewer_attacks.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    rows = load_rows()
    write_literature_map(rows)
    write_hostile(rows)
    write_novelty_boundary(rows)
    write_decision()
    write_claims()
    write_reviewer_attacks(rows)
    print(f"[synthesis] wrote literature docs from {len(rows)} rows")


if __name__ == "__main__":
    main()
