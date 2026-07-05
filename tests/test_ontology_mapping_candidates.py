import json
import shutil
import unittest
import uuid
from pathlib import Path

from scripts.maintenance import generate_ontology_mapping_candidates as mapper
from scripts.maintenance import extract_comparison_terms


def row(source_id, kind, iri, label, term_type="class", tokens=None, definitions=None, source_name="Source"):
    return {
        "source_id": source_id,
        "source_name": source_name,
        "source_family": "demo",
        "source_kind": kind,
        "artifact_path": None,
        "term_iri": iri,
        "local_name": iri.rsplit("/", 1)[-1].rsplit("#", 1)[-1],
        "term_type": term_type,
        "label": label,
        "definitions": definitions or [],
        "comments": [],
        "synonyms": [],
        "parents": [],
        "domains": [],
        "ranges": [],
        "imports": [],
        "normalised_label": " ".join(tokens or extract_comparison_terms.tokens(label)),
        "tokens": tokens or extract_comparison_terms.tokens(label),
        "language": "en",
    }


class TestOntologyMappingCandidates(unittest.TestCase):
    def setUp(self):
        self.temp_dir = Path(".tmp") / f"test_ontology_mapping_candidates_{uuid.uuid4().hex}"
        self.temp_dir.mkdir(parents=True, exist_ok=True)

    def tearDown(self):
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_exact_label_classifies_as_equivalent_class(self):
        external = row("ext", "external_rdf", "https://example.test/Game", "Game", definitions=["A game."])
        uogto = row("uogto_core_games", "uogto", "https://w3id.org/uogto/core#Game", "Game", definitions=["A game."])
        candidate = mapper.make_candidate(external, uogto)
        self.assertIn(candidate["candidate_predicate"], {"owl:equivalentClass", "skos:exactMatch"})
        self.assertGreater(candidate["confidence"], 0.5)
        self.assertTrue(candidate["evidence"]["exact_label"])

    def test_property_type_compatibility_affects_predicate(self):
        external = row("ext", "external_rdf", "https://example.test/hasPlayer", "has player", "object_property")
        uogto = row("uogto_core_agents", "uogto", "https://w3id.org/uogto/core#hasPlayer", "has player", "object_property")
        candidate = mapper.make_candidate(external, uogto)
        self.assertEqual(candidate["candidate_predicate"], "owl:equivalentProperty")
        self.assertTrue(candidate["evidence"]["type_compatible"])

    def test_external_parent_axiom_classifies_as_narrow_match(self):
        external = row("prov_o", "external_rdf", "http://www.w3.org/ns/prov#Activity", "Activity", tokens=["activity"])
        uogto = row("uogto_alignments_prov-o", "uogto", "https://w3id.org/uogto/core#Action", "Action", tokens=["action"])
        uogto["parents"] = [external["term_iri"]]
        candidate = mapper.make_candidate(external, uogto)
        self.assertEqual(candidate["candidate_predicate"], "skos:narrowMatch")
        self.assertGreaterEqual(candidate["confidence"], 0.5)
        self.assertTrue(candidate["evidence"]["external_is_uogto_parent"])

    def test_incompatible_property_class_pair_is_no_match(self):
        external = row("prov_o", "external_rdf", "http://www.w3.org/ns/prov#agent", "agent", "object_property")
        uogto = row("uogto_alignments_prov-o", "uogto", "https://w3id.org/uogto/core#Agent", "Agent", "class")
        candidate = mapper.make_candidate(external, uogto)
        self.assertEqual(candidate["candidate_predicate"], "no_match")
        self.assertFalse(candidate["evidence"]["type_compatible"])

    def test_generate_candidates_is_deterministic_and_external_to_uogto(self):
        rows = [
            row("uogto_core_games", "uogto", "https://w3id.org/uogto/core#Game", "Game"),
            row("uogto_core_agents", "uogto", "https://w3id.org/uogto/core#Player", "Player"),
            row("schema_org", "external_rdf", "https://schema.org/Game", "Game"),
            row("schema_org", "external_rdf", "https://schema.org/Person", "Player"),
        ]
        first = mapper.generate_candidates(rows)
        second = mapper.generate_candidates(rows)
        self.assertEqual(first, second)
        self.assertGreaterEqual(len(first), 2)
        self.assertTrue(all(c["source_id"] == "schema_org" for c in first))
        self.assertTrue(all(c["uogto_source_id"].startswith("uogto_") for c in first))

    def test_generate_candidates_keeps_strongest_row_per_term_pair(self):
        external = row("schema_org", "external_rdf", "https://schema.org/Action", "Action")
        core = row("uogto_core", "uogto", "https://w3id.org/uogto/core#Action", "Action")
        alignment = row("uogto_alignments_schema-org", "uogto", "https://w3id.org/uogto/core#Action", "Action")
        alignment["parents"] = [external["term_iri"]]
        candidates = mapper.generate_candidates([core, alignment, external])
        pair_candidates = [
            candidate
            for candidate in candidates
            if candidate["source_term_iri"] == external["term_iri"]
            and candidate["uogto_term_iri"] == core["term_iri"]
        ]
        self.assertEqual(len(pair_candidates), 1)
        self.assertEqual(pair_candidates[0]["candidate_predicate"], "skos:narrowMatch")

    def test_validate_candidates_rejects_invalid_predicate(self):
        candidate = mapper.make_candidate(
            row("ext", "external_rdf", "https://example.test/Game", "Game"),
            row("uogto", "uogto", "https://w3id.org/uogto/core#Game", "Game"),
        )
        candidate["candidate_predicate"] = "bad:predicate"
        with self.assertRaisesRegex(AssertionError, "invalid predicate"):
            mapper.validate_candidates([candidate])

    def test_generated_repo_candidates_cover_multiple_sources(self):
        rows = mapper.generate_candidates(mapper.read_terms())
        summary = mapper.validate_candidates(rows)
        self.assertGreater(summary["candidate_count"], 100)
        self.assertGreater(summary["source_count"], 3)
        self.assertIn("skos:narrowMatch", summary["by_predicate"])

    def test_write_and_read_jsonl_round_trips(self):
        candidate = mapper.make_candidate(
            row("ext", "external_rdf", "https://example.test/Game", "Game"),
            row("uogto", "uogto", "https://w3id.org/uogto/core#Game", "Game"),
        )
        output = self.temp_dir / "candidates.jsonl"
        mapper.write_jsonl(output, [candidate])
        loaded = mapper.read_jsonl(output)
        self.assertEqual(loaded[0]["source_id"], "ext")
        self.assertEqual(mapper.validate_candidates(loaded)["candidate_count"], 1)


if __name__ == "__main__":
    unittest.main()
