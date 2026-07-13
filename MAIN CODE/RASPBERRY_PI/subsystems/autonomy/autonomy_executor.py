"""
autonomy_executor.py
Recon Rover V1 - Autonomous Intelligence

Translates the scheduled objective into semantic EventBus requests.
"""

from event_bus import EventBus, ObjectiveSelected
from .autonomy_blackboard import AutonomyBlackboard

class AutonomyExecutor:
    def __init__(self, event_bus: EventBus):
        self.event_bus = event_bus

    def execute(self, blackboard: AutonomyBlackboard):
        """Publishes the semantic objective intent."""
        
        if blackboard.selected_objective:
            # We never emit MovementRequest. We emit ObjectiveSelected.
            # The Mission Manager or lower engines handle the actual execution.
            self.event_bus.publish(ObjectiveSelected(
                objective=blackboard.selected_objective,
                constraints=blackboard.coordinator_constraints
            ))
