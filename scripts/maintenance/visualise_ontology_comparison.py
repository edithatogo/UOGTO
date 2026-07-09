import argparse, csv, html, json, math, shutil, subprocess
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DEFAULT_INVENTORY = ROOT / 'docs' / 'ontology-comparison' / 'source-inventory.json'
DEFAULT_REVIEW = ROOT / 'docs' / 'ontology-comparison' / 'mapping-review.csv'
DEFAULT_OVERLAP = ROOT / 'docs' / 'ontology-comparison' / 'overlap-metrics.json'
DEFAULT_NETWORK = ROOT / 'docs' / 'ontology-comparison' / 'network-analysis.json'
DEFAULT_PROVENANCE = ROOT / 'docs' / 'ontology-comparison' / 'source-provenance.json'
DEFAULT_FIGURES = ROOT / 'docs' / 'ontology-comparison' / 'figures'
DEFAULT_COSMOGRAPH = ROOT / 'docs' / 'ontology-comparison' / 'cosmograph'
DEFAULT_PAPER_FIGURES = ROOT / 'docs' / 'paper' / 'figures'
DEFAULT_REPORT = ROOT / 'docs' / 'ontology-comparison' / 'report.md'
REQUIRED_FIGURES = ['source_sizes_bar.svg','match_classes_bar.svg','source_module_overlap_heatmap.svg','source_family_evidence_heatmap.svg','source_family_term_heatmap.svg','uogto_coverage_treemap.svg','source_similarity_network.svg','mapping_flow_sankey.svg','reviewer_workload.svg']
REQUIRED_COSMOGRAPH_IMAGES = ['source_similarity_cosmograph.svg','term_alignment_cosmograph.svg','import_uses_cosmograph.svg']
PAPER_GRAPH_PDFS = {
    'source_similarity_cosmograph.pdf': 'source-similarity-cosmograph.pdf',
    'term_alignment_cosmograph.pdf': 'term-alignment-cosmograph.pdf',
    'import_uses_cosmograph.pdf': 'import-evidence-use-cosmograph.pdf',
}


def load_json(path):
    return json.loads(Path(path).read_text(encoding='utf-8'))


def load_review(path):
    with Path(path).open('r', encoding='utf-8', newline='') as handle:
        return list(csv.DictReader(handle))


def esc(value):
    return html.escape(str(value), quote=True)


PALETTE = ['#0072B2', '#009E73', '#D55E00', '#CC79A7', '#E69F00', '#56B4E9', '#000000', '#999999']
SEQUENTIAL = ['#F7FBFF', '#DEEBF7', '#C6DBEF', '#9ECAE1', '#6BAED6', '#3182BD', '#08519C']
PUBLICATION_LABELS = {
    'bfo': 'Basic Formal Ontology',
    'bpmn_2': 'BPMN 2.0',
    'cellml': 'CellML',
    'devs': 'DEVS simulation',
    'dolce': 'DOLCE ontology',
    'emmo': 'EMMO',
    'fmi': 'Functional Mock-up Interface',
    'game_ontology_project': 'Game Ontology Project',
    'gdl_ii_iii_gdlz': 'GDL-II / GDL-III / GDLZ',
    'gdlf_gamelan': 'Game Description Language',
    'gvgai_vgdl': 'GVGAI / VGDL',
    'hla_fom': 'HLA Federation Object Model',
    'kaos': 'KAoS policy ontology',
    'kisao': 'KiSAO algorithms',
    'ludii': 'Ludii game system',
    'metadata_only_sources': 'Metadata-only sources',
    'miase': 'MIASE',
    'modelica': 'Modelica',
    'oaei': 'Ontology Alignment Evaluation',
    'odd_protocol': 'ODD protocol',
    'ontouml_ufo': 'OntoUML / UFO',
    'osmo': 'OSMO',
    'owl_s': 'OWL-S services',
    'owl_time': 'OWL-Time',
    'p_plan': 'P-Plan',
    'pddl': 'PDDL planning',
    'pnml': 'Petri Net Markup Language',
    'prov_o': 'PROV-O',
    'robot': 'ROBOT ontology tool',
    'sbgn': 'Systems Biology Graphical Notation',
    'sbml': 'Systems Biology Markup Language',
    'sbo': 'Systems Biology Ontology',
    'schema_org': 'schema.org',
    'sed_ml': 'SED-ML',
    'ssn_sosa': 'SSN/SOSA',
    'sssom': 'SSSOM mappings',
    'stanford_gdl': 'Stanford GDL',
    'sysml': 'SysML',
    'vimmp_ontologies': 'VIMMP ontologies',
    'xmile': 'XMILE system dynamics',
}


def title_words(value):
    text = str(value).replace('uogto_extensions_', '').replace('uogto_core_', '')
    text = text.replace('uogto_', '').replace('_', ' ').replace('-', ' ')
    return ' '.join(part.upper() if part in {'rdf', 'owl', 'shacl', 'json', 'llm', 'marl'} else part.capitalize() for part in text.split())


