"""
GDrive Flow - Main Application Entry Point
"""
import sys
import os

# Ensure script directory, _MEIPASS and current directory are in sys.path
script_dir = os.path.dirname(os.path.abspath(__file__))
if script_dir not in sys.path:
    sys.path.insert(0, script_dir)

if hasattr(sys, '_MEIPASS'):
    mei_dir = getattr(sys, '_MEIPASS')
    if mei_dir not in sys.path:
        sys.path.insert(0, mei_dir)

cwd = os.getcwd()
if cwd not in sys.path:
    sys.path.insert(0, cwd)

from ui_main import GDriveApp

def main():
    app = GDriveApp()
    app.mainloop()

if __name__ == "__main__":
    main()
