"""
memory_types.py
Recon Rover V1 - Persistent Memory

Core data models for the cognitive memory system.
"""

from dataclasses import dataclass, field
from typing import List, Optional
import uuid
import time

@dataclass
class MemoryEntry:
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    timestamp: float = field(default_factory=time.time)
    category: str = "WORKING" # WORKING, SHORT_TERM, LONG_TERM, MISSION, SEMANTIC, EPISODIC
    importance: float = 1.0 # 0.0 to 10.0
    mission_id: Optional[str] = None
    location: Optional[str] = None
    tags: List[str] = field(default_factory=list)
    summary: str = ""
    detailed_text: str = ""
    confidence: float = 1.0
    source_module: str = "UNKNOWN"
