import subprocess


# Increase Brightness
def increase_brightness():

    subprocess.run(
        'powershell (Get-WmiObject -Namespace root/WMI -Class WmiMonitorBrightnessMethods).WmiSetBrightness(1,100)',
        shell=True
    )

    return "Brightness Increased"


# Decrease Brightness
def decrease_brightness():

    subprocess.run(
        'powershell (Get-WmiObject -Namespace root/WMI -Class WmiMonitorBrightnessMethods).WmiSetBrightness(1,30)',
        shell=True
    )

    return "Brightness Decreased"