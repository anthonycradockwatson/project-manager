import customtkinter as ctk
from classes import Manager
from automations import Automation, TimeTrigger, StatusTrigger, EmailAction, StatusAction, LogAction
from colour_bs import adjust_colour
from PIL import Image

class AutomationFrame(ctk.CTkFrame):
    def __init__(self,master, width, height):
        super().__init__(master=master)
        self.width=int(0.8*width)
        self.height=int(0.9*height)
        self.configure(width=self.width, height=self.height)

class AutomationWindow(ctk.CTkToplevel):
    def __init__(self, project_id, project_name):
        super().__init__()
        self.project_id=project_id
        self.width = 200
        self.height=300
        self.title(f"{project_name} - Automations")
        self.geometry(f"{self.width}x{self.height}")
        self.store=Manager()
        self.project_obj=self.store.get_item(self.project_id)
        self.attributes("-topmost", True)

    def setup_window(self):
        self.AutomationFrame = AutomationFrame(self,self.width, self.height)
        self.AutomationFrame.grid(row=0, column=0, pady=15, padx=(15,5), sticky="nsew")
        self.AutomationFrame.grid_propagate(False)
        self.AutomationFrame.grid_columnconfigure(0, weight=1)
        self.AutomationFrame.grid_columnconfigure(1, weight=1)

        automation_names=[automation.name for automation in self.project_obj.automations]
        automation_ids=[automation.uuid for automation in self.project_obj.automations]
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
        self.store.reload()
        self.project_obj=self.store.get_item(self.project_id)
        for widget in list(self.winfo_children()):
            widget.destroy()
        self.setup_window()

