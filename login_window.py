import tkinter as tk
from tkinter import font
from tkinter import ttk
import os.path
from os.path import exists

import key


class LoginWindow:
    window = None
    login_label = None
    password_label = None
    confirm_password_label = None
    login = None
    password = None
    confirm_password = None
    main_button = None
    secondary_prompt = None
    secondary_button = None
    response = None
    result = False

    def __init__(self):
        self.window = tk.Tk()

        self.window.resizable(False, False)
        self.window.iconbitmap('images/icon.ico')

        window_width = 320
        window_height = 180

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
        self.window.columnconfigure(3, weight=1)
        self.window.columnconfigure(4, weight=0)

        self.window.rowconfigure(0, weight=0)
        self.window.rowconfigure(1, weight=1)
        self.window.rowconfigure(2, weight=1)
        self.window.rowconfigure(3, weight=1)
        self.window.rowconfigure(4, weight=0)
        self.window.rowconfigure(5, weight=1)
        self.window.rowconfigure(6, weight=1)
        self.window.rowconfigure(7, weight=1)
        self.window.rowconfigure(8, weight=0)

        ttk.Frame(self.window, width=30).grid(column=0, rowspan=7)
        ttk.Frame(self.window, width=0).grid(column=2, rowspan=7)
        ttk.Frame(self.window, width=30).grid(column=4, rowspan=7)

        ttk.Frame(self.window, height=30).grid(columnspan=5, row=0)
        ttk.Frame(self.window, height=0).grid(columnspan=5, row=4)
        ttk.Frame(self.window, height=30).grid(columnspan=5, row=8)

        myFont = tk.font.Font(size=10, family='Arial', weight='normal', slant='roman', underline=False)

        self.logging_in()
        self.window.mainloop()

    def registration(self):
        # REJESTRACJA
        self.window.title("Rejestracja: Bezpieczeństwo Systemów Komputerowych by 184474 & 184440")

        self.login_label = ttk.Label(self.window, text='Login:')
        self.login_label.grid(column=1, row=1)
        self.password_label = ttk.Label(self.window, text='Password:')
        self.password_label.grid(column=1, row=2)
        self.confirm_password_label = ttk.Label(self.window, text='Confirm password:')
        self.confirm_password_label.grid(column=1, row=3)

        self.login = ttk.Entry(self.window)
        self.login.grid(column=3, row=1)
        self.password = ttk.Entry(self.window)
        self.password.grid(column=3, row=2)
        self.confirm_password = ttk.Entry(self.window)
        self.confirm_password.grid(column=3, row=3)

        self.main_button = ttk.Button(self.window, text="Register", command=self.register_func)
        self.main_button.grid(column=1, columnspan=3, row=5)
        self.secondary_prompt = ttk.Label(self.window, text="If you want to use an existing key:")
        self.secondary_prompt.grid(column=1, columnspan=3, row=6, sticky='w')
        self.secondary_button = tk.Button(self.window, text="Login", command=self.switch_to_login, bd=0, fg='blue',
                                          font=tk.font.Font(size=10, slant='italic'))
        self.secondary_button.grid(column=1, columnspan=3, row=6, sticky='e')

        self.response = ttk.Label(self.window, text="")
        self.response.grid(columnspan=5, row=8)

    def logging_in(self):
        # LOGOWANIE
        self.window.title("Logowanie: Bezpieczeństwo Systemów Komputerowych by 184474 & 184440")

        self.login_label = ttk.Label(self.window, text='Login:')
        self.login_label.grid(column=1, row=1)
        self.password_label = ttk.Label(self.window, text='Password:')
        self.password_label.grid(column=1, row=2, rowspan=2)

        self.login = ttk.Entry(self.window)
        self.login.grid(column=3, row=1)
        self.password = ttk.Entry(self.window)
        self.password.grid(column=3, row=2, rowspan=2)

        self.main_button = ttk.Button(self.window, text="Login", command=self.login_func)
        self.main_button.grid(column=1, columnspan=3, row=5)
        self.secondary_prompt = ttk.Label(self.window, text="If you want to create a new key:")
        self.secondary_prompt.grid(column=1, columnspan=3, row=6, sticky='w')
        self.secondary_button = tk.Button(self.window, text="Register", command=self.switch_to_register, bd=0,
                                          fg='blue',
                                          font=tk.font.Font(size=10, slant='italic'))
        self.secondary_button.grid(column=1, columnspan=3, row=6, sticky='e')

        self.response = ttk.Label(self.window, text="")
        self.response.grid(columnspan=5, row=8)

    def register_func(self):
        if self.login.get() == "":
            self.response.config(text="You need to provide a login!")
            return
        if self.password.get() == "":
            self.response.config(text="You need to provide a password!")
            return
        if exists(f"{os.path.curdir}/public_keys/{self.login.get()}.pem") \
                or exists(f"{os.path.curdir}/private_keys/{self.login.get()}.pem"):
            self.response.config(text="There already exists a user with that login!")
            return
        if self.password.get() != self.confirm_password.get():
            self.response.config(text="You password and confiramtion need to match!")
            return
        if key.Key.set_keys(self.login.get(), self.password.get()):
            self.response.config(text="Registered!")
        else:
            self.response.config(text="There was an error while registering!")

    def login_func(self):
        if self.login.get() == "":
            self.response.config(text="You need to provide a login!")
            return
        if self.password.get() == "":
            self.response.config(text="You need to provide a password!")
            return
        if not exists(f"{os.path.curdir}/public_keys/{self.login.get()}.pem") \
                or not exists(f"{os.path.curdir}/private_keys/{self.login.get()}.pem"):
            self.response.config(text="There is no user with that login!")
            return

        if key.Key.check_password(self.login.get(), self.password.get()):
            self.window.destroy()
            self.result = True
        else:
            self.response.config(text="Wrong password!")

    def switch_to_login(self):
        self.window.title("Logowanie: Bezpieczeństwo Systemów Komputerowych by 184474 & 184440")
        self.confirm_password_label.destroy()
        self.confirm_password.destroy()
        self.password_label.grid(column=1, row=2, rowspan=2)
        self.password.grid(column=3, row=2, rowspan=2)
        self.main_button.config(text="Login", command=self.login_func)
        self.secondary_prompt.config(text="If you want to create a new key:")
        self.secondary_button.config(text="Register", command=self.switch_to_register)
        self.response.config(text="")

    def switch_to_register(self):
        self.window.title("Rejestracja: Bezpieczeństwo Systemów Komputerowych by 184474 & 184440")
        self.password_label.grid(column=1, row=2, rowspan=1)
        self.password.grid(column=3, row=2, rowspan=1)
        self.confirm_password_label = ttk.Label(self.window, text='Confirm password:')
        self.confirm_password_label.grid(column=1, row=3)
        self.confirm_password = ttk.Entry(self.window)
        self.confirm_password.grid(column=3, row=3)
        self.main_button.config(text="Register", command=self.register_func)
        self.secondary_prompt.config(text="If you want to use an existing key:")
        self.secondary_button.config(text="Login", command=self.switch_to_login)
        self.response.config(text="")
