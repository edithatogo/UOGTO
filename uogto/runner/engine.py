from __future__ import annotations

import argparse

import rdflib
from rdflib.namespace import RDF, RDFS

UOGTO = rdflib.Namespace("https://w3id.org/uogto/core#")


class RDFGameRunner:
    def __init__(self, ttl_path):
        self.graph = rdflib.Graph()
        self.graph.parse(ttl_path, format=self._format_for_path(ttl_path))

    @staticmethod
    def _format_for_path(path):
        suffix = str(path).lower().rsplit(".", 1)[-1]
        if suffix in {"json", "jsonld"}:
            return "json-ld"
        return "turtle"
        
    def get_game_specification(self):
        # Query for game spec nodes
        q = """
        SELECT ?spec ?label WHERE {
            ?spec a/rdfs:subClassOf* uogto:GameSpecification .
            OPTIONAL { ?spec rdfs:label ?label }
        }
        """
        res = self.graph.query(q, initNs={"uogto": UOGTO, "rdfs": RDFS})
        specs = []
        for row in res:
            specs.append({
                "uri": str(row[0]),
                "label": str(row[1]) if row[1] else None
            })
        return specs
        
    def get_players(self, spec_uri):
        q = """
        SELECT ?player ?label WHERE {
            ?spec_uri uogto:hasPlayer ?player .
            OPTIONAL { ?player rdfs:label ?label }
        }
        """
        res = self.graph.query(q, initNs={"uogto": UOGTO, "rdfs": RDFS}, initBindings={"spec_uri": rdflib.URIRef(spec_uri)})
        players = []
        for row in res:
            players.append({
                "uri": str(row[0]),
                "label": str(row[1]) if row[1] else None
            })
        return players
        
    def get_actions(self, spec_uri, player_uri):
        q = """
        SELECT ?action ?label WHERE {
            ?spec_uri uogto:hasActionSpace ?space .
            ?space uogto:belongsToPlayer ?player_uri .
            ?space uogto:hasAction ?action .
            OPTIONAL { ?action rdfs:label ?label }
        }
        """
        res = self.graph.query(
            q, 
            initNs={"uogto": UOGTO, "rdfs": RDFS}, 
            initBindings={"spec_uri": rdflib.URIRef(spec_uri), "player_uri": rdflib.URIRef(player_uri)}
        )
        actions = []
        for row in res:
            actions.append({
                "uri": str(row[0]),
                "label": str(row[1]) if row[1] else None
            })
        return actions

    def query_payoff(self, spec_uri, action_profile_dict):
        """Return payoffs for an exact player->action profile in a single game.

        The current ontology pattern is StrategyProfile -> PayoffProfile ->
        PlayerPayoffLink. Older examples used PayoffMapping directly. The runner
        supports both, but always scopes candidates through the requested game.
        """

        expected = {str(player): str(action) for player, action in action_profile_dict.items()}
        payoffs = self._query_reified_payoffs(spec_uri, expected)
        if payoffs:
            return payoffs
        return self._query_legacy_payoff_mappings(spec_uri, expected)

    def _query_reified_payoffs(self, spec_uri, expected):
        rows = self.graph.query(
            """
            SELECT ?profile ?payoffProfile ?link ?player ?value WHERE {
                ?spec_uri uogto:hasStrategyProfile ?profile .
                ?profile uogto:hasPayoff ?payoffProfile .
                ?payoffProfile uogto:hasPayoffForPlayer ?link .
                ?link uogto:payoffPlayer ?player ;
                      uogto:payoffValue ?value .
            }
            """,
            initNs={"uogto": UOGTO},
            initBindings={"spec_uri": rdflib.URIRef(spec_uri)},
        )
        by_profile = {}
        for profile, _payoff_profile, _link, player, value in rows:
            by_profile.setdefault(profile, {})[str(player)] = float(value)

        for profile, payoffs in by_profile.items():
            if self._profile_matches(profile, expected):
                return payoffs
        return {}

    def _query_legacy_payoff_mappings(self, spec_uri, expected):
        rows = self.graph.query(
            """
            SELECT ?mapping ?profile ?player ?value WHERE {
                ?spec_uri uogto:hasPayoffMapping ?mapping .
                ?mapping uogto:hasActionProfile ?profile ;
                         uogto:belongsToPlayer ?player ;
                         uogto:payoffValue ?value .
            }
            """,
            initNs={"uogto": UOGTO},
            initBindings={"spec_uri": rdflib.URIRef(spec_uri)},
        )
        by_mapping = {}
        for _mapping, profile, player, value in rows:
            bucket = by_mapping.setdefault(profile, {})
            bucket[str(player)] = float(value)
        for profile, payoffs in by_mapping.items():
            if self._profile_matches(profile, expected):
                return payoffs
        return {}

    def _profile_matches(self, profile, expected):
        rows = self.graph.query(
            """
            SELECT ?player ?action WHERE {
                ?profile uogto:hasAction ?action .
                OPTIONAL { ?action uogto:belongsToPlayer ?player . }
            }
            """,
            initNs={"uogto": UOGTO},
            initBindings={"profile": profile},
        )
        actual_pairs = set()
        unscoped_actions = set()
        has_scoped_actions = False
        for player, action in rows:
            if player is None:
                unscoped_actions.add(str(action))
            else:
                actual_pairs.add((str(player), str(action)))
                has_scoped_actions = True
        if has_scoped_actions:
            expected_pairs = {(player, action) for player, action in expected.items()}
            return actual_pairs == expected_pairs
        return unscoped_actions == set(expected.values())


def main() -> None:
    parser = argparse.ArgumentParser(description="Inspect UOGTO game specifications in a Turtle graph.")
    parser.add_argument("ttl_path", help="Path to a Turtle graph containing UOGTO game data.")
    args = parser.parse_args()
    runner = RDFGameRunner(args.ttl_path)
    for spec in runner.get_game_specification():
        print(f"{spec['uri']}\t{spec.get('label') or ''}")


if __name__ == "__main__":
    main()
