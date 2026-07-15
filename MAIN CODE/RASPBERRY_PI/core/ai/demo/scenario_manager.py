class ScenarioManager:
    def __init__(self, scenario_generator):
        self.scenario_generator = scenario_generator
        
    def load_scenario(self) -> dict:
        return self.scenario_generator.get_recon_scenario()
