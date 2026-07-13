"""
vl_reasoning_bridge.py
Recon Rover V1 - Vision-Language Cognitive Integration

Publishes VL observations to the EventBus for the LLM context.
"""

from event_bus import EventBus, VisionLanguageContextUpdated

class VLReasoningBridge:
    def __init__(self, event_bus: EventBus):
        self.event_bus = event_bus

    def publish_observation(self, observation: str):
        """Sends the compressed semantic observation to the LLMEngine."""
        self.event_bus.publish(VisionLanguageContextUpdated(
            semantics=observation
        ))
