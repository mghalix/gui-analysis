from __future__ import annotations

from enum import Enum


class Extension(Enum):
    CSV = ".csv"
    EXCEL = (".xlsx", ".xls")
    JSON = ".json"
    PICKLE = (".pkl", ".p", ".pickle")
    NA = ""

    @staticmethod
    def from_string(extension: str) -> Extension:
        for ext in Extension:
            if isinstance(ext.value, tuple) and extension in ext.value:
                return ext

            if extension == ext.value:
                return ext

        raise ValueError("Not supported extension")
