from dataclasses import dataclass

@dataclass
class SpeechStatistics:
    wake_words_detected: int = 0
    utterances_processed: int = 0
    commands_parsed: int = 0
    tts_generated: int = 0
    avg_stt_latency_ms: float = 0.0
    avg_tts_latency_ms: float = 0.0
