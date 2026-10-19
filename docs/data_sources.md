# Data Sources

This project uses publicly available research datasets to analyze AI/HPC data-center workloads, compute utilization, power consumption, and thermal behavior.

The project follows a staged integration approach: MIT SuperCloud is the current analytical foundation, while ORNL Summit and the AI training workload dataset are planned extensions subject to verification and compatibility assessment.

## 1. MIT SuperCloud Dataset

**Organization:** MIT AI Accelerator / MIT Supercloud
**Primary use:** GPU/CPU utilization and workload analysis
**Data type:** Observed real-world telemetry
**Integration status:** Currently used

**Repository:** https://github.com/MIT-AI-Accelerator/MIT-Supercloud-Dataset

The dataset contains scheduler logs, CPU and GPU time-series data, compute-node monitoring data, and labeled deep-learning workloads.

The current project uses MIT SuperCloud telemetry for job-level investigation, utilization analysis, exploratory anomaly screening, power-phase comparisons, and energy estimation during selected low-utilization episodes.

**Publication:**
Samsi et al., "The MIT Supercloud Dataset," 2021 IEEE High Performance Extreme Computing Conference (HPEC).
DOI: 10.1109/HPEC49654.2021.9622850

## 2. ORNL Summit Power & Thermal Dataset

**Organization:** Oak Ridge National Laboratory
**System:** OLCF Summit
**Primary use:** Power and thermal analysis
**Data type:** Observed real-world telemetry
**Integration status:** Planned

**Repository:** https://github.com/at-aaims/summit_power_and_thermal_data

The dataset contains power and temperature measurements from CPUs and NVIDIA V100 GPUs on the Summit supercomputer.

Planned applications include power-temperature analysis, thermal behavior investigation, and comparisons of workload phases. The dataset will initially be analyzed independently because Summit and MIT SuperCloud represent different systems and operating contexts.

**Publication:**
Shin et al., "Revealing power, energy and thermal dynamics of a 200PF pre-exascale supercomputer," SC '21.
DOI: 10.1145/3458817.3476188

**License:** CC BY 4.0, as identified in the project's source notes. Verify the applicable license terms for the specific files used before redistribution.

## 3. AI Training Workload Dataset

**Organization:** Research dataset described in Scientific Data (2026)
**Primary use:** AI training power, utilization, memory, and temperature analysis
**Data type:** Reported real-world telemetry
**Integration status:** Candidate for future integration; source verification pending

The proposed dataset is described as containing high-resolution measurements from AI training workloads on GPU systems.

Potential applications include memory behavior analysis, multi-GPU workload investigation, and additional AI training telemetry analysis. Integration depends on verifying the publication, locating the original dataset, reviewing its schema and license, and assessing whether it adds useful coverage beyond the existing sources.

**Publication:**
Elsayed et al., "Characterization of high-resolution AI data center training workloads on single and multiple GPU nodes," Scientific Data, 2026.

**DOI:** Pending verification. Do not cite an unverified DOI or treat this dataset as integrated until its source is confirmed.

## 4. Data Provenance Policy

- Observed measurements from external datasets will not be represented as simulated data.
- Derived metrics calculated from observed measurements will be identified as analytical results.
- Scenario analysis and what-if projections will be explicitly labeled as modeled or illustrative outputs.
- Synthetic data will only be introduced when necessary to represent operational attributes unavailable in the public datasets, and will be clearly identified.
- Each dataset will retain its source identity and provenance. Data from different systems will not be treated as directly interchangeable without assessing differences in hardware, sampling frequency, metric definitions, and workload context.

## 5. Data Quality and Limitations

Data quality is assessed using source manifests, telemetry quality reports, coverage reports, and automated artifact validation.

The current MIT SuperCloud analysis includes a known incomplete-coverage case for job `29381280178268` (U3-32). It is classified for data-quality review rather than performance prioritization because the observed telemetry does not match the expected GPU allocation.

Low utilization is an investigation signal, not proof of wasted resources. Energy measured during selected episodes is not equivalent to verified recoverable energy or demonstrated savings. Exploratory anomaly-screening results are not treated as validated predictions without ground-truth evaluation.

Future dataset integrations will undergo separate schema, coverage, licensing, and quality checks before being used in cross-dataset analysis.