import datetime
from automations import (
    EmailAction,
    LogAction,
    StatusAction,
    StatusTrigger,
    TimeTrigger,
)
from gui.shared.base_view_model import BaseViewModel


class AutomationViewModel(BaseViewModel):
    def get_automation_rows(self, item):
        return [
            {"id": automation.uuid, "name": automation.name}
            for automation in item.automations
        ]

    def collect_values(self, item, name, trigger_values, action_type, action_values):
        triggers = []
        for trigger_type, value in trigger_values:
            if trigger_type == "Status":
                triggers.append(StatusTrigger(item, value))
            elif trigger_type == "Deadline":
                if not value:
                    raise ValueError("Select a deadline for the time trigger.")
                if isinstance(value, str):
                    try:
                        value = datetime.datetime.strptime(
                            value.strip(), "%d-%m-%Y %H:%M"
                        )
                    except ValueError as exc:
                        raise ValueError(
                            "Deadline trigger must use DD-MM-YYYY HH:MM format."
                        ) from exc
                triggers.append(TimeTrigger(item, value))

        if action_type == "Email":
            return name, EmailAction(
                item,
                action_values["sender_email"],
                action_values["recipient_email"],
                action_values["subject"],
                action_values["message"],
                triggers,
            )
        if action_type == "Status":
            return name, StatusAction(item, action_values["target_status"], triggers)
        if action_type == "Log":
            return name, LogAction(item, action_values["log_message"], triggers)
        raise ValueError("Unknown Action Type")

    def get_automation(self, item_id, automation_id):
        item = self.get_item(item_id)
        if item is None:
            return None
        return item.get_automation_obj(automation_id)

    def save_automation(self, item, automation):
        item.add_automation(automation)
        automation.evaluate_status_triggers()
        automation.evaluate_time_triggers()
        self.save(item)

    def delete_automation(self, item, automation_id):
        item.delete_automation(automation_id)
        self.save(item)
