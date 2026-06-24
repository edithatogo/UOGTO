from __future__ import annotations

from scripts.maintenance.build_network_sensitivity import build_network_sensitivity


def test_network_sensitivity_reports_source_and_alignment_changes() -> None:
    terms = [
        {"source_id": "source_a", "imports": ["https://example.org/import/a"]},
        {"source_id": "source_b", "imports": []},
        {"source_id": "source_c", "imports": []},
    ]
    provenance = {
        "sources": [
            {"id": "source_a", "retrieval_mode": "downloaded", "rdf_format": "turtle"},
            {"id": "source_b", "retrieval_mode": "metadata_only"},
            {"id": "source_c", "retrieval_mode": "downloaded", "rdf_format": "xml"},
        ]
    }
    review_rows = [
        {
            "review_status": "accepted",
            "source_term_iri": "https://example.org/source/a",
            "uogto_term_iri": "https://example.org/uogto/game",
            "decision_predicate": "owl:equivalentClass",
            "candidate_predicate": "owl:equivalentClass",
            "source_id": "source_a",
            "uogto_source_id": "uogto_core_games",
        },
        {
            "review_status": "needs_domain_review",
            "source_term_iri": "https://example.org/source/b",
            "uogto_term_iri": "https://example.org/uogto/game",
            "decision_predicate": "skos:relatedMatch",
            "candidate_predicate": "skos:relatedMatch",
            "source_id": "source_b",
            "uogto_source_id": "uogto_core_games",
        },
        {
            "review_status": "rejected",
            "source_term_iri": "https://example.org/source/c",
            "uogto_term_iri": "https://example.org/uogto/action",
            "decision_predicate": "skos:closeMatch",
            "candidate_predicate": "skos:closeMatch",
            "source_id": "source_c",
            "uogto_source_id": "uogto_core_actions",
        },
    ]

    packet = build_network_sensitivity(terms, review_rows, provenance)

    assert packet["schema"] == "uogto.ontology-comparison.network-sensitivity.v1"
    assert packet["summary"]["scenario_count"] == 4
    assert packet["sensitivity"]["metadata_only_exclusion"]["edge_delta"] < 0
    assert packet["sensitivity"]["accepted_only_vs_close_related"]["edge_delta"] > 0
    assert "metadata_only_sources" in packet["scenarios"]["all_sources__accepted_mappings"]["source_graph"]["nodes"]
    assert "metadata_only_sources" not in packet["scenarios"]["parsed_sources_only__accepted_mappings"]["source_graph"]["nodes"]
    assert packet["scenarios"]["all_sources__accepted_plus_close_related"]["alignment_graph"]["metrics"]["edge_count"] == 2
