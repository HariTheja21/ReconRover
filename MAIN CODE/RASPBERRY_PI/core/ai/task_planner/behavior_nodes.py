class NodeStatus:
    SUCCESS = "SUCCESS"
    FAILURE = "FAILURE"
    RUNNING = "RUNNING"

class BehaviorNode:
    def tick(self) -> str:
        raise NotImplementedError

class ActionNode(BehaviorNode):
    def __init__(self, action_func):
        self.action = action_func
        
    def tick(self) -> str:
        return self.action()

class SequenceNode(BehaviorNode):
    def __init__(self, children):
        self.children = children
        
    def tick(self) -> str:
        for child in self.children:
            status = child.tick()
            if status != NodeStatus.SUCCESS:
                return status
        return NodeStatus.SUCCESS

class SelectorNode(BehaviorNode):
    def __init__(self, children):
        self.children = children
        
    def tick(self) -> str:
        for child in self.children:
            status = child.tick()
            if status != NodeStatus.FAILURE:
                return status
        return NodeStatus.FAILURE
