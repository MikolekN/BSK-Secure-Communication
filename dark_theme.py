from tkinter import ttk

dark_theme = {
    ".": {
        "configure": {
            "background": "#2d2d2d",  # Dark grey background
            "foreground": "white",  # White text
        }
    },
    "TLabel": {
        "configure": {
            "foreground": "white",  # White text
        }
    },
    "TButton": {
        "configure": {
            "background": "#3c3f41",  # Dark blue-grey button
            "foreground": "white",  # White text
        }
    },
    "TEntry": {
        "configure": {
            "background": "#2d2d2d",  # Dark grey background
            "foreground": "white",  # White text
            "fieldbackground": "#4d4d4d",
            "insertcolor": "white",
            "bordercolor": "black",
            "lightcolor": "#4d4d4d",
            "darkcolor": "black",
        }
    },
}


def make_dark_theme(window):
    style = ttk.Style()
    style.theme_create('dark', parent="clam", settings=dark_theme)
    style.theme_use('dark')
    window.configure(bg='#2d2d2d')
