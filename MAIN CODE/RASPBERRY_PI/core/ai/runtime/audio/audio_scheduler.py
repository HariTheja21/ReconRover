import asyncio

class AudioScheduler:
    def __init__(self, mic_manager, audio_buffer, vad, wake_detector, speech_recognizer):
        self.mic = mic_manager
        self.buffer = audio_buffer
        self.vad = vad
        self.wake = wake_detector
        self.recognizer = speech_recognizer
        self.is_running = False
        
    async def run_audio_loop(self):
        self.is_running = True
        self.mic.start_stream()
        
        while self.is_running:
            # Stub: read audio chunk, check vad, check wake word, buffer, transcribe
            await asyncio.sleep(0.1)
