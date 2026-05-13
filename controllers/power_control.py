import os
import subprocess

def shutdown_pc():
    os.system("shutdown /s /t 5")
    return "Shutdown Started"


def restart_pc():
    os.system("shutdown /r /t 5")
    return "Restart Started"


def lock_screen():
    subprocess.run(
        "rundll32.exe user32.dll,LockWorkStation"
    )

    return "Screen Locked"