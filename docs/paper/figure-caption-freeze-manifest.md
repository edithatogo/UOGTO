# Figure and Caption Freeze Manifest

Generated: `2026-07-05T08:54:49+00:00`
Status: `frozen`

This manifest freezes manuscript and supplement figure numbering, caption intent, placement callouts, rendered/source file hashes, and image score-loop status. If any frozen surface changes, rerun the image scoring loop before submission.

## Rerun Triggers

- manuscript Figure~\ref callouts change
- supplementary figure numbering S1-S13 changes
- caption/title text changes
- source_path or rendered_path changes in image_scores.csv
- any source or rendered figure file hash changes
- any image score drops below 100/100
- manuscript, supplement, or deck placement changes

## Main Manuscript Figure Callouts

| Label | Frozen caption intent |
| --- | --- |
| `fig:systematic-search-prisma-flow` | Search, screening, and mapping-review flow from source discovery to accepted and rejected mapping evidence. |

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
| Supplementary Figure S8 | ArXiv-safe mapping flow summary | `docs/paper/paper.tex` |
| Supplementary Figure S9 | ArXiv-safe network-analysis summary | `docs/paper/paper.tex` |
| Supplementary Figure S10 | Economics-facing module roadmap | `docs/paper/paper.tex` |
| Supplementary Figure S11 | Cosmograph source-similarity graph image | `docs/ontology-comparison/cosmograph/source_similarity_cosmograph.svg` |
| Supplementary Figure S12 | Cosmograph accepted term-alignment graph image | `docs/ontology-comparison/cosmograph/term_alignment_cosmograph.svg` |
| Supplementary Figure S13 | Cosmograph import and evidence-use graph image | `docs/ontology-comparison/cosmograph/import_uses_cosmograph.svg` |

## Image Score Freeze

| Image ID | Rendered path | Score | Source SHA-256 | Rendered SHA-256 |
| --- | --- | ---: | --- | --- |
| `ontology-source-sizes` | `docs/ontology-comparison/figures/source_sizes_bar.svg` | 100 | `3c94ed9eb40db3889917d46ad52c7229f41396031e60b77065df0b7fce5f70d1` | `3c94ed9eb40db3889917d46ad52c7229f41396031e60b77065df0b7fce5f70d1` |
| `match-classes` | `docs/ontology-comparison/figures/match_classes_bar.svg` | 100 | `ef3108abec1fd1878aa3369730c070dd7b47936c8c3d6d56777d3a36e6e3e808` | `ef3108abec1fd1878aa3369730c070dd7b47936c8c3d6d56777d3a36e6e3e808` |
| `reviewer-workload` | `docs/ontology-comparison/figures/reviewer_workload.svg` | 100 | `d593050ee803d1a6530688f03556ce544deff9fc06d14e19025ec3e42acc59f5` | `d593050ee803d1a6530688f03556ce544deff9fc06d14e19025ec3e42acc59f5` |
| `source-family-evidence` | `docs/ontology-comparison/figures/source_family_evidence_heatmap.svg` | 100 | `3b90c8600d37440dd03244949e573df326f2c880edf415e8b91dcbd887c462af` | `3b90c8600d37440dd03244949e573df326f2c880edf415e8b91dcbd887c462af` |
| `source-family-terms` | `docs/ontology-comparison/figures/source_family_term_heatmap.svg` | 100 | `36a6c9a1bc1537d8af436ab4467ca95fd0d7b0b4d311076ec54e9d15a47da9a1` | `36a6c9a1bc1537d8af436ab4467ca95fd0d7b0b4d311076ec54e9d15a47da9a1` |
| `source-module-overlap` | `docs/ontology-comparison/figures/source_module_overlap_heatmap.svg` | 100 | `2523d587d6e6534d4494c7fd0dec9a371c2f0fdc585061dff5c1682bc3ff2f6c` | `2523d587d6e6534d4494c7fd0dec9a371c2f0fdc585061dff5c1682bc3ff2f6c` |
| `source-similarity-network` | `docs/ontology-comparison/figures/source_similarity_network.svg` | 100 | `c38e579bea50a33044790b9d7755ea21f5404ab5605a33e6fb8514fc2972cc81` | `c38e579bea50a33044790b9d7755ea21f5404ab5605a33e6fb8514fc2972cc81` |
| `mapping-flow` | `docs/ontology-comparison/figures/mapping_flow_sankey.svg` | 100 | `771cf6d73812cb0c6494030876207c8e1dee2bf01592a71127cb167bf627965a` | `771cf6d73812cb0c6494030876207c8e1dee2bf01592a71127cb167bf627965a` |
| `uogto-coverage` | `docs/ontology-comparison/figures/uogto_coverage_treemap.svg` | 100 | `795d7d6fea38050d69046eca3542ae68c3274a5cd15a10f716ac3ab01e334362` | `795d7d6fea38050d69046eca3542ae68c3274a5cd15a10f716ac3ab01e334362` |
| `prisma-source-discovery` | `docs/article-hardening/figures/prisma-2020-source-discovery-flow.pdf` | 100 | `7d9e81be37082e1142a8e7a22370959712326819014ca3b147621f5a653dd463` | `cded4402de29dfa824efcac723c2b82165edab51e3131887a6295dc37525e4dd` |
| `prisma-screening` | `docs/article-hardening/figures/prisma-2020-screening-flow.pdf` | 100 | `df23162e4452728e4a52d3692d29b6fdb5d5c5c620639a65a26c017a13bc522f` | `30adba3a5ed393bf9793a2a713727f378d112915c977846dc113137ecc1622fe` |

## Validation

- PASS: all frozen image score rows are 100/100, source/rendered files exist, supplement figures S1-S13 match the frozen numbering, and manuscript callouts match the frozen labels.
