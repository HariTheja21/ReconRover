"""
al_observation_generator.py
Recon Rover V1 - Audio-Language Cognitive Integration

Generates high-density, token-efficient observations for LLM context.
"""

from .al_context import ALContext

class ALObservationGenerator:
    def generate_observation(self, context: ALContext) -> str:
        """
        Creates a compressed string optimized for LLM token usage.
        Format: [AUDIO] Sound(footsteps, dir=90) | Speech(User: "Hello", c=0.9)
        """
        if not context.recent_events:
            return "[AUDIO] Silence"
            
        obs_parts = []
        
        for event in context.recent_events:
            dir_str = f"dir={event.direction:.0f}°" if event.direction >= 0 else "dir=unk"
            
            if event.event_type == "SOUND":
                cls_clean = event.content.replace("_", " ").title()
                obs_parts.append(f"Sound({cls_clean}, {dir_str})")
            elif event.event_type == "SPEECH":
                obs_parts.append(f"Speech({event.speaker}: \"{event.content}\", c={event.confidence:.2f}, {dir_str})")
                
        return "[AUDIO] " + " | ".join(obs_parts)
