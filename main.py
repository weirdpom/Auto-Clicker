
import tkinter as tk
from tkinter import messagebox
import pyautogui
import keyboard
import threading
import time
import os
import sys

# -----------------------------
# RESOURCE PATH (PYINSTALLER)
# -----------------------------

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.dirname(os.path.abspath(__file__))

    return os.path.join(base_path, relative_path)


# -----------------------------
# VARIABLES
# -----------------------------

clicking = threading.Event()
shutdown = threading.Event()

click_speed = 1 / 5  # Default: 5 clicks per second
clicks_per_second = 5

closing = False


# -----------------------------
# CLICKING FUNCTIONS
# -----------------------------

def click_worker():
    while not shutdown.is_set():

        if clicking.is_set():
            pyautogui.click()
            time.sleep(click_speed)

        else:
            time.sleep(0.01)


def start_clicking():
    if closing:
        return

    clicking.set()
    update_status()


def stop_clicking():
    clicking.clear()
    update_status()


# -----------------------------
# SETTINGS
# -----------------------------

def open_settings():
    settings = tk.Toplevel(root)
    settings.title("Settings")
    settings.geometry("300x220")
    settings.resizable(False, False)

    settings.iconbitmap(icon_path)

    tk.Label(
        settings,
        text="Settings",
        font=("Arial", 16, "bold")
    ).pack(pady=12)

    tk.Label(
        settings,
        text="Clicks per second (1-100)",
        font=("Arial", 10)
    ).pack(pady=5)

    cps_var = tk.IntVar(value=clicks_per_second)

    cps_slider = tk.Scale(
        settings,
        from_=1,
        to=100,
        orient="horizontal",
        variable=cps_var,
        length=230
    )
    cps_slider.pack()

    cps_label = tk.Label(
        settings,
        text=f"Current CPS: {clicks_per_second}"
    )
    cps_label.pack(pady=5)

    def update_cps(value):
        global click_speed, clicks_per_second

        clicks_per_second = int(float(value))
        click_speed = 1 / clicks_per_second

        cps_label.config(
            text=f"Current CPS: {clicks_per_second}"
        )

    cps_slider.config(command=update_cps)


# -----------------------------
# GUI STATUS
# -----------------------------

def update_status():
    if closing:
        return

    try:
        root.after(0, update_status_gui)
    except RuntimeError:
        pass


def update_status_gui():
    if closing:
        return

    if clicking.is_set():
        status_label.config(text="Status: RUNNING", fg="green")
    else:
        status_label.config(text="Status: STOPPED", fg="red")


# -----------------------------
# KEYBOARD SHORTCUTS
# -----------------------------

keyboard.add_hotkey("F5", start_clicking)
keyboard.add_hotkey("F6", stop_clicking)


# -----------------------------
# GUI WINDOW
# -----------------------------

root = tk.Tk()

# Application icon (PyInstaller compatible)
icon_path = resource_path("mouse.ico")

root.iconbitmap(icon_path)

root.title("Auto Clicker")
root.geometry("350x250")
root.minsize(300, 220)

# Top menu
menubar = tk.Menu(root)

settings_menu = tk.Menu(menubar, tearoff=0)
settings_menu.add_command(
    label="Click Speed (CPS)",
    command=open_settings
)

menubar.add_cascade(
    label="Settings",
    menu=settings_menu
)

root.config(menu=menubar)


# Main title
title_label = tk.Label(
    root,
    text="Auto Clicker",
    font=("Arial", 18, "bold")
)
title_label.pack(pady=15)

# Status
status_label = tk.Label(
    root,
    text="Status: STOPPED",
    font=("Arial", 11, "bold"),
    fg="red"
)
status_label.pack(pady=5)

# Current speed
speed_label = tk.Label(
    root,
    text="Speed: 5 CPS",
    font=("Arial", 10)
)
speed_label.pack(pady=3)


# Button container
button_frame = tk.Frame(root)
button_frame.pack(pady=15)

# START button
start_button = tk.Button(
    button_frame,
    text="START (F5)",
    width=12,
    height=2,
    command=start_clicking
)
start_button.pack(side="left", padx=8)

# STOP button
stop_button = tk.Button(
    button_frame,
    text="STOP (F6)",
    width=12,
    height=2,
    command=stop_clicking
)
stop_button.pack(side="left", padx=8)


# -----------------------------
# UPDATE SPEED LABEL
# -----------------------------

def refresh_speed_label():
    if not closing:
        speed_label.config(
            text=f"Speed: {clicks_per_second} CPS"
        )
        root.after(100, refresh_speed_label)


refresh_speed_label()


# -----------------------------
# BACKGROUND CLICKER
# -----------------------------

click_thread = threading.Thread(
    target=click_worker,
    daemon=True
)

click_thread.start()


# -----------------------------
# CLOSE APPLICATION
# -----------------------------

def close_application():
    global closing

    closing = True

    clicking.clear()
    shutdown.set()

    keyboard.unhook_all_hotkeys()

    root.destroy()


root.protocol("WM_DELETE_WINDOW", close_application)


# -----------------------------
# RUN APPLICATION
# -----------------------------

root.mainloop()
