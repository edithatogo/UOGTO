import argparse, csv, html, json, math
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DEFAULT_INVENTORY = ROOT / 'docs' / 'ontology-comparison' / 'source-inventory.json'
DEFAULT_REVIEW = ROOT / 'docs' / 'ontology-comparison' / 'mapping-review.csv'
DEFAULT_OVERLAP = ROOT / 'docs' / 'ontology-comparison' / 'overlap-metrics.json'
DEFAULT_NETWORK = ROOT / 'docs' / 'ontology-comparison' / 'network-analysis.json'
DEFAULT_FIGURES = ROOT / 'docs' / 'ontology-comparison' / 'figures'
DEFAULT_REPORT = ROOT / 'docs' / 'ontology-comparison' / 'report.md'
REQUIRED_FIGURES = ['source_sizes_bar.svg','match_classes_bar.svg','source_module_overlap_heatmap.svg','uogto_coverage_treemap.svg','source_similarity_network.svg','mapping_flow_sankey.svg','reviewer_workload.svg']
PALETTE = ['#24536b', '#4f7c45', '#a65f2a', '#7a4f8f', '#b44b4b', '#3d6fa8', '#8a6b2e', '#4c6b5f']


def load_json(path):
    return json.loads(Path(path).read_text(encoding='utf-8'))


def load_review(path):
    with Path(path).open('r', encoding='utf-8', newline='') as handle:
        return list(csv.DictReader(handle))


def esc(value):
    return html.escape(str(value), quote=True)


def write_svg(path, width, height, body, title):
    path.parent.mkdir(parents=True, exist_ok=True)
    svg = '<svg xmlns="http://www.w3.org/2000/svg" width="{}" height="{}" viewBox="0 0 {} {}" role="img">\n'.format(width, height, width, height)
    svg += '<title>{}</title><style>text{{font-family:Arial,sans-serif;fill:#1f2933}} .small{{font-size:11px}} .label{{font-size:12px}} .title{{font-size:18px;font-weight:700}}</style><rect width="100%" height="100%" fill="#ffffff"/>\n'.format(esc(title))
    svg += body + '\n</svg>\n'
    path.write_text(svg, encoding='utf-8')


def bar_chart(path, title, rows, width=980):
    rows = rows[:20]
    height = 90 + max(1, len(rows)) * 34
    max_value = max([row['value'] for row in rows] or [1])
    parts = ['<text class="title" x="28" y="34">{}</text>'.format(esc(title))]
    for idx, row in enumerate(rows):
        y = 62 + idx * 34
        value = row['value']
        w = 1 if max_value == 0 else int((width - 320) * value / max_value)
        colour = PALETTE[idx % len(PALETTE)]
        parts.append('<text class="label" x="28" y="{}">{}</text>'.format(y + 16, esc(row['label'][:34])))
        parts.append('<rect x="260" y="{}" width="{}" height="24" fill="{}" rx="2"/>'.format(y, w, colour))
        parts.append('<text class="small" x="{}" y="{}">{}</text>'.format(268 + w, y + 16, esc(value)))
    write_svg(path, width, height, '\n'.join(parts), title)


def heatmap(path, title, rows):
    xs = sorted({row['uogto_source_id'] for row in rows})[:14]
    ys = sorted({row['source_id'] for row in rows})[:18]
    values = {(row['uogto_source_id'], row['source_id']): int(row['candidate_count']) for row in rows if row['uogto_source_id'] in xs and row['source_id'] in ys}
    max_value = max(values.values() or [1])
    cell_w, cell_h = 54, 28
    width, height = 220 + len(xs) * cell_w, 120 + len(ys) * cell_h
    parts = ['<text class="title" x="28" y="34">{}</text>'.format(esc(title))]
    for i, x in enumerate(xs):
        parts.append('<text class="small" x="{}" y="88" transform="rotate(-45 {} 88)">{}</text>'.format(210+i*cell_w, 210+i*cell_w, esc(x[:18])))
    for j, y in enumerate(ys):
        parts.append('<text class="small" x="28" y="{}">{}</text>'.format(112+j*cell_h, esc(y[:26])))
    for i, x in enumerate(xs):
        for j, y in enumerate(ys):
            value = values.get((x, y), 0)
            intensity = 0 if max_value == 0 else value / max_value
            colour = 'rgb({},{},{})'.format(245 - int(145 * intensity), 245 - int(82 * intensity), 245 - int(15 * intensity))
            parts.append('<rect x="{}" y="{}" width="{}" height="{}" fill="{}" stroke="#d9e2ec"/>'.format(190+i*cell_w, 94+j*cell_h, cell_w-2, cell_h-2, colour))
            if value:
                parts.append('<text class="small" x="{}" y="{}">{}</text>'.format(208+i*cell_w, 112+j*cell_h, value))
    write_svg(path, width, height, '\n'.join(parts), title)


