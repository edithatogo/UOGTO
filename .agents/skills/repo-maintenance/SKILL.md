---
name: repo-maintenance
description: Handles Pixi package environment, bleeding-edge updates, verification tests, remote issue/PR status parsing, and auto-changelog generation for the UOGTO repository.
---

# Repository Maintenance & Automation Skill

This skill guides the agent in performing automated updates, integrity verification, and remote checks on the UOGTO repository.

## Commands and Tools
All maintenance scripts are orchestrated via the Pixi package manager to ensure environment consistency.

1. **Check Remote GitHub Status**:
   ```bash
   C:\Users\60217257\AppData\Local\pixi\bin\pixi.exe run python scripts/maintenance/check_github.py
   ```
   *   **Inputs**: None (uses GitHub CLI auth or falls back to public API).
   *   **Outputs**: Produces [remote_status.md](file:///C:/Users/60217257/OneDrive%20-%20Flinders/repos/legal-nz/UOGTO/conductor/remote_status.md) detailing recent issues and pull requests.

2. **Upgrade Dependencies to Bleeding Edge**:
   ```bash
   C:\Users\60217257\AppData\Local\pixi\bin\pixi.exe run python scripts/maintenance/update_dependencies.py
   ```
   *   **Inputs**: None.
   *   **Behavior**: Upgrades packages in [pixi.toml](file:///C:/Users/60217257/OneDrive%20-%20Flinders/repos/legal-nz/UOGTO/pixi.toml) and verifies that all unit tests, RDFLib parsers, and SHACL constraint checks pass successfully.

3. **Generate Auto-Changelog**:
   ```bash
   C:\Users\60217257\AppData\Local\pixi\bin\pixi.exe run python scripts/maintenance/generate_changelog.py
   ```
   *   **Inputs**: None.
   *   **Outputs**: Parses recent commits and updates the top of [CHANGELOG.md](file:///C:/Users/60217257/OneDrive%20-%20Flinders/repos/legal-nz/UOGTO/CHANGELOG.md).

## Operational Workflow
Whenever requested to "maintain", "update the repository", or "ensure everything is bleeding edge", follow this protocol:
1. Run the remote status query to check for any open issues or PRs.
2. Run the dependency updater to pull down package updates and verify repository health.
3. Generate the auto-changelog to document the version adjustments.
4. Stage and commit all changed configurations.
