
from pathlib import Path

import pandas as pd


EXPECTED_COLUMNS = [
    "timestamp",
    "gpu_index",
    "utilization_gpu_pct",
    "utilization_memory_pct",
    "memory_free_MiB",
    "memory_used_MiB",
    "temperature_gpu",
    "temperature_memory",
    "power_draw_W",
    "pcie_link_width_current",
]



def load_gpu_telemetry(file_path: str | Path) -> pd.DataFrame:
    """Load one raw GPU telemetry CSV and validate required columns."""
    file_path = Path(file_path)

    if not file_path.is_file():
        raise FileNotFoundError(f"Telemetry file not found: {file_path}")

    df = pd.read_csv(file_path)

    missing_columns = sorted(set(EXPECTED_COLUMNS) - set(df.columns))

    if missing_columns:
        raise ValueError(
            f"{file_path.name} is missing required columns: {missing_columns}"
        )

    # Preserve extra source columns and parse timestamps in memory.
    if pd.api.types.is_numeric_dtype(df["timestamp"]):
        df["timestamp"] = pd.to_datetime(
            df["timestamp"], unit="s", utc=True, errors="coerce"
        )
    else:
        df["timestamp"] = pd.to_datetime(
            df["timestamp"], utc=True, errors="coerce"
        )

    if df["timestamp"].isna().any():
        raise ValueError(
            f"{file_path.name} contains invalid timestamps."
        )

    return df



def validate_gpu_file(file_path: str | Path) -> dict:
    """Return a quality summary for one telemetry file."""
    df = load_gpu_telemetry(file_path)

    extra_columns = sorted(set(df.columns) - set(EXPECTED_COLUMNS))

    return {
        "filename": Path(file_path).name,
        "rows": len(df),
        "gpu_count": df["gpu_index"].nunique(),
        "missing_values": int(df.isna().sum().sum()),
        "duplicate_rows": int(df.duplicated().sum()),
        "invalid_timestamps": int(df["timestamp"].isna().sum()),
        "start_timestamp": df["timestamp"].min(),
        "end_timestamp": df["timestamp"].max(),
        "extra_columns": ", ".join(extra_columns),
    }
