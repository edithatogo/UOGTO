from __future__ import annotations

import argparse
import json
import sys
from collections import deque
from pathlib import Path
from typing import Any, Iterable

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.maintenance import analyse_ontology_networks as networks
from scripts.maintenance import extract_comparison_terms


DEFAULT_TERMS = ROOT / "docs" / "ontology-comparison" / "term-inventory.jsonl"
DEFAULT_REVIEW = ROOT / "docs" / "ontology-comparison" / "mapping-review.csv"
DEFAULT_PROVENANCE = ROOT / "docs" / "ontology-comparison" / "source-provenance.json"
DEFAULT_OUTPUT = ROOT / "docs" / "ontology-comparison" / "network-sensitivity.json"
DEFAULT_REPORT = ROOT / "docs" / "ontology-comparison" / "network-sensitivity.md"
RELATED_PREDICATES = {"skos:closeMatch", "skos:relatedMatch"}


def load_review(path: Path = DEFAULT_REVIEW) -> list[dict[str, Any]]:
    return networks.load_review(path)


def load_json(path: Path) -> dict[str, Any]:
    return networks.load_json(path)


def graph_bridge_terms(metrics: dict[str, Any], limit: int = 20) -> list[dict[str, Any]]:
    return [
        {"node": node, "degree": degree}
        for node, degree in sorted(metrics["degree"].items(), key=lambda item: (-item[1], item[0]))[:limit]
    ]


def graph_communities(metrics: dict[str, Any]) -> list[list[str]]:
    return [list(component) for component in metrics["connected_components"]]


def _graph_metrics(nodes: Iterable[str], edges: list[tuple[str, str, Any]]) -> dict[str, Any]:
    adjacency = {node: set() for node in nodes}
    for left, right, *_ in edges:
        adjacency.setdefault(left, set()).add(right)
        adjacency.setdefault(right, set()).add(left)
    degree = {node: len(neighbours) for node, neighbours in adjacency.items()}
    components: list[list[str]] = []
    seen: set[str] = set()
    for node in sorted(adjacency):
        if node in seen:
            continue
        queue = deque([node])
        seen.add(node)
        component: list[str] = []
        while queue:
            current = queue.popleft()
            component.append(current)
            for neighbour in sorted(adjacency[current]):
                if neighbour not in seen:
                    seen.add(neighbour)
                    queue.append(neighbour)
        components.append(sorted(component))
    return {
        "node_count": len(adjacency),
        "edge_count": len(edges),
        "degree": dict(sorted(degree.items(), key=lambda item: (-item[1], item[0]))),
        "connected_components": components,
        "component_count": len(components),
        "orphan_nodes": sorted([node for node, value in degree.items() if value == 0]),
    }


def source_ontology_graph(terms: list[dict[str, Any]], provenance: dict[str, Any], include_metadata_only: bool = True) -> dict[str, Any]:
    sources = sorted({row["source_id"] for row in terms})
    provenance_sources = provenance.get("sources", [])
    edges: list[tuple[str, str, str]] = []
    for row in terms:
        for imported in row.get("imports", []):
            target = imported.rstrip("/").rsplit("/", 1)[-1] or imported
            edges.append((row["source_id"], f"import:{target}", "imports"))
    for record in provenance_sources:
        if not include_metadata_only and record.get("retrieval_mode") == "metadata_only":
            continue
        if record.get("retrieval_mode") == "downloaded":
            edges.append((record["id"], f"format:{record.get('rdf_format') or record.get('format_classification')}", "format"))
        else:
            edges.append((record["id"], "metadata_only_sources", "metadata"))
    nodes = set(sources) | {edge[1] for edge in edges}
    metrics = _graph_metrics(nodes, edges)
    bridges = graph_bridge_terms(metrics)
    communities = graph_communities(metrics)
    return {"nodes": sorted(nodes), "edges": sorted(edges), "metrics": metrics, "bridge_terms": bridges, "communities": communities}


