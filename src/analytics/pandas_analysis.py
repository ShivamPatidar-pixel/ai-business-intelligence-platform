import pandas as pd


def group_and_aggregate(
    df,
    group_column,
    aggregations
):
    """
    Group data by a column and apply aggregations.
    """

    result = (
        df.groupby(group_column)
        .agg(aggregations)
        .reset_index()
    )

    return result


def get_top_values(
    df,
    column,
    n=10
):
    """
    Return the most frequent values of a column.
    """

    return (
        df[column]
        .value_counts()
        .head(n)
    )


def get_numeric_summary(df):
    """
    Generate summary statistics for numeric columns.
    """

    numeric_columns = df.select_dtypes(
        include="number"
    ).columns

    return df[numeric_columns].describe().T


def calculate_percentage(
    df,
    column
):
    """
    Calculate percentage contribution of a numeric column.
    """

    total = df[column].sum()

    if total == 0:
        return pd.Series(0, index=df.index)

    return (
        df[column] / total * 100
    )