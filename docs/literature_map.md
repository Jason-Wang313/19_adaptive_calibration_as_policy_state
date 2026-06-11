# Literature Map

## Collection Summary
- Landscape sweep: 6710 papers in `docs/related_work_matrix.csv`.
- Serious skim set: 300 top-ranked papers.
- Deep-read set: 225 papers with structured extraction fields.
- Hostile prior-work set: 100 papers selected by novelty-threat score.
- Year range: 1985-2026, median 2019.

## Field Box
The field box is robot calibration under closed-loop embodied policy execution: kinematic, extrinsic, visual-servo, tactile/contact, sim-to-real, and hidden-context adaptation methods that address how model/sensor/action mismatch affects robot behavior.

## Main Clusters From The Serious Skim
- kinematic calibration: 97 papers
- general robot adaptation: 46 papers
- hand-eye/extrinsic calibration: 42 papers
- system identification: 41 papers
- visual servoing: 40 papers
- sim-to-real robustness: 14 papers
- contact/tactile calibration: 14 papers
- hidden-context adaptation: 6 papers

## Hidden Assumptions That May Be False
1. A calibration measured before deployment remains valid for the full policy rollout.
2. Calibration error is small enough to be absorbed by feedback gains.
3. Calibration drift is independent of the task phase and contact history.
4. A single robust policy can cover the full calibration-error distribution without knowing the current drift.
5. Online calibration can be optimized as a separate estimator without changing the control state.
6. Sensor extrinsics are rigid even under tool changes, payload shifts, heat, and cable motion.
7. Kinematic parameters are static within an episode.
8. Dynamics identification and geometric calibration can be separated cleanly.
9. Visual servo feedback makes explicit geometric state unnecessary.
10. The robot can execute calibration motions that are independent of the task objective.
11. Residual policies learn the right correction without representing the physical cause.
12. Latent-context policies will discover calibration variables without calibration-specific supervision.
13. Domain randomization support contains the deployment drift.
14. Calibration uncertainty matters only for planning risk, not for the action itself.
15. The observation frame and action frame fail independently.
16. Calibration can be validated from final task success alone.
17. Estimator convergence is faster than the drift process.
18. Small action-observation errors stay locally linear around the current pose.
19. The same calibration state is observable from all useful task trajectories.
20. Offline benchmarks with fixed camera/robot geometry measure deployment robustness.
21. End-to-end policies can learn around miscalibration without losing sample efficiency.
22. The cost of information-gathering motion is negligible.
23. Calibration is a property of the robot, not of the robot-object-contact system.
24. A controller's memory should track task state but not metrology state.

## Candidate Directions That Break Assumptions
- **Calibration-State Control.** Make calibration a recurrent state variable with a physically interpretable update and use it directly in control. Breaks the offline-calibration assumption and is testable with a minimal hidden-state control system.
- **Task-Embedded Observability.** Design task actions whose ordinary residuals also identify calibration drift, without separate calibration routines. Strong but risks being viewed as active learning unless the mechanism is very specific.
- **Calibration-Causal Residuals.** Constrain residual policies so corrections factor through explicit calibration causes rather than arbitrary action deltas. Promising for learning systems but needs a larger learning stack than this paper can honestly validate.
- **Drift-Aware Benchmarking.** Benchmark policies under nonstationary camera/action map drift. Useful but forbidden as a benchmark-only contribution and not strong enough alone.

## Chosen Direction
**Thesis.** Calibration drift should be represented as policy state: a robot policy should carry an online estimate of the current action-observation calibration map and condition each control action on that estimate, instead of treating calibration as offline preprocessing or as generic robustness noise.

**Central mechanism.** Calibration-State Control (CSC): a low-dimensional recurrent state estimates the local action-to-observation Jacobian with forgetting, exposes that estimate and its conditioning to the policy, and computes task actions through the current calibration state. The policy interface changes from pi(observation, goal) to pi(observation, goal, calibration_state).

## Why This Direction Survived
- It changes the policy state interface, rather than merely adding a larger model, more data, active learning, a verifier, or a benchmark.
- It is directly attacked by online calibration, visual servoing, domain randomization, latent context adaptation, and system identification, so the novelty boundary can be stated sharply.
- It can be tested in a minimal physical-control abstraction where the same observation and goal require different actions under different hidden calibration maps.
- The strongest claim is modest: explicit calibration state can remove an irreducible ambiguity for hidden drift systems when the drift is observable from recent transitions.

## Repeated Prior-Work Patterns
### hidden_assumptions
- 226: calibration can be estimated separately from the policy state
- 182: online updates are stable enough to run beside the controller
- 94: identified parameters remain valid over the planning horizon
- 90: one policy can absorb the calibration distribution without explicit state
- 84: rigid extrinsics are recoverable before or between tasks
- 80: visual feedback can absorb geometric error without representing the cause
- 24: latent context is learned as a generic nuisance rather than a physical calibration variable
- 3: the relevant physical mismatch can be handled outside the policy loop

### variables_treated_as_fixed
- 226: sensor-to-robot or model-to-world transform during policy execution
- 182: the objective while calibration actions perturb task progress
- 94: model structure and parameterization
- 90: deployment drift distribution relative to training randomization
- 84: mount rigidity and synchronized motion observations
- 80: image Jacobian validity near the current pose
- 24: meaning and observability of the latent state
- 3: environment, embodiment, or sensing parameters during one rollout

### failure_modes_ignored
- 226: calibration drift after deployment or under contact-induced slippage
- 182: unobservable motions and estimator/controller feedback loops
- 94: nonstationary parameter drift and partial excitation
- 90: distribution shift outside randomized support
- 84: temperature, cable, tool, or payload shifts during the task
- 80: large drift, occlusion, and nonlocal Jacobian mismatch
- 24: latent collapse or entanglement with task state
- 3: nonstationary shift while the robot is acting

### what_it_makes_less_novel
- 226: treating calibration as an estimable parameter is not new
- 182: performing online calibration during robot operation
- 94: using interaction data to identify model parameters
- 90: robustifying policies against calibration errors
- 84: estimating robot-camera extrinsics
- 80: closing the loop around calibration errors with feedback
- 24: conditioning robot policies on inferred hidden context
- 3: general robot adaptation under model mismatch

### what_it_leaves_open
- 226: how control changes when calibration belief is part of every policy decision
- 182: closed-loop task benefit from carrying calibration as policy memory
- 94: making fast calibration drift a first-class recurrent state rather than a batch ID result
- 90: whether explicit low-dimensional calibration state outperforms robustness at equal data
- 84: policies that condition on continuing extrinsic belief during task execution
- 80: when explicit calibration state improves over pure servo feedback
- 24: calibration-specific observability, update rules, and control guarantees
- 3: a calibration-drift-specific state/control interface

## Important Caveat
The automated sweep uses OpenAlex metadata and abstracts plus rule-based extraction. The deep-read label means structured abstract/metadata review at scale, not full manual PDF reading for every paper. The hostile set is therefore a conservative novelty-threat map to guide claims, not a substitute for final human bibliography review.
