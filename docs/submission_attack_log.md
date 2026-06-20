# Submission Attack Log

Updated: 2026-06-20

## V2 Attack Rounds

1. **"This is just online system identification."** Added Windowed SysID, a hostile baseline that fits the action-observation map from the most recent 14 transitions and uses the same inverse-control interface.
2. **"Residual bias is too weak a baseline."** The v2 baseline is stronger because it carries an explicit calibration map inside the policy loop.
3. **"The RLS estimator may be the whole contribution."** The v2 results narrow the claim: Windowed SysID reaches 0.867 abrupt-bump success and 0.948 severe-random-walk success, so much of the benefit is shared by online calibration-state estimators.
4. **"CSC still needs evidence beyond toy simulation."** The readiness decision stays workshop-only / strong-revise; real robot or higher-fidelity visual-servoing evidence remains required.
5. **"Learned recurrent policies could infer the same state."** This remains unresolved and is explicitly listed as the next major baseline.

## Terminal Assessment

Recoverable v2 baseline weakness was addressed. Remaining weaknesses motivated the v3 full-scale pass.

## V3 Attack Rounds

1. **Paper is too short / not submission-scale.** Expanded to a 25-page manuscript with full-scale results and extended appendices.
2. **Evidence too narrow.** Added eight experiment families with 1,681 batch-row summaries and 14,614 episodes.
3. **RLS estimator may be the whole story.** Family B and the main suite show Windowed SysID is highly competitive, narrowing the claim to calibration as policy state.
4. **Generic memory may be enough.** Family H adds scalar, matrix-not-policy, shuffled, random, delayed-oracle, CSC, and oracle controls.
5. **Observability handwave.** Family C explicitly stresses excitation and the manuscript treats low excitation as a boundary.
6. **Planning utility overclaimed.** Family G is included as a hard stress and is explicitly not used as broad planning-dominance evidence.
7. **PDF link styling depends on implicit defaults.** Added explicit `hyperref` border colors, rebuilt the final PDF, and visually checked all affected link pages against the VLA-v4 role model.

## V3 Terminal Assessment

Submission-ready under the narrow synthetic mechanism claim. Not a real-robot validation claim; not RLS-specific novelty; not dominance over learned recurrent policies.
