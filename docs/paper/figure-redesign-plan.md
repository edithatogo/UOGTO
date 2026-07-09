# Paper Figure Redesign Plan

Date: 2026-07-07

This plan covers the paper figures that currently look weakest in print: the
PRISMA-style source-discovery flow, the roadmap diagram, and the appendix
network/graph figures.

## Current Assessment

- Figure 1 is readable but is not close enough to a standard PRISMA/PRISMA-ScR
  flow layout. It mixes source discovery, comparative source selection, term
  extraction, mapping review, accepted alignments, and negative evidence in a
  custom graph.
- Figure 2 had overlapping/crowded boxes because long module labels were placed
  inside a side-by-side TikZ layout. This has been fixed in `paper.tex`.
- Appendix network figures are generated from a custom SVG renderer in
  `scripts/maintenance/visualise_ontology_comparison.py`. The renderer uses
  simple circular/ring layouts, so it cannot handle clusters, dense edges, or
  label placement well.
- Cosmograph-ready CSV exports are useful for interactive review, but the paper
  needs publication-specific static summaries.

## Recommended Libraries

1. Static network figures for arXiv/PDF:
   - Use `networkx` for graph construction, filtering, metrics, and deterministic
     layouts.
   - Use `matplotlib` for PDF/SVG output because it is reproducible in CI and
     easy to package for arXiv.
   - Add `adjustText` only if label collision remains a problem after limiting
     labels to high-information nodes.
   - Keep Graphviz/pygraphviz optional. Graphviz `sfdp` or `dot` can produce
     better layouts, but pygraphviz is more fragile on Windows and should not be
     required for the main validation path.

2. Interactive graph inspection:
   - Keep the existing Cosmograph CSV exports as the interactive review surface.
   - Do not make Cosmograph the source of the manuscript figures. It is excellent
     for exploration, but less suitable as a deterministic arXiv build input.

3. PRISMA-style flow:
   - The CTAN `prisma-flow-diagram` package is a TikZ abstraction for PRISMA
     2009 flow diagrams: <https://ctan.org/pkg/prisma-flow-diagram>.
   - Its GitHub README includes an Overleaf-oriented example and TikZ command
     API: <https://github.com/ezefranca/prisma-flow-diagram>.
   - The official PRISMA 2020 site provides flow templates and says different
     templates apply depending on review type and source type:
     <https://www.prisma-statement.org/prisma-2020-flow-diagram>.
   - Recommendation: adapt the PRISMA 2020/PRISMA-ScR structure in local TikZ
     rather than adding a new `.sty` dependency. The current workflow is a
     scoping search for ontology-design evidence, not a full intervention
     systematic review.

## Figure-Specific Plan

### Figure 1: PRISMA-Style Source-Discovery Flow

Goal: make this read like a scoping-review search flow without implying that the
project ran a full dual-screened systematic review.

Implementation:

1. Define a local TikZ style block for PRISMA-like figures in `paper.tex` or a
   small included `figures/prisma-flow.tex` file.
2. Use four visual bands: Identification, Screening/eligibility, Included for
   source register, Included for comparative mapping.
3. Keep UOGTO-specific branches:
   - 7 search records: 6 inclusion routes and 1 negative route.
   - 39 retained source records.
   - 21 comparative sources across 17 source families.
   - 4,046 normalized term rows.
   - 460 mapping candidates reviewed.
   - 12 accepted alignments.
   - 448 rejected or non-asserted mapping rows.
4. Put negative evidence in a right-side exclusion/non-assertion box so readers
   see it as a deliberate review output, not a failure count.
5. Render and inspect the PDF page after compilation.

### Figure 2: Economics-Facing Extension Roadmap

Status: implemented in `docs/paper/paper.tex`.

The revised layout uses three top-stage boxes and a wide module-evidence box
below. It removes the previous side-by-side overlap and gives the module list
its own space.

### Appendix Network Figures

Status: implemented in `scripts/maintenance/visualise_ontology_comparison.py`.

Goal: replace dense graph screenshots with three print-purpose figures that
answer specific reader questions.

Recommended replacements:

1. Source-similarity graph:
   - Render a backbone network: maximum spanning tree plus top weighted edges
     per node or per community.
   - Color nodes by kind: UOGTO module, external source family, evidence group.
   - Size nodes by degree or weighted degree.
   - Label only high-degree bridge nodes and named UOGTO modules.
   - Include a small legend and an explicit "edges show overlap signals" note.

2. Accepted term-alignment graph:
   - Use a bipartite left-right layout, not a force-directed graph.
   - Left side: external/source terms.
   - Right side: UOGTO terms.
   - Edge labels or grouped edge color should show accepted mapping type when
     available.
   - This should emphasize sparseness as a design result.

3. Import/evidence-use graph:
   - Use a layered graph rather than a force graph.
   - Suggested layers: evidence level -> source family -> UOGTO module or review
     output.
   - Metadata-only and literature-only evidence should be visually separated
     from parsed RDF/OWL artefacts.

Implementation status:

1. `visualise_ontology_comparison.py` now uses graph-specific static renderers
   for source similarity, accepted term alignments, and import/evidence use.
2. The implementation stays dependency-light by using the existing deterministic
   SVG renderer plus ImageMagick PDF/PNG derivatives. This avoids adding
   optional graph-layout dependencies to the arXiv build path.
3. The default `make ontology-comparison-visuals` path now syncs the generated
   PDF derivatives to the manuscript figure names under `docs/paper/figures/`.
4. Appendix captions in `paper.tex` describe what each graph does and does not
   claim.
5. `tests/test_ontology_visuals.py` covers the paper-PDF sync naming contract.

Future enhancement:

1. If the graphs grow substantially, add a dedicated `networkx`/`matplotlib`
   renderer for backbone extraction and community-aware labeling.
2. Add a visual QA step that renders appendix pages from `docs/paper/paper.pdf`
   and checks that figures are non-empty and page-bounded.

## Validation Checklist

- `pixi run ontology-comparison-visuals`
- `pixi run manuscript-pdf`
- Render affected PDF pages with Poppler and inspect them.
- Check that arXiv source packaging includes only referenced figure files.
- Confirm captions state that graph bridges are review priorities, not semantic
  equivalence claims.
