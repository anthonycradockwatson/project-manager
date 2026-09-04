from gui.shared.base_view_model import BaseViewModel


class ItemEditViewModel(BaseViewModel):
    def collect_values(self, name_entry, status_menu, description_text, deadline):
        name = name_entry.get()
        status = status_menu.get()
        description = description_text.get("1.0", "end")
        return name, status, description, deadline.get()

    def save_item(self, item):
        self.save(item)

    def create_item(self, item_type, name, parent, description, deadline):
        if item_type == "Project":
            return self.add_project(name, description, deadline)
        if parent is None:
            raise ValueError(f"Parent {item_type} parent could not be found.")
        if item_type == "Task":
            return self.add_task(name, parent, description, deadline)
        if item_type == "Subtask":
            return self.add_subtask(name, parent, description, deadline)
        raise ValueError(f"Unknown item type: {item_type}")
