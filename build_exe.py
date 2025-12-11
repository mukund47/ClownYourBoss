import PyInstaller.__main__
import os

print("Building Fake Error App...")

PyInstaller.__main__.run([
    'main.py',
    '--onefile',
    '--noconsole',
    '--name=Error',
    '--uac-admin', # Request admin might help with some system interactions, though HKCU registry doesn't strictly need it.
    '--clean',
    '--distpath=dist'
])

print("Build complete. Executable is in 'dist' folder.")
