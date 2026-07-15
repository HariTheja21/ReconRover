from dataclasses import dataclass

@dataclass
class AudioStatistics:
    total_recognitions: int = 0
    total_tts_generated: int = 0
    wake_words_detected: int = 0
    commands_parsed: int = 0
