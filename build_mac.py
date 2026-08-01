"""
Build script to compile GDrive Flow into a standalone macOS executable / app bundle.
Run this script on macOS: python build_mac.py
"""
import os
import subprocess
import sys
import shutil

def build_mac():
    print("=" * 60)
    print("  Building GDrive Flow (v2.2.1) for macOS...")
    print("  Videcoding by TonNgoDoc")
    print("=" * 60)

    try:
        import customtkinter
        ctk_path = os.path.dirname(customtkinter.__file__)
        add_data_ctk = f"{ctk_path}:customtkinter"
    except ImportError:
        add_data_ctk = None

    png_icon = "icon.png"
    flag_vn = "flag_vn.png"
    flag_en = "flag_en.png"

    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--noconfirm",
        "--onefile",       # Single standalone executable file for macOS
        "--windowed",      # GUI app bundle
        "--name=GDriveFlow",
        "--clean",
    ]

    if add_data_ctk:
        cmd.extend(["--add-data", add_data_ctk])

    if os.path.exists(png_icon):
        cmd.extend(["--add-data", f"{png_icon}:."])
        cmd.extend(["--icon", png_icon])
    if os.path.exists(flag_vn):
        cmd.extend(["--add-data", f"{flag_vn}:."])
    if os.path.exists(flag_en):
        cmd.extend(["--add-data", f"{flag_en}:."])

    cmd.append("main.py")

    print(f"Executing command: {' '.join(cmd)}")
    result = subprocess.run(cmd)

    if result.returncode == 0:
        dist_exe = os.path.abspath(os.path.join("dist", "GDriveFlow"))
        root_exe = os.path.abspath("GDriveFlow_mac")

        if os.path.exists(dist_exe):
            try:
                shutil.copy(dist_exe, root_exe)
                print(f"macOS Executable copied to: {root_exe}")
            except Exception as e:
                print(f"Build ready at: {dist_exe}")

        print("\n" + "=" * 60)
        print("BUILD SUCCESSFUL FOR MACOS!")
        print("Standalone binary ready at: dist/GDriveFlow")
        print("=" * 60)
    else:
        print("\nPyInstaller build failed on macOS!")

if __name__ == "__main__":
    build_mac()
