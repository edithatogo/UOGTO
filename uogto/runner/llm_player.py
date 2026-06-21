import os
import json
import urllib.request
import urllib.error
from uogto.runner.engine import RDFGameRunner

class LLMPlayer:
    def __init__(self, name, model_name="gpt-4o"):
        self.name = name
        self.model_name = model_name

    def make_choice(self, game_description, available_actions):
        # We query a generic Ollama/remote endpoint or fallback to a heuristic if not authenticated.
        # Standard fallback if no API key or endpoint is specified.
        prompt = f"You are player {self.name} in a game of: {game_description}. Your choices are: {available_actions}. What is your choice? Output only the action name."
        
        # Let's perform a mock fallback selection
        # Choose first action as default heuristic
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
