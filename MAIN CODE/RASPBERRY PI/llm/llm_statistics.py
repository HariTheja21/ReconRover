"""
llm_statistics.py
Recon Rover V1 - Local LLM Decision Engine

Tracks inference statistics.
"""

class LLMStatistics:
    def __init__(self):
        self.total_requests = 0
        self.successful_responses = 0
        self.failed_responses = 0
        
    def record_request(self):
        self.total_requests += 1
        
    def record_success(self):
        self.successful_responses += 1
        
    def record_failure(self):
        self.failed_responses += 1
