# Hostile Prior Work

This set contains the 100 papers that most threaten the novelty of calibration-as-policy-state, selected by calibration/adaptation relevance, hostile keyword overlap, and citation signal.

## 1. Data-Driven Model Predictive Control for Uncalibrated Visual Servoing (2023)
- Authors/venue: Tianjiao Han; Hongyu Zhu; Dan Yu / Symmetry
- Problem claimed: This paper addresses the image-based visual servoing (IBVS) control problem with an uncalibrated camera, unknown dynamics, and constraints.
- Actual mechanism introduced: Fits parametric robot geometry or joint/link offsets to reduce pose prediction error.
- Hidden assumptions: calibration can be estimated separately from the policy state; online updates are stable enough to run beside the controller; one policy can absorb the calibration distribution without explicit state; identified parameters remain valid over the planning horizon
- Variables treated as fixed: sensor-to-robot or model-to-world transform during policy execution; the objective while calibration actions perturb task progress; deployment drift distribution relative to training randomization; model structure and parameterization
- Failure modes ignored: calibration drift after deployment or under contact-induced slippage; unobservable motions and estimator/controller feedback loops; distribution shift outside randomized support; nonstationary parameter drift and partial excitation
- What it makes less novel: treating calibration as an estimable parameter is not new; performing online calibration during robot operation; robustifying policies against calibration errors; using interaction data to identify model parameters
- What it leaves open: how control changes when calibration belief is part of every policy decision; closed-loop task benefit from carrying calibration as policy memory; whether explicit low-dimensional calibration state outperforms robustness at equal data; making fast calibrati...
- Locator: https://doi.org/10.3390/sym16010048

## 2. Dynamic Model Formulation and Calibration for Wheeled Mobile Robots (2014)
- Authors/venue: Neal Seegmiller / Research Showcase @ Carnegie Mellon University (Carnegie Mellon University)
- Problem claimed: Advances in hardware design have made wheeled mobile robots (WMRs) exceptionally mobile.
- Actual mechanism introduced: Fits parametric robot geometry or joint/link offsets to reduce pose prediction error.
- Hidden assumptions: calibration can be estimated separately from the policy state; online updates are stable enough to run beside the controller; identified parameters remain valid over the planning horizon
- Variables treated as fixed: sensor-to-robot or model-to-world transform during policy execution; the objective while calibration actions perturb task progress; model structure and parameterization
- Failure modes ignored: calibration drift after deployment or under contact-induced slippage; unobservable motions and estimator/controller feedback loops; nonstationary parameter drift and partial excitation
- What it makes less novel: treating calibration as an estimable parameter is not new; performing online calibration during robot operation; using interaction data to identify model parameters
- What it leaves open: how control changes when calibration belief is part of every policy decision; closed-loop task benefit from carrying calibration as policy memory; making fast calibration drift a first-class recurrent state rather than a batch ID result
- Locator: https://doi.org/10.1184/r1/6716117

## 3. Online parameter estimation via real-time replanning of continuous Gaussian POMDPs (2014)
- Authors/venue: Dustin J. Webb; Kyle L. Crandall; Jur van den Berg / 
- Problem claimed: An accurate dynamics model of a robot is an important ingredient of many algorithms used to solve robotics problems, including motion planning, control, localization, and mapping.
- Actual mechanism introduced: Identifies physical model parameters or residual dynamics from trajectories for control or simulation.
- Hidden assumptions: calibration can be estimated separately from the policy state; online updates are stable enough to run beside the controller; identified parameters remain valid over the planning horizon
- Variables treated as fixed: sensor-to-robot or model-to-world transform during policy execution; the objective while calibration actions perturb task progress; model structure and parameterization
- Failure modes ignored: calibration drift after deployment or under contact-induced slippage; unobservable motions and estimator/controller feedback loops; nonstationary parameter drift and partial excitation
- What it makes less novel: treating calibration as an estimable parameter is not new; performing online calibration during robot operation; using interaction data to identify model parameters
- What it leaves open: how control changes when calibration belief is part of every policy decision; closed-loop task benefit from carrying calibration as policy memory; making fast calibration drift a first-class recurrent state rather than a batch ID result
- Locator: https://doi.org/10.1109/icra.2014.6907743

## 4. Model-Free and Uncalibrated Eye-in-Hand Visual Servoing Approach for Concentric-Tube Robots (2022)
- Authors/venue: Xing Yang; Jiaole Wang; Shuang Song; Max Q.H. Meng / IEEE Transactions on Instrumentation and Measurement
- Problem claimed: This article proposes a model-free and uncalibrated eye-in-hand visual servoing (EiH-VS) approach for controlling concentric-tube robots (CTRs) in minimally invasive surgery (MIS).
- Actual mechanism introduced: Estimates a rigid transform between robot and camera/end-effector frames from paired motion observations.
- Hidden assumptions: calibration can be estimated separately from the policy state; online updates are stable enough to run beside the controller; visual feedback can absorb geometric error without representing the cause; rigid extrinsics are recoverable before or between tasks
- Variables treated as fixed: sensor-to-robot or model-to-world transform during policy execution; the objective while calibration actions perturb task progress; image Jacobian validity near the current pose; mount rigidity and synchronized motion observations
- Failure modes ignored: calibration drift after deployment or under contact-induced slippage; unobservable motions and estimator/controller feedback loops; large drift, occlusion, and nonlocal Jacobian mismatch; temperature, cable, tool, or payload shifts during the task
- What it makes less novel: treating calibration as an estimable parameter is not new; performing online calibration during robot operation; closing the loop around calibration errors with feedback; estimating robot-camera extrinsics
- What it leaves open: how control changes when calibration belief is part of every policy decision; closed-loop task benefit from carrying calibration as policy memory; when explicit calibration state improves over pure servo feedback; policies that condition on continuing extri...
- Locator: https://doi.org/10.1109/tim.2022.3147867

## 5. Adaptive Differential Visual Feedback for Uncalibrated Hand-Eye Coordination and Motor Control (1994)
- Authors/venue: Martin J agersand; Randal C. Nelson / 
- Problem claimed: We propose and implement a novel method for visual space trajectory planning, and adaptive high degree-of-freedom (DOF) visual feedback control.
- Actual mechanism introduced: Estimates a rigid transform between robot and camera/end-effector frames from paired motion observations.
- Hidden assumptions: calibration can be estimated separately from the policy state; latent context is learned as a generic nuisance rather than a physical calibration variable; visual feedback can absorb geometric error without representing the cause; rigid extrinsics are recoverable before or between tasks
- Variables treated as fixed: sensor-to-robot or model-to-world transform during policy execution; meaning and observability of the latent state; image Jacobian validity near the current pose; mount rigidity and synchronized motion observations
- Failure modes ignored: calibration drift after deployment or under contact-induced slippage; latent collapse or entanglement with task state; large drift, occlusion, and nonlocal Jacobian mismatch; temperature, cable, tool, or payload shifts during the task
- What it makes less novel: treating calibration as an estimable parameter is not new; conditioning robot policies on inferred hidden context; closing the loop around calibration errors with feedback; estimating robot-camera extrinsics
- What it leaves open: how control changes when calibration belief is part of every policy decision; calibration-specific observability, update rules, and control guarantees; when explicit calibration state improves over pure servo feedback; policies that condition on continuing...
- Locator: https://openalex.org/W1686193771

## 6. Bayesian Modeling for Optimization and Control in Robotics (2017)
- Authors/venue: Roberto Calandra / Technischen Universitat Darmstadt
- Problem claimed: Robotics has the potential to be one of the most revolutionary technologies in human history.
- Actual mechanism introduced: Identifies physical model parameters or residual dynamics from trajectories for control or simulation.
- Hidden assumptions: calibration can be estimated separately from the policy state; one policy can absorb the calibration distribution without explicit state; identified parameters remain valid over the planning horizon
- Variables treated as fixed: sensor-to-robot or model-to-world transform during policy execution; deployment drift distribution relative to training randomization; model structure and parameterization
- Failure modes ignored: calibration drift after deployment or under contact-induced slippage; distribution shift outside randomized support; nonstationary parameter drift and partial excitation
- What it makes less novel: treating calibration as an estimable parameter is not new; robustifying policies against calibration errors; using interaction data to identify model parameters
- What it leaves open: how control changes when calibration belief is part of every policy decision; whether explicit low-dimensional calibration state outperforms robustness at equal data; making fast calibration drift a first-class recurrent state rather than a batch ID result
- Locator: https://doi.org/10.26083/tuprints-00005878

## 7. Adaptive Neuro-Filtering Based Visual Servo Control of a Robotic Manipulator (2019)
- Authors/venue: Xungao Zhong; Xunyu Zhong; Huosheng Hu; Xiafu Peng / IEEE Access
- Problem claimed: This paper focuses on the solutions to flexibly regulate robotic by vision.
- Actual mechanism introduced: Estimates a rigid transform between robot and camera/end-effector frames from paired motion observations.
- Hidden assumptions: calibration can be estimated separately from the policy state; online updates are stable enough to run beside the controller; visual feedback can absorb geometric error without representing the cause; rigid extrinsics are recoverable before or between tasks
- Variables treated as fixed: sensor-to-robot or model-to-world transform during policy execution; the objective while calibration actions perturb task progress; image Jacobian validity near the current pose; mount rigidity and synchronized motion observations
- Failure modes ignored: calibration drift after deployment or under contact-induced slippage; unobservable motions and estimator/controller feedback loops; large drift, occlusion, and nonlocal Jacobian mismatch; temperature, cable, tool, or payload shifts during the task
- What it makes less novel: treating calibration as an estimable parameter is not new; performing online calibration during robot operation; closing the loop around calibration errors with feedback; estimating robot-camera extrinsics
- What it leaves open: how control changes when calibration belief is part of every policy decision; closed-loop task benefit from carrying calibration as policy memory; when explicit calibration state improves over pure servo feedback; policies that condition on continuing extri...
- Locator: https://doi.org/10.1109/access.2019.2920941

## 8. Online Kinematic Calibration for Legged Robots (2022)
- Authors/venue: Shuo Yang; Howie Choset; Zachary Manchester / IEEE Robotics and Automation Letters
- Problem claimed: This paper describes an online method to calibrate certain kinematic parameters of legged robots, including leg lengths, that can be difficult to measure offline due to dynamic deformation effects and rolling contacts.
- Actual mechanism introduced: Fits parametric robot geometry or joint/link offsets to reduce pose prediction error.
- Hidden assumptions: calibration can be estimated separately from the policy state; online updates are stable enough to run beside the controller
- Variables treated as fixed: sensor-to-robot or model-to-world transform during policy execution; the objective while calibration actions perturb task progress
- Failure modes ignored: calibration drift after deployment or under contact-induced slippage; unobservable motions and estimator/controller feedback loops
- What it makes less novel: treating calibration as an estimable parameter is not new; performing online calibration during robot operation
- What it leaves open: how control changes when calibration belief is part of every policy decision; closed-loop task benefit from carrying calibration as policy memory
- Locator: https://doi.org/10.1109/lra.2022.3186501

## 9. Hybrid Uncalibrated Visual Servoing Control of Harvesting Robots With RGB-D Cameras (2022)
- Authors/venue: Tao Li; Jinpeng Yu; Quan Qiu; Chunjiang Zhao / IEEE Transactions on Industrial Electronics
- Problem claimed: Visual servoing (VS) control has seen wide adoption in harvesting robots.
- Actual mechanism introduced: Uses image/Jacobian feedback to close the loop around visual error despite imperfect calibration.
- Hidden assumptions: calibration can be estimated separately from the policy state; online updates are stable enough to run beside the controller; identified parameters remain valid over the planning horizon; visual feedback can absorb geometric error without representing the cause
- Variables treated as fixed: sensor-to-robot or model-to-world transform during policy execution; the objective while calibration actions perturb task progress; model structure and parameterization; image Jacobian validity near the current pose
- Failure modes ignored: calibration drift after deployment or under contact-induced slippage; unobservable motions and estimator/controller feedback loops; nonstationary parameter drift and partial excitation; large drift, occlusion, and nonlocal Jacobian mismatch
- What it makes less novel: treating calibration as an estimable parameter is not new; performing online calibration during robot operation; using interaction data to identify model parameters; closing the loop around calibration errors with feedback
- What it leaves open: how control changes when calibration belief is part of every policy decision; closed-loop task benefit from carrying calibration as policy memory; making fast calibration drift a first-class recurrent state rather than a batch ID result; when explicit calib...
- Locator: https://doi.org/10.1109/tie.2022.3172778

## 10. Calibration-Free Image-Based Trajectory Tracking Control of Mobile Robots With an Overhead Camera (2019)
- Authors/venue: Xinwu Liang; Hesheng Wang; Yunhui Liu; Bing You; Zhe Liu; Weidong Chen / IEEE Transactions on Automation Science and Engineering
- Problem claimed: To make the controller implementation easier and to enhance the system robustness and control performance in the presence of the camera parameter uncertainties, it is very desired to develop vision-based control approaches without any of...
- Actual mechanism introduced: Fits parametric robot geometry or joint/link offsets to reduce pose prediction error.
- Hidden assumptions: calibration can be estimated separately from the policy state; online updates are stable enough to run beside the controller; one policy can absorb the calibration distribution without explicit state; rigid extrinsics are recoverable before or between tasks
- Variables treated as fixed: sensor-to-robot or model-to-world transform during policy execution; the objective while calibration actions perturb task progress; deployment drift distribution relative to training randomization; mount rigidity and synchronized motion observations
- Failure modes ignored: calibration drift after deployment or under contact-induced slippage; unobservable motions and estimator/controller feedback loops; distribution shift outside randomized support; temperature, cable, tool, or payload shifts during the task
- What it makes less novel: treating calibration as an estimable parameter is not new; performing online calibration during robot operation; robustifying policies against calibration errors; estimating robot-camera extrinsics
- What it leaves open: how control changes when calibration belief is part of every policy decision; closed-loop task benefit from carrying calibration as policy memory; whether explicit low-dimensional calibration state outperforms robustness at equal data; policies that conditi...
- Locator: https://doi.org/10.1109/tase.2019.2951714

## 11. Uncalibrated Adaptive Visual Servoing of Robotic Manipulators with Uncertainties in Kinematics and Dynamics (2023)
- Authors/venue: Guanyu Lai; Aoqi Liu; Weijun Yang; Yuanfeng Chen; Lele Zhao / Actuators
- Problem claimed: In the study, we propose a novel adaptive visual servoing control scheme for robotic manipulators with kinematic and dynamic uncertainties, where the camera used is uncalibrated, which implies that its intrinsic and extrinsic parameters...
- Actual mechanism introduced: Fits parametric robot geometry or joint/link offsets to reduce pose prediction error.
- Hidden assumptions: identified parameters remain valid over the planning horizon; visual feedback can absorb geometric error without representing the cause; rigid extrinsics are recoverable before or between tasks
- Variables treated as fixed: model structure and parameterization; image Jacobian validity near the current pose; mount rigidity and synchronized motion observations
- Failure modes ignored: nonstationary parameter drift and partial excitation; large drift, occlusion, and nonlocal Jacobian mismatch; temperature, cable, tool, or payload shifts during the task
- What it makes less novel: using interaction data to identify model parameters; closing the loop around calibration errors with feedback; estimating robot-camera extrinsics
- What it leaves open: making fast calibration drift a first-class recurrent state rather than a batch ID result; when explicit calibration state improves over pure servo feedback; policies that condition on continuing extrinsic belief during task execution
- Locator: https://doi.org/10.3390/act12040143

