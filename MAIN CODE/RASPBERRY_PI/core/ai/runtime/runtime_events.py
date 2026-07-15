from dataclasses import dataclass
from typing import Dict, Any

@dataclass
class RuntimeInitialized:
    device: str
    timestamp: float

@dataclass
class ProviderLoaded:
    provider_name: str
    timestamp: float

@dataclass
class ModelDownloaded:
    model_name: str
    version: str
    timestamp: float

@dataclass
class BenchmarkCompleted:
    model_name: str
    metrics: dict
    timestamp: float

@dataclass
class ResourceAlert:
    resource_type: str
    value: float
    timestamp: float
