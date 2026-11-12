import csv
import json
import shutil
import unittest
import uuid
from pathlib import Path

from rdflib import Graph, URIRef
from rdflib.namespace import OWL, SKOS

from scripts.maintenance import build_comparison_alignments as align
from scripts.maintenance import generate_ontology_mapping_candidates as mapper


def candidate(confidence=0.9, predicate="skos:exactMatch", flags=None):
    return {
        "source_id": "schema_org",
        "source_term_iri": "https://schema.org/Game",
        "source_label": "Game",
        "source_term_type": "class",
        "uogto_source_id": "uogto_core_games",
        "uogto_term_iri": "https://w3id.org/uogto/core#Game",
        "uogto_label": "Game",
        "uogto_term_type": "class",
        "candidate_predicate": predicate,
        "confidence": confidence,
        "evidence": {"lexical_similarity": 1, "definition_similarity": 0.8, "structural_similarity": 0, "property_signature_similarity": 0, "embedding_similarity": 1, "source_reliability": 1},
        "review_flags": flags or [],
        "status": "candidate",
    }


class TestComparisonAlignments(unittest.TestCase):
    def setUp(self):
        self.temp_dir = Path(".tmp") / f"test_comparison_alignments_{uuid.uuid4().hex}"
        self.temp_dir.mkdir(parents=True, exist_ok=True)

    def tearDown(self):
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_prefill_decision_keeps_high_confidence_candidate_for_review(self):
        status, predicate, reviewer, rationale = align.prefill_decision(candidate())
        self.assertEqual(status, "needs_domain_review")
        self.assertEqual(predicate, "skos:exactMatch")
        self.assertEqual(reviewer, "automation_prefill")
        self.assertIn("candidate only", rationale)

    def test_prefill_decision_accepts_parent_backed_narrow_match(self):
        item = candidate(0.58, "skos:narrowMatch")
        item["evidence"]["external_is_uogto_parent"] = True
        status, predicate, reviewer, rationale = align.prefill_decision(item)
        self.assertEqual(status, "accepted")
        self.assertEqual(predicate, "skos:narrowMatch")
        self.assertEqual(reviewer, "repository_structural_evidence")
        self.assertIn("subclass", rationale)

    def test_prefill_decision_rejects_incompatible_term_types(self):
        item = candidate(0.48, "no_match")
        item["evidence"]["type_compatible"] = False
        status, predicate, reviewer, rationale = align.prefill_decision(item)
        self.assertEqual(status, "rejected")
        self.assertEqual(predicate, "")
        self.assertEqual(reviewer, "automation_prefill")
        self.assertIn("incompatible term types", rationale)

    def test_review_csv_round_trip_and_validation(self):
        rows = align.review_rows([candidate(), candidate(0.3, "skos:relatedMatch", ["low_confidence"])])
        output = self.temp_dir / "review.csv"
        align.write_review_csv(output, rows)
        loaded = align.read_review_csv(output)
        summary = align.validate_review_rows(loaded)
        self.assertEqual(summary["row_count"], 2)
        self.assertIn("needs_domain_review", summary["by_status"])
        with output.open("r", encoding="utf-8", newline="") as handle:
            self.assertIn("decision_predicate", next(csv.reader(handle)))

    def test_alignment_ttl_contains_accepted_mapping(self):
        item = candidate(predicate="skos:narrowMatch")
        item["evidence"]["external_is_uogto_parent"] = True
        rows = align.review_rows([item])
        output = self.temp_dir / "accepted-alignments.ttl"
        triple_count = align.write_alignment_ttl(output, rows)
        self.assertGreater(triple_count, 0)
        graph = Graph(); graph.parse(output, format="turtle")
        self.assertIn((URIRef("https://schema.org/Game"), SKOS.narrowMatch, URIRef("https://w3id.org/uogto/core#Game")), graph)
        self.assertGreaterEqual(align.validate_alignment_ttl(output)["mapping_count"], 1)

    def test_accepted_lexical_equivalence_cannot_bypass_export_guard(self):
        row = align.review_rows([candidate()])[0]
        row["review_status"] = "accepted"
        for export in (align.build_alignment_graph, align.sssom_rows, align.validate_review_rows):
            with self.assertRaisesRegex(AssertionError, "scoped semantic evidence"):
                export([row])

    def test_explicit_scoped_evidence_allows_reviewed_equivalence(self):
        row = align.review_rows([candidate()])[0]
        row["review_status"] = "accepted"
        evidence = json.loads(row["evidence_json"])
        evidence["semantic_equivalence_evidence"] = {
            "source_scope": "Synthetic test concept scope",
            "target_scope": "Synthetic test concept scope",
            "justification": "Synthetic fixture explicitly stipulates the same concept scope.",
            "reference": "tests/test_comparison_alignments.py synthetic fixture",
        }
        row["evidence_json"] = json.dumps(evidence)
        self.assertEqual(align.validate_review_rows([row])["by_status"], {"accepted": 1})
        self.assertEqual(len(align.sssom_rows([row])), 1)
        self.assertIn((URIRef(row["source_term_iri"]), SKOS.exactMatch, URIRef(row["uogto_term_iri"])), align.build_alignment_graph([row]))

    def test_known_bad_equivalences_are_rejected_and_cannot_be_exported(self):
        for (source, target), rationale in align.KNOWN_INCOMPATIBLE_PAIRS.items():
            item = candidate(predicate="owl:equivalentClass")
            item.update(source_term_iri=source, uogto_term_iri=target)
            status, _, reviewer, reason = align.prefill_decision(item)
            self.assertEqual(status, "rejected")
            self.assertEqual(reason, rationale)
            row = align.review_rows([item])[0]
            row.update(review_status="accepted", decision_predicate="skos:exactMatch", reviewer="claimed_review")
            for export in (align.build_alignment_graph, align.sssom_rows, align.validate_review_rows):
                with self.assertRaisesRegex(AssertionError, "Incompatible equivalence"):
                    export([row])

    def test_invalid_review_status_is_rejected(self):
        row = align.review_rows([candidate()])[0]
        row["review_status"] = "maybe"
        with self.assertRaisesRegex(AssertionError, "invalid status"):
            align.validate_review_rows([row])

    def test_generated_repo_review_and_alignment_outputs_validate(self):
        candidates = mapper.read_jsonl(mapper.DEFAULT_OUTPUT)
        rows = align.review_rows(candidates)
        review_summary = align.validate_review_rows(rows)
        self.assertGreater(review_summary["row_count"], 100)
        self.assertIn("accepted", review_summary["by_status"])
        output = self.temp_dir / "accepted-alignments.ttl"
        align.write_alignment_ttl(output, rows)
        ttl_summary = align.validate_alignment_ttl(output)
        self.assertGreater(ttl_summary["mapping_count"], 0)


if __name__ == "__main__":
    unittest.main()