## 12. Leveraging Deep Reinforcement Learning for Reaching Robotic Tasks (2017)
- Authors/venue: Kapil D. Katyal; I-Jeng Wang; Philippe Burlina / 
- Problem claimed: This work leverages Deep Reinforcement Learning (DRL) to make robotic control immune to changes in the robot manipulator or the environment and to perform reaching, collision avoidance and grasping without explicit, prior and fine knowle...
- Actual mechanism introduced: Estimates a rigid transform between robot and camera/end-effector frames from paired motion observations.
- Hidden assumptions: calibration can be estimated separately from the policy state; one policy can absorb the calibration distribution without explicit state; visual feedback can absorb geometric error without representing the cause; rigid extrinsics are recoverable before or between tasks
- Variables treated as fixed: sensor-to-robot or model-to-world transform during policy execution; deployment drift distribution relative to training randomization; image Jacobian validity near the current pose; mount rigidity and synchronized motion observations
- Failure modes ignored: calibration drift after deployment or under contact-induced slippage; distribution shift outside randomized support; large drift, occlusion, and nonlocal Jacobian mismatch; temperature, cable, tool, or payload shifts during the task
- What it makes less novel: treating calibration as an estimable parameter is not new; robustifying policies against calibration errors; closing the loop around calibration errors with feedback; estimating robot-camera extrinsics
- What it leaves open: how control changes when calibration belief is part of every policy decision; whether explicit low-dimensional calibration state outperforms robustness at equal data; when explicit calibration state improves over pure servo feedback; policies that condition...
- Locator: https://doi.org/10.1109/cvprw.2017.71

## 13. 2004 IEEE International Conference on Robotics and Automation (IEEE Cat. No.04CH37508) (2004)
- Authors/venue:  / 
- Problem claimed: The following topics are dealt with: vision based navigation and tracking; automation of manufacturing process; automation of security surveillance; adaptive navigation; humanoids; sensor network; sensor fusion; human-machine interface;...
- Actual mechanism introduced: Fits parametric robot geometry or joint/link offsets to reduce pose prediction error.
- Hidden assumptions: calibration can be estimated separately from the policy state; identified parameters remain valid over the planning horizon; visual feedback can absorb geometric error without representing the cause
- Variables treated as fixed: sensor-to-robot or model-to-world transform during policy execution; model structure and parameterization; image Jacobian validity near the current pose
- Failure modes ignored: calibration drift after deployment or under contact-induced slippage; nonstationary parameter drift and partial excitation; large drift, occlusion, and nonlocal Jacobian mismatch
- What it makes less novel: treating calibration as an estimable parameter is not new; using interaction data to identify model parameters; closing the loop around calibration errors with feedback
- What it leaves open: how control changes when calibration belief is part of every policy decision; making fast calibration drift a first-class recurrent state rather than a batch ID result; when explicit calibration state improves over pure servo feedback
- Locator: https://doi.org/10.1109/robot.2004.1308736

## 14. Adaptive Visual Servoing for an Underwater Soft Robot Considering Refraction Effects (2019)
- Authors/venue: Fan Xu; Hesheng Wang; Zhe Liu; Weidong Chen / IEEE Transactions on Industrial Electronics
- Problem claimed: Robots inspired from marine organisms are tremendously developed for applications of underwater exploration, rescuing, navigation, etc.
- Actual mechanism introduced: Uses image/Jacobian feedback to close the loop around visual error despite imperfect calibration.
- Hidden assumptions: calibration can be estimated separately from the policy state; online updates are stable enough to run beside the controller; visual feedback can absorb geometric error without representing the cause; rigid extrinsics are recoverable before or between tasks
- Variables treated as fixed: sensor-to-robot or model-to-world transform during policy execution; the objective while calibration actions perturb task progress; image Jacobian validity near the current pose; mount rigidity and synchronized motion observations
- Failure modes ignored: calibration drift after deployment or under contact-induced slippage; unobservable motions and estimator/controller feedback loops; large drift, occlusion, and nonlocal Jacobian mismatch; temperature, cable, tool, or payload shifts during the task
- What it makes less novel: treating calibration as an estimable parameter is not new; performing online calibration during robot operation; closing the loop around calibration errors with feedback; estimating robot-camera extrinsics
- What it leaves open: how control changes when calibration belief is part of every policy decision; closed-loop task benefit from carrying calibration as policy memory; when explicit calibration state improves over pure servo feedback; policies that condition on continuing extri...
- Locator: https://doi.org/10.1109/tie.2019.2958254

## 15. Adaptive Control Algorithm for Uncalibrated Position-based Visual Servoing (2022)
- Authors/venue: Shaoying He; Yunwen Xu; Dewei Li; Yugeng Xi / 2022 41st Chinese Control Conference (CCC)
- Problem claimed: The paper proposes an adaptive control algorithm for the uncalibrated position-based visual servoing to complete the tracking task of robot system.
- Actual mechanism introduced: Estimates a rigid transform between robot and camera/end-effector frames from paired motion observations.
- Hidden assumptions: calibration can be estimated separately from the policy state; online updates are stable enough to run beside the controller; visual feedback can absorb geometric error without representing the cause; rigid extrinsics are recoverable before or between tasks
- Variables treated as fixed: sensor-to-robot or model-to-world transform during policy execution; the objective while calibration actions perturb task progress; image Jacobian validity near the current pose; mount rigidity and synchronized motion observations
- Failure modes ignored: calibration drift after deployment or under contact-induced slippage; unobservable motions and estimator/controller feedback loops; large drift, occlusion, and nonlocal Jacobian mismatch; temperature, cable, tool, or payload shifts during the task
- What it makes less novel: treating calibration as an estimable parameter is not new; performing online calibration during robot operation; closing the loop around calibration errors with feedback; estimating robot-camera extrinsics
- What it leaves open: how control changes when calibration belief is part of every policy decision; closed-loop task benefit from carrying calibration as policy memory; when explicit calibration state improves over pure servo feedback; policies that condition on continuing extri...
- Locator: https://doi.org/10.23919/ccc55666.2022.9902236

## 16. Vision-based adaptive tracking control of uncertain robot manipulators (2005)
- Authors/venue: Maruthi R. Akella / IEEE Transactions on Robotics
- Problem claimed: This paper studies the problem of position-tracking adaptive control for planar robotic manipulators through visual servoing under a fixed-camera configuration.
- Actual mechanism introduced: Uses image/Jacobian feedback to close the loop around visual error despite imperfect calibration.
- Hidden assumptions: calibration can be estimated separately from the policy state; online updates are stable enough to run beside the controller; one policy can absorb the calibration distribution without explicit state; identified parameters remain valid over the planning horizon
- Variables treated as fixed: sensor-to-robot or model-to-world transform during policy execution; the objective while calibration actions perturb task progress; deployment drift distribution relative to training randomization; model structure and parameterization
- Failure modes ignored: calibration drift after deployment or under contact-induced slippage; unobservable motions and estimator/controller feedback loops; distribution shift outside randomized support; nonstationary parameter drift and partial excitation
- What it makes less novel: treating calibration as an estimable parameter is not new; performing online calibration during robot operation; robustifying policies against calibration errors; using interaction data to identify model parameters
- What it leaves open: how control changes when calibration belief is part of every policy decision; closed-loop task benefit from carrying calibration as policy memory; whether explicit low-dimensional calibration state outperforms robustness at equal data; making fast calibrati...
- Locator: https://doi.org/10.1109/tro.2005.847608

## 17. Dojo: A Differentiable Physics Engine for Robotics (2022)
- Authors/venue: Taylor A. Howell; Simon Le Cleac'h; Brudigam, Jan; Chen, Qianzhong; Sun, Jiankai; Kolter, J. Zico; et al. / arXiv (Cornell University)
- Problem claimed: We present Dojo, a differentiable physics engine for robotics that prioritizes stable simulation, accurate contact physics, and differentiability with respect to states, actions, and system parameters.
- Actual mechanism introduced: Identifies physical model parameters or residual dynamics from trajectories for control or simulation.
- Hidden assumptions: online updates are stable enough to run beside the controller; identified parameters remain valid over the planning horizon
- Variables treated as fixed: the objective while calibration actions perturb task progress; model structure and parameterization
- Failure modes ignored: unobservable motions and estimator/controller feedback loops; nonstationary parameter drift and partial excitation
- What it makes less novel: performing online calibration during robot operation; using interaction data to identify model parameters
- What it leaves open: closed-loop task benefit from carrying calibration as policy memory; making fast calibration drift a first-class recurrent state rather than a batch ID result
- Locator: https://doi.org/10.48550/arxiv.2203.00806

## 18. Joint Dynamics and Adaptive Feedforward Control of Lightweight Industrial Robots (2020)
- Authors/venue: Emil Madsen / 
- Problem claimed: The use of lightweight strain-wave transmissions in collaborative industrial robots leads to structural compliance and a complex nonlinear behavior of the robot joints.
- Actual mechanism introduced: Identifies physical model parameters or residual dynamics from trajectories for control or simulation.
- Hidden assumptions: online updates are stable enough to run beside the controller; latent context is learned as a generic nuisance rather than a physical calibration variable; identified parameters remain valid over the planning horizon
- Variables treated as fixed: the objective while calibration actions perturb task progress; meaning and observability of the latent state; model structure and parameterization
- Failure modes ignored: unobservable motions and estimator/controller feedback loops; latent collapse or entanglement with task state; nonstationary parameter drift and partial excitation
- What it makes less novel: performing online calibration during robot operation; conditioning robot policies on inferred hidden context; using interaction data to identify model parameters
- What it leaves open: closed-loop task benefit from carrying calibration as policy memory; calibration-specific observability, update rules, and control guarantees; making fast calibration drift a first-class recurrent state rather than a batch ID result
- Locator: https://doi.org/10.7146/aul.384

## 19. Online Behavior-Centric Adaptation for Bipedal Robot Sim-to-Real Transfer With Unmodeled Dynamics Mismatch (2025)
- Authors/venue: Xuechao CHEN; Yidong Du; Zishun Zhou; Zhicheng Yuan; Qingrui Zhao; Fei Meng; et al. / IEEE Transactions on Automation Science and Engineering
- Problem claimed: Bipedal robots have achieved remarkable locomotion capabilities through reinforcement learning (RL), yet their real-world deployment remains hindered by the sim-to-real gap-dynamics mismatches between simulation and reality that degrade...
- Actual mechanism introduced: Identifies physical model parameters or residual dynamics from trajectories for control or simulation.
- Hidden assumptions: online updates are stable enough to run beside the controller; latent context is learned as a generic nuisance rather than a physical calibration variable; identified parameters remain valid over the planning horizon
- Variables treated as fixed: the objective while calibration actions perturb task progress; meaning and observability of the latent state; model structure and parameterization
- Failure modes ignored: unobservable motions and estimator/controller feedback loops; latent collapse or entanglement with task state; nonstationary parameter drift and partial excitation
- What it makes less novel: performing online calibration during robot operation; conditioning robot policies on inferred hidden context; using interaction data to identify model parameters
- What it leaves open: closed-loop task benefit from carrying calibration as policy memory; calibration-specific observability, update rules, and control guarantees; making fast calibration drift a first-class recurrent state rather than a batch ID result
- Locator: https://doi.org/10.1109/tase.2025.3648835

## 20. Visual Calibration, Identification and Control of 6-RSS Parallel Robots (2020)
- Authors/venue: Pengcheng Li / Spectrum Research Repository (Concordia University)
- Problem claimed: Parallel robots present some outstanding advantages in high force-to-weight ratio, better stiffness and theoretical higher accuracy compared with serial manipulators.
- Actual mechanism introduced: Fits parametric robot geometry or joint/link offsets to reduce pose prediction error.
- Hidden assumptions: calibration can be estimated separately from the policy state; online updates are stable enough to run beside the controller; one policy can absorb the calibration distribution without explicit state; identified parameters remain valid over the planning horizon
- Variables treated as fixed: sensor-to-robot or model-to-world transform during policy execution; the objective while calibration actions perturb task progress; deployment drift distribution relative to training randomization; model structure and parameterization
- Failure modes ignored: calibration drift after deployment or under contact-induced slippage; unobservable motions and estimator/controller feedback loops; distribution shift outside randomized support; nonstationary parameter drift and partial excitation
- What it makes less novel: treating calibration as an estimable parameter is not new; performing online calibration during robot operation; robustifying policies against calibration errors; using interaction data to identify model parameters
- What it leaves open: how control changes when calibration belief is part of every policy decision; closed-loop task benefit from carrying calibration as policy memory; whether explicit low-dimensional calibration state outperforms robustness at equal data; making fast calibrati...
- Locator: https://openalex.org/W3217642735

## 21. Hand-Eye Calibration of Surgical Instrument for Robotic Surgery Using Interactive Manipulation (2020)
- Authors/venue: Fangxun Zhong; Zerui Wang; Wei Chen; Kejing He; Yaqing Wang; Yunhui Liu / IEEE Robotics and Automation Letters
- Problem claimed: Conventional robot hand-eye calibration methods are impractical for localizing robotic instruments in minimally-invasive surgeries under intra-corporeal workspace after preoperative set-up.
- Actual mechanism introduced: Estimates a rigid transform between robot and camera/end-effector frames from paired motion observations.
- Hidden assumptions: calibration can be estimated separately from the policy state; rigid extrinsics are recoverable before or between tasks
- Variables treated as fixed: sensor-to-robot or model-to-world transform during policy execution; mount rigidity and synchronized motion observations
- Failure modes ignored: calibration drift after deployment or under contact-induced slippage; temperature, cable, tool, or payload shifts during the task
- What it makes less novel: treating calibration as an estimable parameter is not new; estimating robot-camera extrinsics
- What it leaves open: how control changes when calibration belief is part of every policy decision; policies that condition on continuing extrinsic belief during task execution
- Locator: https://doi.org/10.1109/lra.2020.2967685

## 22. Integrated pre-processing for Bayesian nonlinear system identification with Gaussian processes (2013)
- Authors/venue: Roger Frigola; Carl Edward Rasmussen / 
- Problem claimed: We introduce GP-FNARX: a new model for nonlinear system identification based on a nonlinear autoregressive exogenous model (NARX) with filtered regressors (F) where the nonlinear regression problem is tackled using sparse Gaussian proces...
- Actual mechanism introduced: Identifies physical model parameters or residual dynamics from trajectories for control or simulation.
- Hidden assumptions: online updates are stable enough to run beside the controller; identified parameters remain valid over the planning horizon
- Variables treated as fixed: the objective while calibration actions perturb task progress; model structure and parameterization
- Failure modes ignored: unobservable motions and estimator/controller feedback loops; nonstationary parameter drift and partial excitation
- What it makes less novel: performing online calibration during robot operation; using interaction data to identify model parameters
- What it leaves open: closed-loop task benefit from carrying calibration as policy memory; making fast calibration drift a first-class recurrent state rather than a batch ID result
- Locator: https://doi.org/10.1109/cdc.2013.6760734

## 23. Cerberus: Low-Drift Visual-Inertial-Leg Odometry For Agile Locomotion (2023)
- Authors/venue: Shuo Yang; Zixin Zhang; Zhengyu Fu; Zachary Manchester / 
- Problem claimed: We present an open-source Visual-Inertial-Leg Odometry (VILO) state estimation solution for legged robots, called Cerberus, which precisely estimates position on various terrains in real-time using a set of standard sensors, including st...
- Actual mechanism introduced: Fits parametric robot geometry or joint/link offsets to reduce pose prediction error.
- Hidden assumptions: calibration can be estimated separately from the policy state; online updates are stable enough to run beside the controller
- Variables treated as fixed: sensor-to-robot or model-to-world transform during policy execution; the objective while calibration actions perturb task progress
- Failure modes ignored: calibration drift after deployment or under contact-induced slippage; unobservable motions and estimator/controller feedback loops
- What it makes less novel: treating calibration as an estimable parameter is not new; performing online calibration during robot operation
- What it leaves open: how control changes when calibration belief is part of every policy decision; closed-loop task benefit from carrying calibration as policy memory
- Locator: https://doi.org/10.1109/icra48891.2023.10160486

## 24. Dynamics as Prompts: In-Context Learning for Sim-to-Real System Identifications (2025)
- Authors/venue: Xilun Zhang; Shiqi Liu; Peide Huang; William Jongwon Han; Yiqi Lyu; Mengdi Xu; et al. / IEEE Robotics and Automation Letters
- Problem claimed: Sim-to-real transfer remains a significant challenge in robotics due to the discrepancies between simulated and real-world dynamics.
- Actual mechanism introduced: Randomizes simulator or sensor parameters so a learned policy tolerates calibration variation.
- Hidden assumptions: online updates are stable enough to run beside the controller; one policy can absorb the calibration distribution without explicit state; latent context is learned as a generic nuisance rather than a physical calibration variable; identified parameters remain valid over the planning horizon
- Variables treated as fixed: the objective while calibration actions perturb task progress; deployment drift distribution relative to training randomization; meaning and observability of the latent state; model structure and parameterization
- Failure modes ignored: unobservable motions and estimator/controller feedback loops; distribution shift outside randomized support; latent collapse or entanglement with task state; nonstationary parameter drift and partial excitation
- What it makes less novel: performing online calibration during robot operation; robustifying policies against calibration errors; conditioning robot policies on inferred hidden context; using interaction data to identify model parameters
- What it leaves open: closed-loop task benefit from carrying calibration as policy memory; whether explicit low-dimensional calibration state outperforms robustness at equal data; calibration-specific observability, update rules, and control guarantees; making fast calibration d...
- Locator: https://doi.org/10.1109/lra.2025.3540391

