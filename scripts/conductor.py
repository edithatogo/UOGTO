import sys
import yaml
import json
import argparse

def main():
    parser = argparse.ArgumentParser(description="Conductor task status reporter.")
    parser.add_argument("--json", action="store_true", help="Output status in JSON format.")
    args = parser.parse_args()

    try:
        with open(".conductor/tasks.yaml", "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)
    except Exception as e:
        print(f"Error loading tasks.yaml: {e}", file=sys.stderr)
        sys.exit(1)

    if args.json:
        print(json.dumps(data, indent=2))
        return

    print("=== Conductor Task Status Report ===")
    for phase in data.get("phases", []):
        print(f"\\nPhase: {phase.get('name')} (ID: {phase.get('id')})")
        print(f"Status: {phase.get('status')}")
        for task in phase.get("tasks", []):
            status_icon = "[x]" if task.get("status") == "completed" else "[ ]"
            print(f"  {status_icon} Task: {task.get('id')} ({task.get('status')})")
            print(f"      Owner: {task.get('owner_role')}")
            print(f"      Expected Outputs: {', '.join(task.get('outputs', []))}")
            print(f"      Validation Command: {task.get('validation_command')}")

if __name__ == "__main__":
    main()
