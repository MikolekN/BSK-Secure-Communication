from login_window import LoginWindow
from connection_window import ConnectionWindow
from client import Client

"""
main.py
"""


def make_client():
    log = LoginWindow()
    if log.result:
        if log.login is not None and log.password is not None:
            client = Client(log.login, log.password)
            ConnectionWindow(client)


make_client()
