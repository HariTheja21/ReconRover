from dataclasses import dataclass

@dataclass
class RuntimeStatistics:
    providers_loaded: int = 0
    models_downloaded: int = 0
    benchmarks_run: int = 0
    resource_alerts: int = 0
