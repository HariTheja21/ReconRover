"""
multimodal_manager.py
Recon Rover V1 - Unified Multimodal Context Builder

Handles EventBus ingress and orchestrates the ContextBuilder.
"""

from event_bus import EventBus, ContextReadyForLLM, MultimodalContextUpdated
from .multimodal_context import MultimodalContext
from .context_builder import ContextBuilder
from .context_health import ContextHealth
from .context_statistics import ContextStatistics

class MultimodalManager:
    def __init__(self, event_bus: EventBus):
        self.event_bus = event_bus
        self.context = MultimodalContext()
        self.builder = ContextBuilder(self.context)
        
        self.health = ContextHealth()
        self.stats = ContextStatistics()

    def process_and_publish(self):
        """
        Runs the context builder and publishes the final block.
        Usually called on a 1Hz clock loop by the MultimodalEngine.
        """
        try:
            final_block = self.builder.build_prompt_block()
            
            # This is the master event consumed by the LLM Provider
            self.event_bus.publish(ContextReadyForLLM(
                prompt_block=final_block
            ))
            
            self.event_bus.publish(MultimodalContextUpdated())
            
            self.stats.record_build()
            self.health.record_success()
        except Exception as e:
            self.health.record_error()
