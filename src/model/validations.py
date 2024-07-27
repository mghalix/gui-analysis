from urllib.parse import urlparse

import requests


class Validations:
    @staticmethod
    def validate_url(url: str) -> bool:
        res = urlparse(url)
        return all([res.scheme, res.netloc])

    @staticmethod
    def validate_dataset_url(url: str) -> bool:
        response = requests.head(url, allow_redirects=True)

        exclude_encoding = lambda x: x.split(";")[0]
        # exclude encoding (text/plain;charset=UTF-8) => text/plain
        content_type = exclude_encoding(response.headers["Content-Type"])

        return content_type in [
            "application/json",
            "text/csv",
            "application/vnd.ms-excel",
            "text/plain",
            "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        ]

    @staticmethod
    def validate_kaggle_url(url: str) -> bool:
        netloc = urlparse(url).netloc
        return netloc in ["www.kaggle.com", "kaggle.com"]

    @staticmethod
    def check_internet_connect() -> bool:
        test = "http://www.google.com"
        timeout = 3

        try:
            requests.head(test, timeout=timeout)
            return True
        except (requests.ConnectionError, requests.ConnectTimeout):
            return False
