import os
import sys
import shutil

HOOK_SOURCE = os.path.abspath(os.path.join(os.path.dirname(__file__), "pre_commit_hook.py"))
HOOK_TARGET = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../.git/hooks/pre-commit"))

def install_hook():
    print("Installing git pre-commit hook...")
    
    # Git pre-commit script body
    hook_script = f"""#!/bin/sh
python "{HOOK_SOURCE}"
"""
    
    os.makedirs(os.path.dirname(HOOK_TARGET), exist_ok=True)
    with open(HOOK_TARGET, "w", encoding="utf-8") as f:
        f.write(hook_script)
        
    # Mark executable under Unix/Linux systems if needed
    try:
        os.chmod(HOOK_TARGET, 0o755)
    except OSError:
        pass
        
    print(f"Pre-commit hook successfully installed at: {HOOK_TARGET}")

if __name__ == "__main__":
    install_hook()
