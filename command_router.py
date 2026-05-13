from controllers.power_control import *
from controllers.volume_control import *
from controllers.network_control import *
from controllers.brightness_control import *
from controllers.screenshot_control import *


def execute_intent(intent):

    intent_map = {

        "shutdown": shutdown_pc,
        "restart": restart_pc,
        "lock": lock_screen,

        "volume_up": volume_up,
        "volume_down": volume_down,
        "mute": mute_volume,

        "wifi_on": wifi_on,
        "wifi_off": wifi_off,

        "brightness_up": increase_brightness,
        "brightness_down": decrease_brightness,

        "screenshot": take_screenshot,
    }

    function = intent_map.get(intent)

    if function:
        return function()

    return "Intent Not Found"