import json

class MetricsExporter:
    def __init__(self, db):
        self.db = db
        
    def export_json(self) -> str:
        return json.dumps(self.db.query())
