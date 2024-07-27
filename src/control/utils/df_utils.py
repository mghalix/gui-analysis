from typing import Callable, TypeAlias

import pandas as pd

from ...model.dataset import Dataset
from ...model.extension import Extension

PdRead: TypeAlias = Callable[..., pd.DataFrame]


READERS: dict[Extension, PdRead] = {
    Extension.CSV: pd.read_csv,
    Extension.EXCEL: pd.read_excel,
    Extension.JSON: pd.read_json,
    Extension.PICKLE: pd.read_pickle,
}


def get_reader(ext: Extension) -> PdRead:
    """
    Returns a callable that can read a file with the given extension and return its contents as a pandas DataFrame.

    Args:
        ext (Extension): The file extension to read.

    Returns:
        Callable[..., pd.DataFrame]: A callable that can read a file with the given extension and return its contents as a pandas DataFrame.
    """
    return READERS[ext]


def convert_to_df(dataset: Dataset) -> pd.DataFrame:
    """
    Converts a dataset to a pandas DataFrame.

    Args:
        dataset (Dataset): The dataset to be converted.

    Returns:
        pd.DataFrame: The converted DataFrame.
    """
    reader = get_reader(dataset.ext)
    kwargs = {}
    # return reader(str(dataset))
    if dataset.ext == Extension.CSV:
        kwargs["index_col"] = 0
    return reader(dataset.cached_path, **kwargs)
