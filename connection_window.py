import threading
import time
import tkinter as tk
from tkinter import font
from tkinter import filedialog
from tkinter import ttk
import dark_theme
from constants import DARK_MODE

"""
connection_window.py
"""


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
    progress_bar = None

    client = None
    receive_thread = None

    def __init__(self, client):
        self.client = client

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
        self.window.rowconfigure(4, weight=1)
        self.window.rowconfigure(5, weight=0)
        self.window.rowconfigure(6, weight=1)
        self.window.rowconfigure(7, weight=1)
        self.window.rowconfigure(8, weight=1)
        self.window.rowconfigure(9, weight=0)

        ttk.Frame(self.window, width=5).grid(column=0, rowspan=9)
        ttk.Frame(self.window, width=5).grid(column=4, rowspan=9)

        ttk.Frame(self.window, height=5).grid(columnspan=5, row=0)
        ttk.Frame(self.window, height=5).grid(columnspan=5, row=2)
        ttk.Frame(self.window, height=5).grid(columnspan=5, row=5)
        ttk.Frame(self.window, height=5).grid(columnspan=5, row=9)

        myFont = tk.font.Font(size=10, family='Arial', weight='normal', slant='roman', underline=False)

        self.layout()
        if DARK_MODE:
            dark_theme.make_dark_theme(self.window)
        self.receive_thread = threading.Thread(target=self.receive_messages)
        self.receive_thread.start()
        self.window.mainloop()

    def layout(self):
        self.log_space = tk.LabelFrame(self.window, width=350, height=500)
        if DARK_MODE:
            self.log_space.config(bg='#2d2d2d')
        self.log_space.grid(column=1, columnspan=3, row=1)
        self.log_space.grid_propagate(False)
        self.update_logs()
        self.input_space = ttk.Entry(self.window, width=40)
        self.input_space.grid(column=1, row=3)
        if DARK_MODE:
            self.message_pic = tk.PhotoImage(file='images/arrowright15_dark.gif')
        else:
            self.message_pic = tk.PhotoImage(file='images/arrowright15.gif')
        self.send_message_button = ttk.Button(self.window, image=self.message_pic, command=self.send_message)
        self.send_message_button.grid(column=2, row=3, sticky='e')
        if DARK_MODE:
            self.file_pic = tk.PhotoImage(file='images/file15_dark.gif')
        else:
            self.file_pic = tk.PhotoImage(file='images/file15.gif')
        self.send_file_button = ttk.Button(self.window, image=self.file_pic, command=self.send_file)
        self.send_file_button.grid(column=3, row=3, sticky='e')
        self.progress_bar = ttk.Progressbar(self.window, orient='horizontal', mode='determinate', length=350)
        self.progress_bar.grid(column=1, columnspan=3, row=4)
        self.connection_status_label = ttk.Label(self.window, text="Connection status:")
        self.connection_status_label.grid(column=1, row=6)
        self.connected_label = ttk.Label(self.window, text="disconnected")
        self.connected_label.grid(column=1, row=7)
        self.address_label = ttk.Label(self.window, text="")
        self.address_label.grid(column=1, row=8)
        self.connect_button = ttk.Button(self.window, text="Connect", command=self.connect)
        self.connect_button.grid(column=2, columnspan=2, row=6, rowspan=3, sticky='e')

    def update_logs(self):
        for i in range(len(self.messages)):
            self.log_space.rowconfigure(i, weight=1)
            if DARK_MODE:
                tk.Label(self.log_space, text=self.messages[i], height=30, bg='#2d2d2d', fg='white').grid(row=i)
            else:
                tk.Label(self.log_space, text=self.messages[i], height=30).grid(row=i)

    def send_message(self):
        message = self.input_space.get()
        self.messages.append(message)
        self.update_logs()
        self.client.send_message(message)
        self.input_space.delete(0, len(self.input_space.get()))

    def send_file(self):
        self.file_path = filedialog.askopenfilename(initialdir="/", title="Select a File",
                                                    filetypes=(("Text files", "*.txt*"), ("all files", "*.*")))
        # self.client.send_file(message)

    def receive_messages(self):
        while True:
            time.sleep(1)
            while len(self.client.messages) > 0:
                message = self.client.messages.pop(0)
                self.messages.append(message)
                self.update_logs()

    def connect(self):
        self.connected_label.config(text="Awaiting connection...")
        if self.client.connect():
            self.connected_label.config(text="connected")
            self.address_label.config(text="192.168.0.0:1234")
            self.connect_button.config(text="Disconnect", command=self.disconnect)
        else:
            self.connected_label.config(text="disconnected")

    def disconnect(self):
        self.client.disconnect()
        self.connected_label.config(text="disconnected")
        self.address_label.config(text="")
        self.connect_button.config(text="Connect", command=self.connect)

    def close_connection(self):
        # code for disconnecting, etc.
        self.window.destroy()

