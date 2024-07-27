from tkinter import END, StringVar, Tk, ttk

import src.model.exceptions as exceptions
from src.control.data_handler import DatasetHandler
from src.control.utils.filter import get_num_cols_only_df
from src.model.alert_maker import Alert
from src.model.validations import Validations
from src.view.left_side import LeftSideView
from src.view.right_side import RightSideView

from .utils.colors import Colors
from .utils.custom_entry import CustomEntry


class FetchDatasetView:
    def __init__(self, master: Tk) -> None:
        self.master = master
        dataset_frame = ttk.Frame(master=master, padding="10 70 10 0")
        style = ttk.Style()
        style.configure(
            "TFrame",
            background=Colors.master,
        )

        dataset_frame.configure(style="TFrame")

        style = ttk.Style()
        style.configure("TButton", font="Calibri 11 bold")

        self.url = StringVar()

        self.urltxt = CustomEntry(
            master=dataset_frame,
            placeholder_text="Enter dataset URL",
            textvariable=self.url,
            width=50,
            font="Calibri 15",
            justify="center",
        )

        fetchbtn = ttk.Button(
            dataset_frame,
            text="Get dataset",
            default="active",
            command=self.get_dataset,
            width=10,
            style="TButton",
        )

        dataset_frame.grid(column=0, row=1, sticky="N")
        dataset_frame.rowconfigure(0, weight=1)
        dataset_frame.columnconfigure((0, 1), weight=1)

        self.urltxt.grid(column=0, row=0, sticky="E")
        fetchbtn.grid(column=1, row=0, sticky="W", ipadx=25, padx=20)

        self.l = LeftSideView(self.master)
        self.r = RightSideView(self.master)

    def get_dataset(self, *args) -> None:
        clear = lambda x: x.delete(0, END)
        focus = lambda x: x.focus()

        url = self.urltxt.get()

        if url == "":
            Alert.show_simple_alert("Empty URL", "Please type in dataset URL first.")
            focus(self.urltxt)
            return

        # BUG: Slows down the program
        # if not Validations.check_internet_connect():
        #     Alert.show_warning_message(
        #         title="No internet connection",
        #         content="You must be connected to the internet first before downloading a dataset.",
        #     )
        #     return

        if not Validations.validate_url(url):
            Alert.show_simple_alert(
                title="Invalid URL",
                content="Please type in a dataset URL",
            )
            clear(self.urltxt)
            focus(self.urltxt)
            return

        if not Validations.validate_dataset_url(
            url
        ) and not Validations.validate_kaggle_url(url):
            Alert.show_warning_message(
                title="Warning",
                content=str(exceptions.NotADatasetURL()),
            )
            clear(self.urltxt)
            focus(self.urltxt)
            return

        dataset_handler = DatasetHandler(self.url.get())
        dataset_handler.download()
        df = dataset_handler.load_as_df()
        df = get_num_cols_only_df(df)
        if df.empty:
            Alert.show_warning_message(
                title="",
                content="The dataset you downloaded has no numeric values, please pick another.",
            )
            clear(self.urltxt)
            focus(self.urltxt)
            return

        self.l.reset()
        self.r.reset()
        self.l = LeftSideView(self.master)
        self.r = RightSideView(self.master)
        self.l.refresh_data(df)
        self.r.refresh_data(df)
