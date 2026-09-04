import customtkinter as ctk
from gui.automations.automation_view_model import AutomationViewModel
from colour_bs import adjust_colour
from gui.automations.automation_edit_gui import ChangeAutomationWindow

class AutomationFrame(ctk.CTkFrame):
    def __init__(self,master, width, height):
        super().__init__(master=master)
        self.width=int(0.8*width)
        self.height=int(0.9*height)
        self.configure(width=self.width, height=self.height)

class AutomationWindow(ctk.CTkToplevel):
    def __init__(self, item_id, item_name, master_window=None):
        super().__init__(master=master_window)
        self.project_id=item_id
        self.master_window = master_window
        self.width = 200
        self.height=300
        self.title(f"{item_name} - Automations")
        self.geometry(f"{self.width}x{self.height}")
        self.view_model=AutomationViewModel()
        self.project_obj=self.view_model.get_item(self.project_id)
        self.attributes("-topmost", True)

    def setup_window(self):
        self.AutomationFrame = AutomationFrame(self,self.width, self.height)
        self.AutomationFrame.grid(row=0, column=0, pady=15, padx=(15,5), sticky="nsew")
        self.AutomationFrame.grid_propagate(False)
        self.AutomationFrame.grid_columnconfigure(0, weight=1)
        self.AutomationFrame.grid_columnconfigure(1, weight=1)

        automation_rows = self.view_model.get_automation_rows(self.project_obj)
        automation_names=[row["name"] for row in automation_rows]
        automation_ids=[row["id"] for row in automation_rows]
        button_colour = ctk.ThemeManager.theme["CTkButton"]["fg_color"]
        different_button_colour = adjust_colour(button_colour[0])
        automation_buttons = {}

        for x, name in enumerate(automation_names):
            pady = (10, 3) if x == 0 else 3
            btn_width = int(0.9 * self.AutomationFrame.width)
            pad_x = int(0.05 * self.AutomationFrame.width)
            automation_buttons[x] = ctk.CTkButton(
                self.AutomationFrame,
                text=name,
                command=lambda id=automation_ids[x], name=name: self.button_command(id, name, "edit"),
                width=btn_width,
            )
            automation_buttons[x].grid(column=0, row=x+1, pady=pady, padx=pad_x, sticky="w")

        add_automation_button = ctk.CTkButton(
            self.AutomationFrame,
            text="Add Automation",
            command=lambda: self.button_command(None, "New Automation", "add"),
            fg_color=different_button_colour,
            width=int(0.9 * self.AutomationFrame.width),
        )
        add_automation_button.grid(row=len(automation_names)+1, column=0, pady=10, padx=int(0.05 * self.AutomationFrame.width))

    def button_command(self, id, name, mode):
        if mode=="edit":
            edit_automation_screen = ChangeAutomationWindow(self.project_id, self,  "edit", id)

        elif mode=="add":
            add_automation_screen = ChangeAutomationWindow(self.project_id, self, "add")

    def refresh_view(self):
        self.view_model.reload()
        self.project_obj=self.view_model.get_item(self.project_id)
        for widget in list(self.winfo_children()):
            widget.destroy()
        self.setup_window()
        if self.master_window is not None:
            self.master_window.refresh_view()
