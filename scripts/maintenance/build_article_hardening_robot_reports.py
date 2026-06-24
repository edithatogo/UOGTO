"""Build ROBOT-style ontology reports for article hardening.

The portable baseline stays RDFLib/pySHACL. If ROBOT tooling is available
later, these outputs can be regenerated from the same inputs.
"""

from __future__ import annotations

import argparse
import json
import os
import shutil
import sys
from pathlib import Path

from rdflib import Graph, URIRef
from rdflib.namespace import OWL, RDF

ROOT = Path(__file__).resolve().parents[2]
DOCS = ROOT / "docs" / "article-hardening" / "robot"
DEFAULT_STATUS = DOCS / "status.json"
DEFAULT_REASONER = DOCS / "reasoner-check.md"
DEFAULT_REPORT = DOCS / "report.md"
DEFAULT_MERGED = DOCS / "merged-ontology.ttl"
DEFAULT_DIFF = DOCS / "merge-diff.md"
DEFAULT_EXTRACTED = DOCS / "import-extraction.ttl"
DEFAULT_EXTRACTION_REPORT = DOCS / "import-extraction.md"
ROOT_ONTOLOGY = ROOT / "ontologies" / "core" / "uogto-core.ttl"

if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.maintenance import build_article_hardening_quality as quality_builder  # noqa: E402


def java_toolchain_status() -> dict:
    java_path = shutil.which("java")
    robot_path = shutil.which("robot")
    robot_jar = os.environ.get("ROBOT_JAR")
    robot_available = bool(robot_path or (java_path and robot_jar))
    return {
        "java_available": java_path is not None,
        "java_path": java_path,
        "robot_available": robot_available,
        "robot_command": robot_path,
        "robot_jar": robot_jar,
        "mode": "robot" if robot_available else "portable-baseline",
    }


def load_graphs() -> tuple[list[Path], dict[str, Graph], Graph]:
    module_paths = quality_builder.ttl_files()
    module_graphs = {quality_builder.module_id(path): quality_builder.parse_graph(path) for path in module_paths}
    merged_graph = Graph()
    for graph in module_graphs.values():
        merged_graph += graph
    return module_paths, module_graphs, merged_graph


def root_ontology_iri(graph: Graph) -> URIRef:
    ontologies = [subject for subject in graph.subjects(RDF.type, OWL.Ontology) if isinstance(subject, URIRef)]
    if not ontologies:
        return URIRef(str(ROOT_ONTOLOGY))
    return ontologies[0]


def import_closure() -> Graph:
    # No module imports are currently declared in the repository, so the
    # extracted closure is the root ontology snapshot itself.
    return quality_builder.parse_graph(ROOT_ONTOLOGY)


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def write_json(path: Path, payload: dict) -> None:
    write_text(path, json.dumps(payload, indent=2, ensure_ascii=True, sort_keys=True) + "\n")


def build_merged_turtle(graph: Graph, path: Path) -> int:
    ttl = graph.serialize(format="turtle")
    write_text(path, ttl if isinstance(ttl, str) else ttl.decode("utf-8"))
    return len(graph)


def render_reasoner_check(metrics: dict, toolchain: dict) -> str:
    reasoner = metrics["owl_profile_reasoner_status"]
    lines = [
        "# ROBOT-Style Reasoner Check",
        "",
        "## Toolchain",
        "",
        f"- Java available: {toolchain['java_available']}",
        f"- ROBOT available: {toolchain['robot_available']}",
        f"- Mode: {toolchain['mode']}",
        "",
        "## Portable Baseline",
        "",
        f"- RDF parse status: {reasoner['rdf_parse_status']}",
        f"- OWL profile screen: {reasoner['owl_profile_screen']['status']}",
        f"- OWL RL reasoner status: {reasoner['reasoner']['owlrl_status']}",
        f"- OWL RL triples before closure: {reasoner['reasoner']['owlrl_triples_before']}",
        f"- OWL RL triples after closure: {reasoner['reasoner']['owlrl_triples_after']}",
        f"- pySHACL RDFS example status: {reasoner['pyshacl_examples_rdfs_status']}",
        "",
        "## Notes",
        "",
        "- ROBOT tooling is optional and not required for the portable baseline.",
        "- This report is generated from RDFLib and pySHACL outputs so the repository stays runnable without Java.",
        "",
    ]
    return "\n".join(lines)


def render_report(metrics: dict, toolchain: dict, merged_count: int, root_count: int, import_count: int, diff_count: int) -> str:
    ann = metrics["annotation_completeness"]["global"]
    shacl = metrics["shacl_coverage"]
    reasoner = metrics["owl_profile_reasoner_status"]
    lines = [
        "# ROBOT-Style Ontology Report",
        "",
        "This report preserves a ROBOT-like reporting surface while keeping RDFLib/pySHACL as the baseline.",
        "",
        "## Scope",
        "",
        f"- Ontology files merged: {metrics['scope']['ontology_file_count']}",
        f"- Root ontology: `{quality_builder.rel(ROOT_ONTOLOGY)}`",
        f"- Java available: {toolchain['java_available']}",
        f"- ROBOT available: {toolchain['robot_available']}",
        f"- Operating mode: {toolchain['mode']}",
        "",
        "## Reasoner",
        "",
        f"- OWL profile screen: {reasoner['owl_profile_screen']['status']}",
        f"- OWL RL reasoner status: {reasoner['reasoner']['owlrl_status']}",
        f"- pySHACL RDFS example status: {reasoner['pyshacl_examples_rdfs_status']}",
        "",
        "## Merge",
        "",
        f"- Root triple count: {root_count}",
        f"- Merged triple count: {merged_count}",
        f"- Triples added beyond root: {diff_count}",
        "",
        "## Import Extraction",
        "",
        f"- Declared imports found: {import_count}",
        f"- Extracted triple count: {root_count}",
        "- Because the ontology files do not currently declare owl:imports, the extracted closure is the root ontology snapshot.",
        "",
        "## Quality Snapshot",
        "",
        f"- Label completeness: {ann['label_completeness']}",
        f"- Definition completeness: {ann['definition_completeness']}",
        f"- SHACL target class coverage: {shacl['target_class_coverage']}",
        f"- SHACL property path coverage: {shacl['property_path_coverage']}",
        "",
        "## Limitations",
        "",
        "- ROBOT-specific execution is deferred until a robot binary or jar is configured.",
        "- The portable baseline remains deterministic and suitable for CI without Java.",
        "",
    ]
    return "\n".join(lines)


