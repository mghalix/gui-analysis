from tkinter import Tk, ttk

import pandas as pd

from src.control.utils.correlation import correlation
from src.control.utils.filter import enumerate_df_col_names, get_df_cols_list, prettify
from src.control.utils.func_composition import compose


class LeftSideView:
    def __init__(self, master: Tk) -> None:
        style = ttk.Style()
        style.configure("Enum.TLabel", font="Aerial 14")
        style.configure("Table.TLabel", font="Aerial 14")

        self.init_num_data_frame(master)
        self.init_corr_tbl_frame(master)

        self.num_data_frame.grid(column=0, row=2, sticky="N W")

        self.corr_tbl_frame.grid(column=0, row=3, sticky="N W")

    @classmethod
    def init_num_data_frame(cls, master) -> None:
        cls.num_data_frame = ttk.Frame(master=master, padding="25 80 0 0")
        cls.data_enumlbl = ttk.Label(
            cls.num_data_frame,
            text="Enum Columns",
            style="Enum.TLabel",
        )

        cls.data_enumlbl.grid(column=0, row=0)

    @classmethod
    def init_corr_tbl_frame(cls, master) -> None:
        cls.corr_tbl_frame = ttk.Frame(master=master, padding="25 80 25 150")
        cls.corr_tbl_lbl = ttk.Label(
            cls.corr_tbl_frame,
            text="Correlation Table",
            style="Table.TLabel",
        )
        cls.corr_tbl_lbl.grid(column=0, row=0)

    @classmethod
    def refresh_data(cls, df: pd.DataFrame) -> None:
        cls.df = df
        cls.refresh_num_data_frame()
        cls.refresh_corr_tbl_frame()

    @classmethod
    def refresh_num_data_frame(cls) -> None:
        enum_cols = compose(get_df_cols_list, enumerate_df_col_names)
        cls.enum_dict = enum_cols(cls.df)
        cls.data_enumlbl["text"] = prettify(cls.enum_dict)

    @classmethod
    def refresh_corr_tbl_frame(cls) -> None:
        enum_df = correlation(cls.df).round(2)
        cls.corr_tbl_lbl["text"] = enum_df.to_string(
            justify="center",
            # max_cols=5,
        )

    @classmethod
    def reset(cls):
        cls.num_data_frame.destroy()
        cls.corr_tbl_frame.destroy()
