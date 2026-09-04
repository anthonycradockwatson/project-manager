from datetime import date, datetime
import customtkinter as ctk
import calendar

class DeadlinePicker(ctk.CTkFrame):
    def __init__(self, master, deadline=None):
        super().__init__(master, fg_color="transparent")
        self.selected_date = None
        self.calendar_window = None
        self._selected_hour = 0
        self._selected_minute = 0

        if deadline:
            self._load_deadline(deadline)

        self.date_button = ctk.CTkButton(
            self, text=self.selected_date.strftime("%d-%m-%Y") if self.selected_date else "No deadline",
            command=self._open_calendar, width=145
        )
        self.date_button.pack(side="left", padx=(0, 6))

        self.time_entry = ctk.CTkEntry(
            self, placeholder_text="HH:MM", width=90
        )
        self.time_entry.pack(side="left", padx=3)
        self.time_entry.insert(0, f"{self._selected_hour:02d}:{self._selected_minute:02d}")

        ctk.CTkButton(self, text="Clear", command=self.clear, width=55).pack(
            side="left", padx=(6, 0)
        )

    def _load_deadline(self, deadline):
        if isinstance(deadline, str):
            for date_format in ("%d-%m-%Y %H:%M", "%d-%m-%Y", "%Y-%m-%d %H:%M", "%Y-%m-%d"):
                try:
                    deadline = datetime.strptime(deadline.strip(), date_format)
                    break
                except ValueError:
                    continue

        if isinstance(deadline, datetime):
            self.selected_date = deadline.date()
            self._selected_hour = deadline.hour
            self._selected_minute = deadline.minute
        elif isinstance(deadline, date):
            self.selected_date = deadline
            self._selected_hour = 0
            self._selected_minute = 0
        else:
            return


    def _open_calendar(self):
        if self.calendar_window is not None and self.calendar_window.winfo_exists():
            self.calendar_window.focus_force()
            return

        self.calendar_window = ctk.CTkToplevel(self)
        self.calendar_window.title("Select deadline date")
        self.calendar_window.resizable(False, False)
        self.calendar_window.transient(self.winfo_toplevel())
        self.calendar_window.grab_set()

        calendar_date = self.selected_date or date.today()
        month_state = [calendar_date.year, calendar_date.month]
        header = ctk.CTkFrame(self.calendar_window, fg_color="transparent")
        header.pack(fill="x", padx=10, pady=(10, 4))
        calendar_grid = ctk.CTkFrame(self.calendar_window, fg_color="transparent")
        calendar_grid.pack(padx=10, pady=(0, 10))

        def draw_month():
            for child in calendar_grid.winfo_children():
                child.destroy()

            ctk.CTkButton(
                header, text="<", width=35,
                command=lambda: change_month(-1)
            ).grid(row=0, column=0)
            ctk.CTkLabel(
                header, text=f"{calendar.month_name[month_state[1]]} {month_state[0]}",
                width=170
            ).grid(row=0, column=1)
            ctk.CTkButton(
                header, text=">", width=35,
                command=lambda: change_month(1)
            ).grid(row=0, column=2)

            for column, weekday in enumerate(("Mo", "Tu", "We", "Th", "Fr", "Sa", "Su")):
                ctk.CTkLabel(calendar_grid, text=weekday, width=35).grid(
                    row=0, column=column, pady=(0, 4)
                )

            for row, week in enumerate(calendar.monthcalendar(*month_state), start=1):
                for column, day in enumerate(week):
                    if day:
                        ctk.CTkButton(
                            calendar_grid, text=str(day), width=35,
                            command=lambda day=day: select_date(day)
                        ).grid(row=row, column=column, padx=2, pady=2)

        def change_month(offset):
            month_state[1] += offset
            if month_state[1] == 0:
                month_state[1], month_state[0] = 12, month_state[0] - 1
            elif month_state[1] == 13:
                month_state[1], month_state[0] = 1, month_state[0] + 1
            draw_month()

        def select_date(day):
            self.selected_date = date(month_state[0], month_state[1], day)
            self.date_button.configure(text=self.selected_date.strftime("%d-%m-%Y"))
            self.calendar_window.destroy()
            self.calendar_window = None

        draw_month()

    def clear(self):
        self.selected_date = None
        self.date_button.configure(text="No deadline")

    def get(self):
        if self.selected_date is None:
            return None

        try:
            selected_time = datetime.strptime(
                self.time_entry.get().strip(), "%H:%M"
            ).time()
        except ValueError as exc:
            raise ValueError("Time must use HH:MM format.") from exc
        return datetime.combine(self.selected_date, selected_time)
