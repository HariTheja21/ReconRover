import json

class ReportGenerator:
    def __init__(self, db):
        self.db = db
        
    def generate_summary(self) -> dict:
        metrics = self.db.query()
        return {"report": "summary", "total_metrics": len(metrics)}
