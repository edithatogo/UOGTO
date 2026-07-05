# Repository-only network graph visualisation supplement

This supplement records the actual graph visualisations used to support the manuscript's network-analysis claims. It complements the compact arXiv appendix figures by linking the static graph renders and the Cosmograph-ready node and edge tables.

These figures are exploratory review artefacts. They help readers inspect bridge structure, source overlap, sparse accepted alignments, and evidence-source separation. They do not prove semantic equivalence between game-theory traditions, and they should be interpreted with the network-sensitivity outputs.

## Graph visualisation inventory

| View | Static graph render | Interactive inputs | Main interpretation |
| --- | --- | --- | --- |
| Source-similarity graph | [`source_similarity_cosmograph.svg`](../ontology-comparison/cosmograph/source_similarity_cosmograph.svg); [`png`](../ontology-comparison/cosmograph/source_similarity_cosmograph.png); [`pdf`](../ontology-comparison/cosmograph/source_similarity_cosmograph.pdf) | [`source_similarity_nodes.csv`](../ontology-comparison/cosmograph/source_similarity_nodes.csv); [`source_similarity_edges.csv`](../ontology-comparison/cosmograph/source_similarity_edges.csv) | Shows overlap among UOGTO modules and comparator source families. Useful for identifying bridge modules and review priorities. |
| Accepted term-alignment graph | [`term_alignment_cosmograph.svg`](../ontology-comparison/cosmograph/term_alignment_cosmograph.svg); [`png`](../ontology-comparison/cosmograph/term_alignment_cosmograph.png); [`pdf`](../ontology-comparison/cosmograph/term_alignment_cosmograph.pdf) | [`term_alignment_nodes.csv`](../ontology-comparison/cosmograph/term_alignment_nodes.csv); [`term_alignment_edges.csv`](../ontology-comparison/cosmograph/term_alignment_edges.csv) | Shows the deliberately sparse accepted UOGTO-to-external alignments after conservative mapping review. |
| Import and evidence-use graph | [`import_uses_cosmograph.svg`](../ontology-comparison/cosmograph/import_uses_cosmograph.svg); [`png`](../ontology-comparison/cosmograph/import_uses_cosmograph.png); [`pdf`](../ontology-comparison/cosmograph/import_uses_cosmograph.pdf) | [`import_uses_nodes.csv`](../ontology-comparison/cosmograph/import_uses_nodes.csv); [`import_uses_edges.csv`](../ontology-comparison/cosmograph/import_uses_edges.csv) | Separates parsed artefacts from metadata-only, literature, documentation, and repository evidence surfaces. |

## Figure NG1. Source-similarity graph

![Source-similarity Cosmograph render](../ontology-comparison/cosmograph/source_similarity_cosmograph.svg)

The source-similarity graph contains 69 source or module nodes and 391 weighted overlap edges. It is useful because the manuscript's textual centrality summary can otherwise hide the actual graph shape. Dense regions should be read as evidence of shared vocabulary, import, format, or coverage signals, not as proof that two sources use the same semantics.

## Figure NG2. Accepted term-alignment graph

![Accepted term-alignment Cosmograph render](../ontology-comparison/cosmograph/term_alignment_cosmograph.svg)

The accepted term-alignment graph contains 12 accepted bipartite edges. Its sparseness is informative: UOGTO retains most candidate mappings as rejected or non-asserted evidence rather than converting lexical proximity into asserted equivalence.

## Figure NG3. Import and evidence-use graph

![Import and evidence-use Cosmograph render](../ontology-comparison/cosmograph/import_uses_cosmograph.svg)

The import and evidence-use graph contains 74 nodes in the source/evidence view. It distinguishes parsed RDF/OWL artefacts from structured non-RDF, metadata-only, literature-only, and documentation evidence. This separation is important for the manuscript's claim discipline because documentary relevance and parsed semantic reuse support different strengths of inference.

## How to inspect interactively

1. Open Cosmograph or another graph viewer that accepts node and edge CSV files.
2. Load the matching `*_nodes.csv` and `*_edges.csv` pair from `docs/ontology-comparison/cosmograph/`.
3. Use `node_kind`, `degree`, `source_family`, `evidence_level`, `edge_kind`, and `weight` fields to reproduce the source-similarity, term-alignment, or evidence-use view.
4. Compare any centrality or bridge interpretation against [`network-sensitivity.md`](../ontology-comparison/network-sensitivity.md) before promoting it to a manuscript claim.

## Manuscript relationship

The arXiv manuscript now includes PDF copies of the three actual graph renders in Appendix Figures A3 to A5. This repository supplement remains the richer audit surface because it includes SVG and PNG renders plus the underlying node and edge tables.
