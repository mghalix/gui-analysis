from tkinter import Tk, ttk

import pandas as pd
import seaborn as sns
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

from src.model.alert_maker import Alert

from .utils.custom_entry import CustomEntry


class RightSideView:
    def __init__(self, master: Tk):
        self.init_corr_entry(master)
        self.init_corr_plot(master)
        self.no_num_col_view_update()

        self.corr_entry_frame.grid(column=0, row=2, sticky="N E")
        self.corr_entry_frame.columnconfigure((0, 1, 2), weight=0)
        self.no_num_col_view_update()

    @classmethod
    def init_corr_entry(cls, master: Tk):
        cls.corr_entry_frame = ttk.Frame(master, padding="0 75 25 0")
        FONT = "Calibri 12 bold"
        cls.xentry = CustomEntry(
            cls.corr_entry_frame,
            placeholder_text="x= ...",
            font=FONT,
            width=10,
            justify="center",
        )
        cls.yentry = CustomEntry(
            cls.corr_entry_frame,
            placeholder_text="y= ...",
            font=FONT,
            width=10,
            justify="center",
        )
        cls.showbtn = ttk.Button(
            cls.corr_entry_frame,
            text="Show Plot",
            command=cls.showbtn_action,
        )

        PADX = 10

        cls.xentry.grid(column=0, row=0, padx=PADX, ipady=3)
        cls.yentry.grid(column=1, row=0, padx=PADX, ipady=3)
        cls.showbtn.grid(column=2, row=0, padx=PADX, ipadx=15)

    @classmethod
    def init_corr_plot(cls, master: Tk):
        cls.corr_plot_frame = ttk.Frame(master, padding="0 0 25 150")

    @classmethod
    def refresh_data(cls, df: pd.DataFrame):
        cls.enable_num_col_view()
        cls.df = df

    @classmethod
    def showbtn_action(cls, *args):
        from .left_side import LeftSideView

        x = cls.xentry.get()
        y = cls.yentry.get()

        if x == "" or y == "":
            Alert.show_simple_alert("Empty fields", "Please enter x and y first")
            return

        try:
            x = LeftSideView.enum_dict[int(x)]
            y = LeftSideView.enum_dict[int(y)]
        except KeyError:
            end = len(LeftSideView.enum_dict)
            Alert.show_warning_message(
                "Wrong number", f"Please enter a number from 1 to {end}"
            )
            return

        cls.show_plot(x, y)
        cls.corr_plot_frame.grid(column=0, row=3, sticky="N E")

    @classmethod
    def show_plot(cls, x: str, y: str) -> None:
        fig = Figure(figsize=(5, 5), dpi=100)
        ax = fig.add_subplot(111)

        sns.scatterplot(x=x, y=y, data=cls.df, ax=ax)

        corr = cls.df[x].corr(cls.df[y])

        ax.set_title(f"Correlation: {corr:.2f}")

        canvas = FigureCanvasTkAgg(fig, master=cls.corr_plot_frame)
        canvas.draw()
        cls.canvas = canvas.get_tk_widget()
        cls.canvas.grid(column=0, row=0, sticky="N")

    @classmethod
    def no_num_col_view_update(cls) -> None:
        cls.showbtn.state(["disabled"])

        cls.xentry.clear()
        cls.yentry.clear()

        cls.xentry.state(["readonly"])
        cls.yentry.state(["readonly"])

        if not hasattr(cls, "canvas") or cls.canvas is None:
            return

        cls.canvas.destroy()

    @classmethod
    def enable_num_col_view(cls) -> None:
        cls.showbtn.state(["!disabled"])
        cls.xentry.state(["!readonly"])
        cls.yentry.state(["!readonly"])

    @classmethod
    def reset(cls):
        cls.corr_entry_frame.destroy()
        cls.corr_plot_frame.destroy()
