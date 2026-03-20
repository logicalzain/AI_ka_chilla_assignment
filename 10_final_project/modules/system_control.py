# ============================================================
# system_control.py — PC System Control Module
# ============================================================
# This module controls your PC. It can:
#   - Check battery status
#   - Get date and time
#   - Empty the recycle bin
#   - Take screenshots
#   - Open/search for folders
#   - Launch applications (Notepad, Calculator, etc.)
#   - Lock, shutdown, restart the PC
#   - Control volume
#   - Get system info (CPU, RAM, Disk)
#
# HOW TO CUSTOMIZE:
#   - Add new apps to the 'APP_COMMANDS' dictionary below
#   - Change screenshot save path in config.json
#   - Add more search directories in config.json
# ============================================================

import os
import sys
import time
import ctypes
import subprocess
import datetime
import platform
import shutil

import psutil            # Battery, CPU, RAM, disk info
import pyautogui         # Screenshots

# --- Try to import Windows-specific modules ---
try:
    import winshell       # Recycle bin operations
    WINSHELL_AVAILABLE = True
except ImportError:
    WINSHELL_AVAILABLE = False

# ============================================================
# APP_COMMANDS: Dictionary mapping app names to their commands
# ------------------------------------------------------------
# HOW TO ADD A NEW APP:
#   Just add a new entry like:  "app name": "executable_or_path"
#   Example:  "spotify": "spotify.exe"
# ============================================================
APP_COMMANDS = {
    "notepad": "notepad.exe",
    "calculator": "calc.exe",
    "paint": "mspaint.exe",
    "word": "winword.exe",
    "excel": "excel.exe",
    "powerpoint": "powerpnt.exe",
    "file explorer": "explorer.exe",
    "task manager": "taskmgr.exe",
    "command prompt": "cmd.exe",
    "cmd": "cmd.exe",
    "powershell": "powershell.exe",
    "control panel": "control.exe",
    "settings": "ms-settings:",
    "vs code": "code",
    "vscode": "code",
    "snipping tool": "snippingtool.exe",
    "chrome": "chrome.exe",
    "edge": "msedge.exe",
    "obs": "obs64.exe",
}


def get_battery_status() -> str:
    """
    Get current battery percentage and charging status.
    
    Returns:
        str: Battery info like "Battery: 85% | Charging: Yes"
             or "No battery found" for desktops without battery.
    
    Example:
        print(get_battery_status())
        # Output: "🔋 Battery: 72% | Charging: No | Time left: 2:30:00"
    """
    battery = psutil.sensors_battery()
    if battery is None:
        return "No battery detected. This might be a desktop PC."
    
    percent = battery.percent
    charging = "Yes" if battery.power_plugged else "No"
    
    # --- Calculate time remaining ---
    if battery.secsleft == psutil.POWER_TIME_UNLIMITED:
        time_left = "Fully charged"
    elif battery.secsleft == psutil.POWER_TIME_UNKNOWN:
        time_left = "Calculating..."
    else:
        hours = battery.secsleft // 3600
        minutes = (battery.secsleft % 3600) // 60
        time_left = f"{hours}h {minutes}m"
    
    return f"🔋 Battery: {percent}% | Charging: {charging} | Time left: {time_left}"


def get_date_time() -> str:
    """
    Get the current date and time in a friendly format.
    
    Returns:
        str: Current date and time string
    
    Example:
        print(get_date_time())
        # Output: "📅 Wednesday, 18 March 2026 | 🕐 11:17 PM"
    """
    now = datetime.datetime.now()
    date_str = now.strftime("%A, %d %B %Y")
    time_str = now.strftime("%I:%M %p")
    return f"📅 {date_str} | 🕐 {time_str}"


def get_date() -> str:
    """Get just the current date."""
    now = datetime.datetime.now()
    return f"📅 Today is {now.strftime('%A, %d %B %Y')}"


def get_time() -> str:
    """Get just the current time."""
    now = datetime.datetime.now()
    return f"🕐 Current time is {now.strftime('%I:%M:%S %p')}"


def empty_recycle_bin() -> str:
    """
    Empty the Windows Recycle Bin.
    
    Returns:
        str: Success or error message
    
    Note:
        Requires the 'winshell' package to be installed.
    """
    if not WINSHELL_AVAILABLE:
        return "❌ Cannot empty recycle bin: 'winshell' package not installed."
    
    try:
        winshell.recycle_bin().empty(confirm=False, show_progress=False, sound=False)
        return "🗑️ Recycle Bin has been emptied successfully!"
    except Exception as e:
        return f"❌ Could not empty Recycle Bin: {e}"