## 25. Robust Odometry and Mapping for Multi-LiDAR Systems With Online Extrinsic Calibration (2021)
- Authors/venue: Jianhao Jiao; Haoyang Ye; Yilong Zhu; Ming Liu / IEEE Transactions on Robotics
- Problem claimed: Combining multiple LiDARs enables a robot to maximize its perceptual awareness of environments and obtain sufficient measurements, which is promising for simultaneous localization and mapping (SLAM).
- Actual mechanism introduced: Updates calibration parameters during operation using self-observed sensorimotor consistency constraints.
- Hidden assumptions: calibration can be estimated separately from the policy state; online updates are stable enough to run beside the controller; one policy can absorb the calibration distribution without explicit state; rigid extrinsics are recoverable before or between tasks
- Variables treated as fixed: sensor-to-robot or model-to-world transform during policy execution; the objective while calibration actions perturb task progress; deployment drift distribution relative to training randomization; mount rigidity and synchronized motion observations
- Failure modes ignored: calibration drift after deployment or under contact-induced slippage; unobservable motions and estimator/controller feedback loops; distribution shift outside randomized support; temperature, cable, tool, or payload shifts during the task
- What it makes less novel: treating calibration as an estimable parameter is not new; performing online calibration during robot operation; robustifying policies against calibration errors; estimating robot-camera extrinsics
- What it leaves open: how control changes when calibration belief is part of every policy decision; closed-loop task benefit from carrying calibration as policy memory; whether explicit low-dimensional calibration state outperforms robustness at equal data; policies that conditi...
- Locator: https://doi.org/10.1109/tro.2021.3078287

## 26. Robust realtime robot-world calibration for robotized transcranial magnetic stimulation (2011)
- Authors/venue: Lars Richter; Floris Ernst; Alexander Schlaefer; Achim Schweikard / International Journal of Medical Robotics and Computer Assisted Surgery
- Problem claimed: BACKGROUND: For robotized transcranial magnetic stimulation (TMS), the magnetic coil is placed on the patient's head by a robot.
- Actual mechanism introduced: Estimates a rigid transform between robot and camera/end-effector frames from paired motion observations.
- Hidden assumptions: calibration can be estimated separately from the policy state; online updates are stable enough to run beside the controller; one policy can absorb the calibration distribution without explicit state; rigid extrinsics are recoverable before or between tasks
- Variables treated as fixed: sensor-to-robot or model-to-world transform during policy execution; the objective while calibration actions perturb task progress; deployment drift distribution relative to training randomization; mount rigidity and synchronized motion observations
- Failure modes ignored: calibration drift after deployment or under contact-induced slippage; unobservable motions and estimator/controller feedback loops; distribution shift outside randomized support; temperature, cable, tool, or payload shifts during the task
- What it makes less novel: treating calibration as an estimable parameter is not new; performing online calibration during robot operation; robustifying policies against calibration errors; estimating robot-camera extrinsics
- What it leaves open: how control changes when calibration belief is part of every policy decision; closed-loop task benefit from carrying calibration as policy memory; whether explicit low-dimensional calibration state outperforms robustness at equal data; policies that conditi...
- Locator: https://doi.org/10.1002/rcs.411

## 27. Adaptive robotic visual tracking: theory and experiments (1993)
- Authors/venue: Nikos Papanikolopoulos; P.K. Khosla / IEEE Transactions on Automatic Control
- Problem claimed: The use of a vision sensor in the feedback loop is addressed within the controlled active vision framework.
- Actual mechanism introduced: Uses image/Jacobian feedback to close the loop around visual error despite imperfect calibration.
- Hidden assumptions: calibration can be estimated separately from the policy state; online updates are stable enough to run beside the controller; visual feedback can absorb geometric error without representing the cause
- Variables treated as fixed: sensor-to-robot or model-to-world transform during policy execution; the objective while calibration actions perturb task progress; image Jacobian validity near the current pose
- Failure modes ignored: calibration drift after deployment or under contact-induced slippage; unobservable motions and estimator/controller feedback loops; large drift, occlusion, and nonlocal Jacobian mismatch
- What it makes less novel: treating calibration as an estimable parameter is not new; performing online calibration during robot operation; closing the loop around calibration errors with feedback
- What it leaves open: how control changes when calibration belief is part of every policy decision; closed-loop task benefit from carrying calibration as policy memory; when explicit calibration state improves over pure servo feedback
- Locator: https://doi.org/10.1109/9.210141

## 28. Gaze gesture based human robot interaction for laparoscopic surgery (2017)
- Authors/venue: Kenko Fujii; Gauthier Gras; Antonino Salerno; GuangZhong Yang / Medical Image Analysis
- Problem claimed: While minimally invasive surgery offers great benefits in terms of reduced patient trauma, bleeding, as well as faster recovery time, it still presents surgeons with major ergonomic challenges.
- Actual mechanism introduced: Infers a compact latent context variable from recent interaction and conditions the policy or model on it.
- Hidden assumptions: calibration can be estimated separately from the policy state; online updates are stable enough to run beside the controller; latent context is learned as a generic nuisance rather than a physical calibration variable
- Variables treated as fixed: sensor-to-robot or model-to-world transform during policy execution; the objective while calibration actions perturb task progress; meaning and observability of the latent state
- Failure modes ignored: calibration drift after deployment or under contact-induced slippage; unobservable motions and estimator/controller feedback loops; latent collapse or entanglement with task state
- What it makes less novel: treating calibration as an estimable parameter is not new; performing online calibration during robot operation; conditioning robot policies on inferred hidden context
- What it leaves open: how control changes when calibration belief is part of every policy decision; closed-loop task benefit from carrying calibration as policy memory; calibration-specific observability, update rules, and control guarantees
- Locator: https://doi.org/10.1016/j.media.2017.11.011

## 29. A Modeling and Data-driven Control Framework for Rigid-soft Hybrid Robot with Visual Servoing (2023)
- Authors/venue: Shaoying He; Langlang Sun; Yunwen Xu; Dewei Li / IEEE Robotics and Automation Letters
- Problem claimed: In this letter, a rigid-soft hybrid robot with visual servoing is designed to improve robotic properties of accuracy and safe interaction, where the hybrid robot is connected by a soft robot and six degrees of freedom rigid robot in series.
- Actual mechanism introduced: Estimates a rigid transform between robot and camera/end-effector frames from paired motion observations.
- Hidden assumptions: calibration can be estimated separately from the policy state; visual feedback can absorb geometric error without representing the cause; rigid extrinsics are recoverable before or between tasks
- Variables treated as fixed: sensor-to-robot or model-to-world transform during policy execution; image Jacobian validity near the current pose; mount rigidity and synchronized motion observations
- Failure modes ignored: calibration drift after deployment or under contact-induced slippage; large drift, occlusion, and nonlocal Jacobian mismatch; temperature, cable, tool, or payload shifts during the task
- What it makes less novel: treating calibration as an estimable parameter is not new; closing the loop around calibration errors with feedback; estimating robot-camera extrinsics
- What it leaves open: how control changes when calibration belief is part of every policy decision; when explicit calibration state improves over pure servo feedback; policies that condition on continuing extrinsic belief during task execution
- Locator: https://doi.org/10.1109/lra.2023.3318118

## 30. Modelling Generalized Forces with Reinforcement Learning for Sim-to-Real Transfer (2019)
- Authors/venue: Rae Jeong; Jackie Kay; Francesco Romano; Thomas Lampe; Rothorl, Tom; Abbas Abdolmaleki; et al. / arXiv (Cornell University)
- Problem claimed: Learning robotic control policies in the real world gives rise to challenges in data efficiency, safety, and controlling the initial condition of the system.
- Actual mechanism introduced: Identifies physical model parameters or residual dynamics from trajectories for control or simulation.
- Hidden assumptions: identified parameters remain valid over the planning horizon
- Variables treated as fixed: model structure and parameterization
- Failure modes ignored: nonstationary parameter drift and partial excitation
- What it makes less novel: using interaction data to identify model parameters
- What it leaves open: making fast calibration drift a first-class recurrent state rather than a batch ID result
- Locator: https://doi.org/10.48550/arxiv.1910.09471

## 31. Uncalibrated 6-DoF Robotic Grasping With RGB-D Sensor: A Keypoint-Driven Servoing Method (2024)
- Authors/venue: Junqi Luo; Liucun Zhu; Zhenyu Zhang; Wenhao Bai / IEEE Sensors Journal
- Problem claimed: Existing 6-degree-of-freedom (6-DoF) robotic grasping methods based on 3-D pose estimation often suffer from long-standing issues of quantization errors, inference delays, and susceptibility to interference.
- Actual mechanism introduced: Randomizes simulator or sensor parameters so a learned policy tolerates calibration variation.
- Hidden assumptions: calibration can be estimated separately from the policy state; one policy can absorb the calibration distribution without explicit state; visual feedback can absorb geometric error without representing the cause; rigid extrinsics are recoverable before or between tasks
- Variables treated as fixed: sensor-to-robot or model-to-world transform during policy execution; deployment drift distribution relative to training randomization; image Jacobian validity near the current pose; mount rigidity and synchronized motion observations
- Failure modes ignored: calibration drift after deployment or under contact-induced slippage; distribution shift outside randomized support; large drift, occlusion, and nonlocal Jacobian mismatch; temperature, cable, tool, or payload shifts during the task
- What it makes less novel: treating calibration as an estimable parameter is not new; robustifying policies against calibration errors; closing the loop around calibration errors with feedback; estimating robot-camera extrinsics
- What it leaves open: how control changes when calibration belief is part of every policy decision; whether explicit low-dimensional calibration state outperforms robustness at equal data; when explicit calibration state improves over pure servo feedback; policies that condition...
- Locator: https://doi.org/10.1109/jsen.2024.3367498

## 32. Tightly-Coupled LiDAR-IMU-Wheel Odometry With Online Calibration of a Kinematic Model for Skid-Steering Robots (2024)
- Authors/venue: Taku Okawara; Kenji Koide; Shuji Oishi; Masashi Yokozuka; Atsuhiko Banno; Kentaro Uno; et al. / IEEE Access
- Problem claimed: Tunnels and long corridors are challenging environments for LiDAR-based odometry estimation algorithms because a LiDAR point cloud should degenerate (i.e., point cloud matching cannot work properly) in such environments.
- Actual mechanism introduced: Fits parametric robot geometry or joint/link offsets to reduce pose prediction error.
- Hidden assumptions: calibration can be estimated separately from the policy state; online updates are stable enough to run beside the controller; one policy can absorb the calibration distribution without explicit state; identified parameters remain valid over the planning horizon
- Variables treated as fixed: sensor-to-robot or model-to-world transform during policy execution; the objective while calibration actions perturb task progress; deployment drift distribution relative to training randomization; model structure and parameterization
- Failure modes ignored: calibration drift after deployment or under contact-induced slippage; unobservable motions and estimator/controller feedback loops; distribution shift outside randomized support; nonstationary parameter drift and partial excitation
- What it makes less novel: treating calibration as an estimable parameter is not new; performing online calibration during robot operation; robustifying policies against calibration errors; using interaction data to identify model parameters
- What it leaves open: how control changes when calibration belief is part of every policy decision; closed-loop task benefit from carrying calibration as policy memory; whether explicit low-dimensional calibration state outperforms robustness at equal data; making fast calibrati...
- Locator: https://doi.org/10.1109/access.2024.3461655

## 33. Self-Supervised Sim-to-Real Adaptation for Visual Robotic Manipulation (2019)
- Authors/venue: Rae Jeong; Yusuf Aytar; David Khosid; Yuxiang Zhou; Jackie Kay; Thomas Lampe; et al. / arXiv (Cornell University)
- Problem claimed: Collecting and automatically obtaining reward signals from real robotic visual data for the purposes of training reinforcement learning algorithms can be quite challenging and time-consuming.
- Actual mechanism introduced: Randomizes simulator or sensor parameters so a learned policy tolerates calibration variation.
- Hidden assumptions: online updates are stable enough to run beside the controller; one policy can absorb the calibration distribution without explicit state; latent context is learned as a generic nuisance rather than a physical calibration variable; identified parameters remain valid over the planning horizon
- Variables treated as fixed: the objective while calibration actions perturb task progress; deployment drift distribution relative to training randomization; meaning and observability of the latent state; model structure and parameterization
- Failure modes ignored: unobservable motions and estimator/controller feedback loops; distribution shift outside randomized support; latent collapse or entanglement with task state; nonstationary parameter drift and partial excitation
- What it makes less novel: performing online calibration during robot operation; robustifying policies against calibration errors; conditioning robot policies on inferred hidden context; using interaction data to identify model parameters
- What it leaves open: closed-loop task benefit from carrying calibration as policy memory; whether explicit low-dimensional calibration state outperforms robustness at equal data; calibration-specific observability, update rules, and control guarantees; making fast calibration d...
- Locator: https://doi.org/10.48550/arxiv.1910.09470

## 34. Visual tracking of an end-effector by adaptive kinematic prediction (1997)
- Authors/venue: Andreas Ruf; M. Tonko; Radu Horaud; Hans-Hellmut Nagel / 
- Problem claimed: Presents results of a model-based approach to visual tracking and pose estimation for a moving polyhedral tool in position-based visual servoing.
- Actual mechanism introduced: Fits parametric robot geometry or joint/link offsets to reduce pose prediction error.
- Hidden assumptions: calibration can be estimated separately from the policy state; online updates are stable enough to run beside the controller; one policy can absorb the calibration distribution without explicit state; visual feedback can absorb geometric error without representing the cause
- Variables treated as fixed: sensor-to-robot or model-to-world transform during policy execution; the objective while calibration actions perturb task progress; deployment drift distribution relative to training randomization; image Jacobian validity near the current pose
- Failure modes ignored: calibration drift after deployment or under contact-induced slippage; unobservable motions and estimator/controller feedback loops; distribution shift outside randomized support; large drift, occlusion, and nonlocal Jacobian mismatch
- What it makes less novel: treating calibration as an estimable parameter is not new; performing online calibration during robot operation; robustifying policies against calibration errors; closing the loop around calibration errors with feedback
- What it leaves open: how control changes when calibration belief is part of every policy decision; closed-loop task benefit from carrying calibration as policy memory; whether explicit low-dimensional calibration state outperforms robustness at equal data; when explicit calibra...
- Locator: https://doi.org/10.1109/iros.1997.655115

## 35. Motion control for dynamic mobile robots (2000)
- Authors/venue: Hong Zhang / Scholarly Commons (University of Pennsylvania)
- Problem claimed: In this thesis, we present research results on sensor-based motion planning and nonlinear control for mobile robotic systems.
- Actual mechanism introduced: Uses image/Jacobian feedback to close the loop around visual error despite imperfect calibration.
- Hidden assumptions: calibration can be estimated separately from the policy state; online updates are stable enough to run beside the controller; identified parameters remain valid over the planning horizon; visual feedback can absorb geometric error without representing the cause
- Variables treated as fixed: sensor-to-robot or model-to-world transform during policy execution; the objective while calibration actions perturb task progress; model structure and parameterization; image Jacobian validity near the current pose
- Failure modes ignored: calibration drift after deployment or under contact-induced slippage; unobservable motions and estimator/controller feedback loops; nonstationary parameter drift and partial excitation; large drift, occlusion, and nonlocal Jacobian mismatch
- What it makes less novel: treating calibration as an estimable parameter is not new; performing online calibration during robot operation; using interaction data to identify model parameters; closing the loop around calibration errors with feedback
- What it leaves open: how control changes when calibration belief is part of every policy decision; closed-loop task benefit from carrying calibration as policy memory; making fast calibration drift a first-class recurrent state rather than a batch ID result; when explicit calib...
- Locator: https://openalex.org/W103441712

