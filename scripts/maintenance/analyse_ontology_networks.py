import argparse, csv, json, sys
from collections import Counter, defaultdict, deque
from itertools import combinations
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
from scripts.maintenance import extract_comparison_terms

DEFAULT_TERMS = ROOT / "docs" / "ontology-comparison" / "term-inventory.jsonl"
DEFAULT_REVIEW = ROOT / "docs" / "ontology-comparison" / "mapping-review.csv"
DEFAULT_PROVENANCE = ROOT / "docs" / "ontology-comparison" / "source-provenance.json"
DEFAULT_OUTPUT = ROOT / "docs" / "ontology-comparison" / "network-analysis.json"


def load_review(path=DEFAULT_REVIEW):
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def load_json(path):
    return json.loads(path.read_text(encoding="utf-8"))


def edge_key(left, right):
    return tuple(sorted([left, right]))


def graph_metrics(nodes, edges):
    adjacency = {node: set() for node in nodes}
    for left, right, *_ in edges:
        adjacency.setdefault(left, set()).add(right)
        adjacency.setdefault(right, set()).add(left)
    degree = {node: len(neighbours) for node, neighbours in adjacency.items()}
    components = []
    seen = set()
    for node in sorted(adjacency):
        if node in seen:
            continue
        queue = deque([node]); seen.add(node); component = []
        while queue:
            current = queue.popleft(); component.append(current)
            for neighbour in sorted(adjacency[current]):
                if neighbour not in seen:
                    seen.add(neighbour); queue.append(neighbour)
        components.append(sorted(component))
    closeness = {}
    betweenness_proxy = Counter()
    for start in sorted(adjacency):
        distances = {start: 0}; queue = deque([start])
        while queue:
            current = queue.popleft()
            for neighbour in sorted(adjacency[current]):
                if neighbour not in distances:
                    distances[neighbour] = distances[current] + 1; queue.append(neighbour)
        closeness[start] = round((len(distances) - 1) / sum(distances.values()), 4) if sum(distances.values()) else 0
        for target, distance in distances.items():
            if target != start and distance > 1:
                for middle in adjacency[start] & adjacency[target]:
                    betweenness_proxy[middle] += 1
    return {
        "node_count": len(adjacency),
        "edge_count": len(edges),
        "degree": dict(sorted(degree.items(), key=lambda item: (-item[1], item[0]))),
        "closeness": dict(sorted(closeness.items(), key=lambda item: (-item[1], item[0]))),
        "betweenness_proxy": dict(sorted(betweenness_proxy.items(), key=lambda item: (-item[1], item[0]))),
        "connected_components": components,
        "component_count": len(components),
        "orphan_nodes": sorted([node for node, value in degree.items() if value == 0]),
    }


def source_ontology_graph(terms, provenance):
    sources = sorted({row["source_id"] for row in terms})
    provenance_by_id = {record["id"]: record for record in provenance.get("sources", [])}
    edges = []
    for row in terms:
        for imported in row.get("imports", []):
            target = imported.rstrip("/").rsplit("/", 1)[-1] or imported
            edges.append((row["source_id"], f"import:{target}", "imports"))
    for record in provenance.get("sources", []):
        if record.get("retrieval_mode") == "downloaded":
            edges.append((record["id"], f"format:{record.get('rdf_format') or record.get('format_classification')}", "format"))
        else:
            edges.append((record["id"], "metadata_only_sources", "metadata"))
    nodes = set(sources) | {edge[1] for edge in edges}
    return {"nodes": sorted(nodes), "edges": sorted(edges), "metrics": graph_metrics(nodes, edges)}


def accepted_review_rows(review_rows):
    return [row for row in review_rows if row["review_status"] == "accepted"]


def term_alignment_graph(review_rows):
    accepted = accepted_review_rows(review_rows)
    nodes = set()
    edges = []
    for row in accepted:
        source_node = f"source:{row['source_term_iri']}"
        uogto_node = f"uogto:{row['uogto_term_iri']}"
        nodes.update([source_node, uogto_node])
        edges.append((source_node, uogto_node, row["decision_predicate"] or row["candidate_predicate"]))
    metrics = graph_metrics(nodes, edges)
    bridge_terms = sorted(metrics["degree"].items(), key=lambda item: (-item[1], item[0]))[:25]
    return {"nodes": sorted(nodes), "edges": sorted(edges), "metrics": metrics, "bridge_terms": [{"node": node, "degree": degree} for node, degree in bridge_terms]}


def token_sets_by_source(terms):
    by_source = defaultdict(set)
    for row in terms:
        by_source[row["source_id"]].update(row.get("tokens") or [])
    return by_source


