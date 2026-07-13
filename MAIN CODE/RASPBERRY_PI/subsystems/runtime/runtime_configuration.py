"""
runtime_configuration.py
Recon Rover V1 - Full System Integration

Holds global configuration constants for the entire runtime stack.
"""

from dataclasses import dataclass

@dataclass
class RuntimeConfiguration:
    # Hardware
    serial_port: str = "/dev/ttyUSB0"
    baud_rate: int = 115200
    
    # LLM
    llm_provider: str = "llama_cpp"
    llm_model_path: str = "/models/phi-3-mini.gguf"
    
    # System
    heartbeat_timeout_sec: float = 2.0
    telemetry_cache_tolerance: float = 1.0
    queue_tick_rate_hz: int = 10
    
    # Dashboard
    dashboard_port: int = 8080
