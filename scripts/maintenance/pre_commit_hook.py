#!/usr/bin/env python
import sys
import subprocess
import os
import shutil

# Insert workspace root in python path to resolve modules correctly when executed inside git hook context
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

# Set stdout to UTF-8
sys.stdout.reconfigure(encoding='utf-8')

def run_cmd(cmd):
    env = os.environ.copy()
    # Clear PYTHONPATH/PYTHONHOME when calling Pixi task commands to prevent virtualenv library mismatch
    env.pop("PYTHONPATH", None)
    env.pop("PYTHONHOME", None)
    try:
        res = subprocess.run(cmd, capture_output=True, text=True, check=True, env=env)
        return True, res.stdout
    except subprocess.CalledProcessError as e:
        return False, f"Command failed: {cmd}\nExit Code: {e.returncode}\nError: {e.stderr}"
    except FileNotFoundError:
        return False, f"Executable not found for: {cmd}"

def main():
    print("Running Git Pre-Commit Validations & Hooks...")
    
    # 1. Run Disk Guard Space checks
    from scripts.maintenance.disk_guard import check_disk_space, clean_caches
    if not check_disk_space():
        clean_caches()
        if not check_disk_space():
            print("ERROR: Insufficient disk space to execute commits. Aborting.")
            sys.exit(1)
            
    # 2. Run Semantic Completeness Auditor
    from scripts.maintenance.audit_semantics import audit_semantics
    if not audit_semantics():
        print("ERROR: Semantic completeness audit failed. Add missing rdfs:label/skos:definition annotations.")
        sys.exit(1)
        
    # 3. Run Makefile validations
    pixi_path = shutil.which("pixi")
    if not pixi_path:
        suffix = ".exe" if sys.platform == "win32" else ""
        for candidate in [
            os.path.expanduser(f"~/.pixi/bin/pixi{suffix}"),
            os.path.expanduser(f"~/.local/bin/pixi{suffix}"),
            os.path.expanduser(r"~\AppData\Local\pixi\bin\pixi.exe"),
        ]:
            if os.path.exists(candidate):
                pixi_path = candidate
                break
    if not pixi_path:
        print("ERROR: Pixi executable not found on PATH or in known user install locations.")
        sys.exit(1)
    ok, output = run_cmd([pixi_path, "run", "python", "scripts/validate.py"])
    print(output)
    if not ok:
        print("ERROR: Project RDF/SHACL validation checks failed. Commit aborted.")
        sys.exit(1)
        
    print("Pre-commit checks successfully passed!")

if __name__ == "__main__":
    main()
