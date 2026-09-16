import pandas as pd


# ============================================================
# 1. DETECT PRODUCT / CATEGORY COLUMNS
# ============================================================

def detect_product_category_columns(df):
    """
    Detect possible product and category columns.
    """

    product_columns = []
    category_columns = []

    for column in df.columns:

        column_lower = column.lower()

        # Product related columns
        if any(word in column_lower for word in [
            "product",
            "item",
            "sku",
            "stock",
            "description"
        ]):
            product_columns.append(column)

        # Category related columns
        if any(word in column_lower for word in [
            "category",
            "segment",
            "department",
            "type"
        ]):
            category_columns.append(column)

    return {
        "product_columns": product_columns,
        "category_columns": category_columns
    }


# ============================================================
# 2. PRODUCT PERFORMANCE
# ============================================================

def analyze_product_performance(
    df,
    product_column,
    metric_column,
    aggregation="sum"
):
    """
    Analyze product performance.
    """

    if product_column not in df.columns:
        raise ValueError(
            f"{product_column} not found in dataframe"
        )

    if metric_column not in df.columns:
        raise ValueError(
            f"{metric_column} not found in dataframe"
        )

    if aggregation == "sum":

        result = (
            df.groupby(product_column)[metric_column]
            .sum()
            .reset_index()
        )

    elif aggregation == "mean":

        result = (
            df.groupby(product_column)[metric_column]
            .mean()
            .reset_index()
        )

    elif aggregation == "count":

        result = (
            df.groupby(product_column)[metric_column]
            .count()
            .reset_index()
        )

    elif aggregation == "min":

        result = (
            df.groupby(product_column)[metric_column]
            .min()
            .reset_index()
        )

    elif aggregation == "max":

        result = (
            df.groupby(product_column)[metric_column]
            .max()
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


# ============================================================
# 3. TOP PRODUCTS
# ============================================================

def get_top_products(
    product_performance,
    metric_column,
    n=5
):
    """
    Return top N products.
    """

    result = (
        product_performance
        .sort_values(
            metric_column,
            ascending=False
        )
        .head(n)
        .reset_index(drop=True)
    )

    return result


# ============================================================
# 4. BOTTOM PRODUCTS
# ============================================================

def get_bottom_products(
    product_performance,
    metric_column,
    n=5
):
    """
    Return bottom N products.
    """

    result = (
        product_performance
        .sort_values(
            metric_column,
            ascending=True
        )
        .head(n)
        .reset_index(drop=True)
    )

    return result


# ============================================================
# 5. PRODUCT CONTRIBUTION
# ============================================================

def calculate_product_contribution(
    product_performance,
    metric_column
):
    """
    Calculate contribution percentage
    of each product.
    """

    result = product_performance.copy()

    total = result[metric_column].sum()

    if total == 0:

        result["contribution_%"] = 0

    else:

        result["contribution_%"] = (
            result[metric_column]
            / total
            * 100
        ).round(2)

    return result


# ============================================================
# 6. PRODUCT RANKING
# ============================================================

def rank_products(
    product_performance,
    metric_column
):
    """
    Rank products based on metric.
    """

    result = (
        product_performance
        .sort_values(
            metric_column,
            ascending=False
        )
        .reset_index(drop=True)
    )

    result["rank"] = (
        result.index + 1
    )

    return result


# ============================================================
# 7. CATEGORY PERFORMANCE
# ============================================================

def analyze_category_performance(
    df,
    category_column,
    metric_column,
    aggregation="sum"
):
    """
    Analyze category performance.
    """

    if category_column not in df.columns:
        raise ValueError(
            f"{category_column} not found in dataframe"
        )

    if metric_column not in df.columns:
        raise ValueError(
            f"{metric_column} not found in dataframe"
        )

    if aggregation == "sum":

        result = (
            df.groupby(category_column)[metric_column]
            .sum()
            .reset_index()
        )

    elif aggregation == "mean":

        result = (
            df.groupby(category_column)[metric_column]
            .mean()
            .reset_index()
        )

    elif aggregation == "count":

        result = (
            df.groupby(category_column)[metric_column]
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


# ============================================================
# 8. CATEGORY CONTRIBUTION
# ============================================================

def calculate_category_contribution(
    category_performance,
    metric_column
):
    """
    Calculate contribution percentage
    of each category.
    """

    result = category_performance.copy()

    total = result[metric_column].sum()

    if total == 0:

        result["contribution_%"] = 0

    else:

        result["contribution_%"] = (
            result[metric_column]
            / total
            * 100
        ).round(2)

    return result


# ============================================================
# 9. CATEGORY RANKING
# ============================================================

def rank_categories(
    category_performance,
    metric_column
):
    """
    Rank categories based on metric.
    """

    result = (
        category_performance
        .sort_values(
            metric_column,
            ascending=False
        )
        .reset_index(drop=True)
    )

    result["rank"] = (
        result.index + 1
    )

    return result


# ============================================================
# 10. PRODUCT REPORT
# ============================================================

def create_product_report(
    df,
    product_column,
    metric_column,
    top_n=10
):
    """
    Create complete product analysis report.
    """

    performance = analyze_product_performance(
        df,
        product_column,
        metric_column,
        aggregation="sum"
    )

    performance = calculate_product_contribution(
        performance,
        metric_column
    )

    performance = rank_products(
        performance,
        metric_column
    )

    top_products = get_top_products(
        performance,
        metric_column,
        top_n
    )

    bottom_products = get_bottom_products(
        performance,
        metric_column,
        top_n
    )

    return {
        "total_products": len(performance),
        "top_products": top_products,
        "bottom_products": bottom_products,
        "all_products": performance
    }


# ============================================================
# 11. CATEGORY REPORT
# ============================================================

def create_category_report(
    df,
    category_column,
    metric_column,
    top_n=10
):
    """
    Create complete category analysis report.
    """

    performance = analyze_category_performance(
        df,
        category_column,
        metric_column,
        aggregation="sum"
    )

    performance = calculate_category_contribution(
        performance,
        metric_column
    )

    performance = rank_categories(
        performance,
        metric_column
    )

    top_categories = (
        performance
        .head(top_n)
        .reset_index(drop=True)
    )

    return {
        "total_categories": len(performance),
        "top_categories": top_categories,
        "all_categories": performance
    }


# ============================================================
# 12. PRODUCT INSIGHT
# ============================================================

def generate_product_insight(
    product_performance,
    product_column,
    metric_column
):
    """
    Generate simple business insight.
    """

    if product_performance.empty:

        return {
            "insight": "No product data available."
        }

    data = product_performance.sort_values(
        metric_column,
        ascending=False
    )

    best = data.iloc[0]
    worst = data.iloc[-1]

    total = data[metric_column].sum()

    if total != 0:

        contribution = (
            best[metric_column]
            / total
            * 100
        )

    else:

        contribution = 0

    insight = (
        f"{best[product_column]} is the "
        f"top-performing product with "
        f"{best[metric_column]:.2f} in "
        f"{metric_column}, contributing "
        f"{contribution:.2f}% of total "
        f"{metric_column}. "
        f"{worst[product_column]} is the "
        f"lowest-performing product."
    )

    return {
        "top_product": best[product_column],
        "top_value": best[metric_column],
        "top_contribution_%": round(
            contribution,
            2
        ),
        "bottom_product": worst[product_column],
        "bottom_value": worst[metric_column],
        "insight": insight
    }