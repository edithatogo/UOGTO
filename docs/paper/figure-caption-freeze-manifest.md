# Figure and Caption Freeze Manifest

Generated: `2026-06-25T11:53:28+00:00`
Status: `frozen`

This manifest freezes manuscript and supplement figure numbering, caption intent, placement callouts, rendered/source file hashes, and image score-loop status. If any frozen surface changes, rerun the image scoring loop before submission.

## Rerun Triggers

- manuscript Figure~\ref callouts change
- supplementary figure numbering S1-S7 changes
- caption/title text changes
- source_path or rendered_path changes in image_scores.csv
- any source or rendered figure file hash changes
- any image score drops below 100/100
- manuscript, supplement, or deck placement changes

## Main Manuscript Figure Callouts

| Label | Frozen caption intent |
| --- | --- |
| `fig:architecture` | Semantic separation among game specifications, sessions, traces, strategies, actions, payoffs, outcomes, mechanisms, and execution bindings. |
| `fig:evidence-heatmap` | Source-family evidence levels separating parsed RDF from structured non-RDF, metadata-only, and literature-only evidence. |
| `fig:mapping-flow` | Candidate-to-review-to-alignment flow for conservative ontology mappings. |
| `fig:network-sensitivity` | Network-sensitivity view showing bridge concepts and evidence limits. |
| `fig:reproducibility` | Reproducibility chain from ontology source to validation, mapping, tables, and submission gates. |

## Supplementary Figures

| Number | Title | Primary file |
| --- | --- | --- |
| Supplementary Figure S1 | PRISMA-style source discovery flow | `docs/article-hardening/figures/prisma-2020-source-discovery-flow.svg` |
| Supplementary Figure S2 | PRISMA-style screening flow | `docs/article-hardening/figures/prisma-2020-screening-flow.svg` |
| Supplementary Figure S3 | Source-family evidence-level heatmap | `docs/ontology-comparison/figures/source_family_evidence_heatmap.svg` |
| Supplementary Figure S4 | Mapping flow from candidates to decisions | `docs/ontology-comparison/figures/mapping_flow_sankey.svg` |
| Supplementary Figure S5 | Source-module overlap heatmap | `docs/ontology-comparison/figures/source_module_overlap_heatmap.svg` |
| Supplementary Figure S6 | Source similarity network | `docs/ontology-comparison/figures/source_similarity_network.svg` |
| Supplementary Figure S7 | Reviewer workload and mapping review distribution | `docs/ontology-comparison/figures/reviewer_workload.svg` |

## Image Score Freeze

| Image ID | Rendered path | Score | Source SHA-256 | Rendered SHA-256 |
| --- | --- | ---: | --- | --- |
| `ontology-source-sizes` | `docs/ontology-comparison/figures/source_sizes_bar.svg` | 100 | `3c94ed9eb40db3889917d46ad52c7229f41396031e60b77065df0b7fce5f70d1` | `3c94ed9eb40db3889917d46ad52c7229f41396031e60b77065df0b7fce5f70d1` |
| `match-classes` | `docs/ontology-comparison/figures/match_classes_bar.svg` | 100 | `0da194e3a998d736ff923778b69d69042136f8361c26bcfb3d74e219bd06e154` | `0da194e3a998d736ff923778b69d69042136f8361c26bcfb3d74e219bd06e154` |
| `reviewer-workload` | `docs/ontology-comparison/figures/reviewer_workload.svg` | 100 | `bad498f6214a40d0e5dafcb4792ac7f863fb134933774803329ef9538b322bde` | `bad498f6214a40d0e5dafcb4792ac7f863fb134933774803329ef9538b322bde` |
| `source-family-evidence` | `docs/ontology-comparison/figures/source_family_evidence_heatmap.svg` | 100 | `3b90c8600d37440dd03244949e573df326f2c880edf415e8b91dcbd887c462af` | `3b90c8600d37440dd03244949e573df326f2c880edf415e8b91dcbd887c462af` |
| `source-family-terms` | `docs/ontology-comparison/figures/source_family_term_heatmap.svg` | 100 | `36a6c9a1bc1537d8af436ab4467ca95fd0d7b0b4d311076ec54e9d15a47da9a1` | `36a6c9a1bc1537d8af436ab4467ca95fd0d7b0b4d311076ec54e9d15a47da9a1` |
| `source-module-overlap` | `docs/ontology-comparison/figures/source_module_overlap_heatmap.svg` | 100 | `1712592363b27f2741c9e80353e41d7983ddae4d925cb0bf4bf49c69b6f2f864` | `1712592363b27f2741c9e80353e41d7983ddae4d925cb0bf4bf49c69b6f2f864` |
| `source-similarity-network` | `docs/ontology-comparison/figures/source_similarity_network.svg` | 100 | `c38e579bea50a33044790b9d7755ea21f5404ab5605a33e6fb8514fc2972cc81` | `c38e579bea50a33044790b9d7755ea21f5404ab5605a33e6fb8514fc2972cc81` |
| `mapping-flow` | `docs/ontology-comparison/figures/mapping_flow_sankey.svg` | 100 | `24e77caf87fb7c2f7e39e43961c87072c08488b3561a795c9b96f95402f773b3` | `24e77caf87fb7c2f7e39e43961c87072c08488b3561a795c9b96f95402f773b3` |
| `uogto-coverage` | `docs/ontology-comparison/figures/uogto_coverage_treemap.svg` | 100 | `795d7d6fea38050d69046eca3542ae68c3274a5cd15a10f716ac3ab01e334362` | `795d7d6fea38050d69046eca3542ae68c3274a5cd15a10f716ac3ab01e334362` |
| `prisma-source-discovery` | `docs/article-hardening/figures/prisma-2020-source-discovery-flow.pdf` | 100 | `d27bdea0aebf3f75da2c257539405294bb64ba7486179791210eb0f0e3f918c5` | `cded4402de29dfa824efcac723c2b82165edab51e3131887a6295dc37525e4dd` |
| `prisma-screening` | `docs/article-hardening/figures/prisma-2020-screening-flow.pdf` | 100 | `a5b3d23a331f223681bc6b1a1f784438438556f3fc5f5d91cdac4778c6f38b11` | `30adba3a5ed393bf9793a2a713727f378d112915c977846dc113137ecc1622fe` |

## Validation

- PASS: all frozen image score rows are 100/100, source/rendered files exist, supplement figures S1-S7 match the frozen numbering, and manuscript callouts match the frozen labels.
