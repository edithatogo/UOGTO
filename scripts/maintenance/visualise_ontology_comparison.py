import argparse, csv, html, json, math
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DEFAULT_INVENTORY = ROOT / 'docs' / 'ontology-comparison' / 'source-inventory.json'
DEFAULT_REVIEW = ROOT / 'docs' / 'ontology-comparison' / 'mapping-review.csv'
DEFAULT_OVERLAP = ROOT / 'docs' / 'ontology-comparison' / 'overlap-metrics.json'
DEFAULT_NETWORK = ROOT / 'docs' / 'ontology-comparison' / 'network-analysis.json'
DEFAULT_PROVENANCE = ROOT / 'docs' / 'ontology-comparison' / 'source-provenance.json'
DEFAULT_FIGURES = ROOT / 'docs' / 'ontology-comparison' / 'figures'
DEFAULT_REPORT = ROOT / 'docs' / 'ontology-comparison' / 'report.md'
REQUIRED_FIGURES = ['source_sizes_bar.svg','match_classes_bar.svg','source_module_overlap_heatmap.svg','source_family_evidence_heatmap.svg','source_family_term_heatmap.svg','uogto_coverage_treemap.svg','source_similarity_network.svg','mapping_flow_sankey.svg','reviewer_workload.svg']


def load_json(path):
    return json.loads(Path(path).read_text(encoding='utf-8'))


def load_review(path):
    with Path(path).open('r', encoding='utf-8', newline='') as handle:
        return list(csv.DictReader(handle))


def esc(value):
    return html.escape(str(value), quote=True)


PALETTE = ['#0072B2', '#009E73', '#D55E00', '#CC79A7', '#E69F00', '#56B4E9', '#000000', '#999999']
SEQUENTIAL = ['#F7FBFF', '#DEEBF7', '#C6DBEF', '#9ECAE1', '#6BAED6', '#3182BD', '#08519C']


def scale_colour(value, max_value):
    if not value or not max_value:
        return SEQUENTIAL[0]
    idx = min(len(SEQUENTIAL) - 1, max(0, int(round((len(SEQUENTIAL) - 1) * value / max_value))))
    return SEQUENTIAL[idx]


def write_svg(path, width, height, body, title, caption=None):
    path.parent.mkdir(parents=True, exist_ok=True)
    caption = caption or title
    svg = '<svg xmlns="http://www.w3.org/2000/svg" width="{}" height="{}" viewBox="0 0 {} {}" role="img" aria-labelledby="title desc">\n'.format(width, height, width, height)
    svg += '<title id="title">{}</title><desc id="desc">{}</desc>'.format(esc(title), esc(caption))
    svg += '<style>text{font-family:Arial,Helvetica,sans-serif;fill:#1f2933}.tiny{font-size:12px}.small{font-size:14px}.label{font-size:15px}.title{font-size:24px;font-weight:700}.caption{font-size:14px;fill:#475569}.axis{stroke:#CBD5E1}.callout{font-size:14px;font-weight:700}</style><rect width="100%" height="100%" fill="#ffffff"/>\n'
    svg += body + '\n</svg>\n'
    path.write_text(svg, encoding='utf-8')


def bar_chart(path, title, rows, width=1200, caption=None):
    rows = rows[:20]
    height = 130 + max(1, len(rows)) * 44
    max_value = max([row['value'] for row in rows] or [1])
    parts = ['<text class="title" x="36" y="42">{}</text>'.format(esc(title))]
    if caption:
        parts.append('<text class="caption" x="36" y="70">{}</text>'.format(esc(caption)))
    parts.append('<line class="axis" x1="340" y1="88" x2="{}" y2="88"/>'.format(width - 70))
    for idx, row in enumerate(rows):
        y = 104 + idx * 44
        value = int(row['value'])
        w = 2 if max_value == 0 else int((width - 460) * value / max_value)
        colour = PALETTE[idx % len(PALETTE)]
        parts.append('<text class="label" x="36" y="{}">{}</text>'.format(y + 21, esc(row['label'][:38])))
        parts.append('<rect x="340" y="{}" width="{}" height="28" fill="{}" rx="3"/>'.format(y, w, colour))
        parts.append('<text class="small" x="{}" y="{}">{}</text>'.format(min(width - 70, 352 + w), y + 20, esc(value)))
    write_svg(path, width, height, '\n'.join(parts), title, caption)


