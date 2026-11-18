
import tkinter as tk
import pyautogui
import keyboard
import threading
import time

# -----------------------------
# VARIABLES
# -----------------------------

clicking = threading.Event()
shutdown = threading.Event()

click_speed = 0.1  # 10 clicks per second
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

root.title("Auto Clicker")
root.geometry("350x220")
root.minsize(300, 200)

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
# START BACKGROUND CLICKER
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