def local_name(value):
    text = str(value)
    text = text.split('#')[-1].split('/')[-1]
    if ':' in text:
        text = text.split(':', 1)[1]
    return text


def publication_label(node):
    if node in PUBLICATION_LABELS:
        return PUBLICATION_LABELS[node]
    if node.startswith('source:'):
        return title_words(local_name(node))
    if node.startswith('uogto:'):
        return f"UOGTO: {title_words(local_name(node))}"
    if node.startswith('format:'):
        return f"Format: {title_words(local_name(node))}"
    if node.startswith('import:'):
        return f"Import: {title_words(local_name(node))}"
    if node.startswith('uogto_'):
        return f"UOGTO {title_words(node)}"
    return title_words(local_name(node))


def clip_label(value, limit=42):
    text = publication_label(value)
    return text if len(text) <= limit else text[: limit - 3].rstrip() + '...'


def compact_node_label(node, limit=40):
    text = publication_label(node)
    if node.startswith(('source:', 'uogto:')):
        text = title_words(local_name(node))
    text = text.replace('UOGTO Extensions ', 'UOGTO ')
    return text if len(text) <= limit else text[: limit - 3].rstrip() + '...'


def alignment_source_label(node, limit=40):
    iri = node.removeprefix('source:')
    vocabularies = [
        ('http://ogp.me/ns#', 'OGP'),
        ('http://purl.org/dc/terms/', 'DCTERMS'),
        ('http://www.w3.org/2002/07/owl#', 'OWL'),
        ('http://www.w3.org/ns/prov#', 'PROV'),
        ('http://www.w3.org/ns/sosa/', 'SOSA'),
        ('http://xmlns.com/foaf/0.1/', 'FOAF'),
        ('https://gs1.org/voc/', 'GS1'),
        ('https://schema.org/', 'Schema.org'),
    ]
    prefix = 'Source'
    for namespace, label in vocabularies:
        if iri.startswith(namespace):
            prefix = label
            break
    text = '{} {}'.format(prefix, title_words(local_name(iri)))
    return text if len(text) <= limit else text[: limit - 3].rstrip() + '...'


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
    svg += '<style>text{font-family:Arial,Helvetica,sans-serif;fill:#1f2933}.tiny{font-size:12px}.small{font-size:14px}.label{font-size:15px}.title{font-size:24px;font-weight:700}.caption{font-size:14px;fill:#475569}.axis{stroke:#CBD5E1}.callout{font-size:14px;font-weight:700}.edgeLabel{font-size:12px;paint-order:stroke;stroke:#ffffff;stroke-width:5px;stroke-linejoin:round}</style><rect width="100%" height="100%" fill="#ffffff"/>\n'
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


def node_kind(node):
    if node.startswith('uogto:'):
        return 'uogto_term'
    if node.startswith('source:'):
        return 'external_term'
    if node.startswith('uogto_'):
        return 'uogto_module'
    if node == 'metadata_only_sources':
        return 'evidence_group'
    if node.startswith('format:'):
        return 'format'
    if node.startswith('import:'):
        return 'import'
    return 'source'


