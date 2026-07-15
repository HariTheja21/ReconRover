from typing import List, Dict

class LoopValidator:
    def __init__(self):
        pass

    def validate_loop(self, loop_name: str, test_results: List[bool]) -> bool:
        # Validates that all steps inside a specific control loop passed
        return all(test_results)
