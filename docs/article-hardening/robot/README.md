# ROBOT-Style Ontology Reports

These artifacts provide a Java-backed, ROBOT-style reporting layer for UOGTO article hardening when the toolchain is available.

## Baseline Policy

- RDFLib remains the portable graph-processing baseline.
- pySHACL remains the portable validation baseline.
- ROBOT-style outputs are optional and should never block the portable baseline.

## Toolchain Notes

- `java` is detected if present.
- A ROBOT binary or JAR can be supplied later through the local environment.
- When ROBOT is not configured, the repository still generates deterministic report artifacts from RDFLib graphs.

## Artifacts

- `status.json`
- `reasoner-check.md`
- `report.md`
- `merged-ontology.ttl`
- `merge-diff.md`
- `import-extraction.ttl`
- `import-extraction.md`

