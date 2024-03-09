from tkinter import *
import datetime
from astro import get_lunar_day

class MainWindow:
    def __init__(self, window):
        self.today = datetime.date.today()
        self.selected_year = datetime.date.today().year
        self.selected_month = datetime.date.today().month
        self.window = window
        
        self.rows = 7
        self.columns = 7
        self.init_cell_width = 3
        self.init_cell_height = 2
        self.background_color = "#CCC"
        
        self.create_month_selector()
        self.create_calendar()

    def select_next_month(self):
        self.selected_month += 1
        if self.selected_month > 12:
            print(self.selected_month)
            self.selected_year += 1
            self.selected_month = 1
        self.update_calendar()

    def select_prev_month(self):
        self.selected_month -= 1
        if self.selected_month < 1:
            print(self.selected_month)
            self.selected_year -= 1
            self.selected_month = 12
        self.update_calendar()

    def update_calendar(self):
        self.month_label.config(text=self.get_selected_month_name())
        self.year_label.config(text=self.selected_year)
        self.frame2_calendar.destroy()
        self.create_calendar()

    def create_month_selector(self):
        self.frame1_selector = Frame(self.window)
        self.frame1_selector.pack(side=TOP, fill=X)
        selector = Frame(self.frame1_selector, height=self.init_cell_height)

        self.year_label = Label(selector, text=self.selected_year)
        self.year_label.grid(row=0, column=10)

        arrow1 = Label(selector, text="<")
        arrow2 = Label(selector, text=">")
        arrow1.bind("<Button-1>", lambda e: self.select_prev_month())
        arrow2.bind("<Button-1>", lambda e: self.select_next_month())
        self.month_label = Label(selector, text=self.get_selected_month_name())
        arrow1.grid(row=0, column=0)
        self.month_label.grid(row=0, column=1)
        arrow2.grid(row=0, column=2)
        selector.pack(side=TOP, fill=X)

    def get_selected_month_name(self):
        months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
        return months[self.selected_month - 1]

    def create_weekday_labels(self):
        days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
        for i, day in enumerate(days):
            Label(self.frame2_calendar, text=day, borderwidth=0).grid(row=0, column=i)

    def update_cell(self, row, column, content1:str, content2:str, color1="black", color2="blue", today=False):
        cell = Frame(self.frame2_calendar, width=self.init_cell_width, height=self.init_cell_height)
        label1 = Label(cell, text=content1, fg=color1)
        label2 = Label(cell, text=content2, fg=color2)
        label1.pack(side=TOP)
        label2.pack(side=TOP)
        cell.grid(row=row, column=column)
        if today:
            cell.config(background=self.background_color)
            label1.config(background=self.background_color)
            label2.config(background=self.background_color)
        # cell.bind("<Enter>", lambda e: cell.config(fg="red")) # Highlight cell on hover
        # cell.bind("<Leave>", lambda e: cell.config(fg=color1)) # Unhighlight cell when mouse leaves
        # cell.bind("<Double-1>", lambda e: print(f"Cell {row},{column} was double-clicked.")) # Print message on double-click
    
    def create_days_labels(self):
        start_date = datetime.date(self.selected_year, self.selected_month, 1)
        x = 1
        y = start_date.weekday()
        for _ in range(31):
            if start_date.month!=self.selected_month:
                continue
            lunar_day = get_lunar_day(start_date.year, start_date.month, start_date.day)
            regular_day = start_date.day
            self.update_cell(x, y, str(regular_day), str(lunar_day), 
                             today= (start_date.day==self.today.day) and (start_date.month==self.today.month))
            start_date += datetime.timedelta(days=1)
            y += 1
            if y >= self.columns:
                y = 0
                x += 1

    def create_calendar(self):
        self.frame2_calendar = Frame(self.window)
        self.frame2_calendar.pack(side=TOP, fill=BOTH, expand=True)
        self.create_weekday_labels()
        self.create_days_labels()

if __name__ == "__main__":
    window = Tk()
    window.title("Colorful Grid")
    main_window = MainWindow(window)
    window.mainloop()