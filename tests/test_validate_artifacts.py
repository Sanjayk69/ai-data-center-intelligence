
from pathlib import Path

import pandas as pd

from src.analytics.validate_artifacts import validate_artifacts


PROJECT_ROOT = Path(__file__).resolve().parents[1]
PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"


def test_current_artifacts_pass_validation():
    """The saved project artifacts should satisfy all validation rules."""
    errors = validate_artifacts(PROCESSED_DIR)

    assert errors == [], "\n".join(errors)


def test_duplicate_job_ids_are_detected(tmp_path):
    """Duplicate investigation IDs must fail validation."""
    from src.analytics import validate_artifacts as module

    artifacts = module.load_artifacts(PROCESSED_DIR)
    investigation = artifacts["investigation"].copy()

    investigation = pd.concat(
        [investigation, investigation.iloc[[0]]],
        ignore_index=True,
    )

    investigation.to_csv(
        tmp_path / module.REQUIRED_ARTIFACTS["investigation"],
        index=False,
    )

    for name, df in artifacts.items():
        if name != "investigation":
            df.to_csv(
                tmp_path / module.REQUIRED_ARTIFACTS[name],
                index=False,
            )

    errors = validate_artifacts(tmp_path)

    assert any("duplicate job IDs" in error for error in errors)


def test_u3_32_data_quality_override_is_required(tmp_path):
    """U3-32 must remain classified for data-quality review."""
    from src.analytics import validate_artifacts as module

    artifacts = module.load_artifacts(PROCESSED_DIR)
    investigation = artifacts["investigation"].copy()

    investigation.loc[
        investigation["model"].eq("U3-32"),
        "investigation_tier",
    ] = "Tier 2 - Investigate"

    investigation.to_csv(
        tmp_path / module.REQUIRED_ARTIFACTS["investigation"],
        index=False,
    )

    for name, df in artifacts.items():
        if name != "investigation":
            df.to_csv(
                tmp_path / module.REQUIRED_ARTIFACTS[name],
                index=False,
            )

    errors = validate_artifacts(tmp_path)

    assert any("U3-32 must remain classified" in error for error in errors)
