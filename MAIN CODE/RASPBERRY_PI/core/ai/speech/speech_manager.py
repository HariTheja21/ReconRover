import asyncio
from typing import Any
from .speech_health import SpeechHealth
from .speech_statistics import SpeechStatistics
from .speech_bridge import SpeechBridge
from .audio_capture import AudioCapture
from .audio_preprocessor import AudioPreprocessor
from .voice_activity_detector import VoiceActivityDetector
from .wake_word_detector import WakeWordDetector
from .speech_recognizer import SpeechRecognizer
from .language_detector import LanguageDetector
from .transcript_manager import TranscriptManager
from .conversation_context import ConversationContext
from .command_parser import CommandParser
from .text_to_speech import TextToSpeech
from .audio_postprocessor import AudioPostprocessor
from .speech_engine import SpeechEngine
from .speech_scheduler import SpeechScheduler

class SpeechManager:
    def __init__(self, event_bus: Any):
        self.health = SpeechHealth()
        self.stats = SpeechStatistics()
        self.bridge = SpeechBridge(event_bus)
        
        # Subcomponents
        self.capture = AudioCapture()
        self.pre = AudioPreprocessor()
        self.vad = VoiceActivityDetector()
        self.ww = WakeWordDetector()
        self.stt = SpeechRecognizer()
        self.lang = LanguageDetector()
        self.transcript = TranscriptManager()
        self.context = ConversationContext()
        self.parser = CommandParser()
        self.tts = TextToSpeech()
        self.post = AudioPostprocessor()
        
        # Assembly
        self.engine = SpeechEngine(
            self.pre, self.vad, self.ww, self.stt, self.lang, 
            self.transcript, self.context, self.parser, self.tts, 
            self.post, self.stats, self.bridge.publish_event
        )
        
        self.scheduler = SpeechScheduler(self.engine)
        
        # Connect capture to scheduler
        self.capture.set_callback(lambda audio_data: asyncio.create_task(self.scheduler.enqueue_audio(audio_data)))
        
    async def start(self):
        asyncio.create_task(self.scheduler.run_audio_loop())
        asyncio.create_task(self.scheduler.run_tts_loop())
        await self.capture.start_stream()
        self.health.mic_active = True
