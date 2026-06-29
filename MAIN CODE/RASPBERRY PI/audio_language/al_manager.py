"""
al_manager.py
Recon Rover V1 - Audio-Language Cognitive Integration

Coordinates the internal AL pipeline.
"""

from typing import Dict, Any
from event_bus import EventBus
from .al_context import ALContext
from .al_transcript_builder import ALTranscriptBuilder
from .al_sound_builder import ALSoundBuilder
from .al_observation_generator import ALObservationGenerator
from .al_reasoning_bridge import ALReasoningBridge
from .al_memory_bridge import ALMemoryBridge
from .al_health import ALHealth
from .al_statistics import ALStatistics

class ALManager:
    def __init__(self, event_bus: EventBus):
        self.context = ALContext()
        self.transcript_builder = ALTranscriptBuilder()
        self.sound_builder = ALSoundBuilder()
        
        self.obs_gen = ALObservationGenerator()
        self.reasoning = ALReasoningBridge(event_bus)
        self.memory = ALMemoryBridge(event_bus)
        
        self.health = ALHealth()
        self.stats = ALStatistics()

    def process_speech(self, semantics: Dict[str, Any]):
        try:
            event = self.transcript_builder.build_event(semantics)
            self.context.add_event(event)
            self.stats.record_speech()
            self._update_downstream(event)
            self.health.record_success()
        except Exception:
            self.health.record_error()

    def process_sound(self, semantics: Dict[str, Any]):
        try:
            event = self.sound_builder.build_event(semantics)
            self.context.add_event(event)
            self.stats.record_sound()
            self._update_downstream(event)
            self.health.record_success()
        except Exception:
            self.health.record_error()
            
    def _update_downstream(self, new_event):
        # Memory checks for threats immediately
        self.memory.evaluate_and_publish(new_event)
        self.stats.record_memory()
        
        # Purge stale events before generating observation
        self.context.purge_old_events()
        
        # Update reasoning bridge
        observation = self.obs_gen.generate_observation(self.context)
        self.reasoning.publish_observation(observation)
        self.stats.record_observation()
