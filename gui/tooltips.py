import customtkinter as ctk


class Tooltip:
    def __init__(self, widget, text, delay=300):
        self.widget = widget
        self.text = text
        self.delay = delay
        self.tip_window = None
        self.show_id = None

        widget.bind("<Enter>", self.schedule)
        widget.bind("<Leave>", self.hide)
        widget.bind("<ButtonPress>", self.hide)

    def schedule(self, event=None):
        self.hide()
        self.show_id = self.widget.after(self.delay, self.show)

    def show(self):
        if self.tip_window or not self.text:
            return

        x = self.widget.winfo_rootx() + 20
        y = self.widget.winfo_rooty() + 20

        self.tip_window = ctk.CTkToplevel(self.widget)
        self.tip_window.wm_overrideredirect(True)
        self.tip_window.wm_geometry(f"+{x}+{y}")
        self.tip_window.attributes("-topmost", True)

        label = ctk.CTkLabel(self.tip_window, text=self.text, padx=8, pady=4)
        label.pack()

    def hide(self, event=None):
        if self.show_id is not None:
            self.widget.after_cancel(self.show_id)
            self.show_id = None

        if self.tip_window is not None:
            self.tip_window.destroy()
            self.tip_window = None