def treemap(path, title, rows):
    rows = rows[:12]
    total = sum(row['value'] for row in rows) or 1
    width, height, x, y = 980, 520, 28, 72
    parts = ['<text class="title" x="28" y="34">{}</text>'.format(esc(title))]
    for idx, row in enumerate(rows):
        w = max(60, int((width - 56) * row['value'] / total))
        h = 86 + (idx % 3) * 24
        if x + w > width - 28:
            x, y = 28, y + 126
        colour = PALETTE[idx % len(PALETTE)]
        parts.append('<rect x="{}" y="{}" width="{}" height="{}" fill="{}" opacity="0.88" rx="4"/>'.format(x, y, w, h, colour))
        parts.append('<text class="label" x="{}" y="{}" fill="#ffffff">{}</text>'.format(x+10, y+24, esc(row['label'][:24])))
        parts.append('<text class="small" x="{}" y="{}" fill="#ffffff">{} terms</text>'.format(x+10, y+44, esc(row['value'])))
        x += w + 8
    write_svg(path, width, height, '\n'.join(parts), title)


def network_svg(path, title, graph):
    nodes = [node for node, _ in list(graph.get('metrics', {}).get('degree', {}).items())[:18]] or graph.get('nodes', [])[:18]
    positions = {}
    width, height, cx, cy, radius = 980, 680, 490, 350, 250
    for idx, node in enumerate(nodes):
        angle = 2 * math.pi * idx / max(1, len(nodes))
        positions[node] = (cx + radius * math.cos(angle), cy + radius * math.sin(angle))
    parts = ['<text class="title" x="28" y="34">{}</text>'.format(esc(title))]
    for left, right, value in graph.get('edges', [])[:80]:
        if left in positions and right in positions:
            x1, y1 = positions[left]; x2, y2 = positions[right]
            parts.append('<line x1="{:.1f}" y1="{:.1f}" x2="{:.1f}" y2="{:.1f}" stroke="#bcccdc" stroke-width="1.2"/>'.format(x1,y1,x2,y2))
    for idx, node in enumerate(nodes):
        x, y = positions[node]
        degree = graph.get('metrics', {}).get('degree', {}).get(node, 1)
        r = 7 + min(18, degree * 1.5)
        parts.append('<circle cx="{:.1f}" cy="{:.1f}" r="{}" fill="{}" opacity="0.92"/>'.format(x, y, r, PALETTE[idx % len(PALETTE)]))
        parts.append('<text class="small" x="{:.1f}" y="{:.1f}">{}</text>'.format(x+r+4, y+4, esc(node[:34])))
    write_svg(path, width, height, '\n'.join(parts), title)


