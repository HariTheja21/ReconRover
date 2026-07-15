from dataclasses import dataclass
from typing import Dict, Any

@dataclass
class WakeWordDetected:
    wake_word: str
    confidence: float
    timestamp: float

@dataclass
class SpeechRecognized:
    text: str
    confidence: float
    language: str
    is_final: bool
    timestamp: float

@dataclass
class TranscriptGenerated:
    session_id: str
    speaker_id: str
    text: str
    timestamp: float

@dataclass
class SpeechCommandParsed:
    command: str
    parameters: Dict[str, Any]
    confidence: float
    timestamp: float

@dataclass
class SpeechResponseRequested:
    text: str
    voice_profile: str
    priority: int
    timestamp: float
