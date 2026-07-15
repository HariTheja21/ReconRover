class DemoScenario:
    def __init__(self):
        pass
        
    def get_recon_scenario(self) -> dict:
        return {
            "id": "scenario_recon_01",
            "steps": [
                "Hardware Verification",
                "Vision Startup",
                "Speech Startup",
                "LLM Startup",
                "RAG Initialization",
                "Tool Runtime Initialization",
                "Multi-Agent Runtime Initialization",
                "Mission Planning",
                "Autonomous Exploration",
                "Object Detection",
                "Semantic Memory Updates",
                "Reasoning",
                "Tool Execution",
                "Navigation",
                "Obstacle Avoidance"
            ]
        }
