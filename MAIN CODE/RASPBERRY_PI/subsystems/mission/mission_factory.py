"""
mission_factory.py
Recon Rover V1 - Behavior Engine

Constructs specific behavior trees based on the active mission type.
"""

from logger import Logger
from .behavior_tree import BehaviorNode, Sequence, Selector, Condition, Action, NodeStatus
from event_bus import EventBus
from .state_machine import BehaviorStateMachine, RobotBehaviorState

class MissionFactory:
    def __init__(self, event_bus: EventBus, state_machine: BehaviorStateMachine):
        self.event_bus = event_bus
        self.state_machine = state_machine
        self.log = Logger.get("MissionFactory")

    def build_tree(self, mission_type: str) -> BehaviorNode:
        """Constructs the root behavior tree for the requested mission."""
        self.log.info(f"Building behavior tree for mission: {mission_type}")
        
        if mission_type == "Idle":
            return self._build_idle_tree()
        elif mission_type == "Return Home":
            return self._build_return_home_tree()
        elif mission_type == "Explore" or mission_type == "Exploration":
            return self._build_explore_tree()
        else:
            # Fallback to idle
            self.log.warning(f"No specific tree for {mission_type}. Defaulting to Idle.")
            return self._build_idle_tree()

    def _build_idle_tree(self) -> BehaviorNode:
        def set_idle():
            self.state_machine.set_state(RobotBehaviorState.IDLE)
            return NodeStatus.SUCCESS
            
        return Action("IdleAction", set_idle)

    def _build_return_home_tree(self) -> BehaviorNode:
        def check_battery():
            return True # Mock condition
            
        def navigate_home():
            self.state_machine.set_state(RobotBehaviorState.RETURN_HOME)
            return NodeStatus.RUNNING
            
        return Sequence("ReturnHomeSequence", [
            Condition("BatteryOk", check_battery),
            Action("NavigateHome", navigate_home)
        ])

    def _build_explore_tree(self) -> BehaviorNode:
        def explore():
            self.state_machine.set_state(RobotBehaviorState.EXPLORING)
            return NodeStatus.RUNNING
            
        return Action("ExploreAction", explore)
