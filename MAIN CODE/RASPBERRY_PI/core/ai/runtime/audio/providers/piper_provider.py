from ..audio_provider import AudioProvider

class PiperProvider(AudioProvider):
    def synthesize(self, text: str) -> bytes:
        # Stub Piper TTS
        return b"mock_audio_data_for_piper"