def heatmap(path, title, rows):
    xs = sorted({row['uogto_source_id'] for row in rows})[:14]
    ys = sorted({row['source_id'] for row in rows})[:18]
    values = {(row['uogto_source_id'], row['source_id']): int(row['candidate_count']) for row in rows if row['uogto_source_id'] in xs and row['source_id'] in ys}
    max_value = max(values.values() or [1])
    cell_w, cell_h = 68, 34
    width, height = 300 + len(xs) * cell_w, 160 + len(ys) * cell_h
    parts = ['<text class="title" x="36" y="42">{}</text>'.format(esc(title)), '<text class="caption" x="36" y="72">Darker cells indicate more candidate mappings between a source and a UOGTO module.</text>']
    for i, x in enumerate(xs):
        anchor = 285 + i * cell_w
        parts.append('<text class="tiny" x="{}" y="116" transform="rotate(-45 {} 116)">{}</text>'.format(anchor, anchor, esc(x[:18])))
    for j, y in enumerate(ys):
        parts.append('<text class="small" x="36" y="{}">{}</text>'.format(150+j*cell_h, esc(y[:28])))
    for i, x in enumerate(xs):
        for j, y in enumerate(ys):
            value = values.get((x, y), 0)
            colour = scale_colour(value, max_value)
            parts.append('<rect x="{}" y="{}" width="{}" height="{}" fill="{}" stroke="#E2E8F0"/>'.format(260+i*cell_w, 126+j*cell_h, cell_w-3, cell_h-3, colour))
            if value:
                parts.append('<text class="tiny" x="{}" y="{}">{}</text>'.format(282+i*cell_w, 148+j*cell_h, value))
    parts.append('<text class="caption" x="36" y="{}">Scale: white to blue; labels show non-zero candidate counts.</text>'.format(height - 24))
    write_svg(path, width, height, '\n'.join(parts), title)


def evidence_heatmap(path, title, rows, x_order, y_order):
    values = {(row['evidence_level'], row['family']): int(row['value']) for row in rows}
    max_value = max(values.values() or [1])
    cell_w, cell_h = 138, 34
    width, height = 310 + len(x_order) * cell_w, 160 + len(y_order) * cell_h
    parts = ['<text class="title" x="36" y="42">{}</text>'.format(esc(title)), '<text class="caption" x="36" y="72">Evidence levels are separated so metadata-only coverage is not conflated with parsed RDF evidence.</text>']
    for i, x in enumerate(x_order):
        anchor = 294 + i * cell_w
        parts.append('<text class="tiny" x="{}" y="116" transform="rotate(-45 {} 116)">{}</text>'.format(anchor, anchor, esc(x[:24])))
    for j, y in enumerate(y_order):
        parts.append('<text class="small" x="36" y="{}">{}</text>'.format(150+j*cell_h, esc(y[:30])))
    for i, x in enumerate(x_order):
        for j, y in enumerate(y_order):
            value = values.get((x, y), 0)
            colour = scale_colour(value, max_value)
            parts.append('<rect x="{}" y="{}" width="{}" height="{}" fill="{}" stroke="#E2E8F0"/>'.format(276+i*cell_w, 126+j*cell_h, cell_w-3, cell_h-3, colour))
            if value:
                parts.append('<text class="tiny" x="{}" y="{}">{}</text>'.format(296+i*cell_w, 148+j*cell_h, value))
    parts.append('<text class="caption" x="36" y="{}">Colour scale: white to blue; numbers are source or term counts.</text>'.format(height - 24))
    write_svg(path, width, height, '\n'.join(parts), title)


