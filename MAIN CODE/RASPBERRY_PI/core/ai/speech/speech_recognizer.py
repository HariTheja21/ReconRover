import time

class SpeechRecognizer:
    def __init__(self):
        # Stub for Whisper, Whisper.cpp, or Vosk
        pass
        
    def recognize(self, audio_data: bytes) -> tuple[str, float, float]:
        # Stub: Returns (Transcript, Confidence, Latency)
        start = time.time()
        time.sleep(0.05) # mock inference latency
        latency = (time.time() - start) * 1000
        return "move forward five meters", 0.95, latency