## 36. Learning Active Task-Oriented Exploration Policies for Bridging the Sim-to-Real Gap (2020)
- Authors/venue: Jacky Liang; Saumya Saxena; Oliver Kroemer / 
- Problem claimed: Training robotic policies in simulation suffers from the sim-to-real gap, as simulated dynamics can be different from real-world dynamics.
- Actual mechanism introduced: Randomizes simulator or sensor parameters so a learned policy tolerates calibration variation.
- Hidden assumptions: online updates are stable enough to run beside the controller; one policy can absorb the calibration distribution without explicit state; identified parameters remain valid over the planning horizon
- Variables treated as fixed: the objective while calibration actions perturb task progress; deployment drift distribution relative to training randomization; model structure and parameterization
- Failure modes ignored: unobservable motions and estimator/controller feedback loops; distribution shift outside randomized support; nonstationary parameter drift and partial excitation
- What it makes less novel: performing online calibration during robot operation; robustifying policies against calibration errors; using interaction data to identify model parameters
- What it leaves open: closed-loop task benefit from carrying calibration as policy memory; whether explicit low-dimensional calibration state outperforms robustness at equal data; making fast calibration drift a first-class recurrent state rather than a batch ID result
- Locator: https://doi.org/10.15607/rss.2020.xvi.085

## 37. Underwater Dynamic Visual Servoing for a Soft Robot Arm With Online Distortion Correction (2019)
- Authors/venue: Fan Xu; Hesheng Wang; Jingchuan Wang; Kwok Wai Samuel Au; Weidong Chen / IEEE/ASME Transactions on Mechatronics
- Problem claimed: Bioinspired soft robots have generated increasing attentions due to their optimal performance in specific environments stemming from their unique morphology and sensorimotor capabilities.
- Actual mechanism introduced: Uses image/Jacobian feedback to close the loop around visual error despite imperfect calibration.
- Hidden assumptions: calibration can be estimated separately from the policy state; online updates are stable enough to run beside the controller; identified parameters remain valid over the planning horizon; visual feedback can absorb geometric error without representing the cause
- Variables treated as fixed: sensor-to-robot or model-to-world transform during policy execution; the objective while calibration actions perturb task progress; model structure and parameterization; image Jacobian validity near the current pose
- Failure modes ignored: calibration drift after deployment or under contact-induced slippage; unobservable motions and estimator/controller feedback loops; nonstationary parameter drift and partial excitation; large drift, occlusion, and nonlocal Jacobian mismatch
- What it makes less novel: treating calibration as an estimable parameter is not new; performing online calibration during robot operation; using interaction data to identify model parameters; closing the loop around calibration errors with feedback
- What it leaves open: how control changes when calibration belief is part of every policy decision; closed-loop task benefit from carrying calibration as policy memory; making fast calibration drift a first-class recurrent state rather than a batch ID result; when explicit calib...
- Locator: https://doi.org/10.1109/tmech.2019.2908242

## 38. Robust robotic visual servoing for uncertain systems (2021)
- Authors/venue: Akbar Assa / 
- Problem claimed: The control of robotic manipulators in unstructured environments is a challenging task.
- Actual mechanism introduced: Uses image/Jacobian feedback to close the loop around visual error despite imperfect calibration.
- Hidden assumptions: calibration can be estimated separately from the policy state; one policy can absorb the calibration distribution without explicit state; visual feedback can absorb geometric error without representing the cause
- Variables treated as fixed: sensor-to-robot or model-to-world transform during policy execution; deployment drift distribution relative to training randomization; image Jacobian validity near the current pose
- Failure modes ignored: calibration drift after deployment or under contact-induced slippage; distribution shift outside randomized support; large drift, occlusion, and nonlocal Jacobian mismatch
- What it makes less novel: treating calibration as an estimable parameter is not new; robustifying policies against calibration errors; closing the loop around calibration errors with feedback
- What it leaves open: how control changes when calibration belief is part of every policy decision; whether explicit low-dimensional calibration state outperforms robustness at equal data; when explicit calibration state improves over pure servo feedback
- Locator: https://doi.org/10.32920/ryerson.14668221

## 39. Residual Physics Learning and System Identification for Sim-to-real Transfer of Policies on Buoyancy Assisted Legged Robots (2023)
- Authors/venue: Nitish Sontakke; Hosik Chae; Sang Joon Lee; Tianle Huang; Dennis Hong; S. R. P. van Hal / 
- Problem claimed: The light and soft characteristics of Buoyancy Assisted Lightweight Legged Unit (BALLU) robots have a great potential to provide intrinsically safe interactions in environments involving humans, unlike many heavy and rigid robots.
- Actual mechanism introduced: Identifies physical model parameters or residual dynamics from trajectories for control or simulation.
- Hidden assumptions: online updates are stable enough to run beside the controller; one policy can absorb the calibration distribution without explicit state; identified parameters remain valid over the planning horizon
- Variables treated as fixed: the objective while calibration actions perturb task progress; deployment drift distribution relative to training randomization; model structure and parameterization
- Failure modes ignored: unobservable motions and estimator/controller feedback loops; distribution shift outside randomized support; nonstationary parameter drift and partial excitation
- What it makes less novel: performing online calibration during robot operation; robustifying policies against calibration errors; using interaction data to identify model parameters
- What it leaves open: closed-loop task benefit from carrying calibration as policy memory; whether explicit low-dimensional calibration state outperforms robustness at equal data; making fast calibration drift a first-class recurrent state rather than a batch ID result
- Locator: https://doi.org/10.1109/iros55552.2023.10342062

## 40. Hybrid position-based visual servoing with online calibration for a humanoid robot (2005)
- Authors/venue: G. Taylor; Lindsay Kleeman / 
- Problem claimed: This paper addresses the problem of visual servo control for a humanoid robot in an unstructured domestic environment.
- Actual mechanism introduced: Estimates a rigid transform between robot and camera/end-effector frames from paired motion observations.
- Hidden assumptions: calibration can be estimated separately from the policy state; online updates are stable enough to run beside the controller; one policy can absorb the calibration distribution without explicit state; visual feedback can absorb geometric error without representing the cause
- Variables treated as fixed: sensor-to-robot or model-to-world transform during policy execution; the objective while calibration actions perturb task progress; deployment drift distribution relative to training randomization; image Jacobian validity near the current pose
- Failure modes ignored: calibration drift after deployment or under contact-induced slippage; unobservable motions and estimator/controller feedback loops; distribution shift outside randomized support; large drift, occlusion, and nonlocal Jacobian mismatch
- What it makes less novel: treating calibration as an estimable parameter is not new; performing online calibration during robot operation; robustifying policies against calibration errors; closing the loop around calibration errors with feedback
- What it leaves open: how control changes when calibration belief is part of every policy decision; closed-loop task benefit from carrying calibration as policy memory; whether explicit low-dimensional calibration state outperforms robustness at equal data; when explicit calibra...
- Locator: https://doi.org/10.1109/iros.2004.1389432

## 41. KOVIS: Keypoint-based Visual Servoing with Zero-Shot Sim-to-Real Transfer for Robotics Manipulation (2020)
- Authors/venue: En Yen Puang; Keng Peng Tee; Wei Jing / 
- Problem claimed: We present KOVIS, a novel learning-based, calibration-free visual servoing method for fine robotic manipulation tasks with eye-in-hand stereo camera system.
- Actual mechanism introduced: Randomizes simulator or sensor parameters so a learned policy tolerates calibration variation.
- Hidden assumptions: calibration can be estimated separately from the policy state; online updates are stable enough to run beside the controller; one policy can absorb the calibration distribution without explicit state; visual feedback can absorb geometric error without representing the cause
- Variables treated as fixed: sensor-to-robot or model-to-world transform during policy execution; the objective while calibration actions perturb task progress; deployment drift distribution relative to training randomization; image Jacobian validity near the current pose
- Failure modes ignored: calibration drift after deployment or under contact-induced slippage; unobservable motions and estimator/controller feedback loops; distribution shift outside randomized support; large drift, occlusion, and nonlocal Jacobian mismatch
- What it makes less novel: treating calibration as an estimable parameter is not new; performing online calibration during robot operation; robustifying policies against calibration errors; closing the loop around calibration errors with feedback
- What it leaves open: how control changes when calibration belief is part of every policy decision; closed-loop task benefit from carrying calibration as policy memory; whether explicit low-dimensional calibration state outperforms robustness at equal data; when explicit calibra...
- Locator: https://doi.org/10.1109/iros45743.2020.9341370

## 42. Flexible Self-Calibrated Visual Servoing for a Humanoid Robot (2001)
- Authors/venue: Geoffrey Taylor; Lindsay Kleeman / 
- Problem claimed: This paper develops a flexible position-based visual servo framework to enable a humanoid robot to perform a variety of visually controlled manipulation tasks.
- Actual mechanism introduced: Estimates a rigid transform between robot and camera/end-effector frames from paired motion observations.
- Hidden assumptions: calibration can be estimated separately from the policy state; online updates are stable enough to run beside the controller; one policy can absorb the calibration distribution without explicit state; visual feedback can absorb geometric error without representing the cause
- Variables treated as fixed: sensor-to-robot or model-to-world transform during policy execution; the objective while calibration actions perturb task progress; deployment drift distribution relative to training randomization; image Jacobian validity near the current pose
- Failure modes ignored: calibration drift after deployment or under contact-induced slippage; unobservable motions and estimator/controller feedback loops; distribution shift outside randomized support; large drift, occlusion, and nonlocal Jacobian mismatch
- What it makes less novel: treating calibration as an estimable parameter is not new; performing online calibration during robot operation; robustifying policies against calibration errors; closing the loop around calibration errors with feedback
- What it leaves open: how control changes when calibration belief is part of every policy decision; closed-loop task benefit from carrying calibration as policy memory; whether explicit low-dimensional calibration state outperforms robustness at equal data; when explicit calibra...
- Locator: https://openalex.org/W2166326430

## 43. Visual servoing for humanoid grasping and manipulation tasks (2008)
- Authors/venue: Nikolaus Vahrenkamp; Sebastian Wieland; P. Azad; Diego Gonzalez; Tamim Asfour; Rudiger Dillmann / 
- Problem claimed: Using visual feedback to control the movement of the end-effector is a common approach for robust execution of robot movements in real-world scenarios.
- Actual mechanism introduced: Estimates a rigid transform between robot and camera/end-effector frames from paired motion observations.
- Hidden assumptions: calibration can be estimated separately from the policy state; one policy can absorb the calibration distribution without explicit state; visual feedback can absorb geometric error without representing the cause; rigid extrinsics are recoverable before or between tasks
- Variables treated as fixed: sensor-to-robot or model-to-world transform during policy execution; deployment drift distribution relative to training randomization; image Jacobian validity near the current pose; mount rigidity and synchronized motion observations
- Failure modes ignored: calibration drift after deployment or under contact-induced slippage; distribution shift outside randomized support; large drift, occlusion, and nonlocal Jacobian mismatch; temperature, cable, tool, or payload shifts during the task
- What it makes less novel: treating calibration as an estimable parameter is not new; robustifying policies against calibration errors; closing the loop around calibration errors with feedback; estimating robot-camera extrinsics
- What it leaves open: how control changes when calibration belief is part of every policy decision; whether explicit low-dimensional calibration state outperforms robustness at equal data; when explicit calibration state improves over pure servo feedback; policies that condition...
- Locator: https://doi.org/10.1109/ichr.2008.4755985

## 44. Visual Servoing based on Linear Approximation of the Inverser Kinematics. (1996)
- Authors/venue: Takashi Mitsuda; Noriaki Maru; K. Fujikawa; Fumio Miyazaki / Journal of the Robotics Society of Japan
- Problem claimed: We propose a simple visual servoing based on linear approximation of the inverse kinematics.
- Actual mechanism introduced: Estimates a rigid transform between robot and camera/end-effector frames from paired motion observations.
- Hidden assumptions: calibration can be estimated separately from the policy state; online updates are stable enough to run beside the controller; one policy can absorb the calibration distribution without explicit state; visual feedback can absorb geometric error without representing the cause
- Variables treated as fixed: sensor-to-robot or model-to-world transform during policy execution; the objective while calibration actions perturb task progress; deployment drift distribution relative to training randomization; image Jacobian validity near the current pose
- Failure modes ignored: calibration drift after deployment or under contact-induced slippage; unobservable motions and estimator/controller feedback loops; distribution shift outside randomized support; large drift, occlusion, and nonlocal Jacobian mismatch
- What it makes less novel: treating calibration as an estimable parameter is not new; performing online calibration during robot operation; robustifying policies against calibration errors; closing the loop around calibration errors with feedback
- What it leaves open: how control changes when calibration belief is part of every policy decision; closed-loop task benefit from carrying calibration as policy memory; whether explicit low-dimensional calibration state outperforms robustness at equal data; when explicit calibra...
- Locator: https://doi.org/10.7210/jrsj.14.743

## 45. On the performance of a biologically motivated visual control strategy for robotic hand-eye coordination (2002)
- Authors/venue: Alexa Hauck; Georg Passig; Thomas Schenk; Michael Sorg; Georg Farber / 
- Problem claimed: Research has focused on developing control strategies that allow to work with imprecisely calibrated or even uncalibrated robot systems.
- Actual mechanism introduced: Estimates a rigid transform between robot and camera/end-effector frames from paired motion observations.
- Hidden assumptions: calibration can be estimated separately from the policy state; visual feedback can absorb geometric error without representing the cause; rigid extrinsics are recoverable before or between tasks
- Variables treated as fixed: sensor-to-robot or model-to-world transform during policy execution; image Jacobian validity near the current pose; mount rigidity and synchronized motion observations
- Failure modes ignored: calibration drift after deployment or under contact-induced slippage; large drift, occlusion, and nonlocal Jacobian mismatch; temperature, cable, tool, or payload shifts during the task
- What it makes less novel: treating calibration as an estimable parameter is not new; closing the loop around calibration errors with feedback; estimating robot-camera extrinsics
- What it leaves open: how control changes when calibration belief is part of every policy decision; when explicit calibration state improves over pure servo feedback; policies that condition on continuing extrinsic belief during task execution
- Locator: https://doi.org/10.1109/iros.2000.895205

## 46. Learning Active Task-Oriented Exploration Policies for Bridging the Sim-to-Real Gap (2020)
- Authors/venue: Jacky Liang; Saumya Saxena; Oliver Kroemer / arXiv (Cornell University)
- Problem claimed: Training robotic policies in simulation suffers from the sim-to-real gap, as simulated dynamics can be different from real-world dynamics.
- Actual mechanism introduced: Randomizes simulator or sensor parameters so a learned policy tolerates calibration variation.
- Hidden assumptions: online updates are stable enough to run beside the controller; one policy can absorb the calibration distribution without explicit state; identified parameters remain valid over the planning horizon
- Variables treated as fixed: the objective while calibration actions perturb task progress; deployment drift distribution relative to training randomization; model structure and parameterization
- Failure modes ignored: unobservable motions and estimator/controller feedback loops; distribution shift outside randomized support; nonstationary parameter drift and partial excitation
- What it makes less novel: performing online calibration during robot operation; robustifying policies against calibration errors; using interaction data to identify model parameters
- What it leaves open: closed-loop task benefit from carrying calibration as policy memory; whether explicit low-dimensional calibration state outperforms robustness at equal data; making fast calibration drift a first-class recurrent state rather than a batch ID result
- Locator: https://doi.org/10.48550/arxiv.2006.01952

## 47. Logarithmic Observation of Feature Depth for Image-Based Visual Servoing (2021)
- Authors/venue: Xiangfei Li; Huan Zhao; Han Ding / IEEE Transactions on Automation Science and Engineering
- Problem claimed: Due to the robustness to robot modeling and camera calibration errors and avoidance of complete target geometry, image-based visual servoing has always been an important topic in the fields such as robotics, computer vision and so forth.
- Actual mechanism introduced: Uses image/Jacobian feedback to close the loop around visual error despite imperfect calibration.
- Hidden assumptions: calibration can be estimated separately from the policy state; one policy can absorb the calibration distribution without explicit state; visual feedback can absorb geometric error without representing the cause
- Variables treated as fixed: sensor-to-robot or model-to-world transform during policy execution; deployment drift distribution relative to training randomization; image Jacobian validity near the current pose
- Failure modes ignored: calibration drift after deployment or under contact-induced slippage; distribution shift outside randomized support; large drift, occlusion, and nonlocal Jacobian mismatch
- What it makes less novel: treating calibration as an estimable parameter is not new; robustifying policies against calibration errors; closing the loop around calibration errors with feedback
- What it leaves open: how control changes when calibration belief is part of every policy decision; whether explicit low-dimensional calibration state outperforms robustness at equal data; when explicit calibration state improves over pure servo feedback
- Locator: https://doi.org/10.1109/tase.2021.3125698

