"""
al_reasoning_bridge.py
Recon Rover V1 - Audio-Language Cognitive Integration

Publishes AL observations to the EventBus for the LLM context.
"""

from event_bus import EventBus, AudioLanguageContextUpdated

class ALReasoningBridge:
    def __init__(self, event_bus: EventBus):
        self.event_bus = event_bus

    def publish_observation(self, observation: str):
        """Sends the compressed semantic observation to the LLMEngine."""
        self.event_bus.publish(AudioLanguageContextUpdated(
            semantics=observation
        ))
