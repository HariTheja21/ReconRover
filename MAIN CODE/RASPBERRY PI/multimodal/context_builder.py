"""
context_builder.py
Recon Rover V1 - Unified Multimodal Context Builder

Coordinates the internal formatting pipeline (Merge -> Optimize -> Prioritize -> Format).
"""

from .multimodal_context import MultimodalContext
from .context_merger import ContextMerger
from .context_optimizer import ContextOptimizer
from .context_prioritizer import ContextPrioritizer
from .context_formatter import ContextFormatter

class ContextBuilder:
    def __init__(self, context: MultimodalContext):
        self.context = context
        self.merger = ContextMerger(self.context)
        self.optimizer = ContextOptimizer()
        self.prioritizer = ContextPrioritizer()
        self.formatter = ContextFormatter()
        
    def build_prompt_block(self) -> str:
        """Executes the deterministic funnel to generate the LLM prompt block."""
        self.optimizer.optimize(self.context)
        prioritized = self.prioritizer.prioritize(self.context)
        return self.formatter.format_prompt_block(prioritized)
