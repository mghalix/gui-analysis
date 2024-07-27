import pandas as pd


def correlation(df: pd.DataFrame) -> pd.DataFrame:
    return df.corr(numeric_only=True)