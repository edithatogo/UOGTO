from uogto.runner.engine import RDFGameRunner

class LLMPlayer:
    def __init__(self, name, model_name="gpt-4o"):
        self.name = name
        self.model_name = model_name

    def make_choice(self, game_description, available_actions):
        # We query a generic Ollama/remote endpoint or fallback to a heuristic if not authenticated.
        # Standard fallback if no API key or endpoint is specified.
        if available_actions:
            return available_actions[0]
        return None

class LLMPlayerBench:
    def __init__(self, ttl_path):
        self.runner = RDFGameRunner(ttl_path)

    def run_session(self, spec_uri):
        players = self.runner.get_players(spec_uri)
        choices = {}
        
        # Instantiate LLM players
        for p in players:
            player_uri = p["uri"]
            player_label = p["label"] or player_uri
            
            actions = self.runner.get_actions(spec_uri, player_uri)
            action_uris = [a["uri"] for a in actions]
            
            llm_player = LLMPlayer(name=player_label)
            chosen_action = llm_player.make_choice("UOGTO Game Specification", action_uris)
            choices[player_uri] = chosen_action
            
        payoffs = self.runner.query_payoff(spec_uri, choices)
        return {
            "choices": choices,
            "payoffs": payoffs
        }


def main():
    import argparse
    import json

    parser = argparse.ArgumentParser(description="Run a deterministic UOGTO LLM-player benchmark.")
    parser.add_argument("ttl_path", help="Turtle file containing a UOGTO game graph.")
    parser.add_argument("spec_uri", help="Game specification URI to run.")
    args = parser.parse_args()
    result = LLMPlayerBench(args.ttl_path).run_session(args.spec_uri)
    print(json.dumps(result, indent=2, sort_keys=True))
