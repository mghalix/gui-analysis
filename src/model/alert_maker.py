from tkinter import messagebox


class Alert:
    @staticmethod
    def show_error_message(title: str, content: str) -> None:
        messagebox.showerror(title, content)

    @staticmethod
    def show_simple_alert(title: str = "", content: str = "") -> None:
        messagebox.showinfo(title, content)

    @staticmethod
    def show_warning_message(title: str, content: str) -> None:
        messagebox.showwarning(title, content)

    @staticmethod
    def show_confirmation_message(title: str, content: str) -> bool:
        response = messagebox.askokcancel(title, content)
        return response
