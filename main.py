from login_window import LoginWindow
from connection_window import ConnectionWindow

log = LoginWindow()
if log.result:
    con = ConnectionWindow()
