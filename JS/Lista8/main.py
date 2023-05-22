import zad2
import tkinter as tk
from tkinter import filedialog
import datetime
from tkinter.constants import BOTH, DISABLED, END, FIRST, INSERT, LEFT, NORMAL, RIGHT, SINGLE, UNITS, Y

WIDTH = 750
HEIGHT = 500
PADDING = 15

def read_file(filename):
    lines = ""

    with open(f"{filename}") as f:
        lines = f.readlines()

    return lines

def filter_file_output(from_date, to_date, file_output):
    result = []

    if from_date and to_date:
        for line in file_output:
                time = datetime.datetime.strptime('-'.join(line.split()[:3]), "%b-%d-%H:%M:%S")
                given_from_date = datetime.datetime.strptime('-'.join(line.split()[:2]+[from_date]), "%b-%d-%H:%M")
                given_to_date = datetime.datetime.strptime('-'.join(line.split()[:2]+[to_date]), "%b-%d-%H:%M")
                if time >= given_from_date and time <= given_to_date:
                    result.append(line)
    else:
        for line in file_output:
            result.append(line)

    return result

def detail_raw_log(raw_log):

    dict_log = zad2.raw_log_to_dict(raw_log)

    if not dict_log:
        return None, None, None

    ip = zad2.get_ipv4s_from_log(dict_log)
    
    if ip:
        ip = ip[0]
    
    user = zad2.get_user_from_log(dict_log)

    message = zad2.get_message_type(dict_log)

    return ip, user, message


