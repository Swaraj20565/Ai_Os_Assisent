import pyautogui
from datetime import datetime

def take_screenshot():

    now = datetime.now().strftime("%Y%m%d_%H%M%S")

    file_name = f"screenshot_{now}.png"

    screenshot = pyautogui.screenshot()

    screenshot.save(file_name)

    return f"Screenshot Saved: {file_name}"