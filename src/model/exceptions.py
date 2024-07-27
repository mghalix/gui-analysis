class NotAKaggleURL(ValueError):
    def __init__(self, message="URL does not point to a Kaggle dataset or competition"):
        super().__init__(message)


class NotADatasetURL(ValueError):
    def __init__(self, message="URL does not point to a dataset"):
        super().__init__(message)

