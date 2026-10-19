
from pathlib import Path

import pandas as pd


REQUIRED_ARTIFACTS = {
    "investigation": "mit_supercloud_investigation_view_v9.csv",
    "anomaly": "mit_supercloud_anomaly_screening_comparison_v1.csv",
    "energy": "mit_supercloud_sustained_low_util_episode_energy_v1.csv",
    "power": "mit_supercloud_job_power_phase_contrast_v1.csv",
    "zero_runs": "mit_supercloud_zero_utilization_run_summary_v1.csv",
    "operational_queue": "mit_supercloud_operational_review_queue_v1.csv",
}

EXPECTED_TIER_COUNTS = {
    "Tier 1 - High investigation": 3,
    "Tier 2 - Investigate": 7,
    "Tier 3 - Monitor": 15,
    "Data-quality review": 1,
}


def load_artifacts(processed_dir: Path) -> dict[str, pd.DataFrame]:
    """Load required CSV artifacts, preserving job IDs as strings."""
    artifacts = {}

    for name, filename in REQUIRED_ARTIFACTS.items():
        path = processed_dir / filename

        if not path.is_file():
            raise FileNotFoundError(f"Required artifact missing: {path}")

        artifacts[name] = pd.read_csv(path, dtype={"job_id": str})

    return artifacts


def validate_artifacts(processed_dir: Path) -> list[str]:
    """Return validation errors; an empty list means all checks passed."""
    errors = []

    try:
        artifacts = load_artifacts(processed_dir)
    except (FileNotFoundError, pd.errors.ParserError) as exc:
        return [str(exc)]

    investigation = artifacts["investigation"]

    if len(investigation) != 26:
        errors.append(
            f"Expected 26 investigation rows; found {len(investigation)}."
        )

    if "job_id" not in investigation.columns:
        errors.append("Investigation view is missing job_id.")
        return errors

    if investigation["job_id"].isna().any():
        errors.append("Investigation view contains missing job IDs.")

    if investigation["job_id"].duplicated().any():
        errors.append("Investigation view contains duplicate job IDs.")

    if "investigation_tier" not in investigation.columns:
        errors.append("Investigation view is missing investigation_tier.")
    else:
        actual_counts = investigation["investigation_tier"].value_counts().to_dict()

        if actual_counts != EXPECTED_TIER_COUNTS:
            errors.append(
                "Tier counts differ from expectations. "
                f"Expected {EXPECTED_TIER_COUNTS}; found {actual_counts}."
            )

    base_ids = set(investigation["job_id"].dropna())

    for name, df in artifacts.items():
        if name == "investigation":
            continue

        if "job_id" not in df.columns:
            errors.append(f"{name} artifact is missing job_id.")
            continue

        unknown_ids = set(df["job_id"].dropna()) - base_ids

        if unknown_ids:
            errors.append(
                f"{name} contains unknown job IDs: {sorted(unknown_ids)}."
            )

    energy = artifacts["energy"]
    power = artifacts["power"]

    if energy["job_id"].duplicated().any():
        errors.append("Energy artifact contains duplicate job IDs.")

    if power["job_id"].duplicated().any():
        errors.append("Power artifact contains duplicate job IDs.")

    if not set(energy["job_id"].dropna()) == set(power["job_id"].dropna()):
        errors.append("Energy and power artifacts cover different job IDs.")

        # Confirm the known incomplete-telemetry job remains under review.
    u3_32 = investigation.loc[investigation["model"].eq("U3-32")]

    if len(u3_32) != 1:
        errors.append("Expected exactly one U3-32 record in the investigation view.")
    else:
        row = u3_32.iloc[0]

        if row["investigation_tier"] != "Data-quality review":
            errors.append("U3-32 must remain classified as Data-quality review.")

        if bool(row["allocation_matches"]):
            errors.append("U3-32 unexpectedly reports matching GPU allocation.")

        if "INCOMPLETE" not in str(row["telemetry_coverage_status"]).upper():
            errors.append("U3-32 is missing its incomplete-telemetry status.")

    # Confirm episode GPU-seconds reconcile with power observation counts.
    reconciliation = energy[
        ["job_id", "cumulative_episode_gpu_seconds"]
    ].merge(
        power[["job_id", "episode_observations"]],
        on="job_id",
        how="outer",
        validate="one_to_one",
        indicator=True,
    )

    if not reconciliation["_merge"].eq("both").all():
        errors.append("Energy and power records do not match one-to-one by job ID.")
    else:
        counts_match = reconciliation[
            "cumulative_episode_gpu_seconds"
        ].eq(reconciliation["episode_observations"])

        if not counts_match.all():
            errors.append("Episode GPU-seconds do not match power observation counts.")

    return errors
