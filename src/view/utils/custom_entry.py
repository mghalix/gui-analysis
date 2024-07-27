from sched import Event
from tkinter import END, ttk


class CustomEntry(ttk.Entry):
    def __init__(self, master=None, placeholder_text: str = "", *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self._original_justify = self.cget("justify")
        self.placeholder_text = placeholder_text

        self.on_entry_focus_out(Event)

        self.bind("<FocusIn>", self.on_entry_focus_in)
        self.bind("<FocusOut>", self.on_entry_focus_out)

    def on_entry_focus_in(self, event):
        if self.get() != "":
            return

        self.delete(0, END)
        self.configure(show="", justify=self._original_justify, foreground="black")

    def on_entry_focus_out(self, event):
        if self.get() != "":
            return

        self.insert(0, self.placeholder_text)
        self.configure(justify="center", foreground="gray")

    def get(self):
        if super().get() == self.placeholder_text:
            return ""

        return super().get()

    def reset(self):
        self.delete(0, END)
        self.insert(0, self.placeholder_text)
        self.configure(justify="center", foreground="gray")

    def clear(self):
        self.reset()
