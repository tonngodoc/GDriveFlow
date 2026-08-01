"""
GDrive Downloader Pro - Main Application Entry Point
"""
import sys
import os

# Add current directory to sys.path to ensure modules resolve cleanly
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from ui_main import GDriveApp

def main():
    app = GDriveApp()
    app.mainloop()

if __name__ == "__main__":
    main()