def render_diff(import_count: int, added_triples: int, root_count: int, module_paths: list[Path]) -> str:
    lines = [
        "# ROBOT-Style Merge/Diff Summary",
        "",
        f"- Import declarations detected: {import_count}",
        f"- Root ontology triples: {root_count}",
        f"- Triples added by module aggregation: {added_triples}",
        f"- Module files contributing to merge: {len(module_paths)}",
        "",
        "## Interpretation",
        "",
        "- With no owl:imports graph in the repository, the merge/diff surface is a file-level aggregation rather than a true import-closure diff.",
        "- This still provides a stable regression view for ontology-file churn, term additions, and module-scope growth.",
        "",
    ]
    return "\n".join(lines)


def render_extraction_report(import_count: int, extracted_count: int, toolchain: dict) -> str:
    lines = [
        "# ROBOT-Style Import Extraction",
        "",
        f"- Java available: {toolchain['java_available']}",
        f"- ROBOT available: {toolchain['robot_available']}",
        f"- Declared imports found: {import_count}",
        f"- Extracted triple count: {extracted_count}",
        "",
        "## Notes",
        "",
        "- The repository currently has no owl:imports declarations, so the extracted ontology is the root ontology snapshot.",
        "- If ROBOT tooling is later configured, this output can be regenerated from the same inputs using a true import closure extraction command.",
        "",
    ]
    return "\n".join(lines)


def build_outputs(
    status_path: Path,
    reasoner_path: Path,
    report_path: Path,
    merged_path: Path,
    diff_path: Path,
    extracted_path: Path,
    extraction_report_path: Path,
) -> dict:
    toolchain = java_toolchain_status()
    module_paths, _, merged_graph = load_graphs()
    metrics = quality_builder.build_metrics()
    root_graph = quality_builder.parse_graph(ROOT_ONTOLOGY)
    root_count = len(root_graph)
    merged_count = build_merged_turtle(merged_graph, merged_path)
    extracted_graph = import_closure()
    extracted_count = len(extracted_graph)
    write_text(extracted_path, extracted_graph.serialize(format="turtle"))
    root_iri = root_ontology_iri(root_graph)
    import_count = sum(1 for _ in root_graph.objects(root_iri, OWL.imports))
    diff_count = max(0, merged_count - root_count)
    write_text(reasoner_path, render_reasoner_check(metrics, toolchain))
    write_text(report_path, render_report(metrics, toolchain, merged_count, root_count, import_count, diff_count))
    write_text(diff_path, render_diff(import_count, diff_count, root_count, module_paths))
    write_text(extraction_report_path, render_extraction_report(import_count, extracted_count, toolchain))
    payload = {
        "schema": "uogto.article-hardening.robot-style.v1",
        "created": quality_builder.REGISTER_DATE,
        "mode": toolchain["mode"],
        "toolchain": toolchain,
        "inputs": {
            "ontology_file_count": len(module_paths),
            "root_ontology": quality_builder.rel(ROOT_ONTOLOGY),
            "root_triple_count": root_count,
            "merged_triple_count": merged_count,
        },
        "reasoner": metrics["owl_profile_reasoner_status"],
        "merge": {
            "added_triples": diff_count,
            "module_count": len(module_paths),
        },
        "import_extraction": {
            "declared_import_count": import_count,
            "extracted_triple_count": extracted_count,
        },
        "artifacts": {
            "reasoner_check": quality_builder.rel(reasoner_path),
            "report": quality_builder.rel(report_path),
            "merged_ontology": quality_builder.rel(merged_path),
            "merge_diff": quality_builder.rel(diff_path),
            "import_extraction": quality_builder.rel(extracted_path),
            "import_extraction_report": quality_builder.rel(extraction_report_path),
        },
        "notes": [
            "ROBOT-style outputs are optional and can be regenerated once a robot binary or jar is configured.",
            "The portable baseline continues to use RDFLib and pySHACL.",
        ],
    }
    write_json(status_path, payload)
    return payload


def main() -> None:
    parser = argparse.ArgumentParser(description="Build ROBOT-style ontology reports for article hardening.")
    parser.add_argument("--status", type=Path, default=DEFAULT_STATUS)
    parser.add_argument("--reasoner-check", type=Path, default=DEFAULT_REASONER)
    parser.add_argument("--report", type=Path, default=DEFAULT_REPORT)
    parser.add_argument("--merged", type=Path, default=DEFAULT_MERGED)
    parser.add_argument("--diff", type=Path, default=DEFAULT_DIFF)
    parser.add_argument("--extracted", type=Path, default=DEFAULT_EXTRACTED)
    parser.add_argument("--extraction-report", type=Path, default=DEFAULT_EXTRACTION_REPORT)
    args = parser.parse_args()
    build_outputs(
        args.status,
        args.reasoner_check,
        args.report,
        args.merged,
        args.diff,
        args.extracted,
        args.extraction_report,
    )
    print("ROBOT-style article-hardening reports generated.")


if __name__ == "__main__":
    main()
