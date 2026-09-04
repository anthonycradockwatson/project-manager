import time
import customtkinter as ctk
from gui.main.main_gui import MainWindow
import threading
from manager import Manager

"#7C1313"
if __name__ == "__main__":

    def run_time_thread():
        store=Manager()
        while True:
            for item in store.load_all().values():
                for automation in list(item.automations):
                    try:
                        if automation.evaluate_time_triggers():
                            store.save(item)
                    except ValueError as exc:
                        print(f"Skipping invalid time trigger on {item.name}: {exc}")
            time.sleep(5)

    time_thread=threading.Thread(target=run_time_thread, daemon=True)
    time_thread.start()
    
    window=MainWindow()
    window.setup_window()
    window.mainloop()
