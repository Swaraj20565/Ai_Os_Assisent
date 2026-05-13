
import subprocess

def wifi_on():
    subprocess.run(
        'netsh interface set interface "Wi-Fi" enabled',
        shell=True
    )

    return "WiFi Turned ON"


def wifi_off():
    subprocess.run(
        'netsh interface set interface "Wi-Fi" disabled',
        shell=True
    )

    return "WiFi Turned OFF"