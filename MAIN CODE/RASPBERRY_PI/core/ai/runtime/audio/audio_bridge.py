import json
import logging
from typing import Any

logger = logging.getLogger(__name__)

class AudioBridge:
    def __init__(self, event_bus: Any):
        self.event_bus = event_bus
        
    def publish_event(self, event_type: str, event_dict: dict):
        if not self.event_bus:
            return
            
        try:
            topic = "audio.runtime"
            if event_type in ["WakeWordDetected", "SpeechRecognized", "SpeechCommandParsed"]:
                topic = "audio.input"
            elif event_type == "TextToSpeechCompleted":
                topic = "audio.output"
            elif event_type in ["AudioStatisticsUpdated", "AudioHealthUpdated"]:
                topic = "audio.telemetry"
                
            payload = {"_audio_event_type": event_type, **event_dict}
            self.event_bus.publish(topic, json.dumps(payload))
        except Exception as e:
            logger.error(f"Failed to publish Audio event {event_type}: {e}")
