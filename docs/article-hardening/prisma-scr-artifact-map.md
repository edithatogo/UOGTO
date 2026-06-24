# PRISMA-ScR Artifact Map

This file maps each PRISMA-ScR reporting item to the repository surfaces that carry the corresponding evidence. The protocol checklist uses the same item set; this file expands the rationale so the package can be inspected as a scoping-review evidence bundle rather than a single protocol note.

| # | PRISMA-ScR item | Primary repository artifacts | Notes |
| --- | --- | --- | --- |
| 1 | Title | `docs/article-hardening/protocol.md`; `docs/article-hardening/structured-summary.md`; `docs/article-hardening/protocol-checklist.md` | Frames the work as a scoping-review-style ontology evidence package. |
| 2 | Structured summary | `docs/article-hardening/structured-summary.md` | Provides the package-level abstracted summary. |
| 3 | Rationale | `docs/article-hardening/protocol.md` | States why article hardening is needed after the comparative mapping baseline. |
| 4 | Objectives | `docs/article-hardening/protocol.md` | Enumerates discovery, mapping, quality, competency, and article-evidence goals. |
| 5 | Protocol and registration | `docs/article-hardening/protocol.md`; `conductor/tracks/uogto_article_hardening_protocol_20260624/protocol-standard.md`; `docs/article-hardening/ro-crate-metadata.json` | Shows protocol standard, governance context, and packaged registration surface. |
| 6 | Eligibility criteria | `docs/article-hardening/protocol.md`; `docs/article-hardening/source-extension-inventory.json`; `docs/article-hardening/uogto-inclusion-decisions.md` | Carries the inclusion and exclusion rules used in screening. |
| 7 | Information sources | `docs/article-hardening/protocol.md`; `docs/article-hardening/search-strategy.md`; `docs/article-hardening/search-log.jsonl`; `docs/article-hardening/source-extension-inventory.md` | Lists the source families and discovery channels. |
| 8 | Search | `docs/article-hardening/search-strategy.md`; `docs/article-hardening/search-log.jsonl` | Records search routes, query families, and per-route evidence outcomes. |
| 9 | Selection of sources of evidence | `docs/article-hardening/source-extension-inventory.json`; `docs/article-hardening/source-extension-inventory.md`; `docs/article-hardening/manual-review-sample.csv`; `docs/article-hardening/reviews/phase-review-log.jsonl`; `docs/article-hardening/uogto-inclusion-decisions.md` | Holds screening and reviewer handoff evidence. |
| 10 | Data charting process | `docs/article-hardening/protocol.md`; `docs/article-hardening/quality-metrics.json`; `docs/article-hardening/source-extension-inventory.json` | Defines charting fields and preserves them in structured outputs. |
| 11 | Data items | `docs/article-hardening/protocol.md`; `docs/article-hardening/quality-metrics.json`; `docs/article-hardening/case-studies.json` | Splits evidence by source type, parseability, and mapping relevance. |
| 12 | Critical appraisal of individual sources of evidence | `docs/article-hardening/reasoner-report.md`; `docs/article-hardening/robot/report.md`; `docs/article-hardening/robot/reasoner-check.md`; `docs/article-hardening/quality-metrics.json` | Optional source-level quality appraisal. |
| 13 | Synthesis of results | `docs/article-hardening/protocol.md`; `docs/article-hardening/article-tables/`; `docs/article-hardening/figures/`; `docs/article-hardening/case-studies.md`; `docs/article-hardening/quality-metrics.json` | Collates the package-level synthesis surfaces. |
| 14 | Selection of sources of evidence (results) | `docs/article-hardening/search-log.jsonl`; `docs/article-hardening/manual-review-sample.csv`; `docs/article-hardening/reviews/phase-review-log.jsonl`; `docs/article-hardening/uogto-inclusion-decisions.md` | Captures the decision trail and resulting counts. |
| 15 | Characteristics of sources of evidence | `docs/article-hardening/source-extension-inventory.json`; `docs/article-hardening/source-extension-inventory.md`; `docs/article-hardening/case-studies.json`; `docs/article-hardening/quality-metrics.json` | Summarises the evidence base by family and metadata profile. |
| 16 | Critical appraisal within sources of evidence | `docs/article-hardening/reasoner-report.md`; `docs/article-hardening/robot/merge-diff.md`; `docs/article-hardening/robot/import-extraction.md` | Optional within-source or within-module appraisal surface. |
| 17 | Results of individual sources of evidence | `docs/article-hardening/source-extension-inventory.md`; `docs/article-hardening/case-studies.md`; `docs/article-hardening/article-tables/` | Provides source-level results and extracted descriptors. |
| 18 | Synthesis of results | `docs/article-hardening/article-tables/`; `docs/article-hardening/figures/`; `docs/article-hardening/quality-metrics.json`; `docs/article-hardening/use-case-coverage-matrix.csv` | Supports the comparative and network-style synthesis. |
| 19 | Summary of evidence | `docs/article-hardening/structured-summary.md`; `docs/article-hardening/case-studies.md`; `docs/article-hardening/article-tables/`; `docs/article-hardening/figures/` | Package-level evidence summary for article framing. |
| 20 | Limitations | `docs/article-hardening/protocol.md`; `docs/article-hardening/source-extension-inventory.md`; `docs/article-hardening/reasoner-report.md` | Records search drift, coverage gaps, licence issues, and evidence-strength limits. |
| 21 | Conclusions | `docs/article-hardening/protocol.md`; `docs/article-hardening/structured-summary.md`; `docs/article-hardening/prisma-scr-artifact-map.md` | States what the evidence package supports and where judgement remains. |
| 22 | Funding | `docs/article-hardening/protocol.md`; `docs/article-hardening/ro-crate-metadata.json` | Records funding and conflicts of interest status. |

## Use Notes

- The protocol checklist is the concise compliance surface.
- This map is the inspectable crosswalk used for article drafting and reviewer handoff.
- Both surfaces should stay aligned whenever new source families, evidence levels, or outputs are added.
| 23 | Source discovery flow diagram | `docs/article-hardening/figures/prisma-2020-source-discovery-flow.md` | PRISMA 2020-style discovery flow for search routes, records, and negative evidence. |
| 24 | Screening flow diagram | `docs/article-hardening/figures/prisma-2020-screening-flow.md` | PRISMA 2020-style screening flow for inclusion, exclusion, and retention. |
| 25 | Dual screening and adjudication | `docs/article-hardening/dual-screening.md`; `docs/article-hardening/dual-screening-sample.csv` | Simulated researcher-to-peer-to-red-team review chain for screening and disposition. |
| 26 | RO-Crate package output | `docs/article-hardening/ro-crate-package.md`; `docs/article-hardening/ro-crate-metadata.json` | Early RO-Crate package narrative and metadata surface. |

