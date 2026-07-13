"""
memory_statistics.py
Recon Rover V1 - Persistent Memory

Tracks memory operations.
"""

class MemoryStatistics:
    def __init__(self):
        self.total_writes = 0
        self.total_retrievals = 0
        self.total_summarizations = 0
        self.total_decays = 0

    def record_write(self):
        self.total_writes += 1

    def record_retrieval(self):
        self.total_retrievals += 1

    def record_summarization(self):
        self.total_summarizations += 1
        
    def record_decay(self):
        self.total_decays += 1