def take_screenshot(config: dict) -> str:
    """
    Take a screenshot and save it to the Desktop (or custom path).
    
    Args:
        config (dict): Configuration dictionary (for save path)
    
    Returns:
        str: Path where screenshot was saved, or error message
    """
    try:
        # --- Determine save path ---
        save_dir = config.get('screenshot_save_path', '')
        if not save_dir:
            save_dir = os.path.join(os.path.expanduser("~"), "Desktop")
        
        # --- Create filename with timestamp ---
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"screenshot_{timestamp}.png"
        filepath = os.path.join(save_dir, filename)
        
        # --- Take and save screenshot ---
        screenshot = pyautogui.screenshot()
        screenshot.save(filepath)
        
        return f"📸 Screenshot saved: {filepath}"
    except Exception as e:
        return f"❌ Screenshot failed: {e}"


def search_folder(folder_name: str, config: dict) -> str:
    """
    Search for a folder by name in common directories.
    
    Args:
        folder_name (str): Name of the folder to search for
        config (dict): Configuration dictionary (for search directories)
    
    Returns:
        str: List of found paths, or "not found" message
    """
    search_dirs = config.get('search_directories', ['C:/Users', 'D:/', 'E:/'])
    found = []
    
    for search_dir in search_dirs:
        if not os.path.exists(search_dir):
            continue
        try:
            for root, dirs, files in os.walk(search_dir):
                # --- Limit search depth to 4 levels to avoid very long searches ---
                depth = root.replace(search_dir, '').count(os.sep)
                if depth > 4:
                    dirs.clear()  # Don't go deeper
                    continue
                
                for d in dirs:
                    if folder_name.lower() in d.lower():
                        found.append(os.path.join(root, d))
                        if len(found) >= 10:  # Limit results
                            break
                
                if len(found) >= 10:
                    break
        except PermissionError:
            continue
    
    if found:
        result = f"📁 Found {len(found)} result(s):\n"
        for path in found:
            result += f"  → {path}\n"
        return result.strip()
    else:
        return f"📁 Folder '{folder_name}' not found in search directories."


def open_folder(folder_path: str) -> str:
    """
    Open a folder in Windows File Explorer.
    
    Args:
        folder_path (str): Full path to the folder
    
    Returns:
        str: Success or error message
    """
    if os.path.exists(folder_path):
        os.startfile(folder_path)
        return f"📂 Opened folder: {folder_path}"
    else:
        return f"❌ Folder not found: {folder_path}"


def open_application(app_name: str) -> str:
    """
    Open a Windows application by its friendly name.
    
    The app name is matched against the APP_COMMANDS dictionary.
    
    Args:
        app_name (str): Friendly name like "notepad", "calculator", "vs code"
    
    Returns:
        str: Success or error message
    """
    app_name_lower = app_name.lower().strip()
    
    # --- Check if app is in our dictionary ---
    if app_name_lower in APP_COMMANDS:
        try:
            command = APP_COMMANDS[app_name_lower]
            # ms-settings: type commands need os.startfile
            if command.startswith("ms-"):
                os.startfile(command)
            else:
                subprocess.Popen(command, shell=True)
            return f"✅ Opening {app_name}..."
        except Exception as e:
            return f"❌ Could not open {app_name}: {e}"
    else:
        # --- Try to open it directly as an executable ---
        try:
            subprocess.Popen(app_name_lower, shell=True)
            return f"✅ Trying to open {app_name}..."
        except Exception as e:
            return f"❌ Application '{app_name}' not found. You can add it to APP_COMMANDS in system_control.py"


def lock_pc() -> str:
    """Lock the PC (Windows Lock Screen)."""
    try:
        ctypes.windll.user32.LockWorkStation()
        return "🔒 PC is now locked."
    except Exception as e:
        return f"❌ Could not lock PC: {e}"


def shutdown_pc() -> str:
    """Shutdown the PC (with 30 second delay to allow cancellation)."""
    try:
        os.system("shutdown /s /t 30")
        return "⚠️ PC will shutdown in 30 seconds. Type 'cancel shutdown' to cancel."
    except Exception as e:
        return f"❌ Could not initiate shutdown: {e}"


def restart_pc() -> str:
    """Restart the PC (with 30 second delay to allow cancellation)."""
    try:
        os.system("shutdown /r /t 30")
        return "⚠️ PC will restart in 30 seconds. Type 'cancel shutdown' to cancel."
    except Exception as e:
        return f"❌ Could not initiate restart: {e}"


def cancel_shutdown() -> str:
    """Cancel a pending shutdown or restart."""
    try:
        os.system("shutdown /a")
        return "✅ Shutdown/Restart has been cancelled."
    except Exception as e:
        return f"❌ Could not cancel shutdown: {e}"


