from dataclasses import dataclass

@dataclass
class LLMStatistics:
    prompts_processed: int = 0
    tokens_generated: int = 0
    tools_invoked: int = 0
    agents_orchestrated: int = 0
    errors_encountered: int = 0
