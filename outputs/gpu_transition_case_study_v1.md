# AI Data Center Intelligence: GPU Transition Case Study

## Objective

Characterize sustained low-utilization periods and transitions into sustained
high GPU utilization using observed MIT Supercloud telemetry.

## Case-study jobs

| Metric | U3-128 | U4-128 |
|---|---:|---:|
| Job ID | 25713459161743 | 59638293409445 |
| Initial sustained low-utilization episode | 246 sec | 296 sec |
| Gap to first qualifying high-utilization interval | 7 sec | 13 sec |
| First qualifying high-utilization interval | 262 sec | 617 sec |
| Mean utilization in first qualifying interval | 95.231% | 97.499% |
| Total qualifying high-utilization time | 2,620 sec | 6,304 sec |
| Number of qualifying intervals | 10 | 11 |
| Mean interval power per observed GPU | 190.650 W | 202.793 W |

## Findings

Both jobs show a sequence of sustained near-idle GPU telemetry, intermittent
activity, and subsequent sustained high utilization across the observed GPU
streams.

U3-128 has an initial low-utilization episode of 246 seconds. Its first
qualifying high-utilization interval begins 7 seconds after the recorded
episode end and lasts 262 seconds.

U4-128 has an initial low-utilization episode of 296 seconds. Its first
qualifying high-utilization interval begins 13 seconds after the recorded
episode end and lasts 617 seconds.

U4-128 has more total qualifying high-utilization time in the observed sample.
These results describe two individual jobs and do not establish model-wide
performance or efficiency differences.

## Methodology

- GPU utilization and power are analyzed at one-second resolution.
- A qualifying high-utilization interval requires all observed GPU streams
  to have records for that second and each observed GPU to have utilization
  of at least 75%.
- Qualifying intervals must contain at least 30 consecutive one-second
  timestamps.
- Separate qualifying intervals are split when timestamps are not consecutive
  or the criterion is not met.
- Power values refer to observed GPU power, not total facility energy.

## Limitations

- Low GPU utilization does not, by itself, prove wasted compute or energy.
- Telemetry does not identify the cause of the low-utilization or transition
  periods. Initialization, data preparation, synchronization, and dependency
  waits remain hypotheses rather than established causes.
- Scheduler allocation matching supports the completeness assessment, but
  observed telemetry does not automatically establish full job-runtime coverage.
- Total qualifying seconds sum separate intervals and are not necessarily
  contiguous wall-clock duration.
- Results from two jobs should not be generalized to all workloads or model
  configurations.

## Figures

- `u3_128_transition_timeline_v1.png`
- `u3_128_transition_zoom_v1.png`
- `u4_128_transition_timeline_v1.png`
- `u4_128_transition_zoom_v1.png`

## Data source

MIT Supercloud Dataset:
https://github.com/MIT-AI-Accelerator/MIT-Supercloud-Dataset

Samsi et al., “The MIT Supercloud Dataset,” 2021 IEEE High Performance
Extreme Computing Conference (HPEC), DOI: 10.1109/HPEC49654.2021.9622850.