## 48. Hand-eye calibration and grasping pose calculation with motion error compensation and vertical-component correction for 4-R(2-SS) parallel robot (2020)
- Authors/venue: Qian Zhang; Guoqin Gao / International Journal of Advanced Robotic Systems
- Problem claimed: Due to motion constraint of 4-R(2-SS) parallel robot, it is difficult to calculate the translation component of hand-eye calibration based on the existing model solving method accurately.
- Actual mechanism introduced: Estimates a rigid transform between robot and camera/end-effector frames from paired motion observations.
- Hidden assumptions: calibration can be estimated separately from the policy state; online updates are stable enough to run beside the controller; identified parameters remain valid over the planning horizon; rigid extrinsics are recoverable before or between tasks
- Variables treated as fixed: sensor-to-robot or model-to-world transform during policy execution; the objective while calibration actions perturb task progress; model structure and parameterization; mount rigidity and synchronized motion observations
- Failure modes ignored: calibration drift after deployment or under contact-induced slippage; unobservable motions and estimator/controller feedback loops; nonstationary parameter drift and partial excitation; temperature, cable, tool, or payload shifts during the task
- What it makes less novel: treating calibration as an estimable parameter is not new; performing online calibration during robot operation; using interaction data to identify model parameters; estimating robot-camera extrinsics
- What it leaves open: how control changes when calibration belief is part of every policy decision; closed-loop task benefit from carrying calibration as policy memory; making fast calibration drift a first-class recurrent state rather than a batch ID result; policies that condi...
- Locator: https://doi.org/10.1177/1729881420909012

## 49. MAT: Multi-Fingered Adaptive Tactile Grasping via Deep Reinforcement\n Learning (2019)
- Authors/venue: Bohan Wu; Iretiayo Akinola; Jacob Varley; Peter K. Allen / arXiv (Cornell University)
- Problem claimed: Vision-based grasping systems typically adopt an open-loop execution of a\nplanned grasp.
- Actual mechanism introduced: Uses contact or tactile feedback to estimate geometry, pose, or interaction parameters during manipulation.
- Hidden assumptions: calibration can be estimated separately from the policy state; one policy can absorb the calibration distribution without explicit state
- Variables treated as fixed: sensor-to-robot or model-to-world transform during policy execution; deployment drift distribution relative to training randomization
- Failure modes ignored: calibration drift after deployment or under contact-induced slippage; distribution shift outside randomized support
- What it makes less novel: treating calibration as an estimable parameter is not new; robustifying policies against calibration errors
- What it leaves open: how control changes when calibration belief is part of every policy decision; whether explicit low-dimensional calibration state outperforms robustness at equal data
- Locator: https://doi.org/10.48550/arxiv.1909.04787

## 50. Online Extrinsic Parameter Calibration for Robotic Camera-Encoder System (2019)
- Authors/venue: Xuefeng Wang; Haoyao Chen; Yanjie Li; Hailin Huang / IEEE Transactions on Industrial Informatics
- Problem claimed: Cameras and encoders are widely used in mobile robots, and extrinsic parameter calibration of these sensors is crucial in practical performance.
- Actual mechanism introduced: Estimates a rigid transform between robot and camera/end-effector frames from paired motion observations.
- Hidden assumptions: calibration can be estimated separately from the policy state; online updates are stable enough to run beside the controller; rigid extrinsics are recoverable before or between tasks
- Variables treated as fixed: sensor-to-robot or model-to-world transform during policy execution; the objective while calibration actions perturb task progress; mount rigidity and synchronized motion observations
- Failure modes ignored: calibration drift after deployment or under contact-induced slippage; unobservable motions and estimator/controller feedback loops; temperature, cable, tool, or payload shifts during the task
- What it makes less novel: treating calibration as an estimable parameter is not new; performing online calibration during robot operation; estimating robot-camera extrinsics
- What it leaves open: how control changes when calibration belief is part of every policy decision; closed-loop task benefit from carrying calibration as policy memory; policies that condition on continuing extrinsic belief during task execution
- Locator: https://doi.org/10.1109/tii.2019.2894106

## 51. Fast calibration of embedded non-overlapping cameras (2011)
- Authors/venue: Pierre Lebraly; Eric Royer; Omar Ait-Aider; Clement Deymier; Michel Dhome / 
- Problem claimed: This article deals with a simple and flexible extrinsic calibration method, for non-overlapping camera rig.
- Actual mechanism introduced: Estimates a rigid transform between robot and camera/end-effector frames from paired motion observations.
- Hidden assumptions: calibration can be estimated separately from the policy state; online updates are stable enough to run beside the controller; rigid extrinsics are recoverable before or between tasks
- Variables treated as fixed: sensor-to-robot or model-to-world transform during policy execution; the objective while calibration actions perturb task progress; mount rigidity and synchronized motion observations
- Failure modes ignored: calibration drift after deployment or under contact-induced slippage; unobservable motions and estimator/controller feedback loops; temperature, cable, tool, or payload shifts during the task
- What it makes less novel: treating calibration as an estimable parameter is not new; performing online calibration during robot operation; estimating robot-camera extrinsics
- What it leaves open: how control changes when calibration belief is part of every policy decision; closed-loop task benefit from carrying calibration as policy memory; policies that condition on continuing extrinsic belief during task execution
- Locator: https://doi.org/10.1109/icra.2011.5979743

## 52. Indirect Object-to-Robot Pose Estimation from an External Monocular RGB Camera (2020)
- Authors/venue: Jonathan Tremblay; Stephen Tyree; Terry Mosier; Stan Birchfield / 
- Problem claimed: We present a robotic grasping system that uses a single external monocular RGB camera as input.
- Actual mechanism introduced: Randomizes simulator or sensor parameters so a learned policy tolerates calibration variation.
- Hidden assumptions: calibration can be estimated separately from the policy state; online updates are stable enough to run beside the controller; one policy can absorb the calibration distribution without explicit state; latent context is learned as a generic nuisance rather than a physical calibration variable
- Variables treated as fixed: sensor-to-robot or model-to-world transform during policy execution; the objective while calibration actions perturb task progress; deployment drift distribution relative to training randomization; meaning and observability of the latent state
- Failure modes ignored: calibration drift after deployment or under contact-induced slippage; unobservable motions and estimator/controller feedback loops; distribution shift outside randomized support; latent collapse or entanglement with task state
- What it makes less novel: treating calibration as an estimable parameter is not new; performing online calibration during robot operation; robustifying policies against calibration errors; conditioning robot policies on inferred hidden context
- What it leaves open: how control changes when calibration belief is part of every policy decision; closed-loop task benefit from carrying calibration as policy memory; whether explicit low-dimensional calibration state outperforms robustness at equal data; calibration-specific...
- Locator: https://doi.org/10.1109/iros45743.2020.9341163

## 53. Servomatic: a modular system for robust positioning using stereo visual servoing (2002)
- Authors/venue: Kentaro Toyama; Gregory D. Hager; J. Wang / 
- Problem claimed: We introduce Servomatic, a modular system for robot motion control based on calibration-insensitive visual servoing.
- Actual mechanism introduced: Estimates a rigid transform between robot and camera/end-effector frames from paired motion observations.
- Hidden assumptions: calibration can be estimated separately from the policy state; one policy can absorb the calibration distribution without explicit state; visual feedback can absorb geometric error without representing the cause; rigid extrinsics are recoverable before or between tasks
- Variables treated as fixed: sensor-to-robot or model-to-world transform during policy execution; deployment drift distribution relative to training randomization; image Jacobian validity near the current pose; mount rigidity and synchronized motion observations
- Failure modes ignored: calibration drift after deployment or under contact-induced slippage; distribution shift outside randomized support; large drift, occlusion, and nonlocal Jacobian mismatch; temperature, cable, tool, or payload shifts during the task
- What it makes less novel: treating calibration as an estimable parameter is not new; robustifying policies against calibration errors; closing the loop around calibration errors with feedback; estimating robot-camera extrinsics
- What it leaves open: how control changes when calibration belief is part of every policy decision; whether explicit low-dimensional calibration state outperforms robustness at equal data; when explicit calibration state improves over pure servo feedback; policies that condition...
- Locator: https://doi.org/10.1109/robot.1996.506560

## 54. Motion control of underwater robotic arm using calibration-free visual servoing system (2015)
- Authors/venue: Akihiro Kawamura; Manami Kubo; Kenshiro Yokoi; Norimitsu Sakagami; Sadao Kawamura / 
- Problem claimed: Underwater manipulators are traditionally controlled by skilled operators to achieve tasks, e.g.
- Actual mechanism introduced: Uses image/Jacobian feedback to close the loop around visual error despite imperfect calibration.
- Hidden assumptions: calibration can be estimated separately from the policy state; one policy can absorb the calibration distribution without explicit state; visual feedback can absorb geometric error without representing the cause
- Variables treated as fixed: sensor-to-robot or model-to-world transform during policy execution; deployment drift distribution relative to training randomization; image Jacobian validity near the current pose
- Failure modes ignored: calibration drift after deployment or under contact-induced slippage; distribution shift outside randomized support; large drift, occlusion, and nonlocal Jacobian mismatch
- What it makes less novel: treating calibration as an estimable parameter is not new; robustifying policies against calibration errors; closing the loop around calibration errors with feedback
- What it leaves open: how control changes when calibration belief is part of every policy decision; whether explicit low-dimensional calibration state outperforms robustness at equal data; when explicit calibration state improves over pure servo feedback
- Locator: https://doi.org/10.1109/oceans-genova.2015.7271454

## 55. DURableVS: Data-efficient Unsupervised Recalibrating Visual Servoing via online learning in a structured generative model (2022)
- Authors/venue: Nishad Gothoskar; Miguel Lazaro-Gredilla; Yasemin Bekiroglu; Abhishek Agarwal; Joshua B. Tenenbaum; Vikash K. Mansinghka; et al. / 2022 International Conference on Robotics and Automation (ICRA)
- Problem claimed: Visual servoing enables robotic systems to perform accurate closed-loop control, which is required in many applications.
- Actual mechanism introduced: Fits parametric robot geometry or joint/link offsets to reduce pose prediction error.
- Hidden assumptions: calibration can be estimated separately from the policy state; online updates are stable enough to run beside the controller; visual feedback can absorb geometric error without representing the cause
- Variables treated as fixed: sensor-to-robot or model-to-world transform during policy execution; the objective while calibration actions perturb task progress; image Jacobian validity near the current pose
- Failure modes ignored: calibration drift after deployment or under contact-induced slippage; unobservable motions and estimator/controller feedback loops; large drift, occlusion, and nonlocal Jacobian mismatch
- What it makes less novel: treating calibration as an estimable parameter is not new; performing online calibration during robot operation; closing the loop around calibration errors with feedback
- What it leaves open: how control changes when calibration belief is part of every policy decision; closed-loop task benefit from carrying calibration as policy memory; when explicit calibration state improves over pure servo feedback
- Locator: https://doi.org/10.1109/icra46639.2022.9811607

## 56. Rapid locomotion via reinforcement learning (2024)
- Authors/venue: Gabriel B. Margolis; Ge Yang; Kartik Paigwar; Tao Chen; Pulkit Agrawal / The International Journal of Robotics Research
- Problem claimed: Agile maneuvers such as sprinting and high-speed turning in the wild are challenging for legged robots.
- Actual mechanism introduced: Identifies physical model parameters or residual dynamics from trajectories for control or simulation.
- Hidden assumptions: online updates are stable enough to run beside the controller; one policy can absorb the calibration distribution without explicit state; identified parameters remain valid over the planning horizon
- Variables treated as fixed: the objective while calibration actions perturb task progress; deployment drift distribution relative to training randomization; model structure and parameterization
- Failure modes ignored: unobservable motions and estimator/controller feedback loops; distribution shift outside randomized support; nonstationary parameter drift and partial excitation
- What it makes less novel: performing online calibration during robot operation; robustifying policies against calibration errors; using interaction data to identify model parameters
- What it leaves open: closed-loop task benefit from carrying calibration as policy memory; whether explicit low-dimensional calibration state outperforms robustness at equal data; making fast calibration drift a first-class recurrent state rather than a batch ID result
- Locator: https://doi.org/10.1177/02783649231224053

## 57. Towards Robotic Eye Surgery: Marker-Free, Online Hand-Eye Calibration Using Optical Coherence Tomography Images (2018)
- Authors/venue: Mingchuan Zhou; Mahdi Hamad; Jakob Weiss; Abouzar Eslami; Kai Huang; Mathias Maier; et al. / IEEE Robotics and Automation Letters
- Problem claimed: Ophthalmic microsurgery is known to be a challenging operation, which requires very precise and dexterous manipulation.
- Actual mechanism introduced: Estimates a rigid transform between robot and camera/end-effector frames from paired motion observations.
- Hidden assumptions: calibration can be estimated separately from the policy state; online updates are stable enough to run beside the controller; one policy can absorb the calibration distribution without explicit state; rigid extrinsics are recoverable before or between tasks
- Variables treated as fixed: sensor-to-robot or model-to-world transform during policy execution; the objective while calibration actions perturb task progress; deployment drift distribution relative to training randomization; mount rigidity and synchronized motion observations
- Failure modes ignored: calibration drift after deployment or under contact-induced slippage; unobservable motions and estimator/controller feedback loops; distribution shift outside randomized support; temperature, cable, tool, or payload shifts during the task
- What it makes less novel: treating calibration as an estimable parameter is not new; performing online calibration during robot operation; robustifying policies against calibration errors; estimating robot-camera extrinsics
- What it leaves open: how control changes when calibration belief is part of every policy decision; closed-loop task benefit from carrying calibration as policy memory; whether explicit low-dimensional calibration state outperforms robustness at equal data; policies that conditi...
- Locator: https://doi.org/10.1109/lra.2018.2858744

## 58. Rapid Locomotion via Reinforcement Learning (2022)
- Authors/venue: Gabriel B. Margolis; Ge Yang; Kartik Paigwar; Tao Chen; Pulkit Agrawal / 
- Problem claimed: Agile maneuvers such as sprinting and high-speed turning in the wild are challenging for legged robots.
- Actual mechanism introduced: Identifies physical model parameters or residual dynamics from trajectories for control or simulation.
- Hidden assumptions: online updates are stable enough to run beside the controller; one policy can absorb the calibration distribution without explicit state; identified parameters remain valid over the planning horizon
- Variables treated as fixed: the objective while calibration actions perturb task progress; deployment drift distribution relative to training randomization; model structure and parameterization
- Failure modes ignored: unobservable motions and estimator/controller feedback loops; distribution shift outside randomized support; nonstationary parameter drift and partial excitation
- What it makes less novel: performing online calibration during robot operation; robustifying policies against calibration errors; using interaction data to identify model parameters
- What it leaves open: closed-loop task benefit from carrying calibration as policy memory; whether explicit low-dimensional calibration state outperforms robustness at equal data; making fast calibration drift a first-class recurrent state rather than a batch ID result
- Locator: https://doi.org/10.15607/rss.2022.xviii.022

## 59. TuneNet: One-Shot Residual Tuning for System Identification and\n Sim-to-Real Robot Task Transfer (2019)
- Authors/venue: Adam Allevato; Elaine Schaertl Short; Mitch Pryor; Andrea L. Thomaz / arXiv (Cornell University)
- Problem claimed: As researchers teach robots to perform more and more complex tasks, the need\nfor realistic simulation environments is growing.
- Actual mechanism introduced: Identifies physical model parameters or residual dynamics from trajectories for control or simulation.
- Hidden assumptions: online updates are stable enough to run beside the controller; identified parameters remain valid over the planning horizon
- Variables treated as fixed: the objective while calibration actions perturb task progress; model structure and parameterization
- Failure modes ignored: unobservable motions and estimator/controller feedback loops; nonstationary parameter drift and partial excitation
- What it makes less novel: performing online calibration during robot operation; using interaction data to identify model parameters
- What it leaves open: closed-loop task benefit from carrying calibration as policy memory; making fast calibration drift a first-class recurrent state rather than a batch ID result
- Locator: https://doi.org/10.48550/arxiv.1907.11200

