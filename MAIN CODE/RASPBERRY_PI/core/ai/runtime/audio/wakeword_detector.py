class WakeWordDetector:
    def __init__(self, publish):
        self.publish = publish
        
    def detect(self, audio_data: bytes) -> bool:
        # Stub Wake word
        detected = True
        if detected:
            self.publish("WakeWordDetected", {
                "wake_word": "recon",
                "confidence": 0.99,
                "timestamp": 0.0
            })
        return detected
