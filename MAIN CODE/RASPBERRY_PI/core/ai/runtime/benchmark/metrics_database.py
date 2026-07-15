class MetricsDatabase:
    def __init__(self):
        self.db = []
        
    def save(self, metric: dict):
        self.db.append(metric)
        
    def query(self, **kwargs) -> list:
        return self.db
