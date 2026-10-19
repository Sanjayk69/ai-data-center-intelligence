
from pathlib import Path

import pandas as pd


GROUP_COLUMNS = [
    "job_id",
    "source_filename",
    "rack_node_id",
    "rack_id",
    "node_number",
    "model",
    "workload_family",
    "gpu_index",
    "timestamp_1s",
]

MEASUREMENT_AGGREGATIONS = {
    "utilization_gpu_pct": ("utilization_gpu_pct", "mean"),
    "utilization_memory_pct": ("utilization_memory_pct", "mean"),
    "memory_used_MiB": ("memory_used_MiB", "mean"),
    "memory_free_MiB": ("memory_free_MiB", "mean"),
    "temperature_gpu_avg": ("temperature_gpu", "mean"),
    "temperature_gpu_max": ("temperature_gpu", "max"),
    "temperature_memory_avg": ("temperature_memory", "mean"),
    "power_draw_W": ("power_draw_W", "mean"),
    "pcie_link_width_current": ("pcie_link_width_current", "mean"),
    "raw_observation_count": ("timestamp", "count"),
}


OPTIONAL_AGGREGATIONS = {
    "clocks_current_memory_MHz": (
        "clocks_current_memory_MHz", "mean"
    ),
    "clocks_current_sm_MHz": (
        "clocks_current_sm_MHz", "mean"
    ),
    "clocks_current_video_MHz": (
        "clocks_current_video_MHz", "mean"
    ),
    "power_limit_W": ("power_limit_W", "mean"),
}


def aggregate_gpu_telemetry(
    file_path: str | Path,
    job_id: str,
    model: str,
    workload_family: str,
) -> pd.DataFrame:
    """Aggregate one raw telemetry file into one-second GPU records.

    Source-file identity is retained so that overlapping telemetry streams
    are not accidentally merged across files.
    """
    file_path = Path(file_path)

    if not file_path.is_file():
        raise FileNotFoundError(
            f"Telemetry file not found: {file_path}"
        )

    df = pd.read_csv(file_path)

    required_columns = {
        "timestamp",
        "gpu_index",
        *MEASUREMENT_AGGREGATIONS.keys(),
    }
    # Aggregation input column names differ from output column names.
    required_columns = {
        "timestamp",
        "gpu_index",
        "utilization_gpu_pct",
        "utilization_memory_pct",
        "memory_used_MiB",
        "memory_free_MiB",
        "temperature_gpu",
        "temperature_memory",
        "power_draw_W",
        "pcie_link_width_current",
    }

    missing_columns = sorted(required_columns - set(df.columns))
    if missing_columns:
        raise ValueError(
            f"{file_path.name} is missing columns: {missing_columns}"
        )

    if pd.api.types.is_numeric_dtype(df["timestamp"]):
        df["timestamp"] = pd.to_datetime(
            df["timestamp"],
            unit="s",
            utc=True,
            errors="coerce",
        )
    else:
        df["timestamp"] = pd.to_datetime(
            df["timestamp"],
            utc=True,
            errors="coerce",
        )

    if df["timestamp"].isna().any():
        raise ValueError(
            f"{file_path.name} contains invalid timestamps."
        )

    df["job_id"] = str(job_id)
    df["source_filename"] = file_path.name

    df["job_id"] = str(job_id)
    df["source_filename"] = file_path.name

    # Extract the complete rack/node identity from the filename.
    df["rack_node_id"] = df["source_filename"].str.extract(
        r"-(r\d+-n\d+)\.csv$",
        expand=False,
    )

    if df["rack_node_id"].isna().any():
        raise ValueError(
            f"Could not extract rack/node identity from {file_path.name}"
        )

    df["rack_id"] = df["rack_node_id"].str.extract(
        r"^(r\d+)-",
        expand=False,
    )

    df["node_number"] = df["rack_node_id"].str.extract(
        r"-n(\d+)$",
        expand=False,
    )

    df["model"] = model
    df["workload_family"] = workload_family
    df["timestamp_1s"] = df["timestamp"].dt.floor("1s")

    df["model"] = model
    df["workload_family"] = workload_family
    df["timestamp_1s"] = df["timestamp"].dt.floor("1s")

    aggregations = MEASUREMENT_AGGREGATIONS.copy()

    for output_column, specification in OPTIONAL_AGGREGATIONS.items():
        if specification[0] in df.columns:
            aggregations[output_column] = specification

    result = (
        df.groupby(GROUP_COLUMNS, as_index=False)
        .agg(**aggregations)
        .sort_values(
            ["job_id", "source_filename", "gpu_index", "timestamp_1s"]
        )
        .reset_index(drop=True)
    )

    return result
