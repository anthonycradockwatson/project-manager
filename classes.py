from datetime import date, datetime
import uuid

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

            formats = [
                "%d-%m-%Y %H:%M",
                "%d-%m-%Y",
                "%Y-%m-%d %H:%M",
                "%Y-%m-%d",
            ]
            parsed = None
            for date_format in formats:
                try:
                    parsed = datetime.strptime(deadline, date_format)
                    break
                except ValueError:
                    continue

            if parsed is None:
                raise ValueError("Deadline must be a valid date in DD-MM-YYYY or DD-MM-YYYY HH:MM format.")

            deadline = parsed

        if isinstance(deadline, datetime):
            pass
        elif isinstance(deadline, date):
            try:
                deadline = datetime.combine(deadline, datetime.min.time())
            except TypeError as exc:
                raise ValueError("Deadline must be a valid date or datetime.") from exc
        else:
            raise ValueError("Deadline must be a valid date or datetime.")

        if deadline.time() == datetime.min.time():
            deadline = deadline.replace(hour=0, minute=0)

        if deadline <= datetime.now():
            raise ValueError("Deadline must be in the future.")

        self._deadline = deadline


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
        for automation in list(self.automations):
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
        
