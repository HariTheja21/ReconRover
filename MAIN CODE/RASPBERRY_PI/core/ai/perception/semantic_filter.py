from typing import List, Dict, Any

class SemanticFilter:
    def __init__(self):
        pass
        
    def filter_noise(self, entities: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        # Remove ghost entities or hallucinated objects using semantic logic
        # e.g. A "person" with volume < 0.01m^3 is probably a false positive
        valid = []
        for e in entities:
            # Stub logic
            if e.get("confidence", 0) > 0.3:
                valid.append(e)
        return valid
