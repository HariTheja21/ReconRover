"""
al_context.py
Recon Rover V1 - Audio-Language Cognitive Integration

Maintains the working state for the Audio-Language engine.
"""

from dataclasses import dataclass, field
from typing import Dict, Any, List
import time

@dataclass
class AudioEvent:
    event_type: str  # "SPEECH" or "SOUND"
    content: str
    confidence: float
    timestamp: float = field(default_factory=time.time)
    direction: float = -1.0
    speaker: str = "Unknown"

@dataclass
class ALContext:
    recent_events: List[AudioEvent] = field(default_factory=list)
    world_state: Dict[str, Any] = field(default_factory=dict)
    hazard_state: str = "NONE"
    
    def add_event(self, event: AudioEvent, max_history: int = 10):
        self.recent_events.append(event)
        # Keep only the most recent N events to bound memory
        if len(self.recent_events) > max_history:
            self.recent_events.pop(0)

    def purge_old_events(self, max_age_seconds: float = 60.0):
        current_time = time.time()
        self.recent_events = [
            e for e in self.recent_events 
            if current_time - e.timestamp <= max_age_seconds
        ]
