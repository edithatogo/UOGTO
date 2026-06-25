# Review Matrix

First-pass Nature presubmission review executed on 2026-06-25. Manuscript row updated after full article rewrite and manuscript source checks. Supplement row updated after final journal-style supplement prose, table/figure numbering, SourceRight, and Authentext checks.

| Surface | Reviewer Lane | Score | Status | Priority | Main Finding |
| --- | --- | ---: | --- | --- | --- |
| GitHub documentation | FAIR/reproducibility | 82 | Reviewed | Should-fix | Good documentation and citation guidance; add reviewer quickstart evidence checklist. |
| Repository setup | FAIR/reproducibility | 88 | Reviewed | Should-fix | Validation is green and pytest imports are fixed; document expected command outputs. |
| Ontology core | Ontology engineering | 86 | Reviewed | Should-fix | Core validates with SHACL and examples; add module-level audit table for article review. |
| Game theory coverage | Game-theory professor | 84 | Reviewed | Should-fix | Broad coverage exists; turn missing-element triage into explicit claim boundaries. |
| Simulation and executable semantics | Simulation methods | 81 | Reviewed | Should-fix | Representation exists; add end-to-end trace case studies per major simulation family. |
| Source discovery evidence | FAIR/reproducibility | 87 | Reviewed | Should-fix | Evidence register and RO-Crate surfaces exist; keep live searches and dashboard fresh. |
| Mapping and robustness analyses | Statistics/network analysis | 83 | Reviewed | Should-fix | SSSOM and sensitivity artifacts exist; article needs compact robustness narrative. |
| Manuscript | Nature editorial | 72 | Rewritten | Should-fix | Full article draft now exists; still needs figure integration, editorial polish, and supplement alignment. |
| Supplement | Nature editorial | 90 | Final prose | Should-fix | Supplement now has journal-style sections, Supplementary Tables S1-S11, Supplementary Figures S1-S7, a claim-to-supplement map, SourceRight evidence, and Authentext pass; final numbering should be frozen after manuscript copyedit. |
| PowerPoint | Visual communications | 84 | Status reconciled | Should-fix | The eight-slide editorial deck exists in docs/presentation; privacy audit evidence exists; manuscript/supplement figures are improved to 100, while deck thumbnail export, final figure binding, and readability inspection remain. |
| Red-team objections | Devil's advocate | 64 | Reviewed | Must-fix | Main risk is overclaiming relative to manuscript maturity and review depth. |
| arXiv toolchain hardening | arXiv toolchain | 88 | Reviewed | Should-fix | CI gate passes; missing local external tools are optional advisory benchmarking only. |
| arXiv source leak privacy audit | arXiv toolchain | 78 | Reviewed | Should-fix | CI lane passes; add explicit privacy audit manifest instead of relying on cleaner inference. |

<!-- arxiv-privacy-audit-update -->

### arXiv Source-Leak/Privacy Audit Update

Implemented `docs/paper/arxiv-source-privacy-audit.json` and `docs/paper/arxiv-source-privacy-audit.md` as explicit audit evidence for comments, hidden files, private notes/referee material, unused figures, aux/log/output files, embedded metadata, credentials, and private URLs/local paths. The audit is wired into `arxiv-privacy-audit` and `arxiv-preflight`; missing local external tools remain advisory, not blockers, because CI arXiv preflight is green.
