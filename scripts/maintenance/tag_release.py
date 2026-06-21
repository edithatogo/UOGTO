import subprocess
import sys
import re

def get_latest_tag():
    try:
        res = subprocess.run(["git", "describe", "--tags", "--abbrev=0"], capture_output=True, text=True, check=True)
        return res.stdout.strip()
    except subprocess.CalledProcessError:
        return "v0.1.0"

def increment_version(version, inc_type="patch"):
    match = re.match(r"v?(\d+)\.(\d+)\.(\d+)", version)
    if not match:
        return "v0.1.1"
    major, minor, patch = map(int, match.groups())
    
    if inc_type == "major":
        major += 1
        minor = 0
        patch = 0
    elif inc_type == "minor":
        minor += 1
        patch = 0
    else:
        patch += 1
        
    return f"v{major}.{minor}.{patch}"

def create_git_tag(tag_name):
    print(f"Creating semantic git release tag: {tag_name}")
    try:
        subprocess.run(["git", "tag", "-a", tag_name, "-m", f"Release {tag_name}"], check=True)
        print(f"Tag {tag_name} created successfully.")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Failed to create tag: {e}")
        return False

def main():
    current_tag = get_latest_tag()
    print(f"Current release version: {current_tag}")
    
    # Simple prompt or default to patch increase
    new_tag = increment_version(current_tag, "patch")
    create_git_tag(new_tag)

if __name__ == "__main__":
    main()
