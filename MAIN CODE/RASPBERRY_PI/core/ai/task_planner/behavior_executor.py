class BehaviorExecutor:
    def __init__(self):
        self.active_tree = None
        
    def execute_tree(self, tree):
        self.active_tree = tree
        return self.active_tree.tick()
