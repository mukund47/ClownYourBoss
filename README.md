# ClownYourBoss

A Windows application that displays a fake system error screen. Built with Python and Tkinter.

## Features

- **Full-screen fake error display**: Mimics the Windows Blue Screen of Death (BSOD) error screen
- **Keyboard input capture**: Captures all keyboard input with a hidden unlock code
- **Trackpad control**: Disables trackpad during operation to prevent escape
- **Auto-startup**: Automatically runs at Windows startup
- **Admin privileges**: Runs with elevated privileges for full system control
- **Focus protection**: Maintains focus and triggers restart if user attempts to switch away

## Requirements

- Windows OS
- Python 3.6+ (for running from source)
- Administrator privileges

## Installation

### Option 1: Run from Source

1. Clone this repository:
```bash
git clone https://github.com/yourusername/ClownYourBoss.git
cd ClownYourBoss
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
python main.py
```

### Option 2: Use Pre-built Executable

1. Download the latest release from the [Releases](https://github.com/yourusername/ClownYourBoss/releases) page
2. Run `Error.exe`

## Building from Source

To build an executable:

```bash
python build_exe.py
```

The executable will be created in the `dist` folder.

## Usage

1. Run the application (requires administrator privileges)
2. The fake error screen will appear
3. Type the unlock code: `1234567890`
4. The application will exit and restore normal functionality

## Configuration

You can modify the following settings in `main.py`:

- `UNLOCK_CODE`: The secret code to exit the application (default: "1234567890")
- `SHUTDOWN_DELAY_MS`: Time before automatic shutdown in milliseconds (default: 60000)

## How It Works

1. **Auto-elevation**: Checks for admin privileges and automatically elevates if needed
2. **Startup persistence**: Adds itself to Windows Registry for auto-start
3. **Input blocking**: Captures all keyboard input and suppresses it
4. **Trackpad disable**: Uses PowerShell to disable trackpad hardware
5. **Focus locking**: Maintains window focus and triggers restart on focus loss
6. **Visual countdown**: Displays a fake "error collection" percentage

## Important Notes

⚠️ **Warning**: This application is intended for educational purposes only. Use responsibly and only on systems you own or have permission to use.

- The application will restart the computer if the unlock code is not entered within 60 seconds
- Attempting to switch away (Ctrl+Alt+Del, Alt+Tab, etc.) will trigger an immediate restart
- The trackpad will be disabled while running and restored upon exit
- The application adds itself to Windows startup

## Technical Details

### Technologies Used

- **Python 3.x**: Core programming language
- **Tkinter**: GUI framework
- **keyboard**: Global keyboard hook library
- **ctypes**: Windows API interactions
- **PowerShell**: Hardware device management

### Key Components

- **Admin privilege checking**: Ensures the app runs with necessary permissions
- **Registry manipulation**: For startup persistence
- **PnP device control**: For trackpad enable/disable
- **Global keyboard hooks**: For input capture and suppression

## Uninstalling

To completely remove the application:

1. Run the application and enter the unlock code (1234567890) to exit
2. Delete the registry entry:
   - Open Registry Editor (regedit)
   - Navigate to: `HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Run`
   - Delete the `FakeErrorApp` entry
3. Delete the application files

## License

This project is provided as-is for educational purposes.

## Disclaimer

This software is provided for educational and entertainment purposes only. The author is not responsible for any misuse or damage caused by this application. Always obtain proper authorization before running this software on any system.
