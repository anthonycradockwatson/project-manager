from datetime import datetime, timedelta
import os
import uuid
import smtplib
from dotenv import load_dotenv
from email.message import EmailMessage

load_dotenv() 

class Automation():
    def __init__(self, item, action, name=" "): # item is the task object, name is the name of the automation
        self.item=item
        self.name=name
        self.action=action
        self.uuid=str(uuid.uuid4())

    def evaluate_status_triggers(self):
        for trigger in list(self.action.triggers):
            if trigger.type == "Status" and trigger.is_triggered():
                self.item.delete_automation(self.uuid)
                self.action.execute()
                return True
        return False

    def evaluate_time_triggers (self):
        executed = False
        for trigger in list(self.action.triggers):
            if trigger.type == "Time" and trigger.is_triggered():
                self.item.delete_automation(self.uuid)
                self.action.execute()
                executed = True
        return executed

#----------------------------------------------------------------------------------------------------------------------------------

class Trigger():
    def __init__(self, item, trigger_type, target, condition):
        self.item=item
        self.type=trigger_type
        self.target=target
        self.condition=condition

    def is_triggered(self):
        return self.condition == self.target
    
class TimeTrigger(Trigger):
    def __init__(self, item, target_time):
        super().__init__(item, "Time", target_time, "_deadline")
        if self.target is None or type(self.target) is not datetime:
            raise ValueError(f"Item {self.item.name} does not have a deadline set.")

    def is_triggered(self):
        return datetime.now() >= self.target

    def change_target_time(self, new_time):
        if new_time <= datetime.now():
            raise ValueError("Target time must be in the future.")
        self.target=new_time
        
class StatusTrigger(Trigger):
    def __init__(self, item, target_status):
        super().__init__(item, "Status", target_status, "_status")
    
    def change_target_status(self, new_status):
        self.target=new_status

    def is_triggered(self):
        return self.item.status == self.target

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
        try:
            self.send_email_via_smtp(self.sender_email, self.recipient_email, self.subject, self.message)
        except Exception as e:
            print(f"Failed to send email: {e}")

    def send_email_via_smtp(self, sender_email, recipient_email, subject, message):
        smtp_host = os.getenv("SMTP_HOST")
        smtp_port = int(os.getenv("SMTP_PORT", "587"))
        smtp_user = os.getenv("SMTP_USER")
        smtp_password = os.getenv("SMTP_PASSWORD")

        if not all([smtp_host, smtp_user, smtp_password]):
            raise ValueError("Missing SMTP configuration.")

        msg = EmailMessage()
        msg["Subject"] = subject
        msg["From"] = sender_email
        msg["To"] = recipient_email
        msg.set_content(message)

        with smtplib.SMTP(smtp_host, smtp_port) as server:
            server.starttls()
            server.login(smtp_user, smtp_password)
            server.send_message(msg)

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
