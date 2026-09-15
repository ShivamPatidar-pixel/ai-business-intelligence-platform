import pandas as pd


def detect_datetime_columns(df):
    """
    Detect datetime columns in a dataframe.
    """
    datetime_columns = []

    for column in df.columns:

        # Already datetime
        if pd.api.types.is_datetime64_any_dtype(df[column]):
            datetime_columns.append(column)

        # Try object/string columns
        elif df[column].dtype == "object":
            converted = pd.to_datetime(
                df[column],
                errors="coerce"
            )

            valid_ratio = converted.notna().mean()

            if valid_ratio >= 0.7:
                datetime_columns.append(column)

    return datetime_columns


def prepare_datetime(df, date_column):
    """
    Convert a column to datetime.
    """
    df = df.copy()

    df[date_column] = pd.to_datetime(
        df[date_column],
        errors="coerce"
    )

    df = df.dropna(subset=[date_column])

    return df

def create_time_series(
    df,
    date_column,
    metric_column,
    frequency="M",
    aggregation="sum"
):
    """
    Create time-series data from a dataframe.
    """

    df = prepare_datetime(df, date_column)

    df = df.set_index(date_column)

    if aggregation == "sum":
        series = df[metric_column].resample(frequency).sum()

    elif aggregation == "mean":
        series = df[metric_column].resample(frequency).mean()

    elif aggregation == "count":
        series = df[metric_column].resample(frequency).count()

    elif aggregation == "min":
        series = df[metric_column].resample(frequency).min()

    elif aggregation == "max":
        series = df[metric_column].resample(frequency).max()

    else:
        raise ValueError(
            "Unsupported aggregation"
        )

    result = series.reset_index()

    return result


def calculate_growth(time_series, metric_column):
    """
    Calculate period-over-period growth percentage.
    """

    result = time_series.copy()

    result["growth_%"] = (
        result[metric_column]
        .pct_change()
        .mul(100)
        .round(2)
    )

    return result


def analyze_trend(time_series, metric_column):
    """
    Identify overall trend direction.
    """

    values = time_series[metric_column].dropna()

    if len(values) < 2:
        return "Insufficient Data"

    first_value = values.iloc[0]
    last_value = values.iloc[-1]

    if last_value > first_value:
        return "Increasing"

    elif last_value < first_value:
        return "Decreasing"

    else:
        return "Stable"