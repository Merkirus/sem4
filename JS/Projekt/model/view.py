import tkinter as tk
import datetime
from tkcalendar import Calendar
from tkinter.constants import BOTH, DISABLED, END, FIRST, INSERT, LEFT, NORMAL, RIGHT, SINGLE, UNITS, Y
import json

WIDTH = 750
HEIGHT = 300
PADDING = 15

class GUI():
    def __init__(self) -> None:
       self.root = tk.Tk()
       self.root.title("Weather app")
       self.root.geometry(f"{WIDTH}x{HEIGHT}")
       self.root.columnconfigure(0, minsize=WIDTH/2)
       self.root.columnconfigure(1, minsize=WIDTH/2)

       self.main_left = tk.Frame(self.root)
       self.main_right = tk.Frame(self.root)

       self.icon = tk.StringVar(self.main_right)
       self.temp_max = tk.StringVar(self.main_right)
       self.temp_min = tk.StringVar(self.main_right)
       self.precip = tk.StringVar(self.main_right)
       self.temp_avg = tk.StringVar(self.main_right)
       self.location = tk.StringVar(self.main_left)
       self.refresh_button = tk.Button(self.main_left)
       self.city = tk.StringVar(self.main_right)
       self.error = tk.StringVar(self.main_right)

       d, m, y = [int(x) for x in datetime.datetime.today().strftime("%d-%m-%Y").split('-')]
       self.cal = Calendar(master=self.main_left, selectmode='day', year=y, month=m, day=d, date_pattern='y-mm-dd')

       self.main_config()

    def main_config(self):

        location_label = tk.Label(master=self.main_left, text="City")
        location = tk.Entry(textvariable=self.city,
                                     master=self.main_left,
                                     width=20,
                                     relief=tk.SUNKEN)

        self.refresh_button.config(text='Check', state=DISABLED)

        location_label.grid(column=0, row=0, sticky=tk.W)
        location.grid(column=1, row=0, sticky=tk.W)
        self.cal.grid(column=0, row=1, columnspan=3)

        self.refresh_button.grid(column=2, row=0, sticky=tk.W)
        
        self.main_left.grid(column=0, row=0)
        self.main_right.grid(column=1, row=0)

        for elem in self.main_left.winfo_children():
            elem.grid(padx=5, pady=5)

        for elem in self.main_right.winfo_children():
            elem.grid(padx=5, pady=5)

        for elem in self.root.winfo_children():
            elem.grid(padx=PADDING, pady=PADDING)

    def update_detail(self):
        for widget in self.main_right.winfo_children():
            widget.destroy()

        index = 0

        if self.error.get() != "":
            ip_label = tk.Label(master=self.main_right, text="ERROR")
            ip_label_sunken = tk.Label(master=self.main_right,
                                   textvariable=self.error,
                                   width=30,
                                   relief=tk.SUNKEN,
                                   anchor=tk.W)
            ip_label.grid(column=0, row=index)
            ip_label_sunken.grid(column=1, row=index)
            index += 1
            return
        if self.icon.get() != "":
            ip_label = tk.Label(master=self.main_right, text="Icon")
            ip_label_sunken = tk.Label(master=self.main_right,
                                   textvariable=self.icon,
                                   width=30,
                                   relief=tk.SUNKEN,
                                   anchor=tk.W)
            ip_label.grid(column=0, row=index)
            ip_label_sunken.grid(column=1, row=index)
            index += 1
        if self.temp_max.get() != "":
            user_label = tk.Label(master=self.main_right, text="Temp Max")
            user_label_sunken = tk.Label(master=self.main_right,
                                       textvariable=self.temp_max,
                                       width=30,
                                       relief=tk.SUNKEN,
                                       anchor=tk.W)
            user_label.grid(column=0, row=index)
            user_label_sunken.grid(column=1, row=index)
            index += 1
        if self.temp_min.get() != "":
            message_type_label = tk.Label(master=self.main_right, text="Temp Min")
            message_type_label_sunken = tk.Label(master=self.main_right,
                                       textvariable=self.temp_min,
                                       width=30,
                                       relief=tk.SUNKEN,
                                       anchor=tk.W)
            message_type_label.grid(column=0, row=index)
            message_type_label_sunken.grid(column=1, row=index)
            index += 1
        if self.precip.get() != "":
            message_type_label = tk.Label(master=self.main_right, text="Precipitation")
            message_type_label_sunken = tk.Label(master=self.main_right,
                                       textvariable=self.precip,
                                       width=30,
                                       relief=tk.SUNKEN,
                                       anchor=tk.W)
            message_type_label.grid(column=0, row=index)
            message_type_label_sunken.grid(column=1, row=index)
            index += 1
        if self.temp_avg.get() != "":
            message_type_label = tk.Label(master=self.main_right, text="Temp Avg")
            message_type_label_sunken = tk.Label(master=self.main_right,
                                       textvariable=self.temp_avg,
                                       width=30,
                                       relief=tk.SUNKEN,
                                       anchor=tk.W)
            message_type_label.grid(column=0, row=index)
            message_type_label_sunken.grid(column=1, row=index)

    def update(self, weather_data):
        self.error.set("")
        try:
            weather_data = json.loads(weather_data)
            self.icon.set(weather_data['daily']['weathercode'][0])
            self.temp_max.set(weather_data['daily']['temperature_2m_max'][0])
            self.temp_min.set(weather_data['daily']['temperature_2m_min'][0])
            self.precip.set(weather_data['daily']['precipitation_sum'][0])
            self.temp_avg.set(weather_data['daily']['temperature_2m_avg'][0])
        except:
            self.error.set(weather_data)

        self.update_detail()

    def get_city_date(self):
        self.error.set("")
        if self.city.get() == "":
            self.error.set("City not set")
            self.update_detail()
            return
        if self.cal.get_date() == "":
            self.error.set("Date not set")
            self.update_detail()
            return

        return self.city.get(), self.cal.get_date()

    def set_listener(self, fun):
        self.refresh_button.config(state=NORMAL, command=fun)

    def return_root(self):
        return self.root

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":

    gui = GUI()
