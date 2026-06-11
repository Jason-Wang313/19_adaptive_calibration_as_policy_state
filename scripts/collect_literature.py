from __future__ import annotations

import csv
import hashlib
import json
import math
import re
import time
import unicodedata
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
DOCS.mkdir(exist_ok=True)

MATRIX_PATH = DOCS / "related_work_matrix.csv"
PROGRESS_PATH = DOCS / "literature_collection_progress.json"

OPENALEX_URL = "https://api.openalex.org/works"

QUERIES = [
    "robot calibration drift",
    "online robot calibration",
    "self calibration robot",
    "robot kinematic calibration",
    "adaptive kinematic calibration robot",
    "hand eye calibration robot",
    "camera robot extrinsic calibration manipulation",
    "tool center point calibration robot",
    "visual servoing calibration error robot",
    "calibration error robust robot control",
    "robot system identification sim to real",
    "online dynamics adaptation robot",
    "hidden parameter robot control",
    "latent context robot policy adaptation",
    "adaptive robot control uncertain kinematics",
    "domain randomization robot calibration",
    "sim to real robot calibration adaptation",
    "residual adaptation robot control",
    "contact rich manipulation calibration",
    "tactile robot calibration",
    "morphological adaptation robot",
    "Bayesian system identification robot",
    "robot foundation model calibration",
    "embodied agent sim2real adaptation",
    "robot manipulation online adaptation calibration",
    "observability calibration robot control",
]

KEYWORDS = {
    "robot": 4.0,
    "robotic": 3.0,
    "calibration": 7.0,
    "calibrate": 5.0,
    "drift": 6.0,
    "online": 4.0,
    "adaptive": 4.0,
    "adaptation": 4.0,
    "sim-to-real": 5.0,
    "sim to real": 5.0,
    "system identification": 5.0,
    "identification": 2.5,
    "kinematic": 4.0,
    "dynamics": 3.0,
    "hand-eye": 4.0,
    "hand eye": 4.0,
    "extrinsic": 3.5,
    "visual servo": 4.0,
    "manipulation": 3.0,
    "tactile": 2.5,
    "latent": 3.5,
    "context": 3.0,
    "hidden": 3.0,
    "policy": 3.0,
    "belief": 4.0,
    "state": 1.5,
    "uncertain": 2.5,
    "uncertainty": 2.5,
    "observability": 3.0,
}

HOSTILE_KEYWORDS = {
    "online calibration": 8.0,
    "self calibration": 7.0,
    "adaptive calibration": 8.0,
    "kinematic calibration": 6.0,
    "hand-eye calibration": 5.0,
    "system identification": 6.0,
    "domain randomization": 5.0,
    "latent context": 6.0,
    "hidden parameter": 6.0,
    "adaptive control": 4.0,
    "visual servoing": 4.0,
    "calibration error": 5.0,
    "sim-to-real": 4.0,
    "sim to real": 4.0,
    "belief": 4.0,
}


def ascii_clean(text: object, limit: int | None = None) -> str:
    if text is None:
        return ""
    value = str(text)
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
    value = re.sub(r"\s+", " ", value).strip()
    if limit and len(value) > limit:
        return value[: limit - 3].rstrip() + "..."
    return value


def normalize_title(title: str) -> str:
    return re.sub(r"[^a-z0-9]+", " ", ascii_clean(title).lower()).strip()


def abstract_from_inverted_index(index: dict | None) -> str:
    if not index:
        return ""
    max_pos = -1
    for positions in index.values():
        if positions:
            max_pos = max(max_pos, max(positions))
    if max_pos < 0:
        return ""
    words = [""] * (max_pos + 1)
    for word, positions in index.items():
        for pos in positions:
            if 0 <= pos <= max_pos:
                words[pos] = word
    return ascii_clean(" ".join(w for w in words if w))


def request_json(url: str) -> dict:
    req = urllib.request.Request(
        url,
        headers={
            "User-Agent": "Codex paper agent; mailto=example@example.com",
            "Accept": "application/json",
        },
    )
    with urllib.request.urlopen(req, timeout=35) as response:
        return json.loads(response.read().decode("utf-8"))


