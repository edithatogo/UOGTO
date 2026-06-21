import subprocess
import re
from datetime import datetime
import os
import sys

CHANGELOG_PATH = "CHANGELOG.md"

def get_git_commits():
    try:
        # Get commits since last tag or all commits if no tags exist
        # For simplicity, we query the last 20 commits
        res = subprocess.run(["git", "log", "-n", "20", "--pretty=format:%h|%s"], capture_output=True, text=True, check=True)
        return res.stdout.strip().split("\n")
    except subprocess.CalledProcessError:
        return []

def parse_commits(commits):
    categories = {
        "Features": [],
        "Bug Fixes": [],
        "Documentation": [],
        "Chores & Maintenance": []
    }
    
    for line in commits:
        if not line or "|" not in line:
            continue
        sha, msg = line.split("|", 1)
        
        # Check standard conventional commit prefixes
        if msg.startswith("feat"):
            categories["Features"].append(f"- {msg} ({sha})")
        elif msg.startswith("fix"):
            categories["Bug Fixes"].append(f"- {msg} ({sha})")
        elif msg.startswith("docs"):
            categories["Documentation"].append(f"- {msg} ({sha})")
        elif msg.startswith("chore") or msg.startswith("refactor"):
            categories["Chores & Maintenance"].append(f"- {msg} ({sha})")
            
    return categories

def generate_entry(categories):
    date_str = datetime.now().strftime("%Y-%m-%d")
    entry = f"## [{date_str}]\n\n"
    
    has_content = False
    for cat, items in categories.items():
        if items:
            entry += f"### {cat}\n"
            entry += "\n".join(items) + "\n\n"
            has_content = True
            
    if not has_content:
        entry += "No notable changes in this release.\n\n"
        
    return entry

def update_changelog(new_entry):
    existing_content = ""
    if os.path.exists(CHANGELOG_PATH):
        with open(CHANGELOG_PATH, "r", encoding="utf-8") as f:
            existing_content = f.read()
            
    # Insert new entry right after the header if exists, otherwise at start
    header_pattern = r"^# Changelog\n*"
    match = re.search(header_pattern, existing_content, re.IGNORECASE)
    
    if match:
        header_end = match.end()
        updated_content = existing_content[:header_end] + new_entry + existing_content[header_end:]
    else:
        updated_content = "# Changelog\n\n" + new_entry + existing_content
        
    with open(CHANGELOG_PATH, "w", encoding="utf-8") as f:
        f.write(updated_content)
        
    print(f"Updated {CHANGELOG_PATH} with new entry.")

def main():
    print("Generating changelog from git logs...")
    commits = get_git_commits()
    if not commits:
        print("No commits found or git log failed.", file=sys.stderr)
        sys.exit(1)
        
    categories = parse_commits(commits)
    new_entry = generate_entry(categories)
    update_changelog(new_entry)

if __name__ == "__main__":
    main()
