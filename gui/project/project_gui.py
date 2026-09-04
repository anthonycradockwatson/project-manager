from gui.project.project_view_model import ProjectViewModel
import customtkinter as ctk
from colour_bs import adjust_colour
from datetime import datetime
from gui.project.setup_edit_window import AddWindow
from gui.automations.automation_display_gui import AutomationWindow
from gui.tooltips import Tooltip
from PIL import Image


class ProjectFrame(ctk.CTkFrame):
    def __init__(self,master, width, height):
        super().__init__(master=master)
        self.width=int(0.8*width)
        self.height=int(0.9*height)
        self.configure(width=self.width, height=self.height)
        self.grid(row=0, column=0, pady=15, padx=(15,5), sticky="nsew")


class ProjectWindow(ctk.CTk):
    def __init__(self, project_id, project_name):
        super().__init__()
        self.project_id=project_id
        self.width = 400
        self.height=600
        self.title(f"{project_name}")
        self.geometry(f"{self.width}x{self.height}")
        self.edit_mode=False
        self.ProjectFrame = None
        self.view_model = ProjectViewModel()
        self.project_obj=self.view_model.get_project(self.project_id)
        self.tasks_widgets = {}
        self.subtask_widgets = {}
        self.add_subtask_buttons={}

    def toggle_edit_mode(self):
        self.edit_mode=not self.edit_mode
        if self.edit_mode:
            self.title("Project Manager - Edit Mode")
            self.ProjectFrame.configure(fg_color="#5A1D1D")
        else:
            self.title("Project Manager")
            self.refresh_view()

    def setup_window(self):
        self.tasks_widgets = {}
        self.subtask_widgets = {}
        self.add_subtask_buttons = {}

        self.ProjectFrame = ProjectFrame(self,self.width, self.height)
        self.ProjectFrame.grid_propagate(False)
        self.ProjectFrame.grid_columnconfigure(0, weight=1)  # task names use remaining space
        self.ProjectFrame.grid_columnconfigure(1, minsize=5)
        self.ProjectFrame.grid_columnconfigure(2, minsize=55)

        if self.edit_mode:
            self.toggle_edit_mode()

        if self.project_obj is None:
            raise ValueError(f"Project with id {self.project_id} could not be loaded.")

        task_rows = self.view_model.get_task_rows(self.project_obj)
        task_names=[row["task"].name for row in task_rows]
        task_ids=[row["task"].uuid for row in task_rows]
        button_colour=ctk.ThemeManager.theme["CTkButton"]["fg_color"]
        different_button_colour=adjust_colour(button_colour[0])

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

        back_button = ctk.CTkButton(
            utility_frame, command=self.go_back, width=5, height=5, text="",
            image=ctk.CTkImage(light_image=Image.open("assets/icons/back.png"), size=(15, 15)), 
            fg_color=different_button_colour
        )
        back_button.pack(side="left", padx=10)
        Tooltip(back_button, "Back to Projects")

        row_count=1
        for x in range(len(task_names)):
            
            subtasks = task_rows[x]["subtasks"]
            subtask_names=[subtask.name for subtask in subtasks]
            subtask_ids=[subtask.uuid for subtask in subtasks]
            pady = (10, 3) if x == 0 else 3

            self.tasks_widgets[f"{task_ids[x]}"] = ctk.CTkCheckBox(self.ProjectFrame, text=f"{task_names[x]}",
                    command=lambda id=task_ids[x]: self.checkbox_command(id, "Task"), width=0.1*self.ProjectFrame.width)
            self.tasks_widgets[f"{task_ids[x]}"].grid(column=0, row=row_count, pady=pady, padx=0.05*self.ProjectFrame.width, sticky="w")
            ctk.CTkButton(
                self.ProjectFrame, text="", width=48, height=25,
                image=ctk.CTkImage(light_image=Image.open("assets/icons/workflow.png"), size=(15, 15)),
                fg_color=different_button_colour,
                command=lambda id=task_ids[x], name=task_names[x]: self.open_automation_window(id, name)
            ).grid(column=2, row=row_count, pady=pady, padx=3, sticky="e")
            row_count+=1

            for i in range(len(subtask_names)):
                self.subtask_widgets[f"{task_ids[x]}_{subtask_ids[i]}"] = ctk.CTkCheckBox(self.ProjectFrame, text=f"{subtask_names[i]}",
                    command=lambda id=[subtask_ids[i], task_ids[x]]: self.checkbox_command(id[0], "Subtask", id[1]), 
                    width=0.1*self.ProjectFrame.width)
                self.subtask_widgets[f"{task_ids[x]}_{subtask_ids[i]}"].grid(column=0, row=row_count, pady=pady, padx=0.1*self.ProjectFrame.width, sticky="nw")

                ctk.CTkButton(
                    self.ProjectFrame, text="", width=48, height=25,
                    image=ctk.CTkImage(light_image=Image.open("assets/icons/workflow.png"), size=(15, 15)),
                    fg_color=different_button_colour,
                    command=lambda id=subtask_ids[i], name=subtask_names[i]: self.open_automation_window(id, name)
                ).grid(column=2, row=row_count, pady=pady, padx=3, sticky="e")
                row_count+=1

            self.add_subtask_buttons[f"{task_ids[x]}"] = ctk.CTkButton(self.ProjectFrame, text="Add Subtask",
                    command=lambda task_id=task_ids[x]:self.instantiate_new("Subtask", task_id), fg_color=different_button_colour, width=0.2*self.ProjectFrame.width)
            self.add_subtask_buttons[f"{task_ids[x]}"].grid(row=row_count, column=0, pady=pady, padx=0.1*self.ProjectFrame.width, sticky="w")

            row_count+=1

        add_task_button = ctk.CTkButton(self.ProjectFrame, text="Add Task",
                    command=lambda:self.instantiate_new("Task", self.project_id), fg_color=different_button_colour, width=0.9*self.ProjectFrame.width)
        add_task_button.grid(row=row_count, column=0, pady=10, padx=0.05*self.ProjectFrame.width)

    def go_back(self):
        from gui.main.main_gui import MainWindow
        self.destroy()
        main_window = MainWindow()
        main_window.setup_window()
        main_window.mainloop()

    def checkbox_command(self, id, class_type, task_id=None):
        if self.edit_mode:
            obj=self.view_model.get_item(id)
            if obj is None:
                print(f"Unable to edit object {id}: object not found.")
                self.refresh_view()
                return
            EditWindow=AddWindow(self, class_type, self.project_id, "edit", obj.uuid, obj.name, obj.description, obj.deadline)
            EditWindow.setup_window()
        else:  
            if class_type == "Task":
                self.tasks_widgets[f"{id}"].destroy()
                self.add_subtask_buttons[f"{id}"].destroy()
                self.view_model.delete(id)
            else:
                self.subtask_widgets[f"{task_id}_{id}"].destroy()
                self.view_model.delete(id)
    
    def instantiate_new(self, class_type, parent_id=None):
        new_object_screen = AddWindow(self, class_type, parent_id)
        new_object_screen.setup_window()

    def open_automation_window(self, item_id, item_name):
        automation_window = AutomationWindow(item_id, item_name, self)
        automation_window.setup_window()

    def refresh_view(self):
        if self.ProjectFrame is not None:
            self.ProjectFrame.destroy()
        self.view_model.reload()
        self.project_obj=self.view_model.get_project(self.project_id)
        self.setup_window()