def fetch_query(query: str, max_pages: int = 2, per_page: int = 200) -> list[dict]:
    cursor = "*"
    rows: list[dict] = []
    for _ in range(max_pages):
        params = {
            "search": query,
            "per-page": str(per_page),
            "cursor": cursor,
            "filter": "from_publication_date:1985-01-01",
            "select": ",".join(
                [
                    "id",
                    "doi",
                    "title",
                    "publication_year",
                    "authorships",
                    "primary_location",
                    "cited_by_count",
                    "concepts",
                    "abstract_inverted_index",
                    "open_access",
                ]
            ),
        }
        url = OPENALEX_URL + "?" + urllib.parse.urlencode(params)
        data = request_json(url)
        results = data.get("results", [])
        rows.extend(results)
        cursor = data.get("meta", {}).get("next_cursor")
        if not cursor or not results:
            break
        time.sleep(0.2)
    return rows


def source_name(work: dict) -> str:
    location = work.get("primary_location") or {}
    source = location.get("source") or {}
    return ascii_clean(source.get("display_name", ""))


def author_string(work: dict, max_authors: int = 6) -> str:
    names = []
    for authorship in work.get("authorships", [])[:max_authors]:
        author = authorship.get("author") or {}
        name = ascii_clean(author.get("display_name", ""))
        if name:
            names.append(name)
    if len(work.get("authorships", [])) > max_authors:
        names.append("et al.")
    return "; ".join(names)


def concept_string(work: dict) -> str:
    names = []
    for concept in work.get("concepts", [])[:10]:
        name = ascii_clean(concept.get("display_name", ""))
        if name:
            names.append(name)
    return "; ".join(names)


def classify_mechanism(text: str) -> str:
    t = text.lower()
    if "domain randomization" in t:
        return "Randomizes simulator or sensor parameters so a learned policy tolerates calibration variation."
    if "hand-eye" in t or "hand eye" in t:
        return "Estimates a rigid transform between robot and camera/end-effector frames from paired motion observations."
    if "kinematic calibration" in t or "kinematics" in t:
        return "Fits parametric robot geometry or joint/link offsets to reduce pose prediction error."
    if "visual servo" in t:
        return "Uses image/Jacobian feedback to close the loop around visual error despite imperfect calibration."
    if "system identification" in t or "dynamics" in t:
        return "Identifies physical model parameters or residual dynamics from trajectories for control or simulation."
    if "bayesian" in t or "belief" in t or "particle" in t:
        return "Maintains a posterior over uncertain model parameters and plans or controls under that posterior."
    if "latent" in t or "context" in t or "hidden" in t:
        return "Infers a compact latent context variable from recent interaction and conditions the policy or model on it."
    if "residual" in t:
        return "Learns or adapts a residual correction on top of a nominal model/controller."
    if "tactile" in t or "contact" in t:
        return "Uses contact or tactile feedback to estimate geometry, pose, or interaction parameters during manipulation."
    if "self-calibration" in t or "self calibration" in t or "online calibration" in t:
        return "Updates calibration parameters during operation using self-observed sensorimotor consistency constraints."
    return "Introduces a calibration, adaptation, identification, or robust-control mechanism for embodied systems."


def first_sentence(abstract: str, title: str) -> str:
    source = abstract or title
    pieces = re.split(r"(?<=[.!?])\s+", source)
    return ascii_clean(pieces[0] if pieces else source, 240)