class ChangeAutomationWindow(ctk.CTkToplevel):
    def __init__(self, project_id, master_window, mode="add", automation_id=None):
        super().__init__()
        self.master = master_window
        self.project_id = project_id
        self.automation_id = automation_id
        self.mode = mode
        self.width = 450
        self.height = 700

        self.title("Automation Setup")
        self.geometry(f"{self.width}x{self.height}")
        self.attributes("-topmost", True)

        self.store = Manager()
        self.project_obj = self.store.get_item(self.project_id)
        self.automation_obj = None

        if self.mode == "edit":
            for a in self.project_obj.automations:
                if a.uuid == self.automation_id:
                    self.automation_obj = a
                    break

        # Keep track of dynamically added trigger rows
        self.trigger_rows = []

        self.setup_ui()

    def setup_ui(self):
        self.grid_columnconfigure(1, weight=1)

        # 1. Automation Name
        ctk.CTkLabel(self, text="Automation Name:").grid(row=0, column=0, padx=10, pady=10, sticky="w")
        self.name_entry = ctk.CTkEntry(self, placeholder_text="Automation Name")
        self.name_entry.grid(row=0, column=1, padx=10, pady=10, sticky="ew")

        if self.automation_obj and self.automation_obj.name:
            self.name_entry.insert(0, self.automation_obj.name)

        # 2. Dynamic Triggers Section
        ctk.CTkLabel(self, text="Triggers:", font=("", 13, "bold")).grid(row=1, column=0, padx=10, pady=(10, 2), sticky="w")

        self.triggers_container = ctk.CTkScrollableFrame(self, height=140, fg_color="transparent")
        self.triggers_container.grid(row=2, column=0, columnspan=2, padx=10, pady=5, sticky="nsew")
        self.triggers_container.grid_columnconfigure(0, weight=1)

        add_trig_btn = ctk.CTkButton(self, text="+ Add Trigger", command=self.add_trigger_row)
        add_trig_btn.grid(row=3, column=0, columnspan=2, padx=10, pady=5, sticky="ew")

        # 3. Action Section
        ctk.CTkLabel(self, text="Action Type:").grid(row=4, column=0, padx=10, pady=10, sticky="w")
        self.action_type = ctk.CTkOptionMenu(
            self, values=["Email", "Log", "Status"], command=lambda v: self.render_action_fields()
        )
        self.action_type.grid(row=4, column=1, padx=10, pady=10, sticky="ew")

        # Action parameters frame
        self.action_frame = ctk.CTkFrame(self, fg_color="#252526")
        self.action_frame.grid(row=5, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")
        self.action_frame.grid_columnconfigure(1, weight=1)

        # Buttons
        btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        btn_frame.grid(row=6, column=0, columnspan=2, padx=10, pady=10, sticky="ew")
        btn_frame.grid_columnconfigure((0, 1), weight=1)

        ctk.CTkButton(btn_frame, text="Save", command=self.save_automation_and_close).grid(row=0, column=0, padx=5, sticky="ew")
        if self.mode == "edit":
            ctk.CTkButton(
                btn_frame, text="Delete", fg_color="#970E0E", hover_color="#D31C1C",
                command=self.delete_automation_and_close
            ).grid(row=0, column=1, padx=5, sticky="ew")

        # Populate existing triggers or create a default dynamic row
        existing_triggers = []
        if self.automation_obj and hasattr(self.automation_obj, "action") and self.automation_obj.action:
            act = self.automation_obj.action
            if hasattr(act, "type") and act.type:
                self.action_type.set(act.type)
            if hasattr(act, "triggers") and act.triggers:
                existing_triggers = act.triggers

        if existing_triggers:
            for trig in existing_triggers:
                t_label = "Status" if trig.type == "Status" else "Deadline"
                self.add_trigger_row(initial_type=t_label, initial_val=trig.target)
        else:
            self.add_trigger_row()

        self.render_action_fields()
        self.populate_action_values()

    def add_trigger_row(self, initial_type="Status", initial_val=None):
        """Adds a new trigger UI row into the scrollable container."""
        row_frame = ctk.CTkFrame(self.triggers_container, fg_color="#1E1E1E")
        row_frame.pack(fill="x", pady=3, expand=True)
        row_frame.grid_columnconfigure(1, weight=1)

        # Type Dropdown
        type_menu = ctk.CTkOptionMenu(row_frame, values=["Status", "Deadline"], width=110)
        type_menu.set(initial_type)
        type_menu.grid(row=0, column=0, padx=5, pady=5)

        # Dynamic Value Container
        value_box = [None]  # List wrapper so inner closure can modify reference

        def update_input_widget(selected_type):
            if value_box[0]:
                value_box[0].destroy()
            if selected_type == "Status":
                widget = ctk.CTkOptionMenu(row_frame, values=["Not Started", "In Progress", "Completed"])
                if initial_val and selected_type == initial_type:
                    widget.set(initial_val)
            else:
                widget = ctk.CTkEntry(row_frame, placeholder_text="YYYY-MM-DD")
                if initial_val and selected_type == initial_type:
                    widget.insert(0, str(initial_val))
            widget.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
            value_box[0] = widget

        type_menu.configure(command=update_input_widget)
        update_input_widget(initial_type)

        # Record entry reference tuple
        row_data = (row_frame, type_menu, value_box)
        self.trigger_rows.append(row_data)

        # Delete Button
        def remove_row():
            row_frame.destroy()
            if row_data in self.trigger_rows:
                self.trigger_rows.remove(row_data)
        del_btn = ctk.CTkButton(row_frame, text="", image=ctk.CTkImage(light_image=Image.open("assets/icons/close.png"), 
                                                                       size=(10, 10)), width=20, height=25, fg_color="#970E0E", hover_color="#D31C1C", command=remove_row)
        del_btn.grid(row=0, column=2, padx=5, pady=5)

    def render_action_fields(self):
        for child in self.action_frame.winfo_children():
            child.destroy()

        act_type = self.action_type.get()
        if act_type == "Email":
            ctk.CTkLabel(self.action_frame, text="From:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
            self.sender_email = ctk.CTkEntry(self.action_frame, placeholder_text="sender@example.com")
            self.sender_email.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

            ctk.CTkLabel(self.action_frame, text="To:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
            self.recipient_email = ctk.CTkEntry(self.action_frame, placeholder_text="recipient@example.com")
            self.recipient_email.grid(row=1, column=1, padx=5, pady=5, sticky="ew")

            ctk.CTkLabel(self.action_frame, text="Subject:").grid(row=2, column=0, padx=5, pady=5, sticky="w")
            self.subject_entry = ctk.CTkEntry(self.action_frame, placeholder_text="Subject")
            self.subject_entry.grid(row=2, column=1, padx=5, pady=5, sticky="ew")

            self.email_message = ctk.CTkTextbox(self.action_frame, height=100)
            self.email_message.grid(row=3, column=0, columnspan=2, padx=5, pady=5, sticky="ew")

        elif act_type == "Log":
            ctk.CTkLabel(self.action_frame, text="Log Message:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
            self.log_message = ctk.CTkTextbox(self.action_frame, height=120)
            self.log_message.grid(row=1, column=0, columnspan=2, padx=5, pady=5, sticky="ew")

        elif act_type == "Status":
            ctk.CTkLabel(self.action_frame, text="Target Status:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
            self.new_status = ctk.CTkOptionMenu(self.action_frame, values=["Not Started", "In Progress", "Completed"])
            self.new_status.grid(row=0, column=1, padx=5, pady=5, sticky="w")

    def populate_action_values(self):
        if not self.automation_obj or not self.automation_obj.action:
            return

        act = self.automation_obj.action
        act_type = self.action_type.get()

        if act_type == "Email" and hasattr(act, "sender_email"):
            self.sender_email.insert(0, getattr(act, "sender_email", ""))
            self.recipient_email.insert(0, getattr(act, "recipient_email", ""))
            self.subject_entry.insert(0, getattr(act, "subject", ""))
            self.email_message.insert("1.0", getattr(act, "message", ""))
        elif act_type == "Log" and hasattr(act, "log_message"):
            self.log_message.insert("1.0", getattr(act, "log_message", ""))
        elif act_type == "Status" and hasattr(act, "target_status"):
            self.new_status.set(getattr(act, "target_status", "Not Started"))

    def collect_values(self):
        name = self.name_entry.get().strip() or "Untitled Automation"

        # Dynamically build all Trigger objects from the UI list
        triggers_list = []
        for _, type_menu, value_box in self.trigger_rows:
            t_type = type_menu.get()
            val = value_box[0].get() if value_box[0] else ""
            if t_type == "Status":
                triggers_list.append(StatusTrigger(self.project_obj, val))
            elif t_type == "Deadline":
                triggers_list.append(TimeTrigger(self.project_obj, val))

        act_type = self.action_type.get()
        if act_type == "Email":
            action = EmailAction(
                self.project_obj,
                self.sender_email.get(),
                self.recipient_email.get(),
                self.subject_entry.get(),
                self.email_message.get("1.0", "end-1c"),
                triggers_list
            )
        elif act_type == "Status":
            action = StatusAction(self.project_obj, self.new_status.get(), triggers_list)
        elif act_type == "Log":
            action = LogAction(self.project_obj, self.log_message.get("1.0", "end-1c"), triggers_list)
        else:
            raise ValueError("Unknown Action Type")

        return name, action

    def save_automation_and_close(self):
        try:
            name, action = self.collect_values()
        except Exception as e:
            print(f"Error collecting values: {e}")
            return

        if self.mode == "add":
            new_auto = Automation(self.project_obj, action, name=name)
            self.project_obj.add_automation(new_auto)
        elif self.mode == "edit" and self.automation_obj:
            self.automation_obj.name = name
            self.automation_obj.action = action

        self.store.save(self.project_obj)
        self.destroy()
        self.master.refresh_view()

    def delete_automation_and_close(self):
        if self.automation_id:
            self.project_obj.delete_automation(self.automation_id)
            self.store.save(self.project_obj)
        self.destroy()
        self.master.refresh_view()
   