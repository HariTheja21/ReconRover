class DemoReport:
    def generate(self, success: bool) -> dict:
        return {"mission_status": "SUCCESS" if success else "FAILED", "score": 100 if success else 0}
