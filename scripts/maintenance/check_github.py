import subprocess
import json
import urllib.request
import urllib.error
import sys
import os

REPO = "legal-nz/UOGTO"
OUTPUT_FILE = "conductor/remote_status.md"

def run_cmd(cmd):
    try:
        res = subprocess.run(cmd, capture_output=True, text=True, check=True)
        return res.stdout.strip()
    except (subprocess.CalledProcessError, FileNotFoundError):
        return None

def get_via_gh():
    # Verify gh auth
    auth = run_cmd(["gh", "auth", "status"])
    if not auth:
        return None, None
    
    issues_raw = run_cmd(["gh", "issue", "list", "--repo", REPO, "--limit", "10", "--json", "number,title,state,url,updatedAt"])
    prs_raw = run_cmd(["gh", "pr", "list", "--repo", REPO, "--limit", "10", "--json", "number,title,state,url,updatedAt"])
    
    if issues_raw is None or prs_raw is None:
        return None, None
    
    try:
        issues = json.loads(issues_raw)
        prs = json.loads(prs_raw)
        return issues, prs
    except json.JSONDecodeError:
        return None, None

def get_via_api():
    url = f"https://api.github.com/repos/{REPO}/issues?state=open&per_page=30"
    req = urllib.request.Request(
        url,
        headers={"User-Agent": "UOGTO-Maintenance-Agent"}
    )
    try:
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode())
            issues = []
            prs = []
            for item in data:
                # GitHub's issue endpoint returns PRs too, distinguished by the 'pull_request' key
                formatted = {
                    "number": item.get("number"),
                    "title": item.get("title"),
                    "state": item.get("state"),
                    "url": item.get("html_url"),
                    "updatedAt": item.get("updated_at")
                }
                if "pull_request" in item:
                    prs.append(formatted)
                else:
                    issues.append(formatted)
            return issues[:10], prs[:10]
    except urllib.error.URLError as e:
        print(f"API fallback failed: {e}", file=sys.stderr)
        return None, None

def write_summary(issues, prs):
    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write("# Remote Repository Status\n\n")
        
        f.write("## Open Issues\n")
        if issues:
            for issue in issues:
                f.write(f"- [#{issue['number']}]({issue['url']}): {issue['title']} (Updated: {issue['updatedAt']})\n")
        else:
            f.write("No open issues found.\n")
            
        f.write("\n## Open Pull Requests\n")
        if prs:
            for pr in prs:
                f.write(f"- [#{pr['number']}]({pr['url']}): {pr['title']} (Updated: {pr['updatedAt']})\n")
        else:
            f.write("No open pull requests found.\n")
    print(f"Summary written to {OUTPUT_FILE}")

def write_fallback_summary(reason):
    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write("# Remote Repository Status\n\n")
        f.write("> [!NOTE]\n")
        f.write(f"> Remote repository query not available: {reason}\n\n")
        f.write("## Open Issues\n")
        f.write("No remote connection. Unable to fetch open issues.\n")
        f.write("\n## Open Pull Requests\n")
        f.write("No remote connection. Unable to fetch open pull requests.\n")
    print(f"Fallback summary written to {OUTPUT_FILE}")

def main():
    print("Checking remote repository status...")
    issues, prs = get_via_gh()
    if issues is None or prs is None:
        print("gh CLI not authenticated or failed. Falling back to public GitHub API...")
        issues, prs = get_via_api()
        
    if issues is None and prs is None:
        print("Failed to fetch remote repository data. Writing fallback summary...")
        write_fallback_summary("Repository not found or API access limits exceeded.")
        sys.exit(0)
        
    write_summary(issues, prs)

if __name__ == "__main__":
    main()
