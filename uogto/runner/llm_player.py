"""Deterministic first-action baseline; legacy LLM names remain importable."""

from uogto.runner.engine import RDFGameRunner


class FirstActionPlayer:
    """Select the first supplied action without contacting a model or solver."""

    execution_origin = "deterministic_first_action_baseline"

    def __init__(self, name, model_name="gpt-4o"):
        self.name = name
        # Retained solely for compatibility with the former LLMPlayer API.
        self.model_name = model_name

    def make_choice(self, game_description, available_actions):
        return available_actions[0] if available_actions else None


class FirstActionPlayerBench:
    """Select first actions in graph iteration order and look up stored payoffs."""

    execution_origin = FirstActionPlayer.execution_origin

    def __init__(self, ttl_path):
        self.runner = RDFGameRunner(ttl_path)

    def run_session(self, spec_uri):
        choices = {}
        for player in self.runner.get_players(spec_uri):
            player_uri = player["uri"]
            actions = self.runner.get_actions(spec_uri, player_uri)
            baseline = FirstActionPlayer(name=player["label"] or player_uri)
            choices[player_uri] = baseline.make_choice(
                "UOGTO Game Specification", [action["uri"] for action in actions]
            )
        return {
            "choices": choices,
            "payoffs": self.runner.query_payoff(spec_uri, choices),
            "execution_origin": self.execution_origin,
            "payoff_origin": "stored_graph_lookup",
            "model_request_performed": False,
            "native_solver_performed": False,
        }


# Historical import names and constructor signatures remain supported.
LLMPlayer = FirstActionPlayer
LLMPlayerBench = FirstActionPlayerBench


def main():
    import argparse
    import json

    parser = argparse.ArgumentParser(
        description="Run the UOGTO deterministic first-action reference baseline."
    )
    parser.add_argument("ttl_path", help="Turtle file containing a UOGTO game graph.")
    parser.add_argument("spec_uri", help="Game specification URI to run.")
    args = parser.parse_args()
    result = FirstActionPlayerBench(args.ttl_path).run_session(args.spec_uri)
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
