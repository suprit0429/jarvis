# sys_utils.py
import psutil
import platform

def battery_status():
    try:
        battery = psutil.sensors_battery()
        if battery:
            percent = battery.percent
            plugged = battery.power_plugged
            charging = "charging" if plugged else "not charging"
            return f"Battery is at {percent}% and is currently {charging}."
        else:
            return "Battery information is not available on this system."
    except Exception as e:
        return f"Unable to fetch battery status. Error: {str(e)}"

def system_info():
    try:
        cpu_usage = psutil.cpu_percent(interval=1)
        ram_usage = psutil.virtual_memory().percent
        os_name = platform.system()
        os_version = platform.release()
        return f"CPU usage is {cpu_usage}%, RAM usage is {ram_usage}%, running on {os_name} version {os_version}."
    except Exception as e:
        return f"Unable to fetch system information. Error: {str(e)}"