def treemap(path, title, rows):
    rows = sorted(rows[:14], key=lambda row: (-row['value'], row['label']))
    width, height = 1180, 130 + max(1, len(rows)) * 38
    max_value = max([row['value'] for row in rows] or [1])
    parts = ['<text class="title" x="36" y="42">{}</text>'.format(esc(title)), '<text class="caption" x="36" y="72">Ranked bar view replaces the old treemap so small modules and exact values remain legible.</text>']
    for idx, row in enumerate(rows):
        y = 98 + idx * 38
        value = int(row['value'])
        w = int((width - 460) * value / max_value)
        parts.append('<text class="label" x="36" y="{}">{}</text>'.format(y + 20, esc(row['label'][:38])))
        parts.append('<rect x="340" y="{}" width="{}" height="24" fill="{}" rx="3"/>'.format(y, max(2, w), PALETTE[idx % len(PALETTE)]))
        parts.append('<text class="small" x="{}" y="{}">{} unique terms</text>'.format(min(width - 190, 352 + w), y + 18, value))
    write_svg(path, width, height, '\n'.join(parts), title)


def network_svg(path, title, graph):
    degree_map = graph.get('metrics', {}).get('degree', {})
    nodes = [node for node, _ in sorted(degree_map.items(), key=lambda item: (-item[1], item[0]))[:16]] or graph.get('nodes', [])[:16]
    label_nodes = set(nodes[:8])
    positions = {}
    width, height, cx, cy, radius = 1200, 820, 600, 430, 300
    for idx, node in enumerate(nodes):
        angle = 2 * math.pi * idx / max(1, len(nodes))
        positions[node] = (cx + radius * math.cos(angle), cy + radius * math.sin(angle))
    parts = ['<text class="title" x="36" y="42">{}</text>'.format(esc(title)), '<text class="caption" x="36" y="72">Only the highest-degree bridge sources are labelled; unlabelled nodes remain in the network for context.</text>']
    for left, right, value in graph.get('edges', [])[:120]:
        if left in positions and right in positions:
            x1, y1 = positions[left]; x2, y2 = positions[right]
            width_line = 0.8 + min(3.0, float(value) if isinstance(value, (int, float)) else 1.0)
            parts.append('<line x1="{:.1f}" y1="{:.1f}" x2="{:.1f}" y2="{:.1f}" stroke="#94A3B8" stroke-width="{:.1f}" opacity="0.42"/>'.format(x1,y1,x2,y2,width_line))
    for idx, node in enumerate(nodes):
        x, y = positions[node]
        degree = degree_map.get(node, 1)
        r = 10 + min(22, degree * 1.4)
        parts.append('<circle cx="{:.1f}" cy="{:.1f}" r="{}" fill="{}" opacity="0.94" stroke="#ffffff" stroke-width="2"/>'.format(x, y, r, PALETTE[idx % len(PALETTE)]))
        if node in label_nodes:
            lx = x + r + 8 if x < cx else x - r - 210
            parts.append('<text class="small" x="{:.1f}" y="{:.1f}">{}</text>'.format(lx, y + 5, esc(node[:30])))
    parts.append('<text class="caption" x="36" y="{}">Node size encodes degree. Labels show the top bridge sources only to preserve print readability.</text>'.format(height - 28))
    write_svg(path, width, height, '\n'.join(parts), title)


