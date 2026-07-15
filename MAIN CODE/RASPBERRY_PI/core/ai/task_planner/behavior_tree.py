from .behavior_nodes import BehaviorNode, NodeStatus

class BehaviorTree:
    def __init__(self, root: BehaviorNode):
        self.root = root
        
    def tick(self) -> str:
        return self.root.tick()
