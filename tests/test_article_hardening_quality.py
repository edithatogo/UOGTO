from pathlib import Path

from scripts.maintenance import build_article_hardening_quality as quality


ROOT = Path(__file__).resolve().parents[1]


def test_quality_metrics_outputs_validate():
    summary = quality.check_outputs(
        ROOT / "docs" / "article-hardening" / "quality-metrics.json",
        ROOT / "docs" / "article-hardening" / "reasoner-report.md",
    )
    assert summary["classes"] > 100
    assert summary["properties"] > 50
    assert summary["examples"] >= 10
    assert summary["queries"] >= 10


def test_quality_metrics_include_requested_benchmark_families():
    metrics = quality.read_json(ROOT / "docs" / "article-hardening" / "quality-metrics.json")
    for section in [
        "annotation_completeness",
        "orphan_classes",
        "relation_richness",
        "hierarchy_depth",
        "import_depth",
        "shacl_coverage",
        "shacl_example_module_coverage",
        "examples_per_module",
        "competency_query_coverage",
        "owl_profile_reasoner_status",
    ]:
        assert section in metrics
    assert metrics["annotation_completeness"]["global"]["label_completeness"] == 1.0
    assert metrics["annotation_completeness"]["global"]["definition_completeness"] == 1.0
    assert metrics["hierarchy_depth"]["max_depth"] >= 1
    assert metrics["competency_query_coverage"]["executable_count"] == metrics["scope"]["competency_query_count"]
    assert metrics["competency_query_coverage"]["queries_with_example_graph_links"] == metrics["scope"]["competency_query_count"]
    assert metrics["shacl_example_module_coverage"]["example_graph_coverage"] == 1.0
    assert metrics["shacl_example_module_coverage"]["module_shape_coverage"] == 1.0


def test_quality_metrics_include_local_pitfall_indicators():
    metrics = quality.read_json(ROOT / "docs" / "article-hardening" / "quality-metrics.json")
    pitfall = metrics["pitfall_indicators"]
    assert pitfall["method"].startswith("local OOPS-style")
    assert "missing_labels" in pitfall["indicators"]
    assert "orphan_classes" in pitfall["indicators"]


def test_reasoner_report_contains_quality_sections():
    report = (ROOT / "docs" / "article-hardening" / "reasoner-report.md").read_text(
        encoding="utf-8"
    )
    for section in [
        "## Annotation Completeness",
        "## Structural Metrics",
        "## SHACL and Example Coverage",
        "## Competency Query Coverage",
        "## Pitfall Indicators",
        "## OWL Profile and Reasoner Status",
    ]:
        assert section in report
