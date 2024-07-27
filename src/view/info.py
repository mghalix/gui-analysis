from tkinter import Tk, ttk

from ..model.project import Project
from .utils.colors import Colors


class InfoFrameView:
    def __init__(self, master: Tk, project: Project) -> None:
        style = ttk.Style()
        style.configure(
            "TFrame",
            background=Colors.master,
        )
        info_frame = ttk.Frame(master, style="TFrame")
        style.configure(
            "TLabel",
            background="#0d1117",
            foreground="white",
        )

        title_label = ttk.Label(
            info_frame,
            text=project.title,
            style="TLabel",
            font="Georgia 30 bold",
            padding="0 5 0 5",
        )

        students = "\n".join(str(student) for student in project)
        students_label = ttk.Label(
            info_frame,
            text=students,
            font="Calibri 15",
            style="TLabel",
        )

        info_frame.grid(column=0, row=0, sticky="N")

        title_label.grid(column=0, row=0)
        students_label.grid(column=0, row=1)
