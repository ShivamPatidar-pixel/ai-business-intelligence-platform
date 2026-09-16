import pandas as pd
import matplotlib.pyplot as plt


def plot_bar(
    df,
    category_column,
    value_column,
    title="Bar Chart",
    top_n=None,
    figsize=(10, 6)
):
    """
    Create a bar chart.
    """

    data = df.copy()

    if top_n is not None:
        data = (
            data.sort_values(value_column, ascending=False)
            .head(top_n)
        )

    plt.figure(figsize=figsize)

    plt.bar(
        data[category_column].astype(str),
        data[value_column]
    )

    plt.title(title)
    plt.xlabel(category_column)
    plt.ylabel(value_column)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()


def plot_horizontal_bar(
    df,
    category_column,
    value_column,
    title="Horizontal Bar Chart",
    top_n=None,
    figsize=(10, 6)
):
    """
    Create a horizontal bar chart.
    """

    data = df.copy()

    if top_n is not None:
        data = (
            data.sort_values(value_column, ascending=True)
            .tail(top_n)
        )

    plt.figure(figsize=figsize)

    plt.barh(
        data[category_column].astype(str),
        data[value_column]
    )

    plt.title(title)
    plt.xlabel(value_column)
    plt.ylabel(category_column)
    plt.tight_layout()
    plt.show()


def plot_line(
    df,
    x_column,
    y_column,
    title="Line Chart",
    figsize=(10, 6)
):
    """
    Create a line chart.
    """

    data = df.copy()

    plt.figure(figsize=figsize)

    plt.plot(
        data[x_column],
        data[y_column],
        marker="o"
    )

    plt.title(title)
    plt.xlabel(x_column)
    plt.ylabel(y_column)
    plt.xticks(rotation=45)
    plt.grid(True)
    plt.tight_layout()
    plt.show()


def plot_area(
    df,
    x_column,
    y_column,
    title="Area Chart",
    figsize=(10, 6)
):
    """
    Create an area chart.
    """

    data = df.copy()

    plt.figure(figsize=figsize)

    plt.fill_between(
        data[x_column],
        data[y_column],
        alpha=0.4
    )

    plt.plot(
        data[x_column],
        data[y_column]
    )

    plt.title(title)
    plt.xlabel(x_column)
    plt.ylabel(y_column)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()


def plot_pie(
    df,
    category_column,
    value_column,
    title="Pie Chart",
    top_n=None,
    figsize=(8, 8)
):
    """
    Create a pie chart.
    """

    data = df.copy()

    if top_n is not None:
        data = (
            data.sort_values(value_column, ascending=False)
            .head(top_n)
        )

    plt.figure(figsize=figsize)

    plt.pie(
        data[value_column],
        labels=data[category_column].astype(str),
        autopct="%1.1f%%",
        startangle=90
    )

    plt.title(title)
    plt.tight_layout()
    plt.show()


def plot_histogram(
    df,
    column,
    title="Histogram",
    bins=20,
    figsize=(10, 6)
):
    """
    Create a histogram.
    """

    data = df[column].dropna()

    plt.figure(figsize=figsize)

    plt.hist(
        data,
        bins=bins
    )

    plt.title(title)
    plt.xlabel(column)
    plt.ylabel("Frequency")
    plt.tight_layout()
    plt.show()


def plot_boxplot(
    df,
    column,
    title="Box Plot",
    figsize=(8, 6)
):
    """
    Create a box plot.
    """

    data = df[column].dropna()

    plt.figure(figsize=figsize)

    plt.boxplot(data)

    plt.title(title)
    plt.ylabel(column)
    plt.tight_layout()
    plt.show()


def plot_scatter(
    df,
    x_column,
    y_column,
    title="Scatter Plot",
    figsize=(10, 6)
):
    """
    Create a scatter plot.
    """

    data = df[[x_column, y_column]].dropna()

    plt.figure(figsize=figsize)

    plt.scatter(
        data[x_column],
        data[y_column]
    )

    plt.title(title)
    plt.xlabel(x_column)
    plt.ylabel(y_column)
    plt.tight_layout()
    plt.show()


def plot_top_n(
    df,
    category_column,
    value_column,
    n=10,
    title="Top N"
):
    """
    Plot Top N categories.
    """

    data = (
        df.sort_values(value_column, ascending=False)
        .head(n)
    )

    plot_horizontal_bar(
        data,
        category_column,
        value_column,
        title=title
    )


def create_chart(
    df,
    chart_type,
    x_column=None,
    y_column=None,
    title=None
):
    """
    Generic chart creation function.
    """

    if chart_type == "bar":

        plot_bar(
            df,
            x_column,
            y_column,
            title=title or "Bar Chart"
        )

    elif chart_type == "line":

        plot_line(
            df,
            x_column,
            y_column,
            title=title or "Line Chart"
        )

    elif chart_type == "pie":

        plot_pie(
            df,
            x_column,
            y_column,
            title=title or "Pie Chart"
        )

    elif chart_type == "scatter":

        plot_scatter(
            df,
            x_column,
            y_column,
            title=title or "Scatter Plot"
        )

    else:

        raise ValueError(
            "Unsupported chart type. "
            "Use: bar, line, pie, scatter"
        )