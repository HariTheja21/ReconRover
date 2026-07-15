import json
import logging
from typing import Any

logger = logging.getLogger(__name__)

class SpeechBridge:
    def __init__(self, event_bus: Any):
        self.event_bus = event_bus
        
    def publish_event(self, event_type: str, event_dict: dict):
        if not self.event_bus:
            return
            
        try:
            # Route to autonomy if it's a parsed command or transcript
            if event_type in ["SpeechCommandParsed", "TranscriptGenerated"]:
                self.event_bus.publish("speech.commands", json.dumps(event_dict))
            else:
                self.event_bus.publish("telemetry.speech", json.dumps(event_dict))
        except Exception as e:
            logger.error(f"Failed to publish Speech event {event_type}: {e}")
