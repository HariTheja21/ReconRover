class WakeWordDetector:
    def __init__(self, wake_words=None):
        if wake_words is None:
            wake_words = ["rover", "hey rover"]
        self.wake_words = wake_words
        
    def detect(self, audio_chunk: bytes) -> tuple[bool, str, float]:
        # Stub: e.g. OpenWakeWord or Porcupine integration
        # Returns (Detected, WakeWord, Confidence)
        return False, "", 0.0
        
    def mock_detect(self) -> tuple[bool, str, float]:
        return True, "rover", 0.99
