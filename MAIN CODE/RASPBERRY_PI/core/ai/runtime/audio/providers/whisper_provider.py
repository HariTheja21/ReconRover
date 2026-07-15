from ..audio_provider import AudioProvider

class WhisperProvider(AudioProvider):
    def transcribe(self, audio_data: bytes) -> str:
        # Stub Whisper inference
        return "this is a mock whisper transcription"
