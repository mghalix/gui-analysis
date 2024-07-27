import pandas as pd


def get_num_cols_only_df(df: pd.DataFrame) -> pd.DataFrame:
    return df.select_dtypes(include=["number"])


def get_df_cols_list(df: pd.DataFrame) -> list[str]:
    return df.columns.tolist()


def enumerate_df_col_names(cols: list[str]) -> dict[int, str]:
    cols_enum = {idx: name for idx, name in enumerate(cols, start=1)}
    return cols_enum


def prettify(enumerated_dict: dict[int, str]) -> str:
    return "\n".join([f"{idx}. {name}" for idx, name in enumerated_dict.items()])