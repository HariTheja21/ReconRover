class SpeechHealth:
    def __init__(self):
        self.is_healthy: bool = True
        self.mic_active: bool = False
        self.speaker_active: bool = False
        self.stt_model_loaded: bool = False
        self.tts_model_loaded: bool = False
        self.error_message: str = ""

    def set_error(self, message: str):
        self.is_healthy = False
        self.error_message = message

    def clear_error(self):
        self.is_healthy = True
        self.error_message = ""
