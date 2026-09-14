import pandas as pd
import numpy as np


def detect_date_columns(df):

    date_columns = []

    for col in df.columns:

        if df[col].dtype == "object":

            converted = pd.to_datetime(
                df[col],
                errors="coerce"
            )

            if converted.notna().mean() >= 0.8:
                date_columns.append(col)

    return date_columns


def add_date_features(df):

    df = df.copy()

    date_columns = detect_date_columns(df)

    for col in date_columns:

        df[col] = pd.to_datetime(
            df[col],
            errors="coerce"
        )

        df[f"{col}_year"] = df[col].dt.year
        df[f"{col}_month"] = df[col].dt.month
        df[f"{col}_dayofweek"] = (
            df[col].dt.dayofweek
        )

    return df


def create_features(df):

    df = df.copy()

    df = add_date_features(df)

    return df