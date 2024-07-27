"""
utility functions for working with url & file paths.
"""
import os
import re
import shutil
import zipfile

from ...model.extension import Extension

CACHE_DIR = "cache/"


def get_name(path: str) -> str:
    name, _ = os.path.splitext(path)
    return name.split("/")[-1]


def get_extension(path: str) -> Extension:
    _, ext = os.path.splitext(path)
    try:
        return Extension.from_string("." + ext.split(".")[-1])
    except:
        return Extension.NA


def path_exists(path: str):
    """
    Check if a file or directory exists at the given path.

    Args:
        path (str): The path to check.

    Returns:
        bool: True if the path exists, False otherwise.
    """
    return os.path.exists(path)


def init_cache(path: str) -> None:
    os.makedirs(path, exist_ok=True)


def ls_dir(path: str) -> list[str]:
    return os.listdir(path)


def empty_dir(path: str) -> bool:
    return not bool(ls_dir(path))


def cached(url: str, dir: str) -> str | None:
    if empty_dir(dir):
        return None

    THRESHOLD = 20 / 100
    name = get_name(url)

    replace_nonalpha_with = lambda var, repl: re.sub("[^a-zA-Z]", repl, var)

    cleaned_name = replace_nonalpha_with(name, "")

    end = len(cleaned_name)

    if end >= 7:
        end = max(7, int(end * THRESHOLD))

    part_to_match = cleaned_name[:end]

    ls = ls_dir(dir)
    for file in ls:
        # Remove non-alphabetic characters from the strings
        cleaned_file = replace_nonalpha_with(file, "")

        if part_to_match in cleaned_file:
            return file

    return None


def get_abs_path(dir, file):
    return os.path.join(dir, file)


def unzip(dir: str) -> None:
    for filename in ls_dir(dir):
        if not filename.endswith(".zip"):
            continue

        abs_path = get_abs_path(dir, filename)
        with zipfile.ZipFile(abs_path, "r") as zip_ref:
            for member in zip_ref.namelist():
                if any(member.endswith(ext.value) for ext in Extension):
                    zip_ref.extract(member, dir)

        os.remove(abs_path)


def clear_dir(path: str) -> None:
    shutil.rmtree(path)