def term_alignment_graph(
    review_rows: list[dict[str, Any]],
    include_related: bool = False,
    statuses: set[str] | None = None,
) -> dict[str, Any]:
    accepted_statuses = statuses or {"accepted"}
    nodes: set[str] = set()
    edges: list[tuple[str, str, str]] = []
    for row in review_rows:
        predicate = row.get("decision_predicate") or row.get("candidate_predicate") or ""
        if include_related:
            if row["review_status"] not in {"accepted", "needs_domain_review"}:
                continue
            if row["review_status"] != "accepted" and predicate not in RELATED_PREDICATES:
                continue
        else:
            if row["review_status"] not in accepted_statuses:
                continue
        source_node = f"source:{row['source_term_iri']}"
        uogto_node = f"uogto:{row['uogto_term_iri']}"
        nodes.update([source_node, uogto_node])
        edges.append((source_node, uogto_node, predicate or row["review_status"]))
    metrics = _graph_metrics(nodes, edges)
    bridges = graph_bridge_terms(metrics)
    communities = graph_communities(metrics)
    return {"nodes": sorted(nodes), "edges": sorted(edges), "metrics": metrics, "bridge_terms": bridges, "communities": communities}


def _top_bridge_nodes(graph: dict[str, Any], limit: int = 5) -> list[str]:
    return [entry["node"] for entry in graph["bridge_terms"][:limit]]


def _scenario_delta(before: dict[str, Any], after: dict[str, Any]) -> dict[str, Any]:
    before_nodes = set(before["nodes"])
    after_nodes = set(after["nodes"])
    before_bridges = set(_top_bridge_nodes(before, limit=10))
    after_bridges = set(_top_bridge_nodes(after, limit=10))
    return {
        "node_delta": after["metrics"]["node_count"] - before["metrics"]["node_count"],
        "edge_delta": after["metrics"]["edge_count"] - before["metrics"]["edge_count"],
        "component_delta": after["metrics"]["component_count"] - before["metrics"]["component_count"],
        "bridge_nodes_added": sorted(after_bridges - before_bridges),
        "bridge_nodes_removed": sorted(before_bridges - after_bridges),
        "nodes_added": sorted(after_nodes - before_nodes)[:20],
        "nodes_removed": sorted(before_nodes - after_nodes)[:20],
        "community_count_before": before["metrics"]["component_count"],
        "community_count_after": after["metrics"]["component_count"],
    }


def build_network_sensitivity(
    terms: list[dict[str, Any]],
    review_rows: list[dict[str, Any]],
    provenance: dict[str, Any],
) -> dict[str, Any]:
    source_all = source_ontology_graph(terms, provenance, include_metadata_only=True)
    source_parsed = source_ontology_graph(terms, provenance, include_metadata_only=False)
    alignment_accepted = term_alignment_graph(review_rows, include_related=False, statuses={"accepted"})
    alignment_extended = term_alignment_graph(review_rows, include_related=True, statuses={"accepted", "needs_domain_review"})

    scenarios = {
        "all_sources__accepted_mappings": {
            "source_graph": source_all,
            "alignment_graph": alignment_accepted,
        },
        "parsed_sources_only__accepted_mappings": {
            "source_graph": source_parsed,
            "alignment_graph": alignment_accepted,
        },
        "all_sources__accepted_plus_close_related": {
            "source_graph": source_all,
            "alignment_graph": alignment_extended,
        },
        "parsed_sources_only__accepted_plus_close_related": {
            "source_graph": source_parsed,
            "alignment_graph": alignment_extended,
        },
    }

    sensitivity = {
        "metadata_only_exclusion": _scenario_delta(source_all, source_parsed),
        "accepted_only_vs_close_related": _scenario_delta(alignment_accepted, alignment_extended),
        "bridge_overlap": {
            "source_graph": sorted(set(_top_bridge_nodes(source_all)).intersection(_top_bridge_nodes(source_parsed))),
            "alignment_graph": sorted(set(_top_bridge_nodes(alignment_accepted)).intersection(_top_bridge_nodes(alignment_extended))),
        },
    }

    return {
        "schema": "uogto.ontology-comparison.network-sensitivity.v1",
        "summary": {
            "source_count": len({row["source_id"] for row in terms}),
            "review_row_count": len(review_rows),
            "provenance_source_count": len(provenance.get("sources", [])),
            "scenario_count": len(scenarios),
        },
        "scenarios": scenarios,
        "sensitivity": sensitivity,
    }


