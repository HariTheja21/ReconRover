import asyncio
from typing import Any

from .audio_health import AudioHealth
from .audio_statistics import AudioStatistics
from .audio_bridge import AudioBridge
from .audio_registry import AudioRegistry
from .audio_loader import AudioLoader
from .microphone_manager import MicrophoneManager
from .audio_stream import AudioStream
from .audio_buffer import AudioBuffer
from .audio_preprocessor import AudioPreprocessor
from .audio_postprocessor import AudioPostprocessor
from .voice_activity_detector import VoiceActivityDetector
from .wakeword_detector import WakeWordDetector
from .speech_recognition import SpeechRecognition
from .command_parser import CommandParser
from .text_to_speech import TextToSpeech
from .audio_scheduler import AudioScheduler

from .providers.whisper_provider import WhisperProvider
from .providers.whispercpp_provider import WhisperCPPProvider
from .providers.piper_provider import PiperProvider
from .providers.openai_stt_provider import OpenAI_STTProvider

class AudioRuntime:
    def __init__(self, event_bus: Any):
        self.health = AudioHealth()
        self.stats = AudioStatistics()
        self.bridge = AudioBridge(event_bus)
        
        self.registry = AudioRegistry()
        self._register_default_models()
        
        self.loader = AudioLoader(self.registry)
        
        self.mic = MicrophoneManager()
        self.stream = AudioStream()
        self.buffer = AudioBuffer()
        
        self.preprocessor = AudioPreprocessor()
        self.postprocessor = AudioPostprocessor()
        
        self.vad = VoiceActivityDetector()
        self.wake = WakeWordDetector(self.bridge.publish_event)
        
        self.speech = SpeechRecognition(self.loader, self.preprocessor, self.postprocessor, self.bridge.publish_event)
        self.parser = CommandParser(self.bridge.publish_event)
        self.tts = TextToSpeech(self.loader, self.bridge.publish_event)
        
        self.scheduler = AudioScheduler(self.mic, self.buffer, self.vad, self.wake, self.speech)
        
    def _register_default_models(self):
        self.registry.register("whisper", WhisperProvider)
        self.registry.register("whispercpp", WhisperCPPProvider)
        self.registry.register("piper", PiperProvider)
        self.registry.register("openai_stt", OpenAI_STTProvider)
        
    async def initialize(self):
        return True