def write_csv(path, fieldnames, rows):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('w', encoding='utf-8', newline='') as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def cosmograph_exports(network, output_dir=DEFAULT_COSMOGRAPH):
    output_dir.mkdir(parents=True, exist_ok=True)
    graphs = {
        'source_similarity': network.get('source_similarity_graph', {}),
        'term_alignment': network.get('term_alignment_bipartite_graph', {}),
        'import_uses': network.get('import_uses_graph', {}),
    }
    written = []
    for graph_name, graph in graphs.items():
        degree = graph.get('metrics', {}).get('degree', {})
        edge_rows = []
        nodes = set(graph.get('nodes', []))
        for edge in graph.get('edges', []):
            if len(edge) < 2:
                continue
            source, target = edge[0], edge[1]
            weight = edge[2] if len(edge) > 2 else 1
            nodes.update([source, target])
            edge_rows.append({
                'source': source,
                'target': target,
                'weight': weight,
                'graph': graph_name,
            })
        node_rows = [
            {
                'id': node,
                'label': publication_label(node),
                'kind': node_kind(node),
                'degree': degree.get(node, 0),
                'graph': graph_name,
            }
            for node in sorted(nodes)
        ]
        node_path = output_dir / f'{graph_name}_nodes.csv'
        edge_path = output_dir / f'{graph_name}_edges.csv'
        write_csv(node_path, ['id', 'label', 'kind', 'degree', 'graph'], node_rows)
        write_csv(edge_path, ['source', 'target', 'weight', 'graph'], edge_rows)
        written.extend([node_path, edge_path])
        image_path = output_dir / f'{graph_name}_cosmograph.svg'
        cosmograph_static_svg(image_path, f'{graph_name.replace("_", " ").title()} Cosmograph view', graph, graph_name)
        written.append(image_path)
        written.extend(optional_image_derivatives(image_path))
    if output_dir == DEFAULT_COSMOGRAPH:
        written.extend(sync_paper_graph_pdfs(output_dir))
    readme = output_dir / 'README.md'
    readme.write_text(
        '# Cosmograph-ready network exports\n\n'
        'These CSV files are generated from `docs/ontology-comparison/network-analysis.json` for interactive inspection in Cosmograph or another graph explorer.\n\n'
        'Recommended Cosmograph import settings:\n'
        '- Load an `*_edges.csv` file as links with `source` and `target` columns.\n'
        '- Load the matching `*_nodes.csv` file as node metadata keyed by `id`.\n'
        '- Use `weight` for link weight and `kind` / `degree` for color and size.\n\n'
        'Exports:\n'
        '- `source_similarity_nodes.csv` and `source_similarity_edges.csv`: source-family and source-similarity graph.\n'
        '- `term_alignment_nodes.csv` and `term_alignment_edges.csv`: accepted term-alignment bipartite graph.\n'
        '- `import_uses_nodes.csv` and `import_uses_edges.csv`: import/evidence-use graph.\n\n'
        'Static graph images:\n'
        '- `source_similarity_cosmograph.svg`: source-similarity graph rendering, with optional `.png` and `.pdf` derivatives when ImageMagick is available.\n'
        '- `term_alignment_cosmograph.svg`: accepted term-alignment bipartite graph rendering, with optional `.png` and `.pdf` derivatives when ImageMagick is available.\n'
        '- `import_uses_cosmograph.svg`: import/evidence-use graph rendering, with optional `.png` and `.pdf` derivatives when ImageMagick is available.\n\n'
        'The manuscript uses static SVG/PDF-safe figures for arXiv, while these exports support interactive Cosmograph review.\n',
        encoding='utf-8',
    )
    written.append(readme)
    return written


def sync_paper_graph_pdfs(output_dir, paper_dir=DEFAULT_PAPER_FIGURES):
    written = []
    paper_dir.mkdir(parents=True, exist_ok=True)
    for source_name, target_name in PAPER_GRAPH_PDFS.items():
        source = output_dir / source_name
        if not source.exists():
            continue
        target = paper_dir / target_name
        shutil.copy2(source, target)
        written.append(target)
    return written


def optional_image_derivatives(svg_path):
    magick = shutil.which('magick')
    if not magick:
        return []
    written = []
    for suffix in ('.png', '.pdf'):
        output = svg_path.with_suffix(suffix)
        command = [magick, '-density', '180', str(svg_path), str(output)]
        if suffix == '.pdf':
            command = [magick, '-density', '110', str(svg_path), '-compress', 'Zip', '-quality', '90', str(output)]
        subprocess.run(command, check=True)
        written.append(output)
    return written


def edge_weight(value):
    try:
        return float(value)
    except (TypeError, ValueError):
        return 1.0


def graph_layout(nodes, graph_name):
    width, height = 1400, 980
    cx, cy = width / 2, height / 2 + 40
    if graph_name == 'term_alignment':
        left = [node for node in nodes if node.startswith('source:')]
        right = [node for node in nodes if node.startswith('uogto:')]
        other = [node for node in nodes if node not in set(left) | set(right)]
        positions = {}
        for idx, node in enumerate(left):
            y = 170 + idx * (640 / max(1, len(left) - 1))
            positions[node] = (260, y)
        for idx, node in enumerate(right):
            y = 170 + idx * (640 / max(1, len(right) - 1))
            positions[node] = (1140, y)
        for idx, node in enumerate(other):
            angle = 2 * math.pi * idx / max(1, len(other))
            positions[node] = (cx + 220 * math.cos(angle), cy + 220 * math.sin(angle))
        return positions, width, height
    positions = {}
    rings = [(0, 1), (250, 14), (390, 34), (500, 1000)]
    ordered = list(nodes)
    cursor = 0
    for radius, capacity in rings:
        chunk = ordered[cursor:cursor + capacity]
        cursor += capacity
        if not chunk:
            continue
        for idx, node in enumerate(chunk):
            angle = 2 * math.pi * idx / max(1, len(chunk))
            jitter = 0 if radius == 0 else (idx % 3) * 8
            positions[node] = (cx + (radius + jitter) * math.cos(angle), cy + (radius + jitter) * math.sin(angle))
    return positions, width, height


def cosmograph_static_svg(path, title, graph, graph_name):
    if graph_name == 'source_similarity':
        source_similarity_publication_svg(path, graph)
        return
    if graph_name == 'term_alignment':
        term_alignment_publication_svg(path, graph)
        return
    if graph_name == 'import_uses':
        import_uses_publication_svg(path, graph)
        return
    generic_network_svg(path, title, graph, graph_name)


