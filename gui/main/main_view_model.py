from gui.shared.base_view_model import BaseViewModel


class MainViewModel(BaseViewModel):
    def get_projects(self):
        return [
            item for item in self.load_all().values()
            if item.item_type == "Project"
        ]
