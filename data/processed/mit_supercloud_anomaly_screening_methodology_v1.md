# Anomaly Screening Methodology — v1

## Purpose
Prioritize GPU jobs for further investigation using transparent statistical
screening and an exploratory unsupervised anomaly-detection model.

## Population and data quality
- 26 jobs were present in the investigation dataset.
- 25 allocation-matched jobs were included in performance screening.
- One job with incomplete GPU-allocation telemetry was excluded from
  performance ranking and retained for separate data-quality review.

## Method 1: IQR screening
- Features: low-utilization percentage, longest sustained low-utilization
  episode, and cumulative sustained low-utilization GPU-seconds.
- A feature was flagged when its value exceeded Q3 + 1.5 × IQR.
- Four of the 25 eligible jobs had at least one IQR signal.
- IQR signals indicate statistical extremeness within this small sample;
  they are not ground-truth anomaly labels.

## Method 2: Isolation Forest
- Features: the same three metrics used in the reduced IQR baseline.
- Features were standardized before model fitting.
- Configuration: 300 estimators, contamination=0.10, random_state=42.
- Three of the 25 eligible jobs were flagged in the saved comparison.
- Results are exploratory and sensitive to model configuration and sample
  composition. They are not validated predictive classifications.

## Operational investigation tiers
- Tier 1: cumulative sustained low-utilization GPU time > 791 GPU-seconds
  or longest sustained episode > 300 seconds.
- Tier 2: not Tier 1, and longest sustained episode >= 180 seconds or
  low-utilization percentage > 8.807%.
- Tier 3: neither Tier 1 nor Tier 2 criteria are met.
- Data-quality review overrides performance ranking.
- The 791 and 8.807 thresholds are IQR-derived. The 180- and 300-second
  cutoffs are proposed operational thresholds, not validated limits.

## Episode-energy estimates
- Sampled power was integrated using a one-second-per-sample assumption.
- Estimates cover selected sustained low-utilization episodes for three
  Tier 1 jobs only.
- Energy consumed during these episodes is not equivalent to recoverable
  energy or potential savings.

## Limitations
- Small pilot population; no labeled ground truth for anomaly validation.
- Screening features are correlated and should not be treated as independent
  evidence.
- Telemetry does not establish why utilization was low.
- GPU-level episode durations can represent GPU-seconds rather than wall-clock
  time when multiple GPUs are involved.
- Observed GPU energy is not a direct measure of inefficiency.
- Findings require further validation before operational deployment.

## Output
mit_supercloud_anomaly_screening_comparison_v1.csv