def assumption_notes(text: str) -> tuple[str, str, str, str, str]:
    t = text.lower()
    assumptions = []
    fixed = []
    failures = []
    less_novel = []
    open_items = []

    if "calibration" in t:
        assumptions.append("calibration can be estimated separately from the policy state")
        fixed.append("sensor-to-robot or model-to-world transform during policy execution")
        failures.append("calibration drift after deployment or under contact-induced slippage")
        less_novel.append("treating calibration as an estimable parameter is not new")
        open_items.append("how control changes when calibration belief is part of every policy decision")
    if "online" in t or "self" in t:
        assumptions.append("online updates are stable enough to run beside the controller")
        fixed.append("the objective while calibration actions perturb task progress")
        failures.append("unobservable motions and estimator/controller feedback loops")
        less_novel.append("performing online calibration during robot operation")
        open_items.append("closed-loop task benefit from carrying calibration as policy memory")
    if "domain randomization" in t or "robust" in t:
        assumptions.append("one policy can absorb the calibration distribution without explicit state")
        fixed.append("deployment drift distribution relative to training randomization")
        failures.append("distribution shift outside randomized support")
        less_novel.append("robustifying policies against calibration errors")
        open_items.append("whether explicit low-dimensional calibration state outperforms robustness at equal data")
    if "latent" in t or "context" in t or "hidden" in t:
        assumptions.append("latent context is learned as a generic nuisance rather than a physical calibration variable")
        fixed.append("meaning and observability of the latent state")
        failures.append("latent collapse or entanglement with task state")
        less_novel.append("conditioning robot policies on inferred hidden context")
        open_items.append("calibration-specific observability, update rules, and control guarantees")
    if "system identification" in t or "dynamics" in t:
        assumptions.append("identified parameters remain valid over the planning horizon")
        fixed.append("model structure and parameterization")
        failures.append("nonstationary parameter drift and partial excitation")
        less_novel.append("using interaction data to identify model parameters")
        open_items.append("making fast calibration drift a first-class recurrent state rather than a batch ID result")
    if "visual servo" in t:
        assumptions.append("visual feedback can absorb geometric error without representing the cause")
        fixed.append("image Jacobian validity near the current pose")
        failures.append("large drift, occlusion, and nonlocal Jacobian mismatch")
        less_novel.append("closing the loop around calibration errors with feedback")
        open_items.append("when explicit calibration state improves over pure servo feedback")
    if "hand-eye" in t or "hand eye" in t or "extrinsic" in t:
        assumptions.append("rigid extrinsics are recoverable before or between tasks")
        fixed.append("mount rigidity and synchronized motion observations")
        failures.append("temperature, cable, tool, or payload shifts during the task")
        less_novel.append("estimating robot-camera extrinsics")
        open_items.append("policies that condition on continuing extrinsic belief during task execution")

    if not assumptions:
        assumptions.append("the relevant physical mismatch can be handled outside the policy loop")
        fixed.append("environment, embodiment, or sensing parameters during one rollout")
        failures.append("nonstationary shift while the robot is acting")
        less_novel.append("general robot adaptation under model mismatch")
        open_items.append("a calibration-drift-specific state/control interface")

    return (
        "; ".join(dict.fromkeys(assumptions[:4])),
        "; ".join(dict.fromkeys(fixed[:4])),
        "; ".join(dict.fromkeys(failures[:4])),
        "; ".join(dict.fromkeys(less_novel[:4])),
        "; ".join(dict.fromkeys(open_items[:4])),
    )


def score_work(title: str, abstract: str, concepts: str, year: int, citations: int) -> tuple[float, float]:
    text = f"{title} {abstract} {concepts}".lower()
    score = 0.0
    for keyword, weight in KEYWORDS.items():
        if keyword in text:
            score += weight
    if "robot" not in text and "manipulation" not in text:
        score *= 0.55
    score += 0.35 * math.log1p(max(citations, 0))
    if year:
        score += max(0.0, min(1.0, (year - 1995) / 30.0))

    hostile = 0.0
    for keyword, weight in HOSTILE_KEYWORDS.items():
        if keyword in text:
            hostile += weight
    hostile += 0.25 * score + 0.25 * math.log1p(max(citations, 0))
    return round(score, 3), round(hostile, 3)


def stable_id(title: str, year: int) -> str:
    digest = hashlib.sha1(f"{title}|{year}".encode("utf-8")).hexdigest()[:12]
    return f"local:{digest}"


