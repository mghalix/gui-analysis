import logging as log
from http.client import InvalidURL

import pandas as pd
import requests

import src.model.exceptions as exceptions
from src.model.alert_maker import Alert
from src.model.logger import init_logging_config
from src.model.validations import Validations

from ..model.dataset import Dataset
from .kaggle_handler import KaggleHander
from .utils.df_utils import convert_to_df
from .utils.file_utils import CACHE_DIR, cached, clear_dir, init_cache

init_logging_config()


class DatasetHandler:
    def __init__(self, url) -> None:
        self.dataset = Dataset(url)

    def _fetch(self) -> requests.Response:
        return requests.get(self.dataset.url)

    def download(self) -> None:
        init_cache(self.dataset.dir)

        try:
            k = KaggleHander(self.dataset)
            k.download()
            return
        except exceptions.NotAKaggleURL:
            pass

        self._url_download()

    def _url_download(self) -> None:
        if cached(self.dataset.cached_path, self.dataset.dir):
            log.info(f"Dataset {self.dataset.full_name} is already downloaded!")
            return

        try:
            log.info("Downloading dataset...")
            response = self._fetch()
        except requests.exceptions.ConnectionError:
            Alert.show_warning_message(
                "No connection",
                "You must be connected to the internet in order to download a dataset.",
            )
            return

        if not Validations.validate_dataset_url(self.dataset.url):
            raise exceptions.NotADatasetURL

        with open(self.dataset.cached_path, "wb") as f:
            f.write(response.content)

        log.info(f"Dataset {self.dataset.full_name} has been download successfully!")

    def load_as_df(self) -> pd.DataFrame:
        return convert_to_df(self.dataset)

    @classmethod
    def clear_cache(cls) -> None:
        clear_dir(CACHE_DIR)
        init_cache(CACHE_DIR)
