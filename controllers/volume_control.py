import pyautogui

def volume_up():
    pyautogui.press("volumeup", presses=5)
    return "Volume Increased"


def volume_down():
    pyautogui.press("volumedown", presses=5)
    return "Volume Decreased"


def mute_volume():
    pyautogui.press("volumemute")
    return "Volume Muted"