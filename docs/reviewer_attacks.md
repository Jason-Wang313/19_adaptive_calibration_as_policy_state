# Reviewer Attacks

1. **This is just online calibration.**
   Response: the paper must emphasize that online calibration is prior art; the new part is the policy-state interface and the impossibility/evidence that omitting this state creates action ambiguity.
2. **This is just system identification or latent context.**
   Response: CSC is a physical calibration channel with a defined action-observation Jacobian and update rule; generic latent context is a hostile baseline/related class, not the claimed novelty.
3. **Visual servoing already handles calibration error.**
   Response: servoing closes feedback around error but may not represent the hidden action map; experiments should include feedback baselines and state when servoing is sufficient.
4. **The method is a hand-designed estimator, not a learning paper.**
   Response: the paper should be framed as embodied policy-state design; ICLR relevance comes from state representation for robot policies and sim-to-real adaptation.
5. **Toy simulation is too small.**
   Response: the testbed supports the mechanism and formal claim; paper-readiness may be workshop/revise unless larger hardware or learned-policy experiments are added.
6. **Domain randomization can cover this.**
   Response: compare against robust low-gain/randomized-style baselines and claim efficiency/ambiguity, not universal dominance.
7. **The calibration state may be unobservable.**
   Response: explicitly state observability conditions and include failure cases/conditioning diagnostics.
8. **The literature sweep is automated.**
   Response: mark it as broad abstract-level hostile mapping and keep claims conservative.

## Specific Hostile Papers To Recheck Manually
- Data-Driven Model Predictive Control for Uncalibrated Visual Servoing (2023): Fits parametric robot geometry or joint/link offsets to reduce pose prediction error.
- Dynamic Model Formulation and Calibration for Wheeled Mobile Robots (2014): Fits parametric robot geometry or joint/link offsets to reduce pose prediction error.
- Online parameter estimation via real-time replanning of continuous Gaussian POMDPs (2014): Identifies physical model parameters or residual dynamics from trajectories for control or simulation.
- Model-Free and Uncalibrated Eye-in-Hand Visual Servoing Approach for Concentric-Tube Robots (2022): Estimates a rigid transform between robot and camera/end-effector frames from paired motion observations.
- Adaptive Differential Visual Feedback for Uncalibrated Hand-Eye Coordination and Motor Control (1994): Estimates a rigid transform between robot and camera/end-effector frames from paired motion observations.
- Bayesian Modeling for Optimization and Control in Robotics (2017): Identifies physical model parameters or residual dynamics from trajectories for control or simulation.
- Adaptive Neuro-Filtering Based Visual Servo Control of a Robotic Manipulator (2019): Estimates a rigid transform between robot and camera/end-effector frames from paired motion observations.
- Online Kinematic Calibration for Legged Robots (2022): Fits parametric robot geometry or joint/link offsets to reduce pose prediction error.