def sankey(path, title, rows):
    width, height = 1220, 660
    left = Counter(row['source_id'] for row in rows).most_common(8)
    mid = Counter(row['review_status'] for row in rows).most_common()
    right = Counter(row['uogto_source_id'] for row in rows).most_common(8)
    parts = ['<text class="title" x="36" y="42">{}</text>'.format(esc(title)), '<text class="caption" x="36" y="72">Denominators are mapping-candidate rows; accepted mappings are the asserted alignment subset.</text>']
    def column(items, x, label):
        parts.append('<text class="label" x="{}" y="102">{}</text>'.format(x, esc(label)))
        y, centers = 124, {}
        for idx, (name, count) in enumerate(items):
            h = 26 + min(120, count * 2)
            colour = '#009E73' if name == 'accepted' else ('#D55E00' if name == 'rejected' else PALETTE[idx % len(PALETTE)])
            parts.append('<rect x="{}" y="{}" width="190" height="{}" fill="{}" opacity="0.9" rx="4"/>'.format(x, y, h, colour))
            parts.append('<text class="small" x="{}" y="{}">{} ({})</text>'.format(x+10, y+20, esc(name[:22]), count))
            centers[name] = (x + 190, y + h / 2)
            y += h + 16
        return centers
    lc, mc, rc = column(left, 46, 'Source'), column(mid, 510, 'Review status'), column(right, 950, 'UOGTO module')
    for row in rows[:260]:
        if row['source_id'] in lc and row['review_status'] in mc:
            x1,y1=lc[row['source_id']]; x2,y2=mc[row['review_status']]
            parts.append('<path d="M{},{} C{},{} {},{} {},{}" fill="none" stroke="#64748B" stroke-width="0.7" opacity="0.28"/>'.format(x1,y1,x1+120,y1,x2-120,y2,x2,y2))
        if row['review_status'] in mc and row['uogto_source_id'] in rc:
            x1,y1=mc[row['review_status']]; x2,y2=rc[row['uogto_source_id']]
            parts.append('<path d="M{},{} C{},{} {},{} {},{}" fill="none" stroke="#94A3B8" stroke-width="0.7" opacity="0.24"/>'.format(x1,y1,x1+110,y1,x2-120,y2,x2-190,y2))
    write_svg(path, width, height, '\n'.join(parts), title)

def build_visualisation_data(inventory, review_rows, overlap, network, provenance=None):
    source_names = {source['id']: source.get('name', source['id']) for source in inventory.get('sources', [])}
    if not isinstance(provenance, dict):
        provenance = {}
    provenance_by_id = {record['id']: record for record in provenance.get('sources', [])}
    source_sizes = []
    evidence_source_rows = []
    evidence_term_rows = []
    evidence_totals = Counter()
    for source in inventory.get('sources', []):
        source_id = source['id']
        summary = overlap.get('descriptive_summaries', {}).get(source_id, {})
        prov = provenance_by_id.get(source_id, {})
        evidence = classify_evidence_level(source, prov)
        family = source.get('family', 'uncategorized')
        term_count = int(summary.get('term_count', 0) or 0)
        source_sizes.append({'label': source_names.get(source_id, source_id), 'value': term_count, 'source_id': source_id})
        evidence_source_rows.append({'family': family, 'evidence_level': evidence, 'value': 1})
        evidence_term_rows.append({'family': family, 'evidence_level': evidence, 'value': term_count})
        evidence_totals[evidence] += 1
    source_sizes.sort(key=lambda row: (-row['value'], row['label']))
    match_classes = Counter((row.get('decision_predicate') or row.get('candidate_predicate') or 'unclassified') for row in review_rows)
    review_workload = Counter(row.get('review_status', 'missing') for row in review_rows)
    module_rows = [{'label': row['uogto_source_id'], 'value': row['unique_terms']} for row in overlap.get('uogto_stronger_coverage_areas', [])]
    family_order = sorted({row['family'] for row in evidence_source_rows}, key=lambda family: (-sum(entry['value'] for entry in evidence_source_rows if entry['family'] == family), family))
    evidence_order = ['parsed_rdf', 'structured_non_rdf', 'metadata_only', 'transformed_summary_only', 'excluded', 'other']
    evidence_order = [level for level in evidence_order if level in evidence_totals or any(row['evidence_level'] == level for row in evidence_source_rows)]
    if not evidence_order:
        evidence_order = ['metadata_only']
    evidence_summary = {level: {'source_count': evidence_totals[level], 'term_count': sum(row['value'] for row in evidence_term_rows if row['evidence_level'] == level)} for level in evidence_order}
    return {'source_sizes': source_sizes, 'match_classes': [{'label': k, 'value': v} for k,v in sorted(match_classes.items(), key=lambda item: (-item[1], item[0]))], 'review_workload': [{'label': k, 'value': v} for k,v in sorted(review_workload.items(), key=lambda item: (-item[1], item[0]))], 'heat_rows': overlap.get('bidirectional_overlap', {}).get('source_by_uogto', []), 'module_rows': module_rows, 'network': network.get('source_similarity_graph', {}), 'family_evidence_source_rows': evidence_source_rows, 'family_evidence_term_rows': evidence_term_rows, 'family_order': family_order, 'evidence_order': evidence_order, 'evidence_summary': evidence_summary}


