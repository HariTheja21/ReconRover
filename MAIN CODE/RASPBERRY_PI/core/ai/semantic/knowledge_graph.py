class KnowledgeGraph:
    def __init__(self):
        self.nodes = {}
        self.edges = []
        
    def add_node(self, n_id: str, data: dict):
        self.nodes[n_id] = data
        
    def add_edge(self, source: str, target: str, relation: str):
        self.edges.append({"source": source, "target": target, "relation": relation})
        
    def get_stats(self):
        return len(self.nodes), len(self.edges)
