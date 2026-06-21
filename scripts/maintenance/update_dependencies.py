import subprocess
import sys
import os
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

WINDOWS_PIXI_PATH = r"C:\Users\60217257\AppData\Local\pixi\bin\pixi.exe"

def pixi_command():
    found = shutil.which("pixi")
    if found:
        return found
    if os.name == "nt" and os.path.exists(WINDOWS_PIXI_PATH):
        return WINDOWS_PIXI_PATH
    return "pixi"

def run_cmd(cmd):
    try:
        res = subprocess.run(cmd, capture_output=True, text=True, check=True)
        print(res.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"Command failed: {cmd}\nExit Code: {e.returncode}\nError: {e.stderr}", file=sys.stderr)
        return False
    except FileNotFoundError:
        print(f"Executable not found: {cmd[0]}", file=sys.stderr)
        return False

def main():
    pixi = pixi_command()

    # Integrate protective disk space check
    from scripts.maintenance.disk_guard import check_disk_space, clean_caches
    if not check_disk_space():
        clean_caches()
        if not check_disk_space():
            print("Insufficient disk space to proceed.", file=sys.stderr)
            sys.exit(1)

    print("Updating project dependencies to bleeding edge...")
    # Update command
    if not run_cmd([pixi, "update"]):
        print("Dependency update failed.", file=sys.stderr)
        sys.exit(1)
        
    print("Running project validation, tests, semantic audit, and HTML report generation...")
    if not run_cmd([pixi, "run", "check"]):
        print("Validation tests failed post-update! Reverting changes is recommended.", file=sys.stderr)
        sys.exit(1)
        
    print("Dependency update and verification completed successfully!")

if __name__ == "__main__":
    main()
