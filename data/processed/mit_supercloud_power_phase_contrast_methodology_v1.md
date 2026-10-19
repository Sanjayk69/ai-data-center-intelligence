# GPU Power Phase Contrast — Tier 1 Jobs

## Scope
This analysis compares observed GPU power during selected sustained low-utilization
episodes with observed power outside those episodes for three Tier 1 jobs.

## Results
- U3-128: episode mean power 38.989 W; outside-episode mean power 188.931 W;
  mean difference 149.942 W (79.361% of outside-episode power).
- U4-64: episode mean power 46.216 W; outside-episode mean power 183.356 W;
  mean difference 137.140 W (74.794%).
- U4-128: episode mean power 44.230 W; outside-episode mean power 201.018 W;
  mean difference 156.788 W (78.002%).

## Utilization interpretation
The raw `utilization_gpu_pct` field uses a 0–100 scale. Values within the selected
episodes have a mean of 0.0494 and a maximum of 8.0. The stored episode means match
the raw telemetry for the selected timestamps. The episode means are therefore
already expressed on the raw field's scale and must not be multiplied by 100.

## Limitations
This is a descriptive phase contrast, not a controlled counterfactual. Outside-episode
observations may represent different workload phases. The observed power difference
must not be interpreted as recoverable energy or projected savings. The analysis
covers three selected jobs and is not evidence of general system-wide behavior.