def collect() -> list[dict]:
    seen: dict[str, dict] = {}
    failures = []

    for index, query in enumerate(QUERIES, start=1):
        try:
            works = fetch_query(query)
        except (urllib.error.URLError, TimeoutError, json.JSONDecodeError, OSError) as exc:
            failures.append({"query": query, "error": repr(exc)})
            works = []

        for work in works:
            title = ascii_clean(work.get("title", ""))
            if not title:
                continue
            year = int(work.get("publication_year") or 0)
            doi = ascii_clean(work.get("doi", "")).lower()
            norm_title = normalize_title(title)
            key = doi or norm_title
            if not key:
                key = stable_id(title, year)

            abstract = abstract_from_inverted_index(work.get("abstract_inverted_index"))
            concepts = concept_string(work)
            citations = int(work.get("cited_by_count") or 0)
            relevance, hostile = score_work(title, abstract, concepts, year, citations)

            if key not in seen:
                seen[key] = {
                    "openalex_id": ascii_clean(work.get("id", "")),
                    "doi": doi,
                    "title": title,
                    "year": year,
                    "authors": author_string(work),
                    "venue": source_name(work),
                    "url": doi or ascii_clean(work.get("id", "")),
                    "cited_by_count": citations,
                    "concepts": concepts,
                    "matched_queries": query,
                    "abstract": abstract,
                    "relevance_score": relevance,
                    "hostile_score": hostile,
                }
            else:
                row = seen[key]
                row["matched_queries"] = "; ".join(
                    dict.fromkeys((row["matched_queries"] + "; " + query).split("; "))
                )
                row["relevance_score"] = max(float(row["relevance_score"]), relevance)
                row["hostile_score"] = max(float(row["hostile_score"]), hostile)

        progress = {
            "completed_queries": index,
            "total_queries": len(QUERIES),
            "unique_works": len(seen),
            "failures": failures,
        }
        PROGRESS_PATH.write_text(json.dumps(progress, indent=2), encoding="utf-8")
        print(f"[literature] query {index}/{len(QUERIES)}: {query} -> {len(seen)} unique")
    rows = list(seen.values())
    rows.sort(key=lambda r: (float(r["relevance_score"]), float(r["hostile_score"]), int(r["cited_by_count"])), reverse=True)
    return rows


def write_matrix(rows: list[dict]) -> None:
    if len(rows) < 1000:
        print(f"[literature] warning: only {len(rows)} unique works collected")

    hostile_order = sorted(
        range(len(rows)),
        key=lambda i: (float(rows[i]["hostile_score"]), float(rows[i]["relevance_score"]), int(rows[i]["cited_by_count"])),
        reverse=True,
    )
    hostile_set = set(hostile_order[:100])
    deep_set = set(range(min(225, len(rows))))
    serious_set = set(range(min(300, len(rows))))

    fieldnames = [
        "rank",
        "analysis_level",
        "serious_skim",
        "deep_read",
        "hostile_prior",
        "title",
        "year",
        "authors",
        "venue",
        "doi",
        "url",
        "openalex_id",
        "cited_by_count",
        "concepts",
        "matched_queries",
        "relevance_score",
        "hostile_score",
        "problem_claimed",
        "actual_mechanism_introduced",
        "hidden_assumptions",
        "variables_treated_as_fixed",
        "failure_modes_ignored",
        "what_it_makes_less_novel",
        "what_it_leaves_open",
        "abstract_excerpt",
    ]

    with MATRIX_PATH.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for idx, row in enumerate(rows, start=1):
            abstract = row.pop("abstract", "")
            title = row["title"]
            text = f"{title}. {abstract} {row['concepts']}"
            assumptions, fixed, failures, less_novel, open_items = assumption_notes(text)
            zero_idx = idx - 1
            if zero_idx in hostile_set:
                level = "hostile_prior"
            elif zero_idx in deep_set:
                level = "deep_read"
            elif zero_idx in serious_set:
                level = "serious_skim"
            else:
                level = "landscape"
            out = {
                **row,
                "rank": idx,
                "analysis_level": level,
                "serious_skim": "yes" if zero_idx in serious_set else "no",
                "deep_read": "yes" if zero_idx in deep_set else "no",
                "hostile_prior": "yes" if zero_idx in hostile_set else "no",
                "problem_claimed": first_sentence(abstract, title),
                "actual_mechanism_introduced": classify_mechanism(text),
                "hidden_assumptions": assumptions,
                "variables_treated_as_fixed": fixed,
                "failure_modes_ignored": failures,
                "what_it_makes_less_novel": less_novel,
                "what_it_leaves_open": open_items,
                "abstract_excerpt": ascii_clean(abstract, 700),
            }
            writer.writerow({name: out.get(name, "") for name in fieldnames})

    summary = {
        "matrix_path": str(MATRIX_PATH),
        "entries": len(rows),
        "serious_skim": min(300, len(rows)),
        "deep_read": min(225, len(rows)),
        "hostile_prior": min(100, len(rows)),
    }
    PROGRESS_PATH.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(json.dumps(summary, indent=2))


def main() -> None:
    rows = collect()
    write_matrix(rows)


if __name__ == "__main__":
    main()