class GUI():
    def __init__(self) -> None:
       self.root = tk.Tk()
       self.root.title("Log browser")
       self.root.columnconfigure(0, weight=4)
       self.root.columnconfigure(1, weight=1)

       self.file_bar = tk.Frame(self.root)
       self.nav_bar = tk.Frame(self.root)
       self.main = tk.Frame(self.root)
       self.main_left = tk.Frame(self.main)
       self.main_right = tk.Frame(self.main)
       self.logs = tk.Frame(self.main_left)

       self.filename = tk.StringVar(self.file_bar)
       self.open_button = tk.Button(self.file_bar)
       self.from_date = tk.StringVar(self.main_left)
       self.to_date = tk.StringVar(self.main_left)
       self.prev_button = tk.Button(self.nav_bar)
       self.next_button = tk.Button(self.nav_bar)
       self.refresh_button = tk.Button(self.main_left)
       self.logs_list = tk.Listbox(self.logs) # master

       self.raw_log = tk.StringVar()
       self.raw_logs = []

       self.nav_bar_config()
       self.file_bar_config()
       self.main_config()

       self.file_bar.grid(column=0, row=0)
       self.main.grid(column=0, row=1)
       self.nav_bar.grid(column=0, row=2)

       self.root.mainloop()

    def file_bar_config(self):
        self.file_bar.columnconfigure(0, minsize=WIDTH)

        def select_file():
            filetypes = (
                ('all files', '*.*'),
                ('text files', '*.txt')
            )

            filename_temp = filedialog.askopenfilename(
                title='Open a file',
                initialdir='.',
                filetypes=filetypes)
            
            self.filename.set(filename_temp)

            self.print_logs('y')

            if self.logs_list.size() != 0:
                self.logs_list.selection_set(0)
                self.raw_log.set(self.raw_logs[0]) # pyright: ignore
                self.prev_button.config(state=NORMAL)
                self.next_button.config(state=NORMAL)
                self.refresh_button.config(state=NORMAL)
            else:
                self.raw_log.set("")
            
            self.update_detail()

        self.open_button.config(
            text='Open',
            command=select_file
        )

        file_label = tk.Label(self.file_bar,
                              textvariable=self.filename,
                              width=80,
                              relief=tk.SUNKEN,
                              anchor=tk.W)

        file_label.grid(column=0, row=0, sticky=tk.W)
        self.open_button.grid(column=1, row=0, sticky=tk.E)

        for elem in self.file_bar.winfo_children():
            elem.grid(padx=PADDING, pady=PADDING)

    def nav_bar_config(self):

        self.nav_bar.columnconfigure(0, minsize=WIDTH)

        def forward():
            self.prev_button.config(state=NORMAL)
            new_index = self.logs_list.curselection()[0] + 1
            self.logs_list.selection_clear(0,END)
            self.logs_list.selection_set(new_index) # pyright: ignore
            self.raw_log.set(self.raw_logs[new_index]) # pyright: ignore
            if self.logs_list.curselection()[0] == self.logs_list.size() - 1:
                self.next_button.config(state=DISABLED)

            self.update_detail()

            # logs_list.yview_scroll(1, UNITS)

        def back():
            self.next_button.config(state=NORMAL)
            new_index = self.logs_list.curselection()[0] - 1
            self.logs_list.selection_clear(0,END)
            self.logs_list.selection_set(new_index) # pyright: ignore
            self.raw_log.set(self.raw_logs[new_index]) # pyright: ignore
            if self.logs_list.curselection()[0] == 0:
                self.prev_button.config(state=DISABLED)

            self.update_detail()

            # logs_list.yview_scroll(-1, UNITS)

        self.prev_button.config(
            text='Previous',
            command=back,
            state=DISABLED
        )

        self.next_button.config(
            text='Next',
            command=forward,
            state=DISABLED
        )

        self.prev_button.grid(column=0, row=0, sticky=tk.W)
        self.next_button.grid(column=1, row=0, sticky=tk.E)

        for elem in self.nav_bar.winfo_children():
            elem.grid(padx=PADDING, pady=PADDING)

    def main_config(self):
        self.main.columnconfigure(0, minsize=WIDTH/2)

        self.main.columnconfigure(1, minsize=WIDTH/2)

        from_label = tk.Label(master=self.main_left, text="From")
        from_sunken_label = tk.Entry(textvariable=self.from_date,
                                     master=self.main_left,
                                     width=20,
                                     relief=tk.SUNKEN)

        to_label = tk.Label(master=self.main_left, text="To")
        to_sunken_label = tk.Entry(textvariable=self.to_date,
                                   master=self.main_left,
                                   width=20,
                                   relief=tk.SUNKEN)


        scrollbar = tk.Scrollbar(self.logs)
        scrollbar.pack(side=RIGHT, fill=Y)

        self.logs_list.config(yscrollcommand=scrollbar.set,
                         width=60,
                         selectmode=SINGLE)
        
        self.logs_list.pack(side=LEFT, fill=BOTH)
        scrollbar.config(command=self.logs_list.yview)

        def refresh():
            self.print_logs('y')
            if self.logs_list.size() != 0:
                self.logs_list.selection_set(0)
                self.raw_log.set(self.raw_logs[0]) # pyright: ignore
                self.prev_button.config(state=NORMAL)
                self.next_button.config(state=NORMAL)
            else:
                self.raw_log.set("")
                self.prev_button.config(state=DISABLED)
                self.next_button.config(state=DISABLED)
            
            self.update_detail()


        self.refresh_button.config(text='Refresh',
                              command=refresh,
                              state=DISABLED)

        from_label.grid(column=0, row=0, sticky=tk.W)
        from_sunken_label.grid(column=1, row=0, sticky=tk.W)
        to_label.grid(column=2, row=0, sticky=tk.W)
        to_sunken_label.grid(column=3, row=0, sticky=tk.W)
        
        self.refresh_button.grid(column=4, row=0, sticky=tk.W)
        
        def CurSelection(event):
            if self.logs_list.get(0) and self.logs_list.curselection():
                self.raw_log.set(self.raw_logs[self.logs_list.curselection()[0]])
                if self.logs_list.curselection()[0] == 0:
                    self.prev_button.config(state=DISABLED)
                if self.logs_list.curselection()[0] == self.logs_list.size() - 1:
                    self.next_button.config(state=DISABLED)
                # self.raw_log.set(self.logs_list.get(self.logs_list.curselection()))
                self.update_detail()
            
        self.logs_list.bind('<<ListboxSelect>>',CurSelection)
        self.main_left.grid(column=0, row=0)
        self.main_right.grid(column=1, row=0)

        for elem in self.main_left.winfo_children():
            elem.grid(padx=5, pady=5)

        for elem in self.main_right.winfo_children():
            elem.grid(padx=5, pady=5)

        for elem in self.main.winfo_children():
            elem.grid(padx=PADDING, pady=PADDING)

        self.logs.grid(column=0, row=1, columnspan=5)

    def print_logs(self, filter = 'y'):
        lines = read_file(self.filename.get())
        self.raw_logs = lines

        if filter == 'y':
            lines = filter_file_output(self.from_date.get(), self.to_date.get(), lines)
            self.raw_logs = lines

        if self.logs_list.get(0):
            self.logs_list.delete(0, END)

        LENGTH = 65

        for line in lines:
            self.logs_list.insert(END, line.rstrip() if len(line.rstrip()) < LENGTH else line.rstrip()[:LENGTH+1]+'...')

        self.logs_list.selection_clear(0, END)
        if self.logs_list.curselection():
            self.logs_list.selection_set(0)
            self.raw_log.set(self.raw_logs[self.logs_list.curselection()[0]])

    def update_detail(self):
        ip, user, message_type = detail_raw_log(self.raw_log.get())
        ip_var, user_var, message_type_var = tk.StringVar(), tk.StringVar(), tk.StringVar()

        for widget in self.main_right.winfo_children():
            widget.destroy()

        index = 0

        if ip:
            ip_var.set(ip) # pyright: ignore
            ip_label = tk.Label(master=self.main_right, text="IP")
            ip_label_sunken = tk.Label(master=self.main_right,
                                   textvariable=ip_var,
                                   width=30,
                                   relief=tk.SUNKEN,
                                   anchor=tk.W)
            ip_label.grid(column=0, row=index)
            ip_label_sunken.grid(column=1, row=index)
            index += 1
        if user:
            user_var.set(user)
            user_label = tk.Label(master=self.main_right, text="User")
            user_label_sunken = tk.Label(master=self.main_right,
                                       textvariable=user_var,
                                       width=30,
                                       relief=tk.SUNKEN,
                                       anchor=tk.W)
            user_label.grid(column=0, row=index)
            user_label_sunken.grid(column=1, row=index)
            index += 1
        if message_type:
            message_type_var.set(message_type)
            message_type_label = tk.Label(master=self.main_right, text="Message")
            message_type_label_sunken = tk.Label(master=self.main_right,
                                       textvariable=message_type_var,
                                       width=30,
                                       relief=tk.SUNKEN,
                                       anchor=tk.W)
            message_type_label.grid(column=0, row=index)
            message_type_label_sunken.grid(column=1, row=index)


    def return_root(self):
        return self.root


if __name__ == "__main__":

    gui = GUI()