def graph_nodes_and_edges(graph):
    nodes = set(graph.get('nodes', []))
    edges = []
    for edge in graph.get('edges', []):
        if len(edge) < 2:
            continue
        source, target = edge[0], edge[1]
        weight = edge[2] if len(edge) > 2 else 1
        nodes.update([source, target])
        edges.append((source, target, weight))
    return nodes, edges


def vertical_positions(nodes, x, y0, y1):
    positions = {}
    count = len(nodes)
    if count == 1:
        return {nodes[0]: (x, (y0 + y1) / 2)}
    for idx, node in enumerate(nodes):
        y = y0 + idx * ((y1 - y0) / max(1, count - 1))
        positions[node] = (x, y)
    return positions


def source_similarity_publication_svg(path, graph):
    degree_map = graph.get('metrics', {}).get('degree', {})
    nodes, edges = graph_nodes_and_edges(graph)
    uogto_nodes = [node for node in nodes if node.startswith('uogto_')]
    source_nodes = sorted(nodes - set(uogto_nodes), key=lambda node: (-degree_map.get(node, 0), publication_label(node)))[:18]
    uogto_nodes = sorted(uogto_nodes, key=lambda node: (-degree_map.get(node, 0), publication_label(node)))[:16]
    shown = set(source_nodes) | set(uogto_nodes)
    visible_edges = [
        (left, right, edge_weight(weight))
        for left, right, weight in edges
        if left in shown and right in shown
    ]
    visible_edges = sorted(visible_edges, key=lambda item: (-item[2], publication_label(item[0]), publication_label(item[1])))[:95]
    width, height = 1500, 980
    positions = {}
    positions.update(vertical_positions(source_nodes, 300, 150, 820))
    positions.update(vertical_positions(uogto_nodes, 1180, 150, 820))
    max_weight = max([weight for _, _, weight in visible_edges] or [1])
    parts = [
        '<text class="title" x="48" y="48">Source-similarity backbone</text>',
        '<text class="caption" x="48" y="78">Print view of the strongest overlap links among comparator sources and UOGTO modules. Edges guide review; they are not equivalence claims.</text>',
        '<text class="label" x="112" y="120">Comparator source families</text>',
        '<text class="label" x="1035" y="120">UOGTO bridge modules</text>',
    ]
    for left, right, weight in visible_edges:
        x1, y1 = positions[left]; x2, y2 = positions[right]
        opacity = 0.18 + 0.48 * min(1, weight / max_weight)
        line_width = 0.8 + 5.0 * min(1, weight / max_weight)
        parts.append('<path d="M{:.1f},{:.1f} C610,{:.1f} 890,{:.1f} {:.1f},{:.1f}" fill="none" stroke="#475569" stroke-width="{:.2f}" opacity="{:.2f}"/>'.format(x1 + 132, y1, y1, y2, x2 - 132, y2, line_width, opacity))
    parts.extend([
        '<rect x="574" y="438" width="352" height="74" fill="#F8FAFC" stroke="#CBD5E1" rx="8" opacity="0.96"/>',
        '<text class="small" text-anchor="middle" x="750" y="468">Overlap signals</text>',
        '<text class="tiny" text-anchor="middle" x="750" y="492">labels, terms, imports, formats, and coverage</text>',
    ])
    for node in source_nodes:
        x, y = positions[node]
        parts.append('<rect x="{:.1f}" y="{:.1f}" width="264" height="32" fill="#FEF3C7" stroke="#D97706" rx="5"/>'.format(x - 132, y - 16))
        parts.append('<text class="tiny" text-anchor="middle" x="{:.1f}" y="{:.1f}">{} ({})</text>'.format(x, y + 4, esc(compact_node_label(node, 32)), degree_map.get(node, 0)))
    for node in uogto_nodes:
        x, y = positions[node]
        parts.append('<rect x="{:.1f}" y="{:.1f}" width="264" height="32" fill="#DCFCE7" stroke="#0F766E" rx="5"/>'.format(x - 132, y - 16))
        parts.append('<text class="tiny" text-anchor="middle" x="{:.1f}" y="{:.1f}">{} ({})</text>'.format(x, y + 4, esc(compact_node_label(node, 32)), degree_map.get(node, 0)))
    parts.append('<text class="caption" x="48" y="930">Shown: {} high-degree nodes and {} strongest visible links from {} graph edges.</text>'.format(len(shown), len(visible_edges), len(edges)))
    write_svg(path, width, height, '\n'.join(parts), 'Source-similarity backbone', 'Print-oriented backbone view of source-similarity overlap links.')


