import unittest
import os
import shutil
import uuid
from pathlib import Path
from rdflib import Graph
from uogto.runner.engine import RDFGameRunner, UOGTO

class TestRDFGameRunner(unittest.TestCase):
    def setUp(self):
        # We will create a temporary Turtle file containing a simple NormalFormGame specification
        self.temp_dir = Path(".tmp") / f"test_game_runner_{uuid.uuid4().hex}"
        self.temp_dir.mkdir(parents=True, exist_ok=True)
        self.ttl_path = os.path.join(self.temp_dir, "test_game.ttl")
        
        # Write a simple game graph with Alice and Bob, action choices (Cooperate, Defect),
        # and payoff values mapping to action profiles.
        ttl_content = """
        @prefix uogto:  <https://w3id.org/uogto/core#> .
        @prefix ex:     <http://example.org/> .
        @prefix rdfs:   <http://www.w3.org/2000/01/rdf-schema#> .
        @prefix xsd:    <http://www.w3.org/2001/XMLSchema#> .

        ex:prisoners-dilemma a uogto:GameSpecification ;
            rdfs:label "Prisoner's Dilemma" ;
            uogto:hasPlayer ex:alice, ex:bob ;
            uogto:hasActionSpace ex:alice-space, ex:bob-space ;
            uogto:hasPayoffMapping ex:mapping-cc, ex:mapping-cd, ex:mapping-dc, ex:mapping-dd .

        ex:alice a uogto:Player ;
            rdfs:label "Alice" .

        ex:bob a uogto:Player ;
            rdfs:label "Bob" .

        ex:alice-space a uogto:ActionSpace ;
            uogto:belongsToPlayer ex:alice ;
            uogto:hasAction ex:cooperate, ex:defect .

        ex:bob-space a uogto:ActionSpace ;
            uogto:belongsToPlayer ex:bob ;
            uogto:hasAction ex:cooperate, ex:defect .

        ex:cooperate a uogto:Action ;
            rdfs:label "Cooperate" ;
            uogto:belongsToPlayer ex:alice, ex:bob .

        ex:defect a uogto:Action ;
            rdfs:label "Defect" ;
            uogto:belongsToPlayer ex:alice, ex:bob .

        # Profiles
        ex:profile-cc a uogto:ActionProfile ;
            uogto:hasAction ex:cooperate .

        ex:profile-dd a uogto:ActionProfile ;
            uogto:hasAction ex:defect .

        # Payoff mappings
        ex:mapping-cc a uogto:PayoffMapping ;
            uogto:hasActionProfile ex:profile-cc ;
            uogto:belongsToPlayer ex:alice, ex:bob ;
            uogto:payoffValue 3.0 .

        ex:mapping-dd a uogto:PayoffMapping ;
            uogto:hasActionProfile ex:profile-dd ;
            uogto:belongsToPlayer ex:alice, ex:bob ;
            uogto:payoffValue 1.0 .
        """
        with open(self.ttl_path, "w", encoding="utf-8") as f:
            f.write(ttl_content)
            
        self.runner = RDFGameRunner(self.ttl_path)

    def tearDown(self):
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_get_game_specification(self):
        specs = self.runner.get_game_specification()
        self.assertEqual(len(specs), 1)
        self.assertEqual(specs[0]["uri"], "http://example.org/prisoners-dilemma")
        self.assertEqual(specs[0]["label"], "Prisoner's Dilemma")

    def test_get_players(self):
        players = self.runner.get_players("http://example.org/prisoners-dilemma")
        self.assertEqual(len(players), 2)
        player_uris = {p["uri"] for p in players}
        self.assertIn("http://example.org/alice", player_uris)
        self.assertIn("http://example.org/bob", player_uris)

    def test_get_actions(self):
        actions = self.runner.get_actions("http://example.org/prisoners-dilemma", "http://example.org/alice")
        self.assertEqual(len(actions), 2)
        action_labels = {a["label"] for a in actions}
        self.assertIn("Cooperate", action_labels)
        self.assertIn("Defect", action_labels)

    def test_query_payoff(self):
        profile = {
            "http://example.org/alice": "http://example.org/cooperate",
            "http://example.org/bob": "http://example.org/cooperate"
        }
        payoffs = self.runner.query_payoff("http://example.org/prisoners-dilemma", profile)
        # Verify both players receive payoff 3.0
        self.assertEqual(payoffs.get("http://example.org/alice"), 3.0)
        self.assertEqual(payoffs.get("http://example.org/bob"), 3.0)

    def test_llm_player_bench(self):
        from uogto.runner.llm_player import LLMPlayerBench
        bench = LLMPlayerBench(self.ttl_path)
        res = bench.run_session("http://example.org/prisoners-dilemma")
        self.assertIn("choices", res)
        self.assertIn("payoffs", res)
        self.assertEqual(res["payoffs"].get("http://example.org/alice"), 3.0)

if __name__ == "__main__":
    unittest.main()
