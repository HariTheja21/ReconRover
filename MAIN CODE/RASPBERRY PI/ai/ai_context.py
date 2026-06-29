"""
ai_context.py
Recon Rover V1 - AI Decision Engine

Maintains a bounded snapshot of the rover's current state.
"""

import time
from dataclasses import dataclass, field
from typing import Dict, Any, List

@dataclass
class AIContext:
    last_update: float = field(default_factory=time.perf_counter)
    
    # World Model
    world_state: Dict[str, Any] = field(default_factory=dict)
    
    # Perception
    vision_semantics: Dict[str, Any] = field(default_factory=dict)
    audio_semantics: Dict[str, Any] = field(default_factory=dict)
    
    # Navigation
    navigation_state: str = "IDLE"
    
    # Mission
    mission_state: str = "IDLE"
    current_objective: str = "IDLE"
    
    # System
    battery_level: float = 100.0
    battery_critical: bool = False
    system_health: str = "OK"
    
    def update_vision(self, semantics: dict):
        self.vision_semantics = semantics
        self.last_update = time.perf_counter()
        
    def update_audio(self, semantics: dict):
        self.audio_semantics = semantics
        self.last_update = time.perf_counter()
        
    def update_battery(self, critical: bool):
        self.battery_critical = critical
        self.last_update = time.perf_counter()
