"""
al_sound_builder.py
Recon Rover V1 - Audio-Language Cognitive Integration

Converts raw sound classifications into structured cognitive AudioEvents.
"""

from typing import Dict, Any
from .al_context import AudioEvent

class ALSoundBuilder:
    def build_event(self, semantics: Dict[str, Any]) -> AudioEvent:
        """
        Parses the dictionary emitted by Phase 4.4 Sound Classification.
        """
        sound_class = semantics.get("class", "unknown_sound")
        conf = semantics.get("confidence", 0.0)
        direction = semantics.get("direction", -1.0)
        
        return AudioEvent(
            event_type="SOUND",
            content=sound_class,
            confidence=conf,
            direction=direction
        )
