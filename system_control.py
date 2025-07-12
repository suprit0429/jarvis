import screen_brightness_control as sbc
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

# Brightness
def set_brightness(level):
    try:
        sbc.set_brightness(level)
        return f"Brightness set to {level}%"
    except Exception as e:
        return f"Failed to set brightness: {e}"

# Volume
def set_volume(level):
    try:
        devices = AudioUtilities.GetSpeakers()
        interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        volume = cast(interface, POINTER(IAudioEndpointVolume))
        volume_range = volume.GetVolumeRange()
        min_vol, max_vol = volume_range[0], volume_range[1]
        # Normalize level to 0-1 and set
        level = min(max(level, 0), 100)
        volume_level = min_vol + (max_vol - min_vol) * (level / 100)
        volume.SetMasterVolumeLevel(volume_level, None)
        return f"Volume set to {level}%"
    except Exception as e:
        return f"Failed to set volume: {e}"
