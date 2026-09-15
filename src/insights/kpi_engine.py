import pandas as pd


def generate_basic_kpis(df):
    """
    Generate basic dataset-level KPIs.
    """

    kpis = {}

    kpis["total_rows"] = len(df)
    kpis["total_columns"] = len(df.columns)
    kpis["duplicate_rows"] = df.duplicated().sum()
    kpis["total_missing_values"] = df.isnull().sum().sum()

    numeric_columns = df.select_dtypes(
        include="number"
    ).columns

    categorical_columns = df.select_dtypes(
        include=["object", "string", "category"]
    ).columns

    kpis["numeric_columns"] = len(numeric_columns)
    kpis["categorical_columns"] = len(categorical_columns)

    return kpis


def generate_numeric_kpis(df):
    """
    Generate statistics for numeric columns.
    """

    numeric_columns = df.select_dtypes(
        include="number"
    ).columns

    results = {}

    for col in numeric_columns:

        results[col] = {
            "mean": df[col].mean(),
            "median": df[col].median(),
            "minimum": df[col].min(),
            "maximum": df[col].max(),
            "sum": df[col].sum()
        }

    return results


def get_top_categories(df, top_n=5):
    """
    Get most frequent values from categorical columns.
    """

    results = {}

    categorical_columns = df.select_dtypes(
        include=["object", "string", "category"]
    ).columns

    for col in categorical_columns:

        results[col] = (
            df[col]
            .value_counts()
            .head(top_n)
            .to_dict()
        )

    return results


def generate_insights(df):
    """
    Generate simple automatic dataset insights.
    """

    insights = []

    insights.append(
        f"Dataset contains {len(df)} rows and {len(df.columns)} columns."
    )

    missing = df.isnull().sum().sum()

    if missing > 0:
        insights.append(
            f"Dataset contains {missing} missing values."
        )
    else:
        insights.append(
            "Dataset contains no missing values."
        )

    duplicates = df.duplicated().sum()

    if duplicates > 0:
        insights.append(
            f"Dataset contains {duplicates} duplicate rows."
        )
    else:
        insights.append(
            "No duplicate rows were detected."
        )

    numeric_columns = df.select_dtypes(
        include="number"
    ).columns

    categorical_columns = df.select_dtypes(
        include=["object", "string", "category"]
    ).columns

    insights.append(
        f"Dataset contains {len(numeric_columns)} numeric columns."
    )

    insights.append(
        f"Dataset contains {len(categorical_columns)} categorical columns."
    )

    return insights


# -----------------------------
# KPI ENGINE V2
# -----------------------------

def calculate_contribution(df, column):
    """
    Calculate percentage contribution of a numeric column.
    """

    total = df[column].sum()

    if total == 0:
        return pd.Series(0, index=df.index)

    return (df[column] / total) * 100


def rank_values(df, column, ascending=False):
    """
    Rank values in a dataframe column.
    """

    return df[column].rank(
        ascending=ascending,
        method="dense"
    )


def get_top_n(df, column, n=10):
    """
    Return top N rows based on a column.
    """

    return df.sort_values(
        column,
        ascending=False
    ).head(n)


def get_bottom_n(df, column, n=10):
    """
    Return bottom N rows based on a column.
    """

    return df.sort_values(
        column,
        ascending=True
    ).head(n)