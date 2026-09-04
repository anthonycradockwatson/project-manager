import customtkinter as ctk
from gui.main.main_view_model import MainViewModel
from gui.project.project_gui import ProjectWindow
from colour_bs import adjust_colour
from PIL import Image
from gui.project.setup_edit_window import AddWindow
from gui.tooltips import Tooltip
from gui.automations.automation_display_gui import AutomationWindow

class ProjectFrame(ctk.CTkFrame):
    def __init__(self,master, width, height):
        super().__init__(master=master)
        self.width=int(0.8*width)
        self.height=int(0.9*height)
        self.configure(width=self.width, height=self.height)
        # Do not pack here - let callers decide placement (grid/pack)
 

class MainWindow(ctk.CTk):
    def __init__(self):
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("assets/arctic_blue.json")
        super().__init__()
        self.width = 400
        self.height=600
        self.title("Project Manager")
        self.geometry(f"{self.width}x{self.height}")
        self.edit_mode=False

    def toggle_edit_mode(self):
        self.edit_mode=not self.edit_mode
        if self.edit_mode:
            self.title("Project Manager - Edit Mode")
            self.ProjectFrame.configure(fg_color="#5A1D1D")
        else:
            self.ProjectFrame.configure(fg_color=ctk.ThemeManager.theme["CTkFrame"]["fg_color"])
            self.title("Project Manager")

    def setup_window(self):
        self.ProjectFrame = ProjectFrame(self, self.width, self.height)
        # place the main project frame in the root window
        self.ProjectFrame.grid(row=0, column=0, pady=15, padx=(15,5), sticky="nsew")
        self.ProjectFrame.grid_propagate(False)
        
        self.ProjectFrame.grid_columnconfigure(0, weight=1)
        self.ProjectFrame.grid_columnconfigure(1, weight=1)
        
        self.view_model = MainViewModel()
        if self.edit_mode:
            self.toggle_edit_mode()

        projects = self.view_model.get_projects()
        project_names = [item.name for item in projects]
        project_ids = [item.uuid for item in projects]

        button_colour = ctk.ThemeManager.theme["CTkButton"]["fg_color"]
        different_button_colour = adjust_colour(button_colour[0])

        utility_frame = ctk.CTkFrame(self.ProjectFrame, fg_color="transparent")
        utility_frame.grid(row=0, column=0, columnspan=2, pady=(10, 3), padx=(0, 15), sticky="ew")

        refresh_button = ctk.CTkButton(
            utility_frame, command=self.refresh_view, width=15, height=15, text="",
            image=ctk.CTkImage(light_image=Image.open("assets/icons/refresh.png"), size=(15, 15)), 
            fg_color=different_button_colour
        )
        refresh_button.pack(side="right", padx=5)
        Tooltip(refresh_button, "Refresh")

        edit_button = ctk.CTkButton(
            utility_frame, command=self.toggle_edit_mode, width=15, height=15, text="",
            image=ctk.CTkImage(light_image=Image.open("assets/icons/edit.png"), size=(15, 15)), 
            fg_color=different_button_colour
        )
        edit_button.pack(side="right", padx=5)
        Tooltip(edit_button, "Edit")


        project_buttons = {}
        automation_buttons = {}

        for x in range(len(project_names)):
            if x==0:
                pady=(10,3)
            else:
                pady=3
            btn_width = int(0.7 * self.ProjectFrame.width)
            pad_x = int(0.05 * self.ProjectFrame.width)
            project_buttons[f"{project_ids[x]}"] = ctk.CTkButton(
                self.ProjectFrame,
                text=f"{project_names[x]}",
                command=lambda id=project_ids[x], name=project_names[x]: self.button_command(id, name),
                width=btn_width,
            )
            project_buttons[f"{project_ids[x]}"].grid(column=0, row=x+1, pady=pady, padx=pad_x, sticky="w")

            automation_buttons[f"{project_ids[x]}"] = ctk.CTkButton(
                self.ProjectFrame,
                text='',
                image=ctk.CTkImage(light_image=Image.open("assets/icons/workflow.png"), size=(15, 15)),
                command=lambda id=project_ids[x], name=project_names[x]: self.open_automation_window(id, name),
                fg_color=different_button_colour,
            )
            automation_buttons[f"{project_ids[x]}"].grid(column=1, row=x+1, pady=pady, padx=5, sticky="e")
            Tooltip(automation_buttons[f"{project_ids[x]}"], "Automations")

        add_project_button = ctk.CTkButton(self.ProjectFrame, text="Add Project",
                    command=self.instantiate_new_projects, fg_color=different_button_colour, width=0.9*self.ProjectFrame.width)
        add_project_button.grid(row=len(project_names)+1, column=0, pady=10, padx=0.05*self.ProjectFrame.width)
    
    def open_automation_window(self, project_id, project_name):
        automation_window = AutomationWindow(project_id, project_name)
        automation_window.setup_window()
        automation_window.mainloop()

    def button_command(self, id, name):
        if self.edit_mode:
            obj=self.view_model.get_item(id)
            EditWindow=AddWindow(self, "Project",None, "edit",obj.uuid, obj.name, obj.status, obj.description, obj.deadline)
            EditWindow.setup_window()
        else:
            self.open_project_window(id, name)

    def instantiate_new_projects(self):
        add_project_screen = AddWindow(self, "Project")
        add_project_screen.setup_window()

    def open_project_window(self, project_id, project_name):
        self.destroy() 
        project_window = ProjectWindow(project_id, project_name)
        project_window.setup_window()
        project_window.mainloop()
    
    def refresh_view(self):
        self.view_model.reload()
        for widget in list(self.winfo_children()):
            widget.destroy()
        self.setup_window()
