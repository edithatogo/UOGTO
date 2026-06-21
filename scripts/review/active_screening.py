import json
import os
import sys

INPUT_FILE = "data/processed/deduplicated_results.json"
OUTPUT_FILE = "data/processed/screened_results.json"

# Key target phrases representing structural game theory concepts in UOGTO
KEYWORDS = {
    "normal_form": ["normal form", "matrix game", "payoff matrix", "normal-form"],
    "extensive_form": ["extensive form", "game tree", "subgame", "extensive-form"],
    "cooperative": ["cooperative game", "coalitional game", "characteristic function", "core of the game"],
    "stochastic_marl": ["markov game", "stochastic game", "marl", "reinforcement learning", "bellman"],
    "mechanism_design": ["mechanism design", "auction", "revelation principle", "social choice"]
}

def score_abstract(title, abstract):
    text = f"{title or ''} {abstract or ''}".lower()
    score = 0
    matches = []
    
    for category, terms in KEYWORDS.items():
        found = False
        for term in terms:
            if term in text:
                score += 1
                found = True
        if found:
            matches.append(category)
            
    return score, matches

def main():
    print("Screening records using structural keyword classification...")
    if not os.path.exists(INPUT_FILE):
        print(f"Deduplicated file not found at {INPUT_FILE}.", file=sys.stderr)
        sys.exit(1)
        
    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        records = json.load(f)
        
    screened = []
    for r in records:
        score, matches = score_abstract(r.get("title"), r.get("abstract"))
        # Standard filter: must match at least one structural category
        if score > 0:
            r["relevance_score"] = score
            r["categories"] = matches
            screened.append(r)
            
    # Sort by relevance score desc
    screened.sort(key=lambda x: x["relevance_score"], reverse=True)
    
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(screened, f, indent=2)
        
    print(f"Screened {len(screened)} relevant papers (saved to {OUTPUT_FILE})")

if __name__ == "__main__":
    main()
