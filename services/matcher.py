import json
from typing import List, Dict
from services.embedding import find_most_similar

# Load controls from your known_controls.json
def load_known_controls(path: str = "data/known_control.json") -> List[Dict]:
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data

def match_control(input_description: str, top_n: int = 3) -> List[Dict]:
    known_controls = load_known_controls()

    # Just compare with descriptions
    candidate_texts = [c["description"] for c in known_controls]
    top_matches = find_most_similar(input_description, candidate_texts, top_n=top_n)

    # Map back to full control info
    results = []
    for match_text, score in top_matches:
        for c in known_controls:
            if c["description"] == match_text:
                c["match_score"] = round(score, 4)
                results.append(c)
                break
    return results
