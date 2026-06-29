"""
multimodal_context.py
Recon Rover V1 - Unified Multimodal Context Builder

A structured representation of all rover subsystems.
"""

from dataclasses import dataclass, field
from typing import List, Dict, Any
import time

@dataclass
class SubsystemState:
    content: str = ""
    timestamp: float = 0.0
    
    def update(self, new_content: str):
        self.content = new_content
        self.timestamp = time.time()

@dataclass
class MultimodalContext:
    vision: SubsystemState = field(default_factory=SubsystemState)
    audio: SubsystemState = field(default_factory=SubsystemState)
    world: SubsystemState = field(default_factory=SubsystemState)
    navigation: SubsystemState = field(default_factory=SubsystemState)
    memory: SubsystemState = field(default_factory=SubsystemState)
    mission: SubsystemState = field(default_factory=SubsystemState)
    health: SubsystemState = field(default_factory=SubsystemState)
    battery: SubsystemState = field(default_factory=SubsystemState)
    hazard: SubsystemState = field(default_factory=SubsystemState)