def term_alignment_publication_svg(path, graph):
    degree_map = graph.get('metrics', {}).get('degree', {})
    nodes, edges = graph_nodes_and_edges(graph)
    source_nodes = sorted([node for node in nodes if node.startswith('source:')], key=lambda node: compact_node_label(node))
    uogto_nodes = sorted([node for node in nodes if node.startswith('uogto:')], key=lambda node: compact_node_label(node))
    width, height = 1500, 900
    positions = {}
    positions.update(vertical_positions(source_nodes, 330, 150, 750))
    positions.update(vertical_positions(uogto_nodes, 1165, 150, 750))
    predicate_colours = {
        'owl:equivalentClass': '#0072B2',
        'owl:equivalentProperty': '#009E73',
        'skos:narrowMatch': '#D55E00',
    }
    parts = [
        '<text class="title" x="48" y="48">Accepted term alignments</text>',
        '<text class="caption" x="48" y="78">All 12 accepted UOGTO-to-external mappings. The sparseness is deliberate: candidates are not asserted until reviewed.</text>',
        '<text class="label" x="128" y="118">External terms</text>',
        '<text class="label" x="1015" y="118">UOGTO terms</text>',
    ]
    for left, right, predicate in edges:
        x1, y1 = positions[left]; x2, y2 = positions[right]
        colour = predicate_colours.get(str(predicate), '#64748B')
        parts.append('<path d="M{:.1f},{:.1f} C610,{:.1f} 880,{:.1f} {:.1f},{:.1f}" fill="none" stroke="{}" stroke-width="2.4" opacity="0.74"/>'.format(x1 + 150, y1, y1, y2, x2 - 150, y2, colour))
    for node in source_nodes:
        x, y = positions[node]
        parts.append('<rect x="{:.1f}" y="{:.1f}" width="300" height="34" fill="#EFF6FF" stroke="#2563EB" rx="5"/>'.format(x - 150, y - 17))
        parts.append('<text class="tiny" text-anchor="middle" x="{:.1f}" y="{:.1f}">{} ({})</text>'.format(x, y + 4, esc(alignment_source_label(node, 38)), degree_map.get(node, 0)))
    for node in uogto_nodes:
        x, y = positions[node]
        parts.append('<rect x="{:.1f}" y="{:.1f}" width="300" height="34" fill="#ECFDF5" stroke="#0F766E" rx="5"/>'.format(x - 150, y - 17))
        parts.append('<text class="tiny" text-anchor="middle" x="{:.1f}" y="{:.1f}">{} ({})</text>'.format(x, y + 4, esc(compact_node_label(node, 38)), degree_map.get(node, 0)))
    legend_x, legend_y = 48, 826
    for idx, (label, colour) in enumerate(predicate_colours.items()):
        x = legend_x + idx * 235
        parts.append('<line x1="{}" y1="{}" x2="{}" y2="{}" stroke="{}" stroke-width="3"/>'.format(x, legend_y, x + 34, legend_y, colour))
        parts.append('<text class="tiny" x="{}" y="{}">{}</text>'.format(x + 44, legend_y + 4, esc(label)))
    write_svg(path, width, height, '\n'.join(parts), 'Accepted term alignments', 'Bipartite accepted mapping view with predicate labels.')


def import_uses_publication_svg(path, graph):
    degree_map = graph.get('metrics', {}).get('degree', {})
    nodes, edges = graph_nodes_and_edges(graph)
    imports = sorted([node for node in nodes if node.startswith('import:')], key=lambda node: (-degree_map.get(node, 0), publication_label(node)))
    evidence = sorted([node for node in nodes if node.startswith('format:') or node == 'metadata_only_sources'], key=lambda node: (-degree_map.get(node, 0), publication_label(node)))
    sources = sorted([node for node in nodes if node not in set(imports) | set(evidence)], key=lambda node: (-degree_map.get(node, 0), publication_label(node)))[:24]
    width, height = 1500, 980
    positions = {}
    positions.update(vertical_positions(sources, 270, 145, 845))
    positions.update(vertical_positions(evidence, 750, 260, 720))
    positions.update(vertical_positions(imports, 1210, 170, 810))
    visible = [(left, right, str(kind)) for left, right, kind in edges if left in positions and right in positions]
    parts = [
        '<text class="title" x="48" y="48">Import and evidence-use layers</text>',
        '<text class="caption" x="48" y="78">Layered view separating sources, evidence/format surfaces, and imports. Metadata-only evidence is not treated as a parsed semantic import.</text>',
        '<text class="label" x="160" y="116">Sources</text>',
        '<text class="label" x="640" y="236">Evidence or format surface</text>',
        '<text class="label" x="1124" y="140">Imports</text>',
    ]
    edge_colours = {'metadata': '#9333EA', 'format': '#475569', 'import': '#0F766E'}
    for left, right, kind in visible:
        x1, y1 = positions[left]; x2, y2 = positions[right]
        colour = edge_colours.get(kind, '#64748B')
        parts.append('<path d="M{:.1f},{:.1f} C520,{:.1f} 1000,{:.1f} {:.1f},{:.1f}" fill="none" stroke="{}" stroke-width="1.6" opacity="0.42"/>'.format(x1 + 130, y1, y1, y2, x2 - 130, y2, colour))
    for node in sources:
        x, y = positions[node]
        parts.append('<rect x="{:.1f}" y="{:.1f}" width="260" height="28" fill="#FFF7ED" stroke="#D97706" rx="4"/>'.format(x - 130, y - 14))
        parts.append('<text class="tiny" text-anchor="middle" x="{:.1f}" y="{:.1f}">{}</text>'.format(x, y + 4, esc(compact_node_label(node, 31))))
    for node in evidence:
        x, y = positions[node]
        fill = '#F3E8FF' if node == 'metadata_only_sources' else '#F1F5F9'
        stroke = '#9333EA' if node == 'metadata_only_sources' else '#475569'
        parts.append('<rect x="{:.1f}" y="{:.1f}" width="270" height="40" fill="{}" stroke="{}" rx="6"/>'.format(x - 135, y - 20, fill, stroke))
        parts.append('<text class="small" text-anchor="middle" x="{:.1f}" y="{:.1f}">{} ({})</text>'.format(x, y + 5, esc(compact_node_label(node, 30)), degree_map.get(node, 0)))
    for node in imports:
        x, y = positions[node]
        parts.append('<rect x="{:.1f}" y="{:.1f}" width="260" height="34" fill="#ECFDF5" stroke="#0F766E" rx="5"/>'.format(x - 130, y - 17))
        parts.append('<text class="tiny" text-anchor="middle" x="{:.1f}" y="{:.1f}">{} ({})</text>'.format(x, y + 4, esc(compact_node_label(node, 31)), degree_map.get(node, 0)))
    parts.append('<text class="caption" x="48" y="930">Shown: {} of {} source/evidence/import nodes and {} edges.</text>'.format(len(sources) + len(evidence) + len(imports), len(nodes), len(visible)))
    write_svg(path, width, height, '\n'.join(parts), 'Import and evidence-use layers', 'Layered print view separating source records, evidence surfaces, and imports.')


