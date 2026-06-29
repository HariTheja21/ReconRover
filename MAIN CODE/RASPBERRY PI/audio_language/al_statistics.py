"""
al_statistics.py
Recon Rover V1 - Audio-Language Cognitive Integration

Tracks statistics regarding audio context generation.
"""

class ALStatistics:
    def __init__(self):
        self.speech_processed = 0
        self.sounds_processed = 0
        self.observations_published = 0
        self.memories_triggered = 0
        
    def record_speech(self):
        self.speech_processed += 1
        
    def record_sound(self):
        self.sounds_processed += 1
        
    def record_observation(self):
        self.observations_published += 1
        
    def record_memory(self):
        self.memories_triggered += 1
