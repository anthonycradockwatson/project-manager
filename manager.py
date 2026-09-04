from automations import Automation
from classes import Project, SubTask, Task
from db_function import ObjectStore


class Manager:
    def __init__(self, filename="data/UserProjects.pkl"):
        self.store = ObjectStore(filename)

    def reload(self):
        self.store.objects = self.store.load_all()
        return self.store.objects

    def add_project(self, name, description=None, deadline=None):
        project = Project(name, description, deadline)
        self.store.add(project)
        return project

    def add_task(self, name, project_obj, description="", deadline=None):
        task = Task(name, description, deadline)
        project_obj.tasks.append(task)
        project_obj.task_uuids.append(task.uuid)
        self.store.add(task)
        self.store.update(project_obj)
        return task

    def add_subtask(self, name, task_obj, description="", deadline=None):
        subtask = SubTask(name, description, deadline)
        task_obj.subtasks.append(subtask)
        task_obj.subtask_uuids.append(subtask.uuid)
        self.store.add(subtask)
        self.store.update(task_obj)
        return subtask

    def load_all(self):
        objects = self.store.load_all()
        return {
            key: value for key, value in objects.items()
            if not isinstance(value, Automation)
        }

    def get_item(self, item_id):
        return self.store.get_item(item_id)

    def save(self, obj):
        self.store.update(obj)

    def delete(self, item_id):
        self.reload()
        obj = self.get_item(item_id)
        if not obj:
            return

        if obj.item_type == "Project":
            for task in list(obj.tasks):
                self.delete(task.uuid)
            self.store.delete(item_id)
            return

        if obj.item_type == "Task":
            parent_objs = [
                item for item in self.store.objects.values()
                if item.item_type == "Project" and item_id in item.task_uuids
            ]
            if parent_objs:
                parent_obj = parent_objs[0]
                parent_obj.task_uuids = [
                    task_id for task_id in parent_obj.task_uuids
                    if task_id != item_id
                ]
                parent_obj.tasks = [
                    task for task in parent_obj.tasks
                    if task.uuid != item_id
                ]
                self.store.update(parent_obj)

            for subtask in list(obj.subtasks):
                self.delete(subtask.uuid)
            self.store.delete(item_id)
            return

        parent_objs = [
            item for item in self.store.objects.values()
            if item.item_type == "Task" and item_id in item.subtask_uuids
        ]
        if parent_objs:
            parent_obj = parent_objs[0]
            parent_obj.subtask_uuids = [
                subtask_id for subtask_id in parent_obj.subtask_uuids
                if subtask_id != item_id
            ]
            parent_obj.subtasks = [
                subtask for subtask in parent_obj.subtasks
                if subtask.uuid != item_id
            ]
            self.store.update(parent_obj)

        self.store.delete(item_id)
