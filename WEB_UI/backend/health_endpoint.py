from typing import Dict, Any
from .system_summary import SystemSummary
from .release_manager import ReleaseManager

class HealthEndpoint:
    def __init__(self, summary: SystemSummary, release: ReleaseManager):
        self.summary = summary
        self.release = release
        
    def get_health(self) -> Dict[str, Any]:
        return {
            "status": "OK",
            "version": self.release.get_version_info(),
            "system": self.summary.get_summary()
        }
