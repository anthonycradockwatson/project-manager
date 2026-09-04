from automations import Automation
from gui.automations.automation_view_model import AutomationViewModel
import customtkinter as ctk
from gui.shared.deadline_window_gui import DeadlinePicker
from PIL import Image

class ChangeAutomationWindow(ctk.CTkToplevel):
    def __init__(self, project_id, master_window, mode="add", automation_id=None):
        super().__init__()
        self.master = master_window
        self.project_id = project_id
        self.automation_id = automation_id
        self.mode = mode
        self.width = 450
        self.height = 560
        self.base_trigger_height = 70
        self.trigger_row_height = 48
        self.max_trigger_height = 320

        self.title("Automation Setup")
        self.geometry(f"{self.width}x{self.height}")
        self.attributes("-topmost", True)

        self.view_model = AutomationViewModel()
        self.project_obj = self.view_model.get_item(self.project_id)
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
            self, values=["Email", "Log", "Status"], command=lambda _value: self.render_action_fields()
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
        if self.automation_obj and self.automation_obj.action:
            act = self.automation_obj.action
            if act.type:
                self.action_type.set(act.type)
            if act.triggers:
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
                widget = DeadlinePicker(
                    row_frame, initial_val if selected_type == initial_type else None
                )
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
            self.update_trigger_layout()
        del_btn = ctk.CTkButton(row_frame, text="", image=ctk.CTkImage(light_image=Image.open("assets/icons/close.png"), 
                                                                       size=(10, 10)), width=20, height=25, fg_color="#970E0E", hover_color="#D31C1C", command=remove_row)
        del_btn.grid(row=0, column=2, padx=5, pady=5)
        self.update_trigger_layout()

    def update_trigger_layout(self):
        trigger_height = min(
            self.max_trigger_height,
            max(self.base_trigger_height, len(self.trigger_rows) * self.trigger_row_height),
        )
        self.triggers_container.configure(height=trigger_height)
        self.geometry(f"{self.width}x{self.height + trigger_height - self.base_trigger_height}")

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

        if act_type == "Email":
            self.sender_email.insert(0, act.sender_email)
            self.recipient_email.insert(0, act.recipient_email)
            self.subject_entry.insert(0, act.subject)
            self.email_message.insert("1.0", act.message)
        elif act_type == "Log":
            self.log_message.insert("1.0", act.log_message)
        elif act_type == "Status":
            self.new_status.set(act.target_status)

    def save_automation_and_close(self):
        try:
            trigger_values = [
                (
                    type_menu.get(),
                    value_box[0].get() if value_box[0] else "",
                )
                for _, type_menu, value_box in self.trigger_rows
            ]
            action_values = {}
            action_type = self.action_type.get()
            if action_type == "Email":
                action_values = {
                    "sender_email": self.sender_email.get(),
                    "recipient_email": self.recipient_email.get(),
                    "subject": self.subject_entry.get(),
                    "message": self.email_message.get("1.0", "end-1c"),
                }
            elif action_type == "Status":
                action_values["target_status"] = self.new_status.get()
            elif action_type == "Log":
                action_values["log_message"] = self.log_message.get("1.0", "end-1c")
            name, action = self.view_model.collect_values(
                self.project_obj,
                self.name_entry.get().strip() or "Untitled Automation",
                trigger_values,
                action_type,
                action_values,
            )
        except Exception as e:
            print(f"Error collecting values: {e}")
            return

        if self.mode == "add":
            new_auto = Automation(self.project_obj, action, name=name)
            self.view_model.save_automation(self.project_obj, new_auto)
        elif self.mode == "edit" and self.automation_obj:
            self.automation_obj.name = name
            self.automation_obj.action = action

        self.view_model.save(self.project_obj)
        self.destroy()
        self.master.refresh_view()

    def delete_automation_and_close(self):
        if self.automation_id:
            self.project_obj.delete_automation(self.automation_id)
            self.view_model.save(self.project_obj)
        self.destroy()
        self.master.refresh_view()
   