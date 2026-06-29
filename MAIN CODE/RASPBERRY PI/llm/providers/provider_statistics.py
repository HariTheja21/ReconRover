"""
provider_statistics.py
Recon Rover V1 - Local LLM Framework

Tracks specific API usage metrics per provider.
"""

class ProviderStatistics:
    def __init__(self):
        self.requests = 0
        self.successful_requests = 0
        self.failed_requests = 0
        self.total_prompt_tokens = 0
        self.total_completion_tokens = 0

    def record_success(self, prompt_tokens: int, completion_tokens: int):
        self.requests += 1
        self.successful_requests += 1
        self.total_prompt_tokens += prompt_tokens
        self.total_completion_tokens += completion_tokens

    def record_failure(self):
        self.requests += 1
        self.failed_requests += 1

    @property
    def avg_prompt_tokens(self) -> float:
        if self.successful_requests == 0:
            return 0.0
        return self.total_prompt_tokens / self.successful_requests

    @property
    def avg_completion_tokens(self) -> float:
        if self.successful_requests == 0:
            return 0.0
        return self.total_completion_tokens / self.successful_requests