def sankey(path, title, rows):
    width, height = 980, 560
    left = Counter(row['source_id'] for row in rows).most_common(8)
    mid = Counter(row['review_status'] for row in rows).most_common()
    right = Counter(row['uogto_source_id'] for row in rows).most_common(8)
    parts = ['<text class="title" x="28" y="34">{}</text>'.format(esc(title))]
    def column(items, x, label):
        parts.append('<text class="label" x="{}" y="64">{}</text>'.format(x, esc(label)))
        y, centers = 86, {}
        for idx, (name, count) in enumerate(items):
            h = 18 + count * 2
            parts.append('<rect x="{}" y="{}" width="150" height="{}" fill="{}" opacity="0.88" rx="3"/>'.format(x, y, h, PALETTE[idx % len(PALETTE)]))
            parts.append('<text class="small" x="{}" y="{}">{} ({})</text>'.format(x+8, y+16, esc(name[:18]), count))
            centers[name] = (x + 150, y + h / 2)
            y += h + 14
        return centers
    lc, mc, rc = column(left, 40, 'Source'), column(mid, 410, 'Review status'), column(right, 760, 'UOGTO module')
    for row in rows[:220]:
        if row['source_id'] in lc and row['review_status'] in mc:
            x1,y1=lc[row['source_id']]; x2,y2=mc[row['review_status']]
            parts.append('<path d="M{},{} C{},{} {},{} {},{}" fill="none" stroke="#9fb3c8" stroke-width="0.8" opacity="0.35"/>'.format(x1,y1,x1+90,y1,x2-90,y2,x2,y2))
        if row['review_status'] in mc and row['uogto_source_id'] in rc:
            x1,y1=mc[row['review_status']]; x2,y2=rc[row['uogto_source_id']]
            parts.append('<path d="M{},{} C{},{} {},{} {},{}" fill="none" stroke="#bcccdc" stroke-width="0.8" opacity="0.3"/>'.format(x1,y1,x1+80,y1,x2-90,y2,x2-150,y2))
    write_svg(path, width, height, '\n'.join(parts), title)


def build_visualisation_data(inventory, review_rows, overlap, network):
    source_names = {source['id']: source.get('name', source['id']) for source in inventory.get('sources', [])}
    source_sizes = []
    for source_id, summary in overlap.get('descriptive_summaries', {}).items():
        if summary.get('source_kind') != 'uogto':
            source_sizes.append({'label': source_names.get(source_id, source_id), 'value': summary.get('term_count', 0), 'source_id': source_id})
    source_sizes.sort(key=lambda row: (-row['value'], row['label']))
    match_classes = Counter((row.get('decision_predicate') or row.get('candidate_predicate') or 'unclassified') for row in review_rows)
    review_workload = Counter(row.get('review_status', 'missing') for row in review_rows)
    module_rows = [{'label': row['uogto_source_id'], 'value': row['unique_terms']} for row in overlap.get('uogto_stronger_coverage_areas', [])]
    return {'source_sizes': source_sizes, 'match_classes': [{'label': k, 'value': v} for k,v in sorted(match_classes.items(), key=lambda item: (-item[1], item[0]))], 'review_workload': [{'label': k, 'value': v} for k,v in sorted(review_workload.items(), key=lambda item: (-item[1], item[0]))], 'heat_rows': overlap.get('bidirectional_overlap', {}).get('source_by_uogto', []), 'module_rows': module_rows, 'network': network.get('source_similarity_graph', {})}


