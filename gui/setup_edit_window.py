import customtkinter as ctk
from classes import Manager

class AddWindow(ctk.CTkToplevel):
    def __init__(self, master, item_type, parent_id=None, mode="new", id=None, name=None, status="Not Started", description=None, deadline=None):
        super().__init__(master=master)
        self.item_type=item_type
        self.mode=mode
        self.parent_id=parent_id
        self.id=id
        self.name=name
        self.status=status
        self.description=description
        self.deadline=deadline
        self.title("Add Task")
        self.width=500
        self.height=500
        self.geometry(f"{self.width}x{self.height}")
        self.lift()
        self.focus_force()
        self.attributes('-topmost', True)
        self.store=Manager()
    
    def setup_window(self):
        name, status, description, deadline = setup_edit_window(self, self.item_type, self.mode, self.name, self.status, self.description, self.deadline)
        create_text="Create" if self.mode == "new" else "Save"
        create_button= ctk.CTkButton(self, text=create_text, 
            command=lambda:self.add_task_and_close(*get_edit_inputs(name, status, description, deadline)))
        
        create_button.pack(pady=(10,4))
        cancel_button=ctk.CTkButton(self, text="Cancel", command=self.destroy)
        cancel_button.pack(pady=4)
        if self.mode != "new":
            delete_button=ctk.CTkButton(self, text="Delete", fg_color="#970E0E", text_color="#FFFFFF",hover_color="#D31C1C", command=self.delete_task)
            delete_button.pack(pady=(10,4))

    def delete_task(self):
        self.store.delete(self.id)
        if self.parent_id is not None:
            self.store.save(self.store.get_item(self.parent_id))
        self.store.reload()
        self.destroy()
        self.master.refresh_view()

    def _show_error(self, message):
        if hasattr(self, "success_label"):
            self.success_label.destroy()
        if hasattr(self, "error_label"):
            self.error_label.destroy()
        self.error_label = ctk.CTkLabel(self, text=message, text_color="#A72A2A")
        self.error_label.pack(pady=4)

    def add_task_and_close(self, name, status, description, deadline):
        try:
            if self.mode=="edit":
                obj=self.store.get_item(self.id)
                if obj is None:
                    raise ValueError("The selected item could not be found.")
                obj.name=name
                obj.status=status
                obj.description=description
                obj.deadline=deadline
                self.store.save(obj)

            else:
                if self.item_type=="Project":
                    self.store.add_project(name, description, deadline)
                else:
                    parent_obj = self.store.get_item(self.parent_id)
                    if parent_obj is None:
                        raise ValueError(f"Parent {self.item_type} parent could not be found.")

                    if self.item_type=="Task":
                        self.store.add_task(name, parent_obj, description, deadline)
                    elif self.item_type=="Subtask":
                        self.store.add_subtask(name, parent_obj, description, deadline)

                    self.store.save(parent_obj)
            
            self.destroy()
            self.master.refresh_view()
            
        except ValueError as exc:
            print(f"Something went wrong when creating the {self.item_type}: {exc}")
            self._show_error(str(exc))
        

def setup_edit_window(self, item_type, mode="new", name=None, status="Not Started", description=None, deadline=None):

    if mode=="new":
        label_text=f"New {item_type}"
    else:
        label_text=f"Edit {item_type}"

    main_label=ctk.CTkLabel(self, text=label_text, fg_color=ctk.ThemeManager.theme["CTkFrame"]["fg_color"],
                            width=0.3*self.width, corner_radius=10, font=("source sans pro", 15))
    
    main_label.pack(pady=(20,0))
    name_entry= ctk.CTkEntry(self, placeholder_text="Name")
    name_entry.pack(pady=(10,4))
    if name:
        name_entry.insert(0, name)

    ctk.CTkLabel(self, text="Status").pack(pady=(4,0))
    status_menu=ctk.CTkOptionMenu(self, values=["Not Started", "In Progress", "Completed"], width=200, height=30, corner_radius=10)
    status_menu.pack(pady=(4,0))
    if status != "Not Started":
        status_menu.set(status)

    description_text=None
    description_label= ctk.CTkLabel(self, text="Description:")
    description_label.pack(pady=(4,0))
    description_text= ctk.CTkTextbox(self, height=100)
    description_text.pack(pady=4)
    if description:
        description_text.insert("1.0",description)

    deadline_entry = ctk.CTkEntry(self, placeholder_text="Deadline (DD-MM-YYYY)")
    deadline_entry.pack(pady=4)
    if deadline:
        deadline_entry.insert(0, deadline.strftime("%d-%m-%Y"))

    deadline_hint = ctk.CTkLabel(self, text="Deadline must be a future date in DD-MM-YYYY format.", font=("default", 11))
    deadline_hint.pack(pady=(0, 4))
    return name_entry, status_menu, description_text, deadline_entry

def get_edit_inputs(name_entry, status_menu, description_text, deadline):
    name_entry=name_entry.get()
    status=status_menu.get()
    try:
        description_text=description_text.get("1.0", "end")
    except:
        description_text=""
    try:
        deadline=deadline.get()
    except:
        deadline=None

    return name_entry, status, description_text, deadline