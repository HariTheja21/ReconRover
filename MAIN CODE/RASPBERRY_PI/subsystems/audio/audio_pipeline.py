"""
audio_pipeline.py
Recon Rover V1 - Audio Pipeline

Orchestrator for the asynchronous audio layer (Phase 4.4).
"""

import asyncio
from system.lifecycle_manager import BaseModule
from event_bus import EventBus, AudioCaptured, AudioProcessed

from .microphone_manager import MicrophoneManager
from .audio_buffer import AudioBuffer
from .audio_provider import AudioProvider
from .audio_preprocessor import AudioPreprocessor
from .voice_activity_detector import MockVAD
from .sound_classifier import MockSoundClassifier
from .speech_detector import MockSpeechDetector
from .speech_recognizer import MockSpeechRecognizer
from .direction_estimator import MockDirectionEstimator
from .audio_scene_analyzer import AudioSceneAnalyzer
from .audio_health import AudioHealth
from .audio_statistics import AudioStatistics

class AudioPipeline(BaseModule):
    def __init__(self, event_bus: EventBus):
        super().__init__()
        self.event_bus = event_bus
        
        self.health = AudioHealth()
        self.stats = AudioStatistics()
        
        self.mic = MicrophoneManager(device_id=0, sample_rate=16000)
        self.buffer = AudioBuffer(self.health, self.stats, maxsize=10)
        
        self.provider = AudioProvider(self.mic, self.buffer, self.event_bus, self.health, self.stats)
        self.preprocessor = AudioPreprocessor(self.health)
        
        self.vad = MockVAD()
        self.classifier = MockSoundClassifier()
        self.speech_det = MockSpeechDetector()
        self.speech_rec = MockSpeechRecognizer()
        self.direction = MockDirectionEstimator()
        
        self.analyzer = AudioSceneAnalyzer(self.event_bus)
        
        self._running = False
        self._task = None

    async def initialize(self):
        self.log.info("AudioPipeline (Phase 4.4) initialized.")

    async def start(self):
        self._running = True
        self.provider.start()
        self._task = asyncio.create_task(self._pipeline_loop())
        self.log.info("AudioPipeline started.")

    async def stop(self):
        self._running = False
        self.provider.stop()
        if self._task:
            self._task.cancel()
        self.log.info("AudioPipeline stopped.")

    def health(self) -> str:
        if self.health.mic_status != "CONNECTED":
            return "DEGRADED_MIC_DISCONNECTED"
        return "OK"

    async def _pipeline_loop(self):
        """Pulls audio chunks, preprocesses, classifies, recognizes speech, and analyzes."""
        while self._running:
            try:
                # 1. Get raw audio chunk from bounded buffer
                raw_data = await self.buffer.get()
                self.event_bus.publish(AudioCaptured(timestamp=raw_data["timestamp"]))
                
                # 2. Preprocess (Normalize, Filter)
                processed_data = await self.preprocessor.process(raw_data)
                self.event_bus.publish(AudioProcessed(timestamp=raw_data["timestamp"]))
                self.stats.record_processed()
                
                # 3. Voice Activity Detection
                vad_active = await self.vad.run_detection(processed_data)
                
                # 4. General Sound Classification
                sounds = await self.classifier.run_classification(processed_data)
                
                # 5. Speech Detection (Segmentation)
                speech_segment = await self.speech_det.run_detection(processed_data, vad_active)
                
                # 6. Speech Recognition
                speech_text = None
                if speech_segment:
                    speech_text = await self.speech_rec.run_transcription(speech_segment)
                    
                # 7. Direction Estimation
                doa = await self.direction.run_estimation(processed_data)
                
                # 8. Scene Analysis (Semantic Mapping)
                self.analyzer.analyze(vad_active, sounds, speech_text, doa)
                
                self.buffer.task_done()
            except asyncio.CancelledError:
                break
            except Exception as e:
                self.log.error(f"AudioPipeline loop error: {e}")
                await asyncio.sleep(0.5)
