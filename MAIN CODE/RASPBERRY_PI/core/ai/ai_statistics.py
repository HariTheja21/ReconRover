from dataclasses import dataclass

@dataclass
class AIStatistics:
    total_models_loaded: int = 0
    total_inferences_requested: int = 0
    total_inferences_completed: int = 0
    total_inferences_failed: int = 0
    total_tools_executed: int = 0
    average_inference_latency_ms: float = 0.0
