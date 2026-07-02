# Cosmograph-ready network exports

These CSV files are generated from `docs/ontology-comparison/network-analysis.json` for interactive inspection in Cosmograph or another graph explorer.

Recommended Cosmograph import settings:
- Load an `*_edges.csv` file as links with `source` and `target` columns.
- Load the matching `*_nodes.csv` file as node metadata keyed by `id`.
- Use `weight` for link weight and `kind` / `degree` for color and size.

Exports:
- `source_similarity_nodes.csv` and `source_similarity_edges.csv`: source-family and source-similarity graph.
- `term_alignment_nodes.csv` and `term_alignment_edges.csv`: accepted term-alignment bipartite graph.
- `import_uses_nodes.csv` and `import_uses_edges.csv`: import/evidence-use graph.

Static graph images:
- `source_similarity_cosmograph.svg`: source-similarity graph rendering, with optional `.png` and `.pdf` derivatives when ImageMagick is available.
- `term_alignment_cosmograph.svg`: accepted term-alignment bipartite graph rendering, with optional `.png` and `.pdf` derivatives when ImageMagick is available.
- `import_uses_cosmograph.svg`: import/evidence-use graph rendering, with optional `.png` and `.pdf` derivatives when ImageMagick is available.

The manuscript uses static SVG/PDF-safe figures for arXiv, while these exports support interactive Cosmograph review.
