"""
audio_scene_analyzer.py
Recon Rover V1 - Audio Pipeline

Translates raw audio classification and tracking data into semantic events.
"""

from event_bus import EventBus, SoundDetected, SpeechDetected, DirectionEstimated, AudioSceneUpdated
from logger import Logger
from typing import List, Dict, Optional

class AudioSceneAnalyzer:
    def __init__(self, event_bus: EventBus):
        self.event_bus = event_bus
        self.log = Logger.get("AudioSceneAnalyzer")

    def analyze(self, vad_active: bool, sounds: List[str], speech_text: Optional[str], direction: Optional[Dict[str, float]]):
        """
        Evaluates the aggregated audio data and publishes semantic events.
        """
        scene_data = {
            "vad_active": vad_active,
            "sounds": sounds,
            "speech": speech_text,
            "direction": direction
        }

        # 1. Sound Events
        for sound in sounds:
            if sound != "Unknown":
                self.event_bus.publish(SoundDetected(sound_type=sound))

        # 2. Speech Events
        if speech_text:
            self.event_bus.publish(SpeechDetected(text=speech_text))

        # 3. Direction Events
        if direction:
            self.event_bus.publish(DirectionEstimated(azimuth=direction.get("azimuth", 0.0), elevation=direction.get("elevation", 0.0)))

        # 4. Aggregated Scene Update
        self.event_bus.publish(AudioSceneUpdated(semantics=scene_data))