def get_system_info() -> str:
    """
    Get comprehensive system information.
    
    Returns:
        str: Formatted system info (CPU, RAM, Disk, OS, etc.)
    """
    try:
        # --- CPU Info ---
        cpu_percent = psutil.cpu_percent(interval=1)
        cpu_count = psutil.cpu_count()
        
        # --- RAM Info ---
        ram = psutil.virtual_memory()
        ram_total = round(ram.total / (1024**3), 2)
        ram_used = round(ram.used / (1024**3), 2)
        ram_percent = ram.percent
        
        # --- Disk Info ---
        disk = psutil.disk_usage('/')
        disk_total = round(disk.total / (1024**3), 2)
        disk_used = round(disk.used / (1024**3), 2)
        disk_percent = disk.percent
        
        # --- OS Info ---
        os_info = f"{platform.system()} {platform.release()}"
        machine = platform.machine()
        
        info = f"""💻 System Information:
  🖥️ OS: {os_info} ({machine})
  ⚡ CPU: {cpu_percent}% usage | {cpu_count} cores
  🧠 RAM: {ram_used} GB / {ram_total} GB ({ram_percent}%)
  💾 Disk: {disk_used} GB / {disk_total} GB ({disk_percent}%)"""
        
        return info
    except Exception as e:
        return f"❌ Could not get system info: {e}"


def set_volume(action: str) -> str:
    """
    Control system volume using nircmd (or keyboard simulation).
    
    Args:
        action (str): "up", "down", or "mute"
    
    Returns:
        str: Status message
    """
    try:
        if action == "up":
            # Simulate pressing Volume Up key 5 times
            for _ in range(5):
                pyautogui.press('volumeup')
            return "🔊 Volume increased."
        elif action == "down":
            for _ in range(5):
                pyautogui.press('volumedown')
            return "🔉 Volume decreased."
        elif action == "mute":
            pyautogui.press('volumemute')
            return "🔇 Volume muted/unmuted."
        else:
            return "❌ Unknown volume action. Use 'up', 'down', or 'mute'."
    except Exception as e:
        return f"❌ Volume control error: {e}"


def open_file(file_path: str) -> str:
    """
    Open any file with its default application.
    
    Args:
        file_path (str): Full path to the file
    
    Returns:
        str: Success or error message
    """
    if os.path.exists(file_path):
        try:
            os.startfile(file_path)
            return f"✅ Opened: {file_path}"
        except Exception as e:
            return f"❌ Could not open file: {e}"
    else:
        return f"❌ File not found: {file_path}"


def get_ip_address() -> str:
    """Get the local IP address of this PC."""
    import socket
    try:
        hostname = socket.gethostname()
        ip = socket.gethostbyname(hostname)
        return f"🌐 Hostname: {hostname} | IP Address: {ip}"
    except Exception as e:
        return f"❌ Could not get IP address: {e}"


def set_brightness(action: str) -> str:
    """
    Adjust screen brightness (Windows).

    Args:
        action (str): "up" or "down"

    Returns:
        str: Status message
    """
    try:
        # Try WMI method first (works on most laptops)
        try:
            import wmi
            c = wmi.WMI(namespace='wmi')
            methods = c.WmiMonitorBrightnessMethods()[0]
            current = c.WmiMonitorBrightness()[0].CurrentBrightness
            if action == "up":
                new_val = min(100, current + 15)
                methods.WmiSetBrightness(new_val, 0)
                return f"🔆 Brightness increased to {new_val}%"
            elif action == "down":
                new_val = max(0, current - 15)
                methods.WmiSetBrightness(new_val, 0)
                return f"🔅 Brightness decreased to {new_val}%"
        except Exception:
            # Fallback: try PowerShell
            import subprocess
            if action == "up":
                subprocess.run(
                    ['powershell', '-Command',
                     '(Get-WmiObject -Namespace root/WMI -Class WmiMonitorBrightnessMethods).WmiSetBrightness(1, [Math]::Min(100, (Get-WmiObject -Namespace root/WMI -Class WmiMonitorBrightness).CurrentBrightness + 15))'],
                    capture_output=True
                )
                return "🔆 Brightness increased."
            elif action == "down":
                subprocess.run(
                    ['powershell', '-Command',
                     '(Get-WmiObject -Namespace root/WMI -Class WmiMonitorBrightnessMethods).WmiSetBrightness(1, [Math]::Max(0, (Get-WmiObject -Namespace root/WMI -Class WmiMonitorBrightness).CurrentBrightness - 15))'],
                    capture_output=True
                )
                return "🔅 Brightness decreased."
        return "❌ Unknown brightness action."
    except Exception as e:
        return f"❌ Brightness control error: {e}"
