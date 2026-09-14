import pandas as pd


def clean_data(df):

    df = df.copy()

    # Remove missing important values
    df = df.dropna(
        subset=["CustomerID", "Description"]
    )

    # Remove duplicate records
    df = df.drop_duplicates()

    # Convert date
    df["InvoiceDate"] = pd.to_datetime(
        df["InvoiceDate"]
    )

    # Convert CustomerID to string
    df["CustomerID"] = (
        df["CustomerID"]
        .astype(int)
        .astype(str)
    )

    # Keep valid sales
    df = df[df["Quantity"] > 0]

    df = df[df["UnitPrice"] > 0]

    # Create Sales feature
    df["Sales"] = (
        df["Quantity"] *
        df["UnitPrice"]
    )

    return df