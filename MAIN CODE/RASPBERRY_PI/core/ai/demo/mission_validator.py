class MissionValidator:
    def validate_scenario(self, scenario: dict) -> bool:
        return "id" in scenario and "steps" in scenario
