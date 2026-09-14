import pandas as pd
import numpy as np


def load_data(file_path):

    if file_path.lower().endswith(".csv"):
        return pd.read_csv(file_path)

    elif file_path.lower().endswith((".xlsx", ".xls")):
        return pd.read_excel(file_path)

    else:
        raise ValueError(
            "Only CSV and Excel files are supported."
        )


def clean_column_names(df):

    df = df.copy()

    df.columns = (
        df.columns
        .astype(str)
        .str.strip()
        .str.lower()
        .str.replace(" ", "_")
        .str.replace(r"[^\w]", "", regex=True)
    )

    return df


def remove_duplicates(df):

    return df.drop_duplicates()


def clean_text_columns(df):

    df = df.copy()

    text_columns = df.select_dtypes(
        include=["object", "string"]
    ).columns

    for col in text_columns:
        df[col] = (
            df[col]
            .astype("string")
            .str.strip()
        )

    return df


def clean_data(df):

    df = df.copy()

    # Empty rows and columns
    df = df.dropna(how="all")
    df = df.dropna(axis=1, how="all")

    # Column names
    df = clean_column_names(df)

    # Duplicates
    df = remove_duplicates(df)

    # Text cleaning
    df = clean_text_columns(df)

    return df