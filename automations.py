from datetime import datetime
import os
import uuid


class Automation():
    def __init__(self, item, action, name=" "): # item is the task object, name is the name of the automation
        self.item=item
        self.name=name
        self.action=action
        self.uuid=str(uuid.uuid4())

    def evaluate_status_triggers(self):
        for trigger in self.action.triggers:
            if trigger.type == "Status" and trigger.is_triggered(self.item):
                self.action.execute()

    def evaluate_time_triggers (self):
        for trigger in self.action.triggers:
            if trigger.type == "Time" and trigger.is_triggered(self.item):
                self.action.execute()

#----------------------------------------------------------------------------------------------------------------------------------

class Trigger():
    def __init__(self, item, trigger_type, target, condition):
        self.item=item
        self.type=trigger_type
        self.target=target
        self.condition=condition

    def is_triggered(self, item):
        if getattr(item, self.condition) == self.target:
            return True
    
class TimeTrigger(Trigger):
    def __init__(self, item, time):
        super().__init__(item, "Time", time, "_deadline")
        if item.deadline is None:
            raise ValueError("Item must have a deadline to use Time Automations.")

    def change_remaining_time(self, new_time):
        new_time=int(new_time.total_seconds())
        if new_time<=0:
            self.remaining_time=0
        else:
            self.remaining_time = new_time
        
class StatusTrigger(Trigger):
    def __init__(self, item, target_status):
        super().__init__(item, "Status", target_status, "_status")
    
    def change_target_status(self, new_status):
        self.target=new_status

#---------------------------------------------------------------------------------------------------------------------------------- 
    
class Action():
    def __init__(self, item, action_type, triggers):
        self.item=item
        self.type=action_type
        self.triggers=triggers if triggers is not None else []

    def execute(self):
        pass

class EmailAction(Action):
    def __init__(self, item, sender_email, recipient_email, subject, message, triggers=None):
        super().__init__(item, "Email", triggers)
        self.sender_email = sender_email
        self.recipient_email = recipient_email
        self.subject=subject
        self.message = message

    def change_subject(self, new_subject):
        self.subject=new_subject

    def change_message(self, new_message):
        self.message = new_message
    
    def change_sender_email(self, new_sender_email):
        self.sender_email = new_sender_email
    
    def change_recipient_email(self, new_recipient_email):
        self.recipient_email = new_recipient_email

    def execute(self):
        # Implement email sending logic here
        pass

class StatusAction(Action):
    def __init__(self, item, target_status, triggers=None):
        super().__init__(item, "Status", triggers)
        self.target_status = target_status
    
    def execute(self):
        self.item.status = self.target_status


class LogAction(Action):
    def __init__(self, item, log_message, triggers=None):
        super().__init__(item, "Log", triggers)
        self.log_message = log_message
    
    def change_log_message(self, new_log_message):
        self.log_message = new_log_message
    
    def execute(self):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] \n {self.log_message}"
        dir_path = os.path.join("logs")
        os.makedirs(dir_path, exist_ok=True)
        n=sum(1 for f in os.listdir(dir_path) if f.startswith("log") and f.endswith(".txt"))


        log_file_path = os.path.join("logs", f"log{n}.txt")

        os.makedirs(os.path.dirname(log_file_path), exist_ok=True)

        with open(log_file_path, "w+") as log_file:
            log_file.write(log_entry)