def classify_evidence_level(source, provenance):
    review_status = source.get('review_status')
    licence_disposition = source.get('licence_disposition')
    retrieval_mode = (provenance or {}).get('retrieval_mode')
    parse_status = (provenance or {}).get('parse_status')
    format_classification = (provenance or {}).get('format_classification')
    if review_status == 'excluded' or licence_disposition == 'excluded':
        return 'excluded'
    if licence_disposition == 'transformed_summary_only':
        return 'transformed_summary_only'
    if retrieval_mode == 'downloaded':
        if parse_status == 'parsed':
            return 'parsed_rdf'
        if format_classification == 'non_rdf_or_documentation':
            return 'structured_non_rdf'
        return 'parsed_rdf'
    if retrieval_mode == 'metadata_only':
        return 'metadata_only'
    if licence_disposition == 'needs_licence_review':
        return 'metadata_only'
    return 'other'


def render_report(path, inventory, review_rows, overlap, network, visualisation_data):
    summary, nsummary = overlap['summary'], network['summary']
    accepted = sum(1 for row in review_rows if row.get('review_status') == 'accepted')
    needs_review = sum(1 for row in review_rows if row.get('review_status') == 'needs_domain_review')
    rejected = sum(1 for row in review_rows if row.get('review_status') == 'rejected')
    figures = '\n'.join('- ![{}](figures/{})'.format(name, name) for name in REQUIRED_FIGURES)
    top_sources_md = '\n'.join('| `{}` | {} | {} |'.format(row['source_id'], row['unmatched_terms'], row['candidate_coverage']) for row in overlap.get('recommended_uogto_enhancement_areas', [])[:8])
    central_md = '\n'.join('| `{}` | {} |'.format(row['source_id'], row['centrality_score']) for row in network.get('central_source_families', [])[:8])
    evidence_rows = '\n'.join('| `{}` | {} | {} |'.format(level, counts['source_count'], counts['term_count']) for level, counts in visualisation_data['evidence_summary'].items())
    report = '# Comparative Simulation Ontology Mapping Report\n\n'
    report += '## Scope\nThis report summarises the reproducible comparison of public game-theory, simulation, agent-based modelling, system-dynamics, and adjacent modelling ontologies against UOGTO. It is generated from the track artifacts in `docs/ontology-comparison/`.\n\n'
    report += '## Methodology\nThe workflow uses the discovery protocol, source inventory, source provenance, normalized term inventory, deterministic mapping candidates, reviewed mappings, overlap metrics, and network analysis artifacts. Redistributable RDF sources are parsed directly; non-redistributable or standards-document sources are represented as metadata-only or transformed-summary records so the report does not overclaim source access.\n\n'
    licence_counts = Counter(source.get('licence_disposition', 'unspecified') for source in inventory.get('sources', []))
    licence_rows = '\n'.join('- {}'.format(key, value) for key, value in sorted(licence_counts.items()))
    report += '## Inclusion and Exclusion Summary\nThe discovery protocol records registry, repository, literature, and standards-body routes. Included records are retained when they are ontologies, vocabularies, schemas, metamodels, or formal standards that can inform game-theory or simulation semantics. Narrative-only or non-redistributable resources are not imported as ontology artifacts; they are kept as metadata-only or transformed-summary records where appropriate.\n\n{}\n\n'.format(licence_rows)
    report += '## Mapping Methods\nMapping candidates are generated from exact IRI matches, exact and normalized labels, synonym and token overlap, definition similarity, hierarchy context, property signatures, type compatibility, and source reliability. Only rows with `review_status` equal to `accepted` are emitted to `accepted-alignments.ttl`; rejected, deferred, and `needs_domain_review` rows remain candidate evidence and reviewer workload rather than asserted alignments.\n\n'
    report += '## Source Inventory\n- Candidate sources: {}\n- External terms: {}\n- UOGTO terms: {}\n- Review candidates: {}\n- Accepted mappings: {}\n\n'.format(len(inventory.get('sources', [])), summary['external_term_count'], summary['uogto_term_count'], summary['review_candidate_count'], accepted)
    report += '## Mapping Review Results\n- Accepted: {}\n- Needs domain review: {}\n- Rejected: {}\n\nThe accepted alignment TTL is evidence-backed by `mapping-review.csv`. Candidate and rejected rows remain audit records and should not be treated as asserted ontology alignments.\n\n'.format(accepted, needs_review, rejected)
    report += '## Overlap Findings\n| Source | Unmatched terms | Candidate coverage |\n| --- | ---: | ---: |\n{}\n\n'.format(top_sources_md)
    report += '## Network Findings\n- Source graph nodes: {}\n- Term-alignment bipartite edges: {}\n- Source-similarity edges: {}\n- UOGTO module coverage edges: {}\n\n| Central source or module | Centrality score |\n| --- | ---: |\n{}\n\n'.format(nsummary['source_graph_nodes'], nsummary['alignment_graph_edges'], nsummary['similarity_graph_edges'], nsummary['coverage_graph_edges'], central_md)
    report += '## Evidence-Level Coverage\nThe new heatmaps stratify source-family coverage by evidence level so metadata-only sources, downloaded RDF artifacts, and future transformed-summary or excluded records are not conflated. Source counts and term counts are shown separately to distinguish breadth from depth.\n\n| Evidence level | Source count | Term count |\n| --- | ---: | ---: |\n{}\n\n'.format(evidence_rows)
    report += '## Visualisations\n{}\n\n'.format(figures)
    report += '## Recommended UOGTO Follow-Up Work\n1. Treat accepted mappings as stable crosswalk evidence and keep `accepted-alignments.ttl` in sync with any future review edits.\n2. Prioritise high-volume unmatched sources as candidate extension-review areas rather than immediate equivalence assertions.\n3. Use `needs_domain_review` mappings as reviewer work queues for ontology architects and domain experts.\n4. Keep metadata-only standards separate from parsed RDF sources until their licences and formal artifacts permit stronger comparison.\n5. Re-run `make ontology-comparison-visuals` after any source, mapping, overlap, or network artifact changes.\n\n'
    report += '## Reproducibility\nRun `make ontology-comparison-visuals` to regenerate this report and the SVG figures from the JSON/CSV artifacts. The report intentionally separates accepted alignments from candidates and future-work recommendations.\n'
    path.write_text(report, encoding='utf-8')


