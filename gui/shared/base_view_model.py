from manager import Manager


class BaseViewModel:
    def __init__(self, manager=Manager()):
        self.manager = manager

    def load_all(self):
        return self.manager.load_all()

    def reload(self):
        return self.manager.reload()

    def get_item(self, item_id):
        return self.manager.get_item(item_id)

    def save(self, item):
        return self.manager.save(item)

    def delete(self, item_id):
        return self.manager.delete(item_id)

    def add_project(self, name, description=None, deadline=None):
        return self.manager.add_project(name, description, deadline)

    def add_task(self, name, project, description="", deadline=None):
        return self.manager.add_task(name, project, description, deadline)

    def add_subtask(self, name, task, description="", deadline=None):
        return self.manager.add_subtask(name, task, description, deadline)
