# PRISMA 2020 Screening Flow

This figure adapts the PRISMA 2020 flow-diagram template for the UOGTO article-hardening screening stage. Counts reflect the current repository snapshot on 2026-06-25 and are derived from `docs/article-hardening/source-extension-inventory.json`.

```mermaid
flowchart TD
    A["Candidate sources in source-extension-inventory.json (n=39)"] --> B["Screened against inclusion criteria (n=39)"]
    B --> C["Included in the evidence package (n=39)"]
    B --> D["Excluded after screening (n=0)"]
    A -.-> E["Negative-evidence search route recorded separately (n=1)"]
```

Notes:
- The screening flow remains PRISMA 2020-style, but the object of screening is ontology and evidence-package sources rather than study records.
- The zero-exclusion branch reflects the current package state, where all inventory entries are retained for synthesis and article preparation.