def generic_network_svg(path, title, graph, graph_name):
    degree_map = graph.get('metrics', {}).get('degree', {})
    graph_nodes = set(graph.get('nodes', []))
    for edge in graph.get('edges', []):
        if len(edge) >= 2:
            graph_nodes.update([edge[0], edge[1]])
    ordered_nodes = [node for node, _ in sorted(degree_map.items(), key=lambda item: (-item[1], item[0])) if node in graph_nodes]
    ordered_nodes.extend(sorted(graph_nodes - set(ordered_nodes)))
    max_nodes = 80 if graph_name == 'source_similarity' else 120
    nodes = ordered_nodes[:max_nodes]
    positions, width, height = graph_layout(nodes, graph_name)
    max_degree = max([degree_map.get(node, 0) for node in nodes] or [1])
    parts = [
        '<defs><radialGradient id="bg" cx="50%" cy="45%" r="75%"><stop offset="0%" stop-color="#F8FAFC"/><stop offset="100%" stop-color="#E2E8F0"/></radialGradient></defs>',
        '<rect width="100%" height="100%" fill="url(#bg)"/>',
        '<text class="title" x="42" y="52">{}</text>'.format(esc(title)),
        '<text class="caption" x="42" y="82">Static Cosmograph-style rendering from the generated node/edge CSVs; node size encodes degree and edge opacity encodes weight.</text>',
    ]
    visible_edges = []
    for edge in graph.get('edges', []):
        if len(edge) < 2:
            continue
        left, right = edge[0], edge[1]
        if left not in positions or right not in positions:
            continue
        weight = edge_weight(edge[2] if len(edge) > 2 else 1)
        visible_edges.append((left, right, weight))
    visible_edges = sorted(visible_edges, key=lambda item: -item[2])[:360]
    max_weight = max([weight for _, _, weight in visible_edges] or [1])
    for left, right, weight in visible_edges:
        x1, y1 = positions[left]; x2, y2 = positions[right]
        opacity = 0.15 + 0.55 * min(1, weight / max_weight)
        line_width = 0.7 + 3.4 * min(1, weight / max_weight)
        parts.append('<line x1="{:.1f}" y1="{:.1f}" x2="{:.1f}" y2="{:.1f}" stroke="#334155" stroke-width="{:.2f}" opacity="{:.2f}"/>'.format(x1, y1, x2, y2, line_width, opacity))
    for idx, node in enumerate(nodes):
        x, y = positions[node]
        degree = degree_map.get(node, 0)
        radius = 7 + 20 * (degree / max_degree if max_degree else 0)
        kind = node_kind(node)
        colour = {
            'uogto_term': '#0F766E',
            'external_term': '#2563EB',
            'uogto_module': '#7C2D12',
            'evidence_group': '#9333EA',
            'format': '#475569',
            'import': '#BE123C',
            'source': '#D97706',
        }.get(kind, PALETTE[idx % len(PALETTE)])
        parts.append('<circle cx="{:.1f}" cy="{:.1f}" r="{:.1f}" fill="{}" stroke="#FFFFFF" stroke-width="2" opacity="0.96"/>'.format(x, y, radius, colour))
    if graph_name == 'source_similarity':
        panel_x, panel_y = width - 410, 118
        parts.append('<rect x="{}" y="{}" width="360" height="360" fill="#FFFFFF" opacity="0.88" rx="10"/>'.format(panel_x, panel_y))
        parts.append('<text class="small" x="{}" y="{}">Highest-degree bridge nodes</text>'.format(panel_x + 18, panel_y + 30))
        for idx, node in enumerate(nodes[:12]):
            label = clip_label(node, 36)
            y = panel_y + 58 + idx * 24
            colour = '#7C2D12' if node.startswith('uogto_') else '#D97706'
            parts.append('<circle cx="{}" cy="{}" r="5" fill="{}"/>'.format(panel_x + 20, y - 4, colour))
            parts.append('<text class="tiny" x="{}" y="{}">{} ({})</text>'.format(panel_x + 34, y, esc(label), degree_map.get(node, 0)))
    label_count = 0 if graph_name == 'source_similarity' else 26
    labelled = set(nodes[:label_count])
    for node in nodes:
        if node not in labelled:
            continue
        x, y = positions[node]
        degree = degree_map.get(node, 0)
        radius = 7 + 20 * (degree / max_degree if max_degree else 0)
        label = clip_label(node, 42)
        anchor = 'start' if x < width / 2 else 'end'
        dx = radius + 8 if anchor == 'start' else -radius - 8
        parts.append('<text class="tiny" text-anchor="{}" x="{:.1f}" y="{:.1f}">{}</text>'.format(anchor, x + dx, y + 4, esc(label)))
    legend_x, legend_y = 42, height - 112
    legend = [('source', '#D97706'), ('external term', '#2563EB'), ('UOGTO term/module', '#0F766E'), ('format/import/evidence', '#9333EA')]
    parts.append('<rect x="{}" y="{}" width="520" height="70" fill="#FFFFFF" opacity="0.82" rx="8"/>'.format(legend_x - 12, legend_y - 26))
    for idx, (label, colour) in enumerate(legend):
        x = legend_x + idx * 126
        parts.append('<circle cx="{}" cy="{}" r="7" fill="{}"/>'.format(x, legend_y, colour))
        parts.append('<text class="tiny" x="{}" y="{}">{}</text>'.format(x + 13, legend_y + 4, esc(label)))
    parts.append('<text class="caption" x="42" y="{}">Rendered nodes: {} of {}; rendered edges: {} of {}.</text>'.format(height - 22, len(nodes), len(graph_nodes), len(visible_edges), len(graph.get('edges', []))))
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
    similarity_nodes = network.get('source_similarity_graph', {}).get('metrics', {}).get('node_count', 'not recorded')
    report += '## Network Findings\n- Import/evidence source graph nodes: {}\n- Source-similarity graph nodes: {}\n- Term-alignment bipartite edges: {}\n- Source-similarity edges: {}\n- UOGTO module coverage edges: {}\n\nThe import/evidence graph and source-similarity graph are separate views; their node counts are not expected to match.\n\n| Central source or module | Centrality score |\n| --- | ---: |\n{}\n\n'.format(nsummary['source_graph_nodes'], similarity_nodes, nsummary['alignment_graph_edges'], nsummary['similarity_graph_edges'], nsummary['coverage_graph_edges'], central_md)
    report += '## Evidence-Level Coverage\nThe new heatmaps stratify source-family coverage by evidence level so metadata-only sources, downloaded RDF artifacts, and future transformed-summary or excluded records are not conflated. Source counts and term counts are shown separately to distinguish breadth from depth.\n\n| Evidence level | Source count | Term count |\n| --- | ---: | ---: |\n{}\n\n'.format(evidence_rows)
    report += '## Visualisations\n{}\n\n'.format(figures)
    report += '## Cosmograph Network Images and Interactive Exports\nCosmograph-ready node and edge CSV files are generated under `docs/ontology-comparison/cosmograph/`, alongside static SVG renderings for arXiv-safe review:\n\n'
    report += '- ![source_similarity_cosmograph.svg](cosmograph/source_similarity_cosmograph.svg)\n'
    report += '- ![term_alignment_cosmograph.svg](cosmograph/term_alignment_cosmograph.svg)\n'
    report += '- ![import_uses_cosmograph.svg](cosmograph/import_uses_cosmograph.svg)\n\n'
    report += 'Use the `source` and `target` columns from each `*_edges.csv` file as links, join the matching `*_nodes.csv` file on `id`, and use `weight`, `kind`, and `degree` for link strength, colour, and size.\n\n'
    report += '## Recommended UOGTO Follow-Up Work\n1. Treat accepted mappings as stable crosswalk evidence and keep `accepted-alignments.ttl` in sync with any future review edits.\n2. Prioritise high-volume unmatched sources as candidate extension-review areas rather than immediate equivalence assertions.\n3. Use `needs_domain_review` mappings as reviewer work queues for ontology architects and domain experts.\n4. Keep metadata-only standards separate from parsed RDF sources until their licences and formal artifacts permit stronger comparison.\n5. Re-run `make ontology-comparison-visuals` after any source, mapping, overlap, or network artifact changes.\n\n'
    report += '## Reproducibility\nRun `make ontology-comparison-visuals` to regenerate this report and the SVG figures from the JSON/CSV artifacts. The report intentionally separates accepted alignments from candidates and future-work recommendations.\n'
    path.write_text(report, encoding='utf-8')


