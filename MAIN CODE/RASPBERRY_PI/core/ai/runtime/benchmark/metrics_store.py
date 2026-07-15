class MetricsStore:
    def __init__(self, db):
        self.db = db
        
    def store_metric(self, name: str, value: dict):
        self.db.save({"name": name, "value": value})
