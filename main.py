import time
import customtkinter as ctk
from gui.main_gui import MainWindow
import threading
from classes import Manager

"#7C1313"
if __name__ == "__main__":

    def run_time_thread():
        store=Manager()
        while True:
            for item in store.load_all().values():
                for automation in item.automations:
                    automation.evaluate_time_triggers()
            time.sleep(30)

    time_thread=threading.Thread(target=run_time_thread, daemon=True)
    time_thread.start()
    
    window=MainWindow()
    window.setup_window()
    window.mainloop()

"""
Things to do:

Convert from datetime to time delta and fix the surrounding logic
Set up automation widgets for tasks and subtasks
Add in a get remaining time and use the lowest value to have the time automation only run then
Add automation trigger checks when a new automation is created
Make the Email automation actually send an email
Make the automation setup height adjust depending on the number of triggers
"""