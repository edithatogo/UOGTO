import csv
import shutil
import unittest
import uuid
from pathlib import Path

from scripts.maintenance import build_comparison_alignments as align


class TestSssomMappingOutputs(unittest.TestCase):
    def setUp(self):
        self.temp_dir = Path(".tmp") / f"test_sssom_mapping_outputs_{uuid.uuid4().hex}"
        self.temp_dir.mkdir(parents=True, exist_ok=True)

    def tearDown(self):
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_known_alignment_iris_contract_to_curies(self):
        self.assertEqual(align.curie_for_iri("https://w3id.org/uogto/core#Agent"), "uogto:Agent")
        self.assertEqual(align.curie_for_iri("http://www.w3.org/ns/prov#Agent"), "prov:Agent")
        self.assertEqual(align.curie_for_iri("http://www.w3.org/2002/07/owl#Thing"), "owl:Thing")

    def test_sssom_outputs_are_generated_from_accepted_rows(self):
        rows = align.review_rows([
            {
                "source_id": "schema_org",
                "source_term_iri": "https://schema.org/Action",
                "source_label": "Action",
                "source_term_type": "class",
                "uogto_source_id": "uogto_core_uogto-core",
                "uogto_term_iri": "https://w3id.org/uogto/core#Action",
                "uogto_label": "Action",
                "uogto_term_type": "class",
                "candidate_predicate": "owl:equivalentClass",
                "confidence": 0.9,
                "evidence": {
                    "exact_label": True,
                    "exact_iri": False,
                    "normalized_label": True,
                    "synonym": False,
                },
                "review_flags": [],
                "status": "candidate",
            }
        ])
        tsv = self.temp_dir / "accepted-alignments.sssom.tsv"
        metadata = self.temp_dir / "accepted-alignments.sssom.yml"
        summary = align.write_sssom_outputs(tsv, metadata, rows)
        self.assertEqual(summary["row_count"], 1)
        with tsv.open("r", encoding="utf-8", newline="") as handle:
            loaded = list(csv.DictReader(handle, delimiter="\t"))
        self.assertEqual(loaded[0]["subject_id"], "schema:Action")
        self.assertEqual(loaded[0]["object_id"], "uogto:Action")
        self.assertEqual(loaded[0]["mapping_justification"], "semapv:LexicalMatching")

    def test_repo_sssom_outputs_validate(self):
        summary = align.validate_sssom_outputs()
        self.assertEqual(summary["row_count"], 12)


if __name__ == "__main__":
    unittest.main()
