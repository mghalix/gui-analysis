from tkinter import Tk

from src.control.data_handler import DatasetHandler
from src.model.dataset import Dataset

from ..model.project import Project
from .dataset_fetcher import FetchDatasetView
from .info import InfoFrameView
from .utils.colors import Colors


class Runner:
    def __init__(self, project: Project) -> None:
        self.project = project

    def config_root(self, root: Tk) -> None:
        root.title("GUI for Data Analysis")
        root.geometry("1240x980")
        root.configure(bg=Colors.master)

        # root.resizable(width=False, height=False)
        root.columnconfigure(0, weight=1)
        root.rowconfigure((0, 1, 2, 3), weight=0)

    def run(self) -> None:
        # DatasetHandler.clear_cache()

        root = Tk()
        self.config_root(root)
        InfoFrameView(root, self.project)
        FetchDatasetView(root)
        root.mainloop()
