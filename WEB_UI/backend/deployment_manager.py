import os

class DeploymentManager:
    def __init__(self):
        self.env = os.getenv("ROVER_ENV", "PRODUCTION")
        
    def is_production(self) -> bool:
        return self.env.upper() == "PRODUCTION"
        
    def verify_deployment(self) -> bool:
        # Check required directories
        required_dirs = ["data", "logs", "config"]
        for d in required_dirs:
            if not os.path.exists(d):
                os.makedirs(d, exist_ok=True)
        return True
