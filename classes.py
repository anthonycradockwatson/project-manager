from datetime import datetime
import uuid
from db_function import ObjectStore
from automations import Automation

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
        clean_dict = {
            key: val for key, val in objects.items() 
            if not isinstance(val, Automation)
        }
        return clean_dict

    def get_item(self, id):
        return self.store.get_item(id)
    
    def save(self, obj):
        self.store.update(obj)
    
    def delete(self, id):
        self.reload()
        obj=self.get_item(id)
        if not obj:
            return

        if obj.item_type=="Project":
            for task in list(obj.tasks):
                self.delete(task.uuid)
            self.store.delete(id)
            return

        if obj.item_type=="Task":
            parent_objs=[item for item in self.store.objects.values() if item.item_type=="Project" and id in item.task_uuids]
            if parent_objs:
                parent_obj = parent_objs[0]
                parent_obj.task_uuids = [task_id for task_id in parent_obj.task_uuids if task_id != id]
                parent_obj.tasks = [task for task in parent_obj.tasks if task.uuid != id]
                self.store.update(parent_obj)

            for subtask in list(obj.subtasks):
                self.delete(subtask.uuid)
            self.store.delete(id)
            return

        parent_objs=[item for item in self.store.objects.values() if item.item_type=="Task" and id in item.subtask_uuids]
        if parent_objs:
            parent_obj = parent_objs[0]
            parent_obj.subtask_uuids = [subtask_id for subtask_id in parent_obj.subtask_uuids if subtask_id != id]
            parent_obj.subtasks = [subtask for subtask in parent_obj.subtasks if subtask.uuid != id]
            self.store.update(parent_obj)

        self.store.delete(id)

class Item():
    def __init__(self, name, description="", deadline=None, status="Not Started", item_type=None, automations=[]):
        self.uuid=str(uuid.uuid4())
        self._name=name
        self.automations=automations
        self._description=description
        self.deadline=deadline
        self._status=status
        self.item_type=item_type

    @property
    def name(self):
        return self._name
    
    @name.setter
    def name(self, name):
        self._name=name

    @property
    def deadline(self):
        return self._deadline

    @deadline.setter
    def deadline(self, deadline):
        if deadline is None:
            self._deadline = None
            return

        if isinstance(deadline, str):
            deadline = deadline.strip()
            if not deadline:
                self._deadline = None
                return
            try:
                deadline = datetime.strptime(deadline, "%d-%m-%Y").date()
            except ValueError as exc:
                raise ValueError("Deadline must be a valid date in DD-MM-YYYY format.") from exc

        if isinstance(deadline, datetime):
            deadline = deadline.date()

        if deadline <= datetime.now().date():
            raise ValueError("Deadline must be in the future.")
        self._deadline = deadline

        for automation in self.automations:
            for trigger in automation.action.triggers:
                if trigger.type == "Time":
                    trigger.change_remaining_time(self._deadline - datetime.now().date())

    @property
    def description(self):
        return self._description
    
    @description.setter
    def description(self,description):
        self._description=description

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, status):
        self._status=status  
        for automation in self.automations:
            automation.evaluate_status_triggers()

    def get_automation_obj(self, automation_id):
        obj=[obj for obj in self.automations if obj.uuid == automation_id]
        return obj[0] if obj else None

    def add_automation(self, automation_obj):
        self.automations.append(automation_obj)

    def delete_automation(self, automation_id):
        obj=self.get_automation_obj(automation_id)
        if obj:
            self.automations.remove(obj)



class Project(Item):
    def __init__(self, project_name, description="", deadline=None, status="Not Started"):
        super().__init__(project_name, description, deadline, status, item_type="Project", automations=[])
        self.tasks=[]
        self.task_uuids=[]

    def add_task(self, task):
        self.tasks.append(task)

class Task(Item):
    def __init__(self, task_name, description="", deadline=None, status="Not Started"):
        super().__init__(task_name, description, deadline, status, item_type="Task", automations=[])
        self.subtasks=[]
        self.subtask_uuids=[]
        self.tags=[] 

    def add_subtask(self, subtask):
        self.subtasks.append(subtask)

    def add_tag(self, tag):
        if tag not in self.tags:
            self.tags.append(tag)


class SubTask(Item):
    def __init__(self, sub_task_name, description="", deadline=None, status="Not Started"):
        super().__init__(sub_task_name, description, deadline, status, item_type="SubTask", automations=[])
        