def build_outputs(inventory, review_rows, overlap, network, provenance=None, figures_dir=DEFAULT_FIGURES, report_path=DEFAULT_REPORT):
    if isinstance(provenance, (str, Path)) and isinstance(figures_dir, (str, Path)) and report_path == DEFAULT_REPORT:
        report_path = Path(figures_dir)
        figures_dir = Path(provenance)
        provenance = {}
    data = build_visualisation_data(inventory, review_rows, overlap, network, provenance)
    figures_dir.mkdir(parents=True, exist_ok=True)
    bar_chart(figures_dir / 'source_sizes_bar.svg', 'External source sizes', data['source_sizes'])
    bar_chart(figures_dir / 'match_classes_bar.svg', 'Mapping predicate classes', data['match_classes'])
    heatmap(figures_dir / 'source_module_overlap_heatmap.svg', 'Source by UOGTO module overlap', data['heat_rows'])
    evidence_heatmap(figures_dir / 'source_family_evidence_heatmap.svg', 'Source-family coverage by evidence level (source count)', data['family_evidence_source_rows'], data['evidence_order'], data['family_order'])
    evidence_heatmap(figures_dir / 'source_family_term_heatmap.svg', 'Source-family coverage by evidence level (term count)', data['family_evidence_term_rows'], data['evidence_order'], data['family_order'])
    treemap(figures_dir / 'uogto_coverage_treemap.svg', 'UOGTO unique coverage areas', data['module_rows'])
    network_svg(figures_dir / 'source_similarity_network.svg', 'Source similarity network', data['network'])
    sankey(figures_dir / 'mapping_flow_sankey.svg', 'Mapping review flow', review_rows)
    bar_chart(figures_dir / 'reviewer_workload.svg', 'Reviewer workload by status', data['review_workload'])
    render_report(report_path, inventory, review_rows, overlap, network, data)
    return {'figures': [str(figures_dir / name) for name in REQUIRED_FIGURES], 'report': str(report_path)}


