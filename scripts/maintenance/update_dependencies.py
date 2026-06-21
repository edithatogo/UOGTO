import subprocess
import sys
import os

PIXI_PATH = r"C:\Users\60217257\AppData\Local\pixi\bin\pixi.exe"

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
    print("Updating project dependencies to bleeding edge...")
    # Update command
    if not run_cmd([PIXI_PATH, "update"]):
        print("Dependency update failed.", file=sys.stderr)
        sys.exit(1)
        
    print("Running project validation tests...")
    # Run test command
    if not run_cmd([PIXI_PATH, "run", "test"]):
        print("Validation tests failed post-update! Reverting changes is recommended.", file=sys.stderr)
        sys.exit(1)
        
    print("Dependency update and verification completed successfully!")

if __name__ == "__main__":
    main()
