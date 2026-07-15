from ..audio_provider import AudioProvider

class OpenAI_STTProvider(AudioProvider):
    def transcribe(self, audio_data: bytes) -> str:
        # Stub OpenAI API inference
        return "this is an openai transcription"