def build_outputs(inventory, review_rows, overlap, network, provenance=None, figures_dir=DEFAULT_FIGURES, report_path=DEFAULT_REPORT, cosmograph_dir=DEFAULT_COSMOGRAPH):
    if isinstance(provenance, (str, Path)) and isinstance(figures_dir, (str, Path)) and report_path == DEFAULT_REPORT:
        report_path = Path(figures_dir)
        figures_dir = Path(provenance)
        provenance = {}
        if cosmograph_dir == DEFAULT_COSMOGRAPH:
            cosmograph_dir = report_path.parent / 'cosmograph'
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
    cosmograph_exports(network, cosmograph_dir)
    render_report(report_path, inventory, review_rows, overlap, network, data)
    return {'figures': [str(figures_dir / name) for name in REQUIRED_FIGURES], 'report': str(report_path)}


def validate_outputs(figures_dir=DEFAULT_FIGURES, report_path=DEFAULT_REPORT, cosmograph_dir=DEFAULT_COSMOGRAPH):
    missing = [name for name in REQUIRED_FIGURES if not (figures_dir / name).exists()]
    if missing:
        raise AssertionError('Missing visualisation figures: ' + ', '.join(missing))
    missing_cosmograph = [name for name in REQUIRED_COSMOGRAPH_IMAGES if not (cosmograph_dir / name).exists()]
    if missing_cosmograph:
        raise AssertionError('Missing Cosmograph static images: ' + ', '.join(missing_cosmograph))
    for name in REQUIRED_FIGURES:
        text = (figures_dir / name).read_text(encoding='utf-8')
        if '<svg' not in text or '</svg>' not in text:
            raise AssertionError('Figure is not valid SVG text: ' + name)
    for name in REQUIRED_COSMOGRAPH_IMAGES:
        text = (cosmograph_dir / name).read_text(encoding='utf-8')
        if '<svg' not in text or '</svg>' not in text:
            raise AssertionError('Cosmograph image is not valid SVG text: ' + name)
    report = report_path.read_text(encoding='utf-8')
    required = ['# Comparative Simulation Ontology Mapping Report','## Methodology','## Inclusion and Exclusion Summary','## Mapping Methods','## Source Inventory','## Mapping Review Results','## Overlap Findings','## Network Findings','## Evidence-Level Coverage','## Visualisations','## Cosmograph Network Images and Interactive Exports','## Recommended UOGTO Follow-Up Work','## Reproducibility']
    for section in required:
        if section not in report:
            raise AssertionError('Missing report section: ' + section)
    for name in REQUIRED_FIGURES:
        if 'figures/' + name not in report:
            raise AssertionError('Report does not link figure: ' + name)
    for name in REQUIRED_COSMOGRAPH_IMAGES:
        if 'cosmograph/' + name not in report:
            raise AssertionError('Report does not link Cosmograph image: ' + name)
    return {'figure_count': len(REQUIRED_FIGURES), 'cosmograph_image_count': len(REQUIRED_COSMOGRAPH_IMAGES), 'report': str(report_path)}


