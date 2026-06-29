"""
al_transcript_builder.py
Recon Rover V1 - Audio-Language Cognitive Integration

Converts raw speech transcripts into structured cognitive AudioEvents.
"""

from typing import Dict, Any
from .al_context import AudioEvent

class ALTranscriptBuilder:
    def build_event(self, semantics: Dict[str, Any]) -> AudioEvent:
        """
        Parses the dictionary emitted by Phase 4.4 Speech Recognition.
        """
        text = semantics.get("transcript", "")
        conf = semantics.get("confidence", 0.0)
        speaker = semantics.get("speaker", "Unknown")
        direction = semantics.get("direction", -1.0)
        
        return AudioEvent(
            event_type="SPEECH",
            content=text,
            confidence=conf,
            direction=direction,
            speaker=speaker
        )