## 60. Visual servoing in robotic manufacturing systems for accurate positioning (2007)
- Authors/venue: Zheng Li / Spectrum Research Repository (Concordia University)
- Problem claimed: Automated robotic manufacturing systems require accurate robot positioning.
- Actual mechanism introduced: Estimates a rigid transform between robot and camera/end-effector frames from paired motion observations.
- Hidden assumptions: calibration can be estimated separately from the policy state; online updates are stable enough to run beside the controller; one policy can absorb the calibration distribution without explicit state; visual feedback can absorb geometric error without representing the cause
- Variables treated as fixed: sensor-to-robot or model-to-world transform during policy execution; the objective while calibration actions perturb task progress; deployment drift distribution relative to training randomization; image Jacobian validity near the current pose
- Failure modes ignored: calibration drift after deployment or under contact-induced slippage; unobservable motions and estimator/controller feedback loops; distribution shift outside randomized support; large drift, occlusion, and nonlocal Jacobian mismatch
- What it makes less novel: treating calibration as an estimable parameter is not new; performing online calibration during robot operation; robustifying policies against calibration errors; closing the loop around calibration errors with feedback
- What it leaves open: how control changes when calibration belief is part of every policy decision; closed-loop task benefit from carrying calibration as policy memory; whether explicit low-dimensional calibration state outperforms robustness at equal data; when explicit calibra...
- Locator: https://openalex.org/W262488008

## 61. Robotics Arm Visual Servo: Estimation of Arm-Space Kinematics Relations with Epipolar Geometry (2012)
- Authors/venue: Ebrahim A. Mattar / InTech eBooks
- Problem claimed: Numerous advances in robotics have been inspired by reliable concepts of biological systems.
- Actual mechanism introduced: Fits parametric robot geometry or joint/link offsets to reduce pose prediction error.
- Hidden assumptions: calibration can be estimated separately from the policy state; visual feedback can absorb geometric error without representing the cause
- Variables treated as fixed: sensor-to-robot or model-to-world transform during policy execution; image Jacobian validity near the current pose
- Failure modes ignored: calibration drift after deployment or under contact-induced slippage; large drift, occlusion, and nonlocal Jacobian mismatch
- What it makes less novel: treating calibration as an estimable parameter is not new; closing the loop around calibration errors with feedback
- What it leaves open: how control changes when calibration belief is part of every policy decision; when explicit calibration state improves over pure servo feedback
- Locator: https://doi.org/10.5772/25605

## 62. Markerless Camera-to-Robot Pose Estimation via Self-Supervised Sim-to-Real Transfer (2023)
- Authors/venue: Jingpei Lu; Florian Richter; Michael C. Yip / 
- Problem claimed: Solving the camera-to-robot pose is a fundamental requirement for vision-based robot control, and is a process that takes considerable effort and cares to make accurate.
- Actual mechanism introduced: Randomizes simulator or sensor parameters so a learned policy tolerates calibration variation.
- Hidden assumptions: calibration can be estimated separately from the policy state; online updates are stable enough to run beside the controller; one policy can absorb the calibration distribution without explicit state; visual feedback can absorb geometric error without representing the cause
- Variables treated as fixed: sensor-to-robot or model-to-world transform during policy execution; the objective while calibration actions perturb task progress; deployment drift distribution relative to training randomization; image Jacobian validity near the current pose
- Failure modes ignored: calibration drift after deployment or under contact-induced slippage; unobservable motions and estimator/controller feedback loops; distribution shift outside randomized support; large drift, occlusion, and nonlocal Jacobian mismatch
- What it makes less novel: treating calibration as an estimable parameter is not new; performing online calibration during robot operation; robustifying policies against calibration errors; closing the loop around calibration errors with feedback
- What it leaves open: how control changes when calibration belief is part of every policy decision; closed-loop task benefit from carrying calibration as policy memory; whether explicit low-dimensional calibration state outperforms robustness at equal data; when explicit calibra...
- Locator: https://doi.org/10.1109/cvpr52729.2023.02040

## 63. A Simultaneous Optimization Method of Calibration and Measurement for a Typical Hand-Eye Positioning System (2020)
- Authors/venue: Yuan Zhang; Zhi-cheng Qiu; Xianmin Zhang / IEEE Transactions on Instrumentation and Measurement
- Problem claimed: Hand-eye calibration is one of the key technologies of robot hand and eye coordination operation.
- Actual mechanism introduced: Estimates a rigid transform between robot and camera/end-effector frames from paired motion observations.
- Hidden assumptions: calibration can be estimated separately from the policy state; online updates are stable enough to run beside the controller; rigid extrinsics are recoverable before or between tasks
- Variables treated as fixed: sensor-to-robot or model-to-world transform during policy execution; the objective while calibration actions perturb task progress; mount rigidity and synchronized motion observations
- Failure modes ignored: calibration drift after deployment or under contact-induced slippage; unobservable motions and estimator/controller feedback loops; temperature, cable, tool, or payload shifts during the task
- What it makes less novel: treating calibration as an estimable parameter is not new; performing online calibration during robot operation; estimating robot-camera extrinsics
- What it leaves open: how control changes when calibration belief is part of every policy decision; closed-loop task benefit from carrying calibration as policy memory; policies that condition on continuing extrinsic belief during task execution
- Locator: https://doi.org/10.1109/tim.2020.3013308

## 64. Visual Representations for Semantic Target Driven Navigation (2019)
- Authors/venue: Arsalan Mousavian; Alexander Toshev; Marek Fiser; Jana Kosecka; Ayzaan Wahid; James C. Davidson / 
- Problem claimed: What is a good visual representation for navigation?
- Actual mechanism introduced: Randomizes simulator or sensor parameters so a learned policy tolerates calibration variation.
- Hidden assumptions: one policy can absorb the calibration distribution without explicit state; latent context is learned as a generic nuisance rather than a physical calibration variable; identified parameters remain valid over the planning horizon
- Variables treated as fixed: deployment drift distribution relative to training randomization; meaning and observability of the latent state; model structure and parameterization
- Failure modes ignored: distribution shift outside randomized support; latent collapse or entanglement with task state; nonstationary parameter drift and partial excitation
- What it makes less novel: robustifying policies against calibration errors; conditioning robot policies on inferred hidden context; using interaction data to identify model parameters
- What it leaves open: whether explicit low-dimensional calibration state outperforms robustness at equal data; calibration-specific observability, update rules, and control guarantees; making fast calibration drift a first-class recurrent state rather than a batch ID result
- Locator: https://doi.org/10.1109/icra.2019.8793493

## 65. Robot Model Identification and Learning: A Modern Perspective (2023)
- Authors/venue: Taeyoon Lee; Jaewoon Kwon; Patrick M. Wensing; Frank C. Park / Annual Review of Control Robotics and Autonomous Systems
- Problem claimed: In recent years, the increasing complexity and safety-critical nature of robotic tasks have highlighted the importance of accurate and reliable robot models.
- Actual mechanism introduced: Identifies physical model parameters or residual dynamics from trajectories for control or simulation.
- Hidden assumptions: identified parameters remain valid over the planning horizon
- Variables treated as fixed: model structure and parameterization
- Failure modes ignored: nonstationary parameter drift and partial excitation
- What it makes less novel: using interaction data to identify model parameters
- What it leaves open: making fast calibration drift a first-class recurrent state rather than a batch ID result
- Locator: https://doi.org/10.1146/annurev-control-061523-102310

## 66. Visual Servoing of Robot Manipulators Part I: Projective Kinematics (1999)
- Authors/venue: Andreas Ruf; Radu Horaud / The International Journal of Robotics Research
- Problem claimed: Visual servoing of robot manipulators is a key technique where the appearance of an object in the image plane is used to control the velocity of the end-effector such that the desired position is reached in the scene.
- Actual mechanism introduced: Fits parametric robot geometry or joint/link offsets to reduce pose prediction error.
- Hidden assumptions: calibration can be estimated separately from the policy state; visual feedback can absorb geometric error without representing the cause
- Variables treated as fixed: sensor-to-robot or model-to-world transform during policy execution; image Jacobian validity near the current pose
- Failure modes ignored: calibration drift after deployment or under contact-induced slippage; large drift, occlusion, and nonlocal Jacobian mismatch
- What it makes less novel: treating calibration as an estimable parameter is not new; closing the loop around calibration errors with feedback
- What it leaves open: how control changes when calibration belief is part of every policy decision; when explicit calibration state improves over pure servo feedback
- Locator: https://doi.org/10.1177/02783649922067744

## 67. Pose Estimation for Robot Manipulators via Keypoint Optimization and Sim-to-Real Transfer (2022)
- Authors/venue: Jingpei Lu; Florian Richter; Michael C. Yip / IEEE Robotics and Automation Letters
- Problem claimed: Keypoint detection is an essential building block for many robotic applications like motion capture and pose estimation.
- Actual mechanism introduced: Randomizes simulator or sensor parameters so a learned policy tolerates calibration variation.
- Hidden assumptions: calibration can be estimated separately from the policy state; online updates are stable enough to run beside the controller; one policy can absorb the calibration distribution without explicit state
- Variables treated as fixed: sensor-to-robot or model-to-world transform during policy execution; the objective while calibration actions perturb task progress; deployment drift distribution relative to training randomization
- Failure modes ignored: calibration drift after deployment or under contact-induced slippage; unobservable motions and estimator/controller feedback loops; distribution shift outside randomized support
- What it makes less novel: treating calibration as an estimable parameter is not new; performing online calibration during robot operation; robustifying policies against calibration errors
- What it leaves open: how control changes when calibration belief is part of every policy decision; closed-loop task benefit from carrying calibration as policy memory; whether explicit low-dimensional calibration state outperforms robustness at equal data
- Locator: https://doi.org/10.1109/lra.2022.3151981

## 68. Fine-tuning Deep Reinforcement Learning Policies with r-STDP for Domain Adaptation (2022)
- Authors/venue: Mahmoud Akl; Yulia Sandamirskaya; Deniz Ergene; Florian Walter; Alois Knoll / 
- Problem claimed: Using deep reinforcement learning policies that are trained in simulation on real robotic platforms requires fine-tuning due to discrepancies between simulated and real environments.
- Actual mechanism introduced: Randomizes simulator or sensor parameters so a learned policy tolerates calibration variation.
- Hidden assumptions: one policy can absorb the calibration distribution without explicit state; identified parameters remain valid over the planning horizon
- Variables treated as fixed: deployment drift distribution relative to training randomization; model structure and parameterization
- Failure modes ignored: distribution shift outside randomized support; nonstationary parameter drift and partial excitation
- What it makes less novel: robustifying policies against calibration errors; using interaction data to identify model parameters
- What it leaves open: whether explicit low-dimensional calibration state outperforms robustness at equal data; making fast calibration drift a first-class recurrent state rather than a batch ID result
- Locator: https://doi.org/10.1145/3546790.3546804

## 69. Improving Image-Based Visual Servoing with Three-Dimensional Features (2003)
- Authors/venue: Enric Cervera; Angel P. del Pobil; Francois Berry; Philippe Martinet / The International Journal of Robotics Research
- Problem claimed: Neither of the classical visual servoing approaches, position-based and image-based, are completely satisfactory.
- Actual mechanism introduced: Estimates a rigid transform between robot and camera/end-effector frames from paired motion observations.
- Hidden assumptions: calibration can be estimated separately from the policy state; one policy can absorb the calibration distribution without explicit state; visual feedback can absorb geometric error without representing the cause; rigid extrinsics are recoverable before or between tasks
- Variables treated as fixed: sensor-to-robot or model-to-world transform during policy execution; deployment drift distribution relative to training randomization; image Jacobian validity near the current pose; mount rigidity and synchronized motion observations
- Failure modes ignored: calibration drift after deployment or under contact-induced slippage; distribution shift outside randomized support; large drift, occlusion, and nonlocal Jacobian mismatch; temperature, cable, tool, or payload shifts during the task
- What it makes less novel: treating calibration as an estimable parameter is not new; robustifying policies against calibration errors; closing the loop around calibration errors with feedback; estimating robot-camera extrinsics
- What it leaves open: how control changes when calibration belief is part of every policy decision; whether explicit low-dimensional calibration state outperforms robustness at equal data; when explicit calibration state improves over pure servo feedback; policies that condition...
- Locator: https://doi.org/10.1177/027836490302210003

## 70. Insert-One: One-Shot Robust Visual-Force Servoing for Novel Object Insertion with 6-DoF Tracking (2024)
- Authors/venue: Haonan Chang; Abdeslam Boularias; Siddarth Jain / 
- Problem claimed: Recent advancements in autonomous robotic assembly have shown promising results, especially in addressing the precision insertion challenge.
- Actual mechanism introduced: Uses image/Jacobian feedback to close the loop around visual error despite imperfect calibration.
- Hidden assumptions: calibration can be estimated separately from the policy state; one policy can absorb the calibration distribution without explicit state; visual feedback can absorb geometric error without representing the cause
- Variables treated as fixed: sensor-to-robot or model-to-world transform during policy execution; deployment drift distribution relative to training randomization; image Jacobian validity near the current pose
- Failure modes ignored: calibration drift after deployment or under contact-induced slippage; distribution shift outside randomized support; large drift, occlusion, and nonlocal Jacobian mismatch
- What it makes less novel: treating calibration as an estimable parameter is not new; robustifying policies against calibration errors; closing the loop around calibration errors with feedback
- What it leaves open: how control changes when calibration belief is part of every policy decision; whether explicit low-dimensional calibration state outperforms robustness at equal data; when explicit calibration state improves over pure servo feedback
- Locator: https://doi.org/10.1109/iros58592.2024.10801884

## 71. Safety-Enhanced Model-Free Visual Servoing for Continuum Tubular Robots Through Singularity Avoidance in Confined Environments (2019)
- Authors/venue: Keyu Wu; GuoNiu Zhu; Liao Wu; WenChao Gao; Shuang Song; Chwee Ming Lim; et al. / IEEE Access
- Problem claimed: Minimally invasive procedures have gained ever-increasing popularity due to their advantages of smaller incisions, faster recoveries, fewer complications, and reduced scarring to name a few.
- Actual mechanism introduced: Estimates a rigid transform between robot and camera/end-effector frames from paired motion observations.
- Hidden assumptions: calibration can be estimated separately from the policy state; visual feedback can absorb geometric error without representing the cause; rigid extrinsics are recoverable before or between tasks
- Variables treated as fixed: sensor-to-robot or model-to-world transform during policy execution; image Jacobian validity near the current pose; mount rigidity and synchronized motion observations
- Failure modes ignored: calibration drift after deployment or under contact-induced slippage; large drift, occlusion, and nonlocal Jacobian mismatch; temperature, cable, tool, or payload shifts during the task
- What it makes less novel: treating calibration as an estimable parameter is not new; closing the loop around calibration errors with feedback; estimating robot-camera extrinsics
- What it leaves open: how control changes when calibration belief is part of every policy decision; when explicit calibration state improves over pure servo feedback; policies that condition on continuing extrinsic belief during task execution
- Locator: https://doi.org/10.1109/access.2019.2891952

## 72. Sim-to-Real Transfer of Robotic Control with Dynamics Randomization (2018)
- Authors/venue: Xue Bin Peng; Marcin Andrychowicz; Wojciech Zaremba; Pieter Abbeel / 
- Problem claimed: Simulations are attractive environments for training agents as they provide an abundant source of data and alleviate certain safety concerns during the training process.
- Actual mechanism introduced: Identifies physical model parameters or residual dynamics from trajectories for control or simulation.
- Hidden assumptions: calibration can be estimated separately from the policy state; one policy can absorb the calibration distribution without explicit state; identified parameters remain valid over the planning horizon
- Variables treated as fixed: sensor-to-robot or model-to-world transform during policy execution; deployment drift distribution relative to training randomization; model structure and parameterization
- Failure modes ignored: calibration drift after deployment or under contact-induced slippage; distribution shift outside randomized support; nonstationary parameter drift and partial excitation
- What it makes less novel: treating calibration as an estimable parameter is not new; robustifying policies against calibration errors; using interaction data to identify model parameters
- What it leaves open: how control changes when calibration belief is part of every policy decision; whether explicit low-dimensional calibration state outperforms robustness at equal data; making fast calibration drift a first-class recurrent state rather than a batch ID result
- Locator: https://doi.org/10.1109/icra.2018.8460528

