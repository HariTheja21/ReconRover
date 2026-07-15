from dataclasses import dataclass

@dataclass
class WakeWordDetected:
    wake_word: str
    confidence: float
    timestamp: float

@dataclass
class SpeechRecognized:
    text: str
    confidence: float
    timestamp: float

@dataclass
class SpeechCommandParsed:
    command: str
    intent: str
    timestamp: float

@dataclass
class TextToSpeechCompleted:
    text: str
    duration_sec: float
    timestamp: float

@dataclass
class AudioStatisticsUpdated:
    total_recognitions: int
    total_tts_generated: int
    timestamp: float

@dataclass
class AudioHealthUpdated:
    is_healthy: bool
    error_message: str
    timestamp: float
