import pandas as pd


def detect_entity_columns(df):
    """
    Detect categorical/entity columns.
    """

    entity_columns = []

    for column in df.columns:

        dtype = df[column].dtype

        if (
            dtype == "object"
            or str(dtype) == "category"
        ):
            entity_columns.append(column)

    return entity_columns


def analyze_entity_performance(
    df,
    entity_column,
    metric_column,
    aggregation="sum"
):
    """
    Analyze metric performance by entity.
    """

    if entity_column not in df.columns:
        raise ValueError(
            f"{entity_column} not found in dataframe"
        )

    if metric_column not in df.columns:
        raise ValueError(
            f"{metric_column} not found in dataframe"
        )

    if aggregation == "sum":

        result = (
            df.groupby(entity_column)[metric_column]
            .sum()
            .reset_index()
        )

    elif aggregation == "mean":

        result = (
            df.groupby(entity_column)[metric_column]
            .mean()
            .reset_index()
        )

    elif aggregation == "count":

        result = (
            df.groupby(entity_column)[metric_column]
            .count()
            .reset_index()
        )

    else:

        raise ValueError(
            "Unsupported aggregation"
        )

    result = result.sort_values(
        metric_column,
        ascending=False
    )

    return result.reset_index(drop=True)


def calculate_entity_contribution(
    entity_performance,
    metric_column
):
    """
    Calculate each entity's contribution percentage.
    """

    result = entity_performance.copy()

    total = result[metric_column].sum()

    if total == 0:
        result["contribution_%"] = 0

    else:
        result["contribution_%"] = (
            result[metric_column] / total * 100
        ).round(2)

    return result


def get_top_entities(
    entity_performance,
    metric_column,
    n=5
):
    """
    Return top N entities.
    """

    return (
        entity_performance
        .sort_values(
            metric_column,
            ascending=False
        )
        .head(n)
        .reset_index(drop=True)
    )


def get_best_and_worst_entity(
    entity_performance,
    metric_column
):
    """
    Identify best and worst performing entities.
    """

    if entity_performance.empty:

        return {
            "best_entity": None,
            "best_value": None,
            "worst_entity": None,
            "worst_value": None
        }

    entity_column = entity_performance.columns[0]

    best_row = entity_performance.iloc[0]
    worst_row = entity_performance.iloc[-1]

    return {
        "best_entity": best_row[entity_column],
        "best_value": best_row[metric_column],
        "worst_entity": worst_row[entity_column],
        "worst_value": worst_row[metric_column]
    }


def generate_entity_insight(
    entity_performance,
    metric_column
):
    """
    Generate a business insight from entity performance.
    """

    if entity_performance.empty:

        return {
            "insight": "No entity data available."
        }

    entity_column = entity_performance.columns[0]

    best = entity_performance.iloc[0]
    worst = entity_performance.iloc[-1]

    total = entity_performance[metric_column].sum()

    if total == 0:

        contribution = 0

    else:

        contribution = (
            best[metric_column] / total * 100
        )

    insight = (
        f"{best[entity_column]} is the top-performing "
        f"{entity_column} with "
        f"{best[metric_column]:.2f} in "
        f"{metric_column}, contributing "
        f"{contribution:.2f}% of the total. "
        f"{worst[entity_column]} is the "
        f"lowest-performing entity with "
        f"{worst[metric_column]:.2f}."
    )

    return {
        "top_entity": best[entity_column],
        "top_value": best[metric_column],
        "top_contribution_%": round(
            contribution,
            2
        ),
        "bottom_entity": worst[entity_column],
        "bottom_value": worst[metric_column],
        "insight": insight
    }
    
def rank_entities(
    df,
    entity_column,
    metric_column,
    min_records=1
):
    """
    Rank entities based on metric performance.

    min_records:
        Minimum number of records required
        for an entity to be included.
    """

    if entity_column not in df.columns:
        raise ValueError(
            f"{entity_column} not found in dataframe"
        )

    if metric_column not in df.columns:
        raise ValueError(
            f"{metric_column} not found in dataframe"
        )

    entity_counts = (
        df.groupby(entity_column)
        .size()
        .reset_index(name="record_count")
    )

    entity_performance = (
        df.groupby(entity_column)[metric_column]
        .sum()
        .reset_index()
    )

    result = entity_performance.merge(
        entity_counts,
        on=entity_column
    )

    result = result[
        result["record_count"] >= min_records
    ]

    result = result.sort_values(
        metric_column,
        ascending=False
    )

    result["rank"] = range(
        1,
        len(result) + 1
    )

    return result.reset_index(drop=True)


def compare_entities(
    entity_performance,
    entity_column,
    metric_column,
    entity_a,
    entity_b
):
    """
    Compare two entities.
    """

    data = entity_performance[
        entity_performance[entity_column].isin(
            [entity_a, entity_b]
        )
    ].copy()

    if len(data) < 2:
        return {
            "error": "One or both entities were not found."
        }

    data = data.set_index(entity_column)

    value_a = data.loc[
        entity_a,
        metric_column
    ]

    value_b = data.loc[
        entity_b,
        metric_column
    ]

    difference = value_a - value_b

    if value_b != 0:
        difference_percent = (
            difference / abs(value_b)
        ) * 100
    else:
        difference_percent = None

    return {
        "entity_a": entity_a,
        "entity_b": entity_b,
        "value_a": value_a,
        "value_b": value_b,
        "difference": round(difference, 2),
        "difference_%": (
            round(difference_percent, 2)
            if difference_percent is not None
            else None
        )
    }
    
    
    
def create_entity_report(
    df,
    entity_column,
    metric_column,
    top_n=10,
    min_records=1
):
    """
    Create a complete entity analysis report.
    """

    ranked = rank_entities(
        df=df,
        entity_column=entity_column,
        metric_column=metric_column,
        min_records=min_records
    )

    if ranked.empty:
        return {
            "entity_column": entity_column,
            "metric_column": metric_column,
            "total_entities": 0,
            "top_entities": ranked,
            "best_entity": None,
            "worst_entity": None,
            "insight": "No sufficient entity data available."
        }

    top_entities = ranked.head(top_n)

    best = ranked.iloc[0]
    worst = ranked.iloc[-1]

    return {
        "entity_column": entity_column,
        "metric_column": metric_column,
        "total_entities": len(ranked),
        "top_entities": top_entities,
        "best_entity": best[entity_column],
        "best_value": best[metric_column],
        "worst_entity": worst[entity_column],
        "worst_value": worst[metric_column]
    }
    
    
    