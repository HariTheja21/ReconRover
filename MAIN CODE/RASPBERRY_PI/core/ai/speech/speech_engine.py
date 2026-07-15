import asyncio
import time
from typing import Callable, Any
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

class SpeechEngine:
    def __init__(self, pre: AudioPreprocessor, vad: VoiceActivityDetector, ww: WakeWordDetector,
                 stt: SpeechRecognizer, lang: LanguageDetector, transcript: TranscriptManager,
                 context: ConversationContext, parser: CommandParser, tts: TextToSpeech, 
                 post: AudioPostprocessor, stats: Any, publish: Callable):
        self.pre = pre
        self.vad = vad
        self.ww = ww
        self.stt = stt
        self.lang = lang
        self.transcript = transcript
        self.context = context
        self.parser = parser
        self.tts = tts
        self.post = post
        self.stats = stats
        self.publish = publish
        
        self.listening_state = False # True after wake word
        
    async def process_audio_chunk(self, chunk: bytes):
        proc_chunk = self.pre.process(chunk)
        
        # 1. Wake word detection (passive listening)
        if not self.listening_state:
            detected, ww_str, conf = self.ww.detect(proc_chunk)
            if detected:
                self.listening_state = True
                self.stats.wake_words_detected += 1
                self.publish("WakeWordDetected", {
                    "_speech_event_type": "WakeWordDetected",
                    "wake_word": ww_str,
                    "confidence": conf,
                    "timestamp": asyncio.get_event_loop().time()
                })
            return
            
        # 2. Voice Activity Detection (active listening)
        if not self.vad.is_speech(proc_chunk):
            # Silence detected, process buffer
            self.listening_state = False
            await self._process_utterance(proc_chunk)
            
    async def _process_utterance(self, audio_buffer: bytes):
        # 3. Speech-to-Text
        text, conf, latency = self.stt.recognize(audio_buffer)
        self.stats.avg_stt_latency_ms = (self.stats.avg_stt_latency_ms * 0.9) + (latency * 0.1)
        self.stats.utterances_processed += 1
        
        # 4. Language Detection
        lang_code = self.lang.detect(text)
        
        self.publish("SpeechRecognized", {
            "_speech_event_type": "SpeechRecognized",
            "text": text,
            "confidence": conf,
            "language": lang_code,
            "is_final": True,
            "timestamp": asyncio.get_event_loop().time()
        })
        
        # 5. Transcription Management
        self.transcript.add_utterance(text, "user")
        self.publish("TranscriptGenerated", {
            "_speech_event_type": "TranscriptGenerated",
            "session_id": self.transcript.session_id,
            "speaker_id": "user",
            "text": text,
            "timestamp": asyncio.get_event_loop().time()
        })
        
        # 6. Command Parsing (Local Fallback)
        cmd, params, cmd_conf = self.parser.parse(text)
        if cmd != "unknown":
            self.stats.commands_parsed += 1
            self.publish("SpeechCommandParsed", {
                "_speech_event_type": "SpeechCommandParsed",
                "command": cmd,
                "parameters": params,
                "confidence": cmd_conf,
                "timestamp": asyncio.get_event_loop().time()
            })
            
    async def process_tts_request(self, text: str, voice: str):
        # 7. Text-to-Speech Generation
        audio, latency = self.tts.synthesize(text, voice)
        self.stats.avg_tts_latency_ms = (self.stats.avg_tts_latency_ms * 0.9) + (latency * 0.1)
        self.stats.tts_generated += 1
        
        final_audio = self.post.process(audio)
        # Stub: Play final_audio via PyAudio/SoundDevice
        self.transcript.add_utterance(text, "rover")