def main():
    parser = argparse.ArgumentParser(description='Generate ontology comparison figures and report.')
    parser.add_argument('--inventory', type=Path, default=DEFAULT_INVENTORY)
    parser.add_argument('--review', type=Path, default=DEFAULT_REVIEW)
    parser.add_argument('--overlap', type=Path, default=DEFAULT_OVERLAP)
    parser.add_argument('--network', type=Path, default=DEFAULT_NETWORK)
    parser.add_argument('--provenance', type=Path, default=DEFAULT_PROVENANCE)
    parser.add_argument('--figures-dir', type=Path, default=DEFAULT_FIGURES)
    parser.add_argument('--cosmograph-dir', type=Path, default=DEFAULT_COSMOGRAPH)
    parser.add_argument('--report', type=Path, default=DEFAULT_REPORT)
    parser.add_argument('--check-only', action='store_true')
    args = parser.parse_args()
    if not args.check_only:
        build_outputs(load_json(args.inventory), load_review(args.review), load_json(args.overlap), load_json(args.network), load_json(args.provenance), args.figures_dir, args.report, args.cosmograph_dir)
    summary = validate_outputs(args.figures_dir, args.report, args.cosmograph_dir)
    print('Ontology comparison visuals valid: {} figures, {} Cosmograph images, report {}'.format(summary['figure_count'], summary['cosmograph_image_count'], summary['report']))


if __name__ == '__main__':
    main()
