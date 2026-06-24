import argparse, csv, json, sys
from pathlib import Path
from rdflib import Graph


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
from scripts.maintenance import build_comparison_alignments as align
BASE = ROOT / "docs" / "ontology-comparison"
REQUIRED_FILES = [
    "discovery-protocol.md",
    "source-inventory.json",
    "source-inventory.md",
    "source-provenance.json",
    "inclusion-exclusion-log.jsonl",
    "term-inventory.jsonl",
    "mapping-candidates.jsonl",
    "mapping-review.csv",
    "accepted-alignments.ttl",
    "accepted-alignments.sssom.yml",
    "accepted-alignments.sssom.tsv",
    "overlap-metrics.json",
    "network-analysis.json",
    "network-sensitivity.json",
    "report.md",
]
REQUIRED_FIGURES = [
    "source_sizes_bar.svg",
    "match_classes_bar.svg",
    "source_module_overlap_heatmap.svg",
    "source_family_evidence_heatmap.svg",
    "source_family_term_heatmap.svg",
    "uogto_coverage_treemap.svg",
    "source_similarity_network.svg",
    "mapping_flow_sankey.svg",
    "reviewer_workload.svg",
]


def read_json(path):
    return json.loads(path.read_text(encoding="utf-8"))


def read_jsonl(path):
    with path.open("r", encoding="utf-8") as handle:
        return [json.loads(line) for line in handle if line.strip()]


def read_csv(path):
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def validate_artifacts(base=BASE):
    base = Path(base)
    missing = [name for name in REQUIRED_FILES if not (base / name).exists()]
    if missing:
        raise AssertionError("Missing ontology comparison artifacts: " + ", ".join(missing))
    inventory = read_json(base / "source-inventory.json")
    provenance = read_json(base / "source-provenance.json")
    terms = read_jsonl(base / "term-inventory.jsonl")
    candidates = read_jsonl(base / "mapping-candidates.jsonl")
    review = read_csv(base / "mapping-review.csv")
    overlap = read_json(base / "overlap-metrics.json")
    network = read_json(base / "network-analysis.json")
    sensitivity = read_json(base / "network-sensitivity.json")
    if len(inventory.get("sources", [])) < 20:
        raise AssertionError("Source inventory must contain the discovered seed source set")
    if len(provenance.get("sources", [])) != len(inventory.get("sources", [])):
        raise AssertionError("Every inventory source must have provenance")
    if len(terms) < 1000 or len(candidates) < 100 or len(review) != len(candidates):
        raise AssertionError("Term, candidate, and review artifacts are not internally consistent")
    if overlap.get("schema") != "uogto.ontology-comparison.overlap-metrics.v1":
        raise AssertionError("Unexpected overlap metrics schema")
    if network.get("schema") != "uogto.ontology-comparison.network-analysis.v1":
        raise AssertionError("Unexpected network analysis schema")
    if sensitivity.get("schema") != "uogto.ontology-comparison.network-sensitivity.v1":
        raise AssertionError("Unexpected network sensitivity schema")
    accepted = [row for row in review if row.get("review_status") == "accepted"]
    if overlap["summary"].get("accepted_mapping_count") != len(accepted):
        raise AssertionError("Overlap accepted mapping count does not match mapping review")
    graph = Graph(); graph.parse(base / "accepted-alignments.ttl", format="turtle")
    if len(graph) == 0:
        raise AssertionError("Accepted alignment TTL must parse with triples")
    sssom_summary = align.validate_sssom_outputs(
        base / "accepted-alignments.sssom.tsv",
        base / "accepted-alignments.sssom.yml",
        expected_count=len(accepted),
    )
    figures_dir = base / "figures"
    report = (base / "report.md").read_text(encoding="utf-8")
    for name in REQUIRED_FIGURES:
        figure = figures_dir / name
        if not figure.exists():
            raise AssertionError("Missing figure: " + name)
        text = figure.read_text(encoding="utf-8")
        if "<svg" not in text or "</svg>" not in text:
            raise AssertionError("Figure is not SVG: " + name)
        if "figures/" + name not in report:
            raise AssertionError("Report does not link figure: " + name)
    for section in ["## Inclusion and Exclusion Summary", "## Mapping Methods", "## Evidence-Level Coverage"]:
        if section not in report:
            raise AssertionError("Report missing required section: " + section)
    if "Candidate and rejected rows remain audit records" not in report:
        raise AssertionError("Report must separate accepted evidence from candidate/future work")
    return {
        "sources": len(inventory["sources"]),
        "terms": len(terms),
        "candidates": len(candidates),
        "accepted_mappings": len(accepted),
        "figures": len(REQUIRED_FIGURES),
        "sssom_rows": sssom_summary["row_count"],
    }


def main():
    parser = argparse.ArgumentParser(description="Validate generated ontology comparison artifacts.")
    parser.add_argument("--base", type=Path, default=BASE)
    args = parser.parse_args()
    summary = validate_artifacts(args.base)
    print("Ontology comparison artifacts valid: {sources} sources, {terms} terms, {candidates} candidates, {accepted_mappings} accepted mappings, {figures} figures.".format(**summary))


if __name__ == "__main__":
    main()