def write_json(path: Path, packet: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(packet, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def write_report(path: Path, packet: dict[str, Any]) -> None:
    scenarios = packet["scenarios"]
    sensitivity = packet["sensitivity"]
    lines = [
        "# Network analysis sensitivity",
        "",
        "This report compares network communities and bridge terms across the key network-analysis toggles.",
        "",
        "## Scenarios",
        "",
        "| scenario | source nodes | source edges | source communities | alignment nodes | alignment edges | alignment communities |",
        "| --- | ---: | ---: | ---: | ---: | ---: | ---: |",
    ]
    for name, payload in scenarios.items():
        source_graph = payload["source_graph"]
        alignment_graph = payload["alignment_graph"]
        lines.append(
            "| {} | {} | {} | {} | {} | {} | {} |".format(
                name,
                source_graph["metrics"]["node_count"],
                source_graph["metrics"]["edge_count"],
                source_graph["metrics"]["component_count"],
                alignment_graph["metrics"]["node_count"],
                alignment_graph["metrics"]["edge_count"],
                alignment_graph["metrics"]["component_count"],
            )
        )
    lines.extend(
        [
            "",
            "## Sensitivity",
            "",
            f"- Metadata-only exclusion changed source communities by {sensitivity['metadata_only_exclusion']['component_delta']}.",
            f"- Metadata-only exclusion changed source bridge nodes by removing {', '.join(sensitivity['metadata_only_exclusion']['bridge_nodes_removed']) or 'none'}.",
            f"- Accepting close/related mappings changed alignment communities by {sensitivity['accepted_only_vs_close_related']['component_delta']}.",
            f"- Accepting close/related mappings changed alignment bridge nodes by adding {', '.join(sensitivity['accepted_only_vs_close_related']['bridge_nodes_added']) or 'none'}.",
            "",
            "## Bridge Overlap",
            "",
            f"- Source-graph bridge overlap: {', '.join(sensitivity['bridge_overlap']['source_graph']) or 'none'}.",
            f"- Alignment-graph bridge overlap: {', '.join(sensitivity['bridge_overlap']['alignment_graph']) or 'none'}.",
            "",
            "The accepted-only and close/related variants let the article report how much network structure depends on conservative review versus permissive relational inclusion.",
        ]
    )
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def generate_report(
    terms_path: Path = DEFAULT_TERMS,
    review_path: Path = DEFAULT_REVIEW,
    provenance_path: Path = DEFAULT_PROVENANCE,
    output_path: Path = DEFAULT_OUTPUT,
    report_path: Path = DEFAULT_REPORT,
) -> dict[str, Any]:
    terms = extract_comparison_terms.read_jsonl(terms_path)
    review_rows = load_review(review_path)
    provenance = load_json(provenance_path)
    packet = build_network_sensitivity(terms, review_rows, provenance)
    write_json(output_path, packet)
    write_report(report_path, packet)
    return packet


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--terms", type=Path, default=DEFAULT_TERMS)
    parser.add_argument("--review", type=Path, default=DEFAULT_REVIEW)
    parser.add_argument("--provenance", type=Path, default=DEFAULT_PROVENANCE)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--report", type=Path, default=DEFAULT_REPORT)
    args = parser.parse_args(argv)
    generate_report(args.terms, args.review, args.provenance, args.output, args.report)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
