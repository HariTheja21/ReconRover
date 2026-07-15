from ..audio_provider import AudioProvider

class WhisperCPPProvider(AudioProvider):
    def transcribe(self, audio_data: bytes) -> str:
        # Stub Whisper.cpp inference
        return "this is a fast whisper cpp transcription"