def render_report(path, inventory, review_rows, overlap, network):
    summary, nsummary = overlap['summary'], network['summary']
    accepted = sum(1 for row in review_rows if row.get('review_status') == 'accepted')
    needs_review = sum(1 for row in review_rows if row.get('review_status') == 'needs_domain_review')
    rejected = sum(1 for row in review_rows if row.get('review_status') == 'rejected')
    figures = '\n'.join('- ![{}](figures/{})'.format(name, name) for name in REQUIRED_FIGURES)
    top_sources_md = '\n'.join('| `{}` | {} | {} |'.format(row['source_id'], row['unmatched_terms'], row['candidate_coverage']) for row in overlap.get('recommended_uogto_enhancement_areas', [])[:8])
    central_md = '\n'.join('| `{}` | {} |'.format(row['source_id'], row['centrality_score']) for row in network.get('central_source_families', [])[:8])
    report = '# Comparative Simulation Ontology Mapping Report\n\n'
    report += '## Scope\nThis report summarises the reproducible comparison of public game-theory, simulation, agent-based modelling, system-dynamics, and adjacent modelling ontologies against UOGTO. It is generated from the track artifacts in `docs/ontology-comparison/`.\n\n'
    report += '## Methodology\nThe workflow uses the discovery protocol, source inventory, source provenance, normalized term inventory, deterministic mapping candidates, reviewed mappings, overlap metrics, and network analysis artifacts. Redistributable RDF sources are parsed directly; non-redistributable or standards-document sources are represented as metadata-only or transformed-summary records so the report does not overclaim source access.\n\n'
    report += '## Source Inventory\n- Candidate sources: {}\n- External terms: {}\n- UOGTO terms: {}\n- Review candidates: {}\n- Accepted mappings: {}\n\n'.format(len(inventory.get('sources', [])), summary['external_term_count'], summary['uogto_term_count'], summary['review_candidate_count'], accepted)
    report += '## Mapping Review Results\n- Accepted: {}\n- Needs domain review: {}\n- Rejected: {}\n\nThe accepted alignment TTL is evidence-backed by `mapping-review.csv`. Candidate and rejected rows remain audit records and should not be treated as asserted ontology alignments.\n\n'.format(accepted, needs_review, rejected)
    report += '## Overlap Findings\n| Source | Unmatched terms | Candidate coverage |\n| --- | ---: | ---: |\n{}\n\n'.format(top_sources_md)
    report += '## Network Findings\n- Source graph nodes: {}\n- Term-alignment bipartite edges: {}\n- Source-similarity edges: {}\n- UOGTO module coverage edges: {}\n\n| Central source or module | Centrality score |\n| --- | ---: |\n{}\n\n'.format(nsummary['source_graph_nodes'], nsummary['alignment_graph_edges'], nsummary['similarity_graph_edges'], nsummary['coverage_graph_edges'], central_md)
    report += '## Visualisations\n{}\n\n'.format(figures)
    report += '## Recommended UOGTO Follow-Up Work\n1. Treat accepted mappings as stable crosswalk evidence and keep `accepted-alignments.ttl` in sync with any future review edits.\n2. Prioritise high-volume unmatched sources as candidate extension-review areas rather than immediate equivalence assertions.\n3. Use `needs_domain_review` mappings as reviewer work queues for ontology architects and domain experts.\n4. Keep metadata-only standards separate from parsed RDF sources until their licences and formal artifacts permit stronger comparison.\n5. Re-run `make ontology-comparison-visuals` after any source, mapping, overlap, or network artifact changes.\n\n'
    report += '## Reproducibility\nRun `make ontology-comparison-visuals` to regenerate this report and the SVG figures from the JSON/CSV artifacts. The report intentionally separates accepted alignments from candidates and future-work recommendations.\n'
    path.write_text(report, encoding='utf-8')


def build_outputs(inventory, review_rows, overlap, network, figures_dir=DEFAULT_FIGURES, report_path=DEFAULT_REPORT):
    data = build_visualisation_data(inventory, review_rows, overlap, network)
    figures_dir.mkdir(parents=True, exist_ok=True)
    bar_chart(figures_dir / 'source_sizes_bar.svg', 'External source sizes', data['source_sizes'])
    bar_chart(figures_dir / 'match_classes_bar.svg', 'Mapping predicate classes', data['match_classes'])
    heatmap(figures_dir / 'source_module_overlap_heatmap.svg', 'Source by UOGTO module overlap', data['heat_rows'])
    treemap(figures_dir / 'uogto_coverage_treemap.svg', 'UOGTO unique coverage areas', data['module_rows'])
    network_svg(figures_dir / 'source_similarity_network.svg', 'Source similarity network', data['network'])
    sankey(figures_dir / 'mapping_flow_sankey.svg', 'Mapping review flow', review_rows)
    bar_chart(figures_dir / 'reviewer_workload.svg', 'Reviewer workload by status', data['review_workload'])
    render_report(report_path, inventory, review_rows, overlap, network)
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
    required = ['# Comparative Simulation Ontology Mapping Report','## Methodology','## Source Inventory','## Mapping Review Results','## Overlap Findings','## Network Findings','## Visualisations','## Recommended UOGTO Follow-Up Work','## Reproducibility']
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
    parser.add_argument('--figures-dir', type=Path, default=DEFAULT_FIGURES)
    parser.add_argument('--report', type=Path, default=DEFAULT_REPORT)
    parser.add_argument('--check-only', action='store_true')
    args = parser.parse_args()
    if not args.check_only:
        build_outputs(load_json(args.inventory), load_review(args.review), load_json(args.overlap), load_json(args.network), args.figures_dir, args.report)
    summary = validate_outputs(args.figures_dir, args.report)
    print('Ontology comparison visuals valid: {} figures, report {}'.format(summary['figure_count'], summary['report']))


if __name__ == '__main__':
    main()
