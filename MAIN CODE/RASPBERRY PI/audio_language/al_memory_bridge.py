"""
al_memory_bridge.py
Recon Rover V1 - Audio-Language Cognitive Integration

Identifies major audio shifts or threats to trigger episodic memories.
"""

from event_bus import EventBus, AudioSummaryUpdated
from .al_context import AudioEvent

class ALMemoryBridge:
    def __init__(self, event_bus: EventBus):
        self.event_bus = event_bus
        self.threat_keywords = ["help", "stop", "intruder", "fire", "danger"]
        self.threat_sounds = ["glass_breaking", "gunshot", "siren", "explosion", "screaming"]

    def evaluate_and_publish(self, event: AudioEvent):
        """
        Determines if the audio event is important enough to log in episodic memory.
        """
        is_important = False
        summary = ""
        
        if event.event_type == "SPEECH":
            text_lower = event.content.lower()
            if any(kw in text_lower for kw in self.threat_keywords):
                is_important = True
                summary = f"Heard threatening speech from {event.speaker}: '{event.content}'"
                
        elif event.event_type == "SOUND":
            if event.content in self.threat_sounds:
                is_important = True
                summary = f"Heard critical sound: {event.content}"
                
        if is_important:
            self.event_bus.publish(AudioSummaryUpdated(
                summary=summary
            ))
