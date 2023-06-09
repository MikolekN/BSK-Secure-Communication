import time
import tkinter as tk
from tkinter import font
from tkinter import filedialog
from tkinter import ttk


class ConnectionWindow:
    window = None
    log_space = None
    input_space = None
    send_message_button = None
    send_file_button = None
    connection_status_label = None
    connected_label = None
    address_label = None
    connect_button = None
    messages = ["Hallo1", "Hallo2", "Hallo3"]
    message_pic = None
    file_pic = None
    file_path = None

    def close_connection(self):
        # code for disconnecting, etc.
        self.window.destroy()

    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Wysyłanie: Bezpieczeństwo Systemów Komputerowych by 184474 & 184440")

        self.window.protocol("WM_DELETE_WINDOW", self.close_connection)
        self.window.resizable(False, False)
        self.window.iconbitmap('images/icon.ico')

        window_width = 360
        window_height = 640

        # get the screen dimension
        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()

        # find the center point
        center_x = int(screen_width / 2 - window_width / 2)
        center_y = int(screen_height / 2 - window_height / 2)
        self.window.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')

        self.window.columnconfigure(0, weight=0)
        self.window.columnconfigure(1, weight=1)
        self.window.columnconfigure(2, weight=0)
        self.window.columnconfigure(3, weight=0)
        self.window.columnconfigure(4, weight=0)

        self.window.rowconfigure(0, weight=0)
        self.window.rowconfigure(1, weight=2)
        self.window.rowconfigure(2, weight=0)
        self.window.rowconfigure(3, weight=1)
        self.window.rowconfigure(4, weight=0)
        self.window.rowconfigure(5, weight=1)
        self.window.rowconfigure(6, weight=1)
        self.window.rowconfigure(7, weight=1)
        self.window.rowconfigure(8, weight=0)

        ttk.Frame(self.window, width=5).grid(column=0, rowspan=9)
        ttk.Frame(self.window, width=5).grid(column=4, rowspan=9)

        ttk.Frame(self.window, height=5).grid(columnspan=5, row=0)
        ttk.Frame(self.window, height=5).grid(columnspan=5, row=2)
        ttk.Frame(self.window, height=5).grid(columnspan=5, row=4)
        ttk.Frame(self.window, height=5).grid(columnspan=5, row=8)

        myFont = tk.font.Font(size=10, family='Arial', weight='normal', slant='roman', underline=False)

        self.layout()
        self.window.mainloop()

    def update_logs(self):
        if self.log_space:
            self.log_space.destroy()
        self.log_space = tk.LabelFrame(self.window, width=350, height=500)
        self.log_space.grid(column=1, columnspan=3, row=1)
        self.log_space.grid_propagate(False)
        for i in range(len(self.messages)):
            self.log_space.rowconfigure(i, weight=1)
            tk.Label(self.log_space, text=self.messages[i], height=30).grid(row=i)

    def send_message(self):
        self.messages.append(self.input_space.get())
        self.update_logs()
        # code for sending the message
        self.input_space.delete(0, len(self.input_space.get()))

    def send_file(self):
        self.file_path = filedialog.askopenfilename(initialdir="/",
                                              title="Select a File",
                                              filetypes=(("Text files",
                                                          "*.txt*"),
                                                         ("all files",
                                                          "*.*")))
        # code for sending a file

    def connect(self):
        self.connected_label.config(text="Awaiting connection...")
        # code for connecting to server
        self.connected_label.config(text="Connected.")
        self.address_label.config(text="192.168.0.0:1234")

    def layout(self):
        self.update_logs()
        self.input_space = ttk.Entry(self.window, width=40)
        self.input_space.grid(column=1, row=3)
        self.message_pic = tk.PhotoImage(file='images/arrowright15.gif')
        self.send_message_button = ttk.Button(self.window, image=self.message_pic, command=self.send_message)
        self.send_message_button.grid(column=2, row=3, sticky='e')
        self.file_pic = tk.PhotoImage(file='images/file15.gif')
        self.send_file_button = ttk.Button(self.window, image=self.file_pic, command=self.send_file)
        self.send_file_button.grid(column=3, row=3, sticky='e')
        self.connection_status_label = tk.Label(self.window, text="Connection status:")
        self.connection_status_label.grid(column=1, row=5)
        self.connected_label = ttk.Label(self.window, text="disconnected")
        self.connected_label.grid(column=1, row=6)
        self.address_label = ttk.Label(self.window, text="")
        self.address_label.grid(column=1, row=7)
        self.connect_button = ttk.Button(self.window, text="Connect", command=self.connect)
        self.connect_button.grid(column=2, columnspan=2, row=5, rowspan=3, sticky='e')