import logging

import pandas as pd

from src.control.data_handler import DatasetHandler
from src.control.utils import filter, func_composition
from src.model.project import Project
from src.model.student import Student
from src.view.runner import Runner

def setup() -> None:
    movies = pd.read_pickle("./data/movies.p")
    # Get only numeric columns
    myfunc = func_composition.compose(
        filter.get_num_cols_only_df,
        filter.get_df_cols_list,
        filter.enumerate_df_col_names,
    )

    myfunc(movies)


def create_project() -> Project:
    title = "Analysis Project"

    students = [
        Student(1, "Seba"),
        Student(2, "Sawsan"),
        Student(3, "Sara"),
        Student(4, "Mona"),
    ]

    return Project(title, students)


def main() -> None:
    project = create_project()
    Runner(project).run()

    URL = [
        "https://raw.githubusercontent.com/cs109/2014_data/master/countries.csv",
        "https://raw.githubusercontent.com/MainakRepositor/Datasets/master/Typing%20Speed/texts.csv",
        "https://www.kaggle.com/datasets/ohinhaque/ocd-patient-dataset-demographics-and-clinical-data",
        "https://www.kaggle.com/datasets/piyushborhade/diabetes-dataset",
    ]

    # d = DatasetHandler(URL[3])
    # d.clear_cache()
    # d.download()


if __name__ == "__main__":
    main()
