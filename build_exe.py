"""
Build script to compile DriveFlow Pro into a single standalone Windows DriveFlow.exe file
"""
import os
import subprocess
import sys
import shutil

# Ensure UTF-8 output encoding for Windows terminal
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

def build_exe():
    print("=" * 60)
    print("  Building DriveFlow Pro (v1.7.0) to a Single Standalone .exe file...")
    print("  Developed by TON NGO DOC")
    print("=" * 60)

    try:
        import customtkinter
        ctk_path = os.path.dirname(customtkinter.__file__)
        add_data_ctk = f"{ctk_path}{os.pathsep}customtkinter"
    except ImportError:
        add_data_ctk = None

    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--noconfirm",
        "--onefile",      # Single standalone .exe file
        "--windowed",     # Native GUI app (no black CMD console window)
        "--name=DriveFlow",
        "--clean",
    ]

    if add_data_ctk:
        cmd.extend(["--add-data", add_data_ctk])

    cmd.append("main.py")

    print(f"Executing command: {' '.join(cmd)}")
    result = subprocess.run(cmd)

    if result.returncode == 0:
        dist_exe = os.path.abspath(os.path.join("dist", "DriveFlow.exe"))
        root_exe = os.path.abspath("DriveFlow.exe")

        copied = False
        if os.path.exists(dist_exe):
            try:
                shutil.copy(dist_exe, root_exe)
                copied = True
            except PermissionError:
                print(f"\n⚠️ Notice: Could not overwrite '{root_exe}' because DriveFlow.exe is currently running.")
                print(f"   The updated binary was built successfully and is ready at: '{dist_exe}'")

        print("\n" + "=" * 60)
        print("BUILD SUCCESSFUL!")
        if copied:
            print(f"Single Executable created directly at: {root_exe}")
        else:
            print(f"Single Executable created at: {dist_exe}")
        print("=" * 60)
    else:
        print("\nPyInstaller build failed!")

if __name__ == "__main__":
    build_exe()