def source_similarity_graph(terms, threshold=0.12):
    token_sets = token_sets_by_source(terms)
    nodes = sorted(token_sets)
    edges = []
    for left, right in combinations(nodes, 2):
        union = token_sets[left] | token_sets[right]
        score = len(token_sets[left] & token_sets[right]) / len(union) if union else 0
        if score >= threshold:
            edges.append((left, right, round(score, 4)))
    communities = defaultdict(list)
    for source, tokens in token_sets.items():
        signature = sorted(tokens)[:1] or ["empty"]
        communities[signature[0]].append(source)
    return {"nodes": nodes, "edges": sorted(edges), "metrics": graph_metrics(nodes, edges), "communities": {key: sorted(value) for key, value in sorted(communities.items())}}


def uogto_module_coverage_graph(review_rows):
    nodes = set()
    edges = []
    for row in review_rows:
        if row["review_status"] not in {"accepted", "needs_domain_review"}:
            continue
        nodes.update([row["source_id"], row["uogto_source_id"]])
        edges.append((row["source_id"], row["uogto_source_id"], row["review_status"]))
    return {"nodes": sorted(nodes), "edges": sorted(edges), "metrics": graph_metrics(nodes, edges)}


def source_family_clusters(terms):
    family_members = defaultdict(list)
    for row in terms:
        family_members[row["source_family"]].append(row["source_id"])
    return {family: sorted(set(sources)) for family, sources in sorted(family_members.items())}


def central_sources(*graphs):
    scores = Counter()
    for graph in graphs:
        for node, degree in graph["metrics"].get("degree", {}).items():
            if not node.startswith("source:") and not node.startswith("uogto:") and not node.startswith("format:") and not node.startswith("import:"):
                scores[node] += degree
    return [{"source_id": source, "centrality_score": score} for source, score in scores.most_common(25)]


def build_network_analysis(terms, review_rows, provenance):
    source_graph = source_ontology_graph(terms, provenance)
    alignment_graph = term_alignment_graph(review_rows)
    similarity_graph = source_similarity_graph(terms)
    coverage_graph = uogto_module_coverage_graph(review_rows)
    return {
        "schema": "uogto.ontology-comparison.network-analysis.v1",
        "summary": {
            "source_graph_nodes": source_graph["metrics"]["node_count"],
            "alignment_graph_edges": alignment_graph["metrics"]["edge_count"],
            "similarity_graph_edges": similarity_graph["metrics"]["edge_count"],
            "coverage_graph_edges": coverage_graph["metrics"]["edge_count"],
        },
        "source_ontology_graph": source_graph,
        "term_alignment_bipartite_graph": alignment_graph,
        "source_similarity_graph": similarity_graph,
        "import_uses_graph": source_graph,
        "uogto_module_coverage_graph": coverage_graph,
        "source_family_clusters": source_family_clusters(terms),
        "central_source_families": central_sources(source_graph, similarity_graph, coverage_graph),
        "isolated_modelling_paradigms": similarity_graph["metrics"]["orphan_nodes"],
        "bridge_terms": alignment_graph["bridge_terms"],
        "orphan_terms": alignment_graph["metrics"]["orphan_nodes"],
    }


def write_json(path, packet):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(packet, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def validate_network_analysis(packet):
    if packet.get("schema") != "uogto.ontology-comparison.network-analysis.v1":
        raise AssertionError("Unexpected network analysis schema")
    required = ["source_ontology_graph", "term_alignment_bipartite_graph", "source_similarity_graph", "import_uses_graph", "uogto_module_coverage_graph"]
    for key in required:
        if key not in packet or "metrics" not in packet[key]:
            raise AssertionError(f"Missing network graph {key}")
    if packet["term_alignment_bipartite_graph"]["metrics"]["edge_count"] <= 0:
        raise AssertionError("Term alignment graph must contain accepted mapping edges")
    return {"alignment_edges": packet["term_alignment_bipartite_graph"]["metrics"]["edge_count"], "similarity_edges": packet["source_similarity_graph"]["metrics"]["edge_count"]}


def main():
    parser = argparse.ArgumentParser(description="Analyse ontology comparison networks.")
    parser.add_argument("--terms", type=Path, default=DEFAULT_TERMS)
    parser.add_argument("--review", type=Path, default=DEFAULT_REVIEW)
    parser.add_argument("--provenance", type=Path, default=DEFAULT_PROVENANCE)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--check-only", action="store_true")
    args = parser.parse_args()
    if args.check_only:
        packet = load_json(args.output)
    else:
        packet = build_network_analysis(extract_comparison_terms.read_jsonl(args.terms), load_review(args.review), load_json(args.provenance))
        write_json(args.output, packet)
    summary = validate_network_analysis(packet)
    print(f"Ontology network analysis valid: {summary['alignment_edges']} alignment edges, {summary['similarity_edges']} source similarity edges.")

if __name__ == "__main__":
    main()
