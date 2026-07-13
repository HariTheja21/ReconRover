"""
behavior_tree.py
Recon Rover V1 - Behavior Engine

Deterministic Behavior Tree implementation for autonomous execution.
"""

from abc import ABC, abstractmethod
from enum import Enum, auto
from typing import List, Callable
from event_bus import EventBus
from logger import Logger

class NodeStatus(Enum):
    SUCCESS = auto()
    FAILURE = auto()
    RUNNING = auto()

class BehaviorNode(ABC):
    def __init__(self, name: str):
        self.name = name

    @abstractmethod
    def tick(self) -> NodeStatus:
        pass

class Sequence(BehaviorNode):
    """Executes children in order. Fails if any child fails."""
    def __init__(self, name: str, children: List[BehaviorNode]):
        super().__init__(name)
        self.children = children
        self.current_idx = 0

    def tick(self) -> NodeStatus:
        while self.current_idx < len(self.children):
            child = self.children[self.current_idx]
            status = child.tick()
            
            if status == NodeStatus.RUNNING:
                return NodeStatus.RUNNING
            elif status == NodeStatus.FAILURE:
                self.current_idx = 0
                return NodeStatus.FAILURE
            elif status == NodeStatus.SUCCESS:
                self.current_idx += 1
                
        self.current_idx = 0
        return NodeStatus.SUCCESS

class Selector(BehaviorNode):
    """Executes children in order. Succeeds if any child succeeds."""
    def __init__(self, name: str, children: List[BehaviorNode]):
        super().__init__(name)
        self.children = children
        self.current_idx = 0

    def tick(self) -> NodeStatus:
        while self.current_idx < len(self.children):
            child = self.children[self.current_idx]
            status = child.tick()
            
            if status == NodeStatus.RUNNING:
                return NodeStatus.RUNNING
            elif status == NodeStatus.SUCCESS:
                self.current_idx = 0
                return NodeStatus.SUCCESS
            elif status == NodeStatus.FAILURE:
                self.current_idx += 1
                
        self.current_idx = 0
        return NodeStatus.FAILURE

class Condition(BehaviorNode):
    """Evaluates a boolean function."""
    def __init__(self, name: str, condition_fn: Callable[[], bool]):
        super().__init__(name)
        self.condition_fn = condition_fn

    def tick(self) -> NodeStatus:
        return NodeStatus.SUCCESS if self.condition_fn() else NodeStatus.FAILURE

class Action(BehaviorNode):
    """Executes an action via a provided function."""
    def __init__(self, name: str, action_fn: Callable[[], NodeStatus]):
        super().__init__(name)
        self.action_fn = action_fn

    def tick(self) -> NodeStatus:
        return self.action_fn()
