import rdflib
from rdflib.namespace import RDF, RDFS

UOGTO = rdflib.Namespace("https://w3id.org/uogto/core#")

class RDFGameRunner:
    def __init__(self, ttl_path):
        self.graph = rdflib.Graph()
        self.graph.parse(ttl_path, format="turtle")
        
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
        # action_profile_dict maps player_uri -> action_uri
        # Query for payoff value mapping to this specific action profile
        # We search for a payoff mapped to the spec, containing payoff values for players
        q = """
        SELECT ?player ?value WHERE {
            ?spec_uri uogto:hasPayoffMapping ?mapping .
            ?mapping uogto:hasActionProfile ?profile .
            ?profile uogto:hasAction ?action .
            ?action uogto:belongsToPlayer ?player .
            ?mapping uogto:hasPayoffValue ?payoff .
            ?payoff uogto:belongsToPlayer ?player .
            ?payoff uogto:payoffValue ?value .
        }
        """
        # Let's run a custom filter or query based on the active graph structure
        # Since different games use custom profiles, we can fetch all mappings and filter in Python
        q_all_mappings = """
        SELECT ?mapping ?profile ?player ?val WHERE {
            ?mapping uogto:hasActionProfile ?profile .
            ?mapping uogto:payoffValue ?val .
            ?mapping uogto:belongsToPlayer ?player .
        }
        """
        # Let's query all payoffs matching the action list
        res = self.graph.query(q_all_mappings, initNs={"uogto": UOGTO})
        payoffs = {}
        
        # Action profiles in ontology are often collections or nodes with actions linked
        # Let's find matches where the action profile contains all the matching actions
        for row in res:
            mapping_node, profile_node, player, value = row
            # Query actions linked to this profile
            q_actions = """
            SELECT ?action WHERE {
                ?profile_node uogto:hasAction ?action .
            }
            """
            actions_res = self.graph.query(q_actions, initNs={"uogto": UOGTO}, initBindings={"profile_node": profile_node})
            profile_actions = {str(r[0]) for r in actions_res}
            
            # Match if profile actions are exactly the actions chosen
            chosen_actions = {str(a) for a in action_profile_dict.values()}
            if profile_actions == chosen_actions:
                payoffs[str(player)] = float(value)
                
        return payoffs