## 73. Sim-to-Real Transfer for Biped Locomotion (2019)
- Authors/venue: Wenhao Yu; Visak Kumar; Greg Turk; C. Karen Liu / 
- Problem claimed: We present a new approach for transfer of dynamic robot control policies such as biped locomotion from simulation to real hardware.
- Actual mechanism introduced: Identifies physical model parameters or residual dynamics from trajectories for control or simulation.
- Hidden assumptions: latent context is learned as a generic nuisance rather than a physical calibration variable; identified parameters remain valid over the planning horizon
- Variables treated as fixed: meaning and observability of the latent state; model structure and parameterization
- Failure modes ignored: latent collapse or entanglement with task state; nonstationary parameter drift and partial excitation
- What it makes less novel: conditioning robot policies on inferred hidden context; using interaction data to identify model parameters
- What it leaves open: calibration-specific observability, update rules, and control guarantees; making fast calibration drift a first-class recurrent state rather than a batch ID result
- Locator: https://doi.org/10.1109/iros40897.2019.8968053

## 74. On-orbit hand-eye calibration using cooperative target (2014)
- Authors/venue: Zheng Wen; Yuefeng Wang; Na Di; Mingming Jin / 
- Problem claimed: Aiming at the on-orbit hand-eye calibration problem of space robot arm, a new method for solving the position and orientation of the wrist-mounted camera with respect to the robot wrist is proposed using cooperative target.
- Actual mechanism introduced: Estimates a rigid transform between robot and camera/end-effector frames from paired motion observations.
- Hidden assumptions: calibration can be estimated separately from the policy state; rigid extrinsics are recoverable before or between tasks
- Variables treated as fixed: sensor-to-robot or model-to-world transform during policy execution; mount rigidity and synchronized motion observations
- Failure modes ignored: calibration drift after deployment or under contact-induced slippage; temperature, cable, tool, or payload shifts during the task
- What it makes less novel: treating calibration as an estimable parameter is not new; estimating robot-camera extrinsics
- What it leaves open: how control changes when calibration belief is part of every policy decision; policies that condition on continuing extrinsic belief during task execution
- Locator: https://openalex.org/W2468938089

## 75. Sim-to-Real: Mapless Navigation for USVs Using Deep Reinforcement Learning (2022)
- Authors/venue: Ning Wang; Yabiao Wang; YuMing Zhao; Yong Wang; Zhigang Li / Journal of Marine Science and Engineering
- Problem claimed: In recent years, mapless navigation using deep reinforcement learning algorithms has shown significant advantages in improving robot motion planning capabilities.
- Actual mechanism introduced: Randomizes simulator or sensor parameters so a learned policy tolerates calibration variation.
- Hidden assumptions: one policy can absorb the calibration distribution without explicit state; identified parameters remain valid over the planning horizon
- Variables treated as fixed: deployment drift distribution relative to training randomization; model structure and parameterization
- Failure modes ignored: distribution shift outside randomized support; nonstationary parameter drift and partial excitation
- What it makes less novel: robustifying policies against calibration errors; using interaction data to identify model parameters
- What it leaves open: whether explicit low-dimensional calibration state outperforms robustness at equal data; making fast calibration drift a first-class recurrent state rather than a batch ID result
- Locator: https://doi.org/10.3390/jmse10070895

## 76. Globally Optimal Symbolic Hand-Eye Calibration (2020)
- Authors/venue: Jin Wu; Ming Liu; Yilong Zhu; Zuhao Zou; MingZhe Dai; Chengxi Zhang; et al. / IEEE/ASME Transactions on Mechatronics
- Problem claimed: Hand-eye calibration (HEC) is a kernel technique guaranteeing precision industrial visual servoing and robotic grasping.
- Actual mechanism introduced: Estimates a rigid transform between robot and camera/end-effector frames from paired motion observations.
- Hidden assumptions: calibration can be estimated separately from the policy state; visual feedback can absorb geometric error without representing the cause; rigid extrinsics are recoverable before or between tasks
- Variables treated as fixed: sensor-to-robot or model-to-world transform during policy execution; image Jacobian validity near the current pose; mount rigidity and synchronized motion observations
- Failure modes ignored: calibration drift after deployment or under contact-induced slippage; large drift, occlusion, and nonlocal Jacobian mismatch; temperature, cable, tool, or payload shifts during the task
- What it makes less novel: treating calibration as an estimable parameter is not new; closing the loop around calibration errors with feedback; estimating robot-camera extrinsics
- What it leaves open: how control changes when calibration belief is part of every policy decision; when explicit calibration state improves over pure servo feedback; policies that condition on continuing extrinsic belief during task execution
- Locator: https://doi.org/10.1109/tmech.2020.3019306

## 77. Accuracy assessment and kinematic calibration of the robotic endoscopic microsurgical system (2016)
- Authors/venue: Lihang Feng; Paul Wilkening; Yunuscan Sevimli; Marcin Balicki; Kevin Olds; Russell H. Taylor / 
- Problem claimed: This paper explores the general stereotactic accuracy of the Robotic Endoscopic Microsurgical System (REMS) by calibrating with a standard optical tracking system.
- Actual mechanism introduced: Estimates a rigid transform between robot and camera/end-effector frames from paired motion observations.
- Hidden assumptions: calibration can be estimated separately from the policy state; rigid extrinsics are recoverable before or between tasks
- Variables treated as fixed: sensor-to-robot or model-to-world transform during policy execution; mount rigidity and synchronized motion observations
- Failure modes ignored: calibration drift after deployment or under contact-induced slippage; temperature, cable, tool, or payload shifts during the task
- What it makes less novel: treating calibration as an estimable parameter is not new; estimating robot-camera extrinsics
- What it leaves open: how control changes when calibration belief is part of every policy decision; policies that condition on continuing extrinsic belief during task execution
- Locator: https://doi.org/10.1109/embc.2016.7591872

## 78. What can be learned from human reach-to-grasp movements for the design of robotic hand-eye systems? (2003)
- Authors/venue: Alexa Hauck; Michael Sorg; Georg Farber; Thomas Schenk / 
- Problem claimed: In the field of robot motion control, visual servoing has been proposed as the suitable strategy to cope with imprecise models and calibration errors.
- Actual mechanism introduced: Estimates a rigid transform between robot and camera/end-effector frames from paired motion observations.
- Hidden assumptions: calibration can be estimated separately from the policy state; one policy can absorb the calibration distribution without explicit state; visual feedback can absorb geometric error without representing the cause; rigid extrinsics are recoverable before or between tasks
- Variables treated as fixed: sensor-to-robot or model-to-world transform during policy execution; deployment drift distribution relative to training randomization; image Jacobian validity near the current pose; mount rigidity and synchronized motion observations
- Failure modes ignored: calibration drift after deployment or under contact-induced slippage; distribution shift outside randomized support; large drift, occlusion, and nonlocal Jacobian mismatch; temperature, cable, tool, or payload shifts during the task
- What it makes less novel: treating calibration as an estimable parameter is not new; robustifying policies against calibration errors; closing the loop around calibration errors with feedback; estimating robot-camera extrinsics
- What it leaves open: how control changes when calibration belief is part of every policy decision; whether explicit low-dimensional calibration state outperforms robustness at equal data; when explicit calibration state improves over pure servo feedback; policies that condition...
- Locator: https://doi.org/10.1109/robot.1999.773976

## 79. A Single-Point Pose Constraint Based 6R Robot Kinematic Calibration Method Through Monocular Vision (2023)
- Authors/venue: Yongxing Liu; Xiaoqi Tang; Bao Song; Jinglong Zhong; Xiangdong Zhou / 
- Problem claimed: This paper proposes a 6R robot kinematic closed-loop calibration method, in order to improve the 6R robot kinematic absolute positioning accuracy, that establishes a single-point pose constraint through the monocular vision-based pose me...
- Actual mechanism introduced: Estimates a rigid transform between robot and camera/end-effector frames from paired motion observations.
- Hidden assumptions: calibration can be estimated separately from the policy state; rigid extrinsics are recoverable before or between tasks
- Variables treated as fixed: sensor-to-robot or model-to-world transform during policy execution; mount rigidity and synchronized motion observations
- Failure modes ignored: calibration drift after deployment or under contact-induced slippage; temperature, cable, tool, or payload shifts during the task
- What it makes less novel: treating calibration as an estimable parameter is not new; estimating robot-camera extrinsics
- What it leaves open: how control changes when calibration belief is part of every policy decision; policies that condition on continuing extrinsic belief during task execution
- Locator: https://doi.org/10.1109/isoirs59890.2023.00040

## 80. Sim-to-Real: Learning Agile Locomotion For Quadruped Robots (2018)
- Authors/venue: Jie Tan; Tingnan Zhang; Erwin Coumans; Atl Iscen; Yunfei Bai; Danijar Hafner; et al. / 
- Problem claimed: Designing agile locomotion for quadruped robots often requires extensive expertise and tedious manual tuning.
- Actual mechanism introduced: Identifies physical model parameters or residual dynamics from trajectories for control or simulation.
- Hidden assumptions: one policy can absorb the calibration distribution without explicit state; identified parameters remain valid over the planning horizon
- Variables treated as fixed: deployment drift distribution relative to training randomization; model structure and parameterization
- Failure modes ignored: distribution shift outside randomized support; nonstationary parameter drift and partial excitation
- What it makes less novel: robustifying policies against calibration errors; using interaction data to identify model parameters
- What it leaves open: whether explicit low-dimensional calibration state outperforms robustness at equal data; making fast calibration drift a first-class recurrent state rather than a batch ID result
- Locator: https://doi.org/10.15607/rss.2018.xiv.010

## 81. Visual servoing of robot manipulator without camera calibration (2002)
- Authors/venue: Chien Chern Cheah; S. Kawamura; S. Arimoto / 
- Problem claimed: In this paper, visual-based feedback control laws are proposed for setpoint control of robots without camera and kinematic calibrations.
- Actual mechanism introduced: Fits parametric robot geometry or joint/link offsets to reduce pose prediction error.
- Hidden assumptions: calibration can be estimated separately from the policy state; visual feedback can absorb geometric error without representing the cause
- Variables treated as fixed: sensor-to-robot or model-to-world transform during policy execution; image Jacobian validity near the current pose
- Failure modes ignored: calibration drift after deployment or under contact-induced slippage; large drift, occlusion, and nonlocal Jacobian mismatch
- What it makes less novel: treating calibration as an estimable parameter is not new; closing the loop around calibration errors with feedback
- What it leaves open: how control changes when calibration belief is part of every policy decision; when explicit calibration state improves over pure servo feedback
- Locator: https://doi.org/10.1109/amc.1998.743638

## 82. Internal models in sensorimotor integration: perspectives from adaptive control theory (2005)
- Authors/venue: Chung Tin; ChiSang Poon / Journal of Neural Engineering
- Problem claimed: Internal models and adaptive controls are empirical and mathematical paradigms that have evolved separately to describe learning control processes in brain systems and engineering systems, respectively.
- Actual mechanism introduced: Identifies physical model parameters or residual dynamics from trajectories for control or simulation.
- Hidden assumptions: identified parameters remain valid over the planning horizon
- Variables treated as fixed: model structure and parameterization
- Failure modes ignored: nonstationary parameter drift and partial excitation
- What it makes less novel: using interaction data to identify model parameters
- What it leaves open: making fast calibration drift a first-class recurrent state rather than a batch ID result
- Locator: https://doi.org/10.1088/1741-2560/2/3/s01

## 83. Sim-to-Real: Learning Agile Locomotion For Quadruped Robots (2018)
- Authors/venue: Jie Tan; Tingnan Zhang; Erwin Coumans; Atl Iscen; Yunfei Bai; Danijar Hafner; et al. / arXiv (Cornell University)
- Problem claimed: Designing agile locomotion for quadruped robots often requires extensive expertise and tedious manual tuning.
- Actual mechanism introduced: Identifies physical model parameters or residual dynamics from trajectories for control or simulation.
- Hidden assumptions: one policy can absorb the calibration distribution without explicit state; identified parameters remain valid over the planning horizon
- Variables treated as fixed: deployment drift distribution relative to training randomization; model structure and parameterization
- Failure modes ignored: distribution shift outside randomized support; nonstationary parameter drift and partial excitation
- What it makes less novel: robustifying policies against calibration errors; using interaction data to identify model parameters
- What it leaves open: whether explicit low-dimensional calibration state outperforms robustness at equal data; making fast calibration drift a first-class recurrent state rather than a batch ID result
- Locator: https://doi.org/10.48550/arxiv.1804.10332

## 84. Sim-to-real transfer of active suspension control using deep reinforcement learning (2024)
- Authors/venue: Viktor Wiberg; Erik Wallin; Arvid Falldin; Tobias Semberg; Morgan Rossander; Eddie Wadbro; et al. / Robotics and Autonomous Systems
- Problem claimed: We explore sim-to-real transfer of deep reinforcement learning controllers for a heavy vehicle with active suspensions designed for traversing rough terrain.
- Actual mechanism introduced: Randomizes simulator or sensor parameters so a learned policy tolerates calibration variation.
- Hidden assumptions: one policy can absorb the calibration distribution without explicit state; identified parameters remain valid over the planning horizon
- Variables treated as fixed: deployment drift distribution relative to training randomization; model structure and parameterization
- Failure modes ignored: distribution shift outside randomized support; nonstationary parameter drift and partial excitation
- What it makes less novel: robustifying policies against calibration errors; using interaction data to identify model parameters
- What it leaves open: whether explicit low-dimensional calibration state outperforms robustness at equal data; making fast calibration drift a first-class recurrent state rather than a batch ID result
- Locator: https://doi.org/10.1016/j.robot.2024.104731

## 85. Sim-to-Real Transfer of Compliant Bipedal Locomotion on Torque Sensor-Less Gear-Driven Humanoid (2023)
- Authors/venue: Shimpei Masuda; Kuniyuki Takahashi / 
- Problem claimed: Sim-to-real is a mainstream method to cope with the large number of trials needed by typical deep reinforcement learning methods.
- Actual mechanism introduced: Identifies physical model parameters or residual dynamics from trajectories for control or simulation.
- Hidden assumptions: identified parameters remain valid over the planning horizon
- Variables treated as fixed: model structure and parameterization
- Failure modes ignored: nonstationary parameter drift and partial excitation
- What it makes less novel: using interaction data to identify model parameters
- What it leaves open: making fast calibration drift a first-class recurrent state rather than a batch ID result
- Locator: https://doi.org/10.1109/humanoids57100.2023.10375181

## 86. Deep adaptive control with online identification for industrial robots (2022)
- Authors/venue: Tan Shen; Xuechun Qiao; Yunlong Dong; YuRan Wang; Wei Zhang; Ye Yuan / Science China Technological Sciences
- Problem claimed: Deep adaptive control with online identification for industrial robots
- Actual mechanism introduced: Identifies physical model parameters or residual dynamics from trajectories for control or simulation.
- Hidden assumptions: online updates are stable enough to run beside the controller; identified parameters remain valid over the planning horizon
- Variables treated as fixed: the objective while calibration actions perturb task progress; model structure and parameterization
- Failure modes ignored: unobservable motions and estimator/controller feedback loops; nonstationary parameter drift and partial excitation
- What it makes less novel: performing online calibration during robot operation; using interaction data to identify model parameters
- What it leaves open: closed-loop task benefit from carrying calibration as policy memory; making fast calibration drift a first-class recurrent state rather than a batch ID result
- Locator: https://doi.org/10.1007/s11431-022-2183-7

