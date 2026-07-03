from pathlib import Path

import rdflib
from rdflib.namespace import RDF, RDFS

UOGTO = rdflib.Namespace("https://w3id.org/uogto/core#")


class RDFGameRunner:
    def __init__(self, ttl_path):
        self.graph = rdflib.Graph()
        self.graph.parse(ttl_path, format="turtle")

    def get_game_specification(self):
        q = """
        SELECT ?spec ?label WHERE {
            ?spec a ?type .
            OPTIONAL { ?type rdfs:subClassOf* uogto:GameSpecification }
            FILTER (?type = uogto:GameSpecification || EXISTS { ?type rdfs:subClassOf* uogto:GameSpecification })
            OPTIONAL { ?spec rdfs:label ?label }
        }
        """
        res = self.graph.query(q, initNs={"uogto": UOGTO, "rdfs": RDFS})
        seen = set()
        specs = []
        for spec, label in res:
            if spec in seen:
                continue
            seen.add(spec)
            specs.append({"uri": str(spec), "label": str(label) if label else None})
        return sorted(specs, key=lambda item: item["uri"])

    def get_players(self, spec_uri):
        q = """
        SELECT ?player ?label WHERE {
            ?spec_uri uogto:hasPlayer ?player .
            OPTIONAL { ?player rdfs:label ?label }
        }
        """
        res = self.graph.query(
            q,
            initNs={"uogto": UOGTO, "rdfs": RDFS},
            initBindings={"spec_uri": rdflib.URIRef(spec_uri)},
        )
        return [
            {"uri": str(player), "label": str(label) if label else None}
            for player, label in res
        ]

    def get_actions(self, spec_uri, player_uri):
        q = """
        SELECT ?action ?label WHERE {
            ?spec_uri uogto:hasActionSpace ?space .
            ?space uogto:belongsToPlayer ?player_uri .
            ?space uogto:hasAction ?action .
            OPTIONAL { ?action rdfs:label ?label }
        }
        """
        bindings = {"spec_uri": rdflib.URIRef(spec_uri), "player_uri": rdflib.URIRef(player_uri)}
        res = self.graph.query(q, initNs={"uogto": UOGTO, "rdfs": RDFS}, initBindings=bindings)
        return [
            {"uri": str(action), "label": str(label) if label else None}
            for action, label in res
        ]

    def query_payoff(self, spec_uri, action_profile_dict):
        payoffs = self._query_current_payoff_pattern(spec_uri, action_profile_dict)
        if payoffs:
            return payoffs
        return self._query_legacy_payoff_mapping(spec_uri, action_profile_dict)

    def _profile_actions(self, profile):
        actions = set()
        for predicate in [UOGTO.hasAction, UOGTO.selectsAction, UOGTO.comprisesStrategy, UOGTO.hasStrategy]:
            actions.update(str(action) for action in self.graph.objects(profile, predicate))
        return actions

    def _profile_matches(self, profile, action_profile_dict):
        expected_actions = {str(action) for action in action_profile_dict.values()}
        profile_actions = self._profile_actions(profile)
        return profile_actions == expected_actions

    def _query_current_payoff_pattern(self, spec_uri, action_profile_dict):
        spec = rdflib.URIRef(spec_uri)
        results = {}
        profile_predicates = [UOGTO.hasStrategyProfile, UOGTO.hasActionProfile]
        for profile_predicate in profile_predicates:
            for profile in self.graph.objects(spec, profile_predicate):
                if not self._profile_matches(profile, action_profile_dict):
                    continue
                for payoff_profile in self.graph.objects(profile, UOGTO.hasPayoff):
                    for link in self.graph.objects(payoff_profile, UOGTO.hasPayoffForPlayer):
                        players = list(self.graph.objects(link, UOGTO.payoffPlayer))
                        values = list(self.graph.objects(link, UOGTO.payoffValue)) or list(
                            self.graph.objects(link, UOGTO.utilityValue)
                        )
                        if players and values:
                            results[str(players[0])] = float(values[0])
        return results

    def _query_legacy_payoff_mapping(self, spec_uri, action_profile_dict):
        q_all_mappings = """
        SELECT ?mapping ?profile ?player ?val WHERE {
            ?spec_uri uogto:hasPayoffMapping ?mapping .
            ?mapping uogto:hasActionProfile ?profile .
            ?mapping uogto:payoffValue ?val .
            ?mapping uogto:belongsToPlayer ?player .
        }
        """
        res = self.graph.query(
            q_all_mappings,
            initNs={"uogto": UOGTO},
            initBindings={"spec_uri": rdflib.URIRef(spec_uri)},
        )
        payoffs = {}
        for _, profile_node, player, value in res:
            if self._profile_matches(profile_node, action_profile_dict):
                payoffs[str(player)] = float(value)
        return payoffs
