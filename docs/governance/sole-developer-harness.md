# Sole-Developer Harness

UOGTO is maintained as a sole-developer repository. The repository owner may author, validate, and merge changes without an independent approving review or code-owner approval.

## Required controls

- Pull requests remain the normal integration record for non-urgent changes.
- The `Required Gate` and `validate` status checks remain required on `main`.
- The author must run the relevant local checks, normally `make validate` and `make test`, and record exceptions in the pull request or Conductor runlog.
- Conductor tracks, repository evidence, GitHub issues, and Project #8 remain the operational audit trail.
- Registry curator/maintainer decisions, publication, DOI, and other external service outcomes remain separate gates. Passing repository CI does not imply external acceptance.

## Review terminology

Automated checks, self-review, Conductor review, and agent-assisted review are internal process controls. They must not be described as independent peer review or independent domain-expert approval.

## Re-enabling collaboration

If the project gains additional maintainers, the repository owner should re-enable required approving reviews and code-owner review through GitHub branch protection, update this policy, and record the change in the Conductor runlog.