## 87. Hand-eye calibration of line structured-light sensor by scanning and reconstruction of a free-placed standard cylindrical target (2024)
- Authors/venue: Zhengping Deng; Yisheng Ruan; Fei Hao; Tianyao Liu / Measurement
- Problem claimed: A cylinder instead of sphere is used for calibration, which is easy to manufacture and can cover a larger robot workspace .
- Actual mechanism introduced: Estimates a rigid transform between robot and camera/end-effector frames from paired motion observations.
- Hidden assumptions: calibration can be estimated separately from the policy state; online updates are stable enough to run beside the controller; one policy can absorb the calibration distribution without explicit state; rigid extrinsics are recoverable before or between tasks
- Variables treated as fixed: sensor-to-robot or model-to-world transform during policy execution; the objective while calibration actions perturb task progress; deployment drift distribution relative to training randomization; mount rigidity and synchronized motion observations
- Failure modes ignored: calibration drift after deployment or under contact-induced slippage; unobservable motions and estimator/controller feedback loops; distribution shift outside randomized support; temperature, cable, tool, or payload shifts during the task
- What it makes less novel: treating calibration as an estimable parameter is not new; performing online calibration during robot operation; robustifying policies against calibration errors; estimating robot-camera extrinsics
- What it leaves open: how control changes when calibration belief is part of every policy decision; closed-loop task benefit from carrying calibration as policy memory; whether explicit low-dimensional calibration state outperforms robustness at equal data; policies that conditi...
- Locator: https://doi.org/10.1016/j.measurement.2024.114487

## 88. Robot Visual Servoing Grasping Based on Top-Down Keypoint Detection Network (2023)
- Authors/venue: Junqi Luo; Liucun Zhu; Liang Li; Peitao Hong / IEEE Transactions on Instrumentation and Measurement
- Problem claimed: The paradigm of "deep-learning visual perception + hand-eye transformation + motion planning" for robot grasping has demonstrated viable capabilities in specific scenarios.
- Actual mechanism introduced: Randomizes simulator or sensor parameters so a learned policy tolerates calibration variation.
- Hidden assumptions: calibration can be estimated separately from the policy state; one policy can absorb the calibration distribution without explicit state; visual feedback can absorb geometric error without representing the cause; rigid extrinsics are recoverable before or between tasks
- Variables treated as fixed: sensor-to-robot or model-to-world transform during policy execution; deployment drift distribution relative to training randomization; image Jacobian validity near the current pose; mount rigidity and synchronized motion observations
- Failure modes ignored: calibration drift after deployment or under contact-induced slippage; distribution shift outside randomized support; large drift, occlusion, and nonlocal Jacobian mismatch; temperature, cable, tool, or payload shifts during the task
- What it makes less novel: treating calibration as an estimable parameter is not new; robustifying policies against calibration errors; closing the loop around calibration errors with feedback; estimating robot-camera extrinsics
- What it leaves open: how control changes when calibration belief is part of every policy decision; whether explicit low-dimensional calibration state outperforms robustness at equal data; when explicit calibration state improves over pure servo feedback; policies that condition...
- Locator: https://doi.org/10.1109/tim.2023.3335521

## 89. Sim-to-real transfer of active suspension control using deep reinforcement learning (2023)
- Authors/venue: Viktor Wiberg; Erik Wallin; Arvid Falldin; Tobias Semberg; Morgan Rossander; Eddie Wadbro; et al. / arXiv (Cornell University)
- Problem claimed: We explore sim-to-real transfer of deep reinforcement learning controllers for a heavy vehicle with active suspensions designed for traversing rough terrain.
- Actual mechanism introduced: Randomizes simulator or sensor parameters so a learned policy tolerates calibration variation.
- Hidden assumptions: one policy can absorb the calibration distribution without explicit state; identified parameters remain valid over the planning horizon
- Variables treated as fixed: deployment drift distribution relative to training randomization; model structure and parameterization
- Failure modes ignored: distribution shift outside randomized support; nonstationary parameter drift and partial excitation
- What it makes less novel: robustifying policies against calibration errors; using interaction data to identify model parameters
- What it leaves open: whether explicit low-dimensional calibration state outperforms robustness at equal data; making fast calibration drift a first-class recurrent state rather than a batch ID result
- Locator: https://doi.org/10.48550/arxiv.2306.11171

## 90. A modular system for robust positioning using feedback from stereo vision (1997)
- Authors/venue: Gregory D. Hager / IEEE Transactions on Robotics and Automation
- Problem claimed: This paper introduces a modular framework for robot motion control using stereo vision.
- Actual mechanism introduced: Estimates a rigid transform between robot and camera/end-effector frames from paired motion observations.
- Hidden assumptions: calibration can be estimated separately from the policy state; one policy can absorb the calibration distribution without explicit state; rigid extrinsics are recoverable before or between tasks
- Variables treated as fixed: sensor-to-robot or model-to-world transform during policy execution; deployment drift distribution relative to training randomization; mount rigidity and synchronized motion observations
- Failure modes ignored: calibration drift after deployment or under contact-induced slippage; distribution shift outside randomized support; temperature, cable, tool, or payload shifts during the task
- What it makes less novel: treating calibration as an estimable parameter is not new; robustifying policies against calibration errors; estimating robot-camera extrinsics
- What it leaves open: how control changes when calibration belief is part of every policy decision; whether explicit low-dimensional calibration state outperforms robustness at equal data; policies that condition on continuing extrinsic belief during task execution
- Locator: https://doi.org/10.1109/70.611326

## 91. Automatic Online Calibration of Cameras and Lasers (2013)
- Authors/venue: Jesse Levinson; Sebastian Thrun / 
- Problem claimed: The combined use of 3D scanning lasers with 2D cameras has become increasingly popular in mobile robotics, as the sparse depth measurements of the former augment the dense color information of the latter.
- Actual mechanism introduced: Updates calibration parameters during operation using self-observed sensorimotor consistency constraints.
- Hidden assumptions: calibration can be estimated separately from the policy state; online updates are stable enough to run beside the controller
- Variables treated as fixed: sensor-to-robot or model-to-world transform during policy execution; the objective while calibration actions perturb task progress
- Failure modes ignored: calibration drift after deployment or under contact-induced slippage; unobservable motions and estimator/controller feedback loops
- What it makes less novel: treating calibration as an estimable parameter is not new; performing online calibration during robot operation
- What it leaves open: how control changes when calibration belief is part of every policy decision; closed-loop task benefit from carrying calibration as policy memory
- Locator: https://doi.org/10.15607/rss.2013.ix.029

## 92. 2 1/2 D visual servoing (1999)
- Authors/venue: Ezio Malis; Francois Chaumette; S. Boudet / IEEE Transactions on Robotics and Automation
- Problem claimed: We propose an approach to vision-based robot control, called 2 1/2 D visual servoing, which avoids the respective drawbacks of classical position-based and image-based visual servoing.
- Actual mechanism introduced: Uses image/Jacobian feedback to close the loop around visual error despite imperfect calibration.
- Hidden assumptions: calibration can be estimated separately from the policy state; one policy can absorb the calibration distribution without explicit state; visual feedback can absorb geometric error without representing the cause
- Variables treated as fixed: sensor-to-robot or model-to-world transform during policy execution; deployment drift distribution relative to training randomization; image Jacobian validity near the current pose
- Failure modes ignored: calibration drift after deployment or under contact-induced slippage; distribution shift outside randomized support; large drift, occlusion, and nonlocal Jacobian mismatch
- What it makes less novel: treating calibration as an estimable parameter is not new; robustifying policies against calibration errors; closing the loop around calibration errors with feedback
- What it leaves open: how control changes when calibration belief is part of every policy decision; whether explicit low-dimensional calibration state outperforms robustness at equal data; when explicit calibration state improves over pure servo feedback
- Locator: https://doi.org/10.1109/70.760345

## 93. Calibration of Parallel Kinematic Machines: Theory and Applications (2006)
- Authors/venue: Giovanni Legnani; Diego Tosi; Riccardo Adamini; Irene Fassi / 
- Problem claimed: Introduction\nAs already stated in the chapter addressing the calibration of serial manipulators, kinematic calibration is a procedure for the identification and the consequent compensation of the geometrical pose errors of a robot.
- Actual mechanism introduced: Fits parametric robot geometry or joint/link offsets to reduce pose prediction error.
- Hidden assumptions: calibration can be estimated separately from the policy state; online updates are stable enough to run beside the controller
- Variables treated as fixed: sensor-to-robot or model-to-world transform during policy execution; the objective while calibration actions perturb task progress
- Failure modes ignored: calibration drift after deployment or under contact-induced slippage; unobservable motions and estimator/controller feedback loops
- What it makes less novel: treating calibration as an estimable parameter is not new; performing online calibration during robot operation
- What it leaves open: how control changes when calibration belief is part of every policy decision; closed-loop task benefit from carrying calibration as policy memory
- Locator: https://doi.org/10.5772/4897

## 94. Automatic self-contained calibration of an industrial dual-arm robot with cameras using self-contact, planar constraints, and self-observation (2021)
- Authors/venue: Karla Stepanova; Jakub Rozlivek; Frantisek Puciow; Pavel Krsek; Tomas Pajdla; Matej Hoffmann / Robotics and Computer-Integrated Manufacturing
- Problem claimed: We present a robot kinematic calibration method that combines complementary calibration approaches: self-contact, planar constraints, and self-observation.
- Actual mechanism introduced: Fits parametric robot geometry or joint/link offsets to reduce pose prediction error.
- Hidden assumptions: calibration can be estimated separately from the policy state; online updates are stable enough to run beside the controller
- Variables treated as fixed: sensor-to-robot or model-to-world transform during policy execution; the objective while calibration actions perturb task progress
- Failure modes ignored: calibration drift after deployment or under contact-induced slippage; unobservable motions and estimator/controller feedback loops
- What it makes less novel: treating calibration as an estimable parameter is not new; performing online calibration during robot operation
- What it leaves open: how control changes when calibration belief is part of every policy decision; closed-loop task benefit from carrying calibration as policy memory
- Locator: https://doi.org/10.1016/j.rcim.2021.102250

## 95. Hand-eye calibration of arc welding robot and laser vision sensor through semidefinite programming (2018)
- Authors/venue: Yanbiao Zou; Xiangzhi Chen / Industrial Robot the international journal of robotics research and application
- Problem claimed: Purpose This paper aims to propose a hand-eye calibration method of arc welding robot and laser vision sensor by using semidefinite programming (SDP).
- Actual mechanism introduced: Estimates a rigid transform between robot and camera/end-effector frames from paired motion observations.
- Hidden assumptions: calibration can be estimated separately from the policy state; rigid extrinsics are recoverable before or between tasks
- Variables treated as fixed: sensor-to-robot or model-to-world transform during policy execution; mount rigidity and synchronized motion observations
- Failure modes ignored: calibration drift after deployment or under contact-induced slippage; temperature, cable, tool, or payload shifts during the task
- What it makes less novel: treating calibration as an estimable parameter is not new; estimating robot-camera extrinsics
- What it leaves open: how control changes when calibration belief is part of every policy decision; policies that condition on continuing extrinsic belief during task execution
- Locator: https://doi.org/10.1108/ir-02-2018-0034

## 96. RGGNet: Tolerance Aware LiDAR-Camera Online Calibration With Geometric Deep Learning and Generative Model (2020)
- Authors/venue: Kaiwen Yuan; Zhenyu Guo; Z. Jane Wang / IEEE Robotics and Automation Letters
- Problem claimed: Accurate LiDAR-camera online calibration is critical for modern autonomous vehicles and robot platforms.
- Actual mechanism introduced: Updates calibration parameters during operation using self-observed sensorimotor consistency constraints.
- Hidden assumptions: calibration can be estimated separately from the policy state; online updates are stable enough to run beside the controller
- Variables treated as fixed: sensor-to-robot or model-to-world transform during policy execution; the objective while calibration actions perturb task progress
- Failure modes ignored: calibration drift after deployment or under contact-induced slippage; unobservable motions and estimator/controller feedback loops
- What it makes less novel: treating calibration as an estimable parameter is not new; performing online calibration during robot operation
- What it leaves open: how control changes when calibration belief is part of every policy decision; closed-loop task benefit from carrying calibration as policy memory
- Locator: https://doi.org/10.1109/lra.2020.3026958

## 97. Adaptive Calibration of Soft Sensors Using Optimal Transportation Transfer Learning for Mass Production and LongTerm Usage (2020)
- Authors/venue: Dongwook Kim; Junghan Kwon; Byungjun Jeon; YongLae Park / Advanced Intelligent Systems
- Problem claimed: Soft sensors suffer from high manufacturing tolerances and signal drift from longterm usage, which degrades their practicality.
- Actual mechanism introduced: Updates calibration parameters during operation using self-observed sensorimotor consistency constraints.
- Hidden assumptions: calibration can be estimated separately from the policy state; online updates are stable enough to run beside the controller
- Variables treated as fixed: sensor-to-robot or model-to-world transform during policy execution; the objective while calibration actions perturb task progress
- Failure modes ignored: calibration drift after deployment or under contact-induced slippage; unobservable motions and estimator/controller feedback loops
- What it makes less novel: treating calibration as an estimable parameter is not new; performing online calibration during robot operation
- What it leaves open: how control changes when calibration belief is part of every policy decision; closed-loop task benefit from carrying calibration as policy memory
- Locator: https://doi.org/10.1002/aisy.201900178

## 98. Data-Driven Optimization of Discontinuous and Continuous Fiber Composite Processes Using Machine Learning: A Review (2025)
- Authors/venue: Ivan Malashin; Dmitry Martysyuk; Andrei Gantimurov; Vladimir Nelyub; . . / Polymers
- Problem claimed: This paper surveys the application of machine learning in fiber composite manufacturing, highlighting its role in adaptive process control, defect detection, and real-time quality assurance.
- Actual mechanism introduced: Randomizes simulator or sensor parameters so a learned policy tolerates calibration variation.
- Hidden assumptions: one policy can absorb the calibration distribution without explicit state
- Variables treated as fixed: deployment drift distribution relative to training randomization
- Failure modes ignored: distribution shift outside randomized support
- What it makes less novel: robustifying policies against calibration errors
- What it leaves open: whether explicit low-dimensional calibration state outperforms robustness at equal data
- Locator: https://doi.org/10.3390/polym17182557

## 99. Identifiable parameters for parallel robots kinematic calibration (2002)
- Authors/venue: S. Besnard; Wisama Khalil / 
- Problem claimed: Presents a numerical method for the determination of the identifiable parameters of parallel robots.
- Actual mechanism introduced: Fits parametric robot geometry or joint/link offsets to reduce pose prediction error.
- Hidden assumptions: calibration can be estimated separately from the policy state; online updates are stable enough to run beside the controller
- Variables treated as fixed: sensor-to-robot or model-to-world transform during policy execution; the objective while calibration actions perturb task progress
- Failure modes ignored: calibration drift after deployment or under contact-induced slippage; unobservable motions and estimator/controller feedback loops
- What it makes less novel: treating calibration as an estimable parameter is not new; performing online calibration during robot operation
- What it leaves open: how control changes when calibration belief is part of every policy decision; closed-loop task benefit from carrying calibration as policy memory
- Locator: https://doi.org/10.1109/robot.2001.933055

## 100. Research on online calibration of lidar and camera for intelligent connected vehicles based on depth-edge matching (2021)
- Authors/venue: Zhan Guo; Zuming Xiao / Nonlinear Engineering
- Problem claimed: Abstract The practicality of online calibration algorithms in actual autonomous driving scenarios is enhanced by proposing an online calibration method for intelligent networked automotive lidar and camera based on depth-edge matching.
- Actual mechanism introduced: Estimates a rigid transform between robot and camera/end-effector frames from paired motion observations.
- Hidden assumptions: calibration can be estimated separately from the policy state; online updates are stable enough to run beside the controller; rigid extrinsics are recoverable before or between tasks
- Variables treated as fixed: sensor-to-robot or model-to-world transform during policy execution; the objective while calibration actions perturb task progress; mount rigidity and synchronized motion observations
- Failure modes ignored: calibration drift after deployment or under contact-induced slippage; unobservable motions and estimator/controller feedback loops; temperature, cable, tool, or payload shifts during the task
- What it makes less novel: treating calibration as an estimable parameter is not new; performing online calibration during robot operation; estimating robot-camera extrinsics
- What it leaves open: how control changes when calibration belief is part of every policy decision; closed-loop task benefit from carrying calibration as policy memory; policies that condition on continuing extrinsic belief during task execution
- Locator: https://doi.org/10.1515/nleng-2021-0038