def validate_outputs(figures_dir=DEFAULT_FIGURES, report_path=DEFAULT_REPORT):
    missing = [name for name in REQUIRED_FIGURES if not (figures_dir / name).exists()]
    if missing:
        raise AssertionError('Missing visualisation figures: ' + ', '.join(missing))
    for name in REQUIRED_FIGURES:
        text = (figures_dir / name).read_text(encoding='utf-8')
        if '<svg' not in text or '</svg>' not in text:
            raise AssertionError('Figure is not valid SVG text: ' + name)
    report = report_path.read_text(encoding='utf-8')
    required = ['# Comparative Simulation Ontology Mapping Report','## Methodology','## Inclusion and Exclusion Summary','## Mapping Methods','## Source Inventory','## Mapping Review Results','## Overlap Findings','## Network Findings','## Evidence-Level Coverage','## Visualisations','## Recommended UOGTO Follow-Up Work','## Reproducibility']
    for section in required:
        if section not in report:
            raise AssertionError('Missing report section: ' + section)
    for name in REQUIRED_FIGURES:
        if 'figures/' + name not in report:
            raise AssertionError('Report does not link figure: ' + name)
    return {'figure_count': len(REQUIRED_FIGURES), 'report': str(report_path)}


def main():
    parser = argparse.ArgumentParser(description='Generate ontology comparison figures and report.')
    parser.add_argument('--inventory', type=Path, default=DEFAULT_INVENTORY)
    parser.add_argument('--review', type=Path, default=DEFAULT_REVIEW)
    parser.add_argument('--overlap', type=Path, default=DEFAULT_OVERLAP)
    parser.add_argument('--network', type=Path, default=DEFAULT_NETWORK)
    parser.add_argument('--provenance', type=Path, default=DEFAULT_PROVENANCE)
    parser.add_argument('--figures-dir', type=Path, default=DEFAULT_FIGURES)
    parser.add_argument('--report', type=Path, default=DEFAULT_REPORT)
    parser.add_argument('--check-only', action='store_true')
    args = parser.parse_args()
    if not args.check_only:
        build_outputs(load_json(args.inventory), load_review(args.review), load_json(args.overlap), load_json(args.network), load_json(args.provenance), args.figures_dir, args.report)
    summary = validate_outputs(args.figures_dir, args.report)
    print('Ontology comparison visuals valid: {} figures, report {}'.format(summary['figure_count'], summary['report']))


if __name__ == '__main__':
    main()
