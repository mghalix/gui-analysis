import logging as log
from enum import Enum, auto
from typing import Callable
from urllib.parse import urlparse

import kaggle

from src.control.utils.file_utils import cached, get_extension, get_name, unzip
from src.model.dataset import Dataset
from src.model.exceptions import NotAKaggleURL
from src.model.validations import Validations


class KaggleType(Enum):
    DATASET = auto()
    COMPETITION = auto()


class KaggleHander:
    def __init__(self, dataset: Dataset) -> None:
        if not Validations.validate_kaggle_url(dataset.url):
            raise NotAKaggleURL(f"Invalid Kaggle URL: {dataset.url}")

        self.dataset = dataset
        self.parsed_url = urlparse(dataset.url)

    def _get_type(self) -> KaggleType:
        if "competition" in self.parsed_url.path:
            return KaggleType.COMPETITION

        return KaggleType.DATASET

    def download(self):
        if cached(self.dataset.url, self.dataset.dir):
            self.dataset = self.correct_dataset_info()
            log.info(f"Dataset {self.dataset.full_name} is already downloaded!")
            return

        DOWNLOADER: dict[KaggleType, Callable[..., None]] = {
            KaggleType.DATASET: self._kaggle_data_downloader,
            KaggleType.COMPETITION: self._kaggle_comp_downloader,
        }

        log.info("Downloading dataset from kaggle...")
        DOWNLOADER[self._get_type()]()
        self.correct_dataset_info()
        log.info(f"Dataset {self.dataset.full_name} has been download successfully!")

    def correct_dataset_info(self) -> Dataset:
        m = cached(self.dataset.url, self.dataset.dir)
        if m:
            self._dataset_setter_from(m)

        return self.dataset

    def _kaggle_data_downloader(self) -> None:
        def get_dataset_string() -> str:
            return self.parsed_url.path.lstrip("/").replace("datasets/", "")

        dataset_string = get_dataset_string()

        kaggle.api.authenticate()
        kaggle.api.dataset_download_files(
            dataset_string, path=self.dataset.dir, unzip=True
        )

    def _kaggle_comp_downloader(self) -> None:
        def get_dataset_string() -> str:
            return (
                self.parsed_url.path.lstrip("/")
                .replace("competitions/", "")
                .split("/")[0]
            )

        dataset_string = get_dataset_string()

        kaggle.api.authenticate()
        kaggle.api.competition_download_files(dataset_string, path=self.dataset.dir)
        unzip(self.dataset.dir)

    def _dataset_setter_from(self, filename: str) -> None:
        self.dataset.name = get_name(filename)
        self.dataset.ext = get_extension(filename)
