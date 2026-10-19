# AI Data Center Optimization Experiment — v1

## Objective
Investigate sustained GPU low-utilization episodes in three priority jobs and assess whether telemetry supports actionable operational follow-up.

## Scope
- Dataset: MIT Supercloud GPU telemetry pilot.
- Hardware: Volta GPUs.
- Priority jobs: U3-128 (25713459161743), U4-64 (48020198141948), U4-128 (59638293409445).
- Sampling: approximately one-second telemetry observations.
- Scheduler event histories and workload-stage logs were not identified in the local project data during this investigation.

## Method
1. Select sustained low-utilization episodes from the existing episode analysis.
2. Estimate episode energy by summing observed GPU power samples under a one-second-per-sample assumption.
3. Compare episode power and utilization with observations outside the selected episodes on the same GPUs.
4. Examine zero-utilization runs, memory occupancy, and temporal overlap across GPUs.
5. Consolidate evidence and operational follow-up recommendations in the investigation view.

## Findings

### Energy observed during selected episodes
- U4-128: 4 episodes, 1,160 GPU-seconds, approximately 14.275 Wh.
- U3-128: 6 episodes, 979 GPU-seconds, approximately 10.602 Wh.
- U4-64: 1 episode, 386 GPU-seconds, approximately 4.955 Wh.
- Total across selected episodes: approximately 29.832 Wh.

This is energy consumed during the selected episodes, not recoverable energy or demonstrated savings.

### Power and utilization contrast
Mean power was substantially lower during selected episodes than outside them on the same GPUs:
- U3-128: approximately 38.99 W during episodes versus 188.93 W outside.
- U4-64: approximately 46.22 W versus 183.36 W.
- U4-128: approximately 44.23 W versus 201.02 W.

Utilization was also much lower during episodes. These are descriptive contrasts, not controlled counterfactuals: the outside periods may represent different workload phases.

### Zero-utilization runs
Using a provisional review rule of at least 180 consecutive zero-utilization seconds with positive mean power produced seven GPU-level candidate runs across the three priority jobs. The 180-second threshold is an operational proposal, not a validated universal threshold.

### Cross-GPU overlap
Selected low-utilization episodes overlapped across up to four GPUs for U3-128 and U4-128. U4-64 had a single observed GPU in its selected episode. Temporal overlap supports checking for a shared workload phase or dependency, but does not prove synchronization bottlenecks or a shared root cause.

### Memory observations
Memory occupancy remained high during and outside selected episodes. This is evidence that memory remained allocated or reported as used while compute utilization was low; it does not establish that the memory allocation was unnecessary.

## Sensitivity scenarios
Hypothetical reductions in the 29.832 Wh of episode energy:
- 10%: approximately 2.983 Wh.
- 25%: approximately 7.458 Wh.
- 50%: approximately 14.916 Wh.

These are illustrative sensitivity calculations only. They are not forecasts, verified savings, or evidence that these reductions are achievable.

## Data and interpretation limitations
- The pilot contains 26 jobs represented by 35 telemetry files.
- The reviewed manifest identifies Volta GPU type and requested-resource metadata.
- The reviewed telemetry quality report reports zero missing values, duplicate rows, and invalid timestamps in the listed files.
- No separate scheduler event histories or workload-stage logs were found by the local filename search. This does not prove that such sources do not exist elsewhere.
- Power contrasts may reflect normal workload phases, synchronization, data movement, or other causes that telemetry alone cannot distinguish.
- No controlled intervention or before/after validation has demonstrated energy savings.
- Findings are specific to this small pilot and should not be generalized to all workloads or GPU systems.

## Recommended follow-up
1. Correlate candidate episode timestamps with scheduler state transitions and job lifecycle events, if those records can be obtained.
2. Inspect workload-stage logs or application traces for U3-128 and U4-128 around overlapping episodes.
3. Review the seven prolonged zero-utilization runs with the workload owner before proposing configuration changes.
4. Test any proposed intervention against a baseline using comparable workload phases and report energy, throughput, and completion time.
5. Treat energy reduction as validated only after a controlled measurement.

## Conclusion
The pilot supports an evidence-based investigation queue for sustained low-utilization behavior. It does not yet establish root cause or achievable energy savings. The next meaningful validation step is to combine telemetry with scheduler or application-level evidence and evaluate interventions under controlled conditions.
