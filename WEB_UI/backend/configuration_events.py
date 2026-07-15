from dataclasses import dataclass, field
from typing import Dict, Any

@dataclass
class ConfigurationUpdatedEvent:
    profile_id: str
    changes: Dict[str, Any]
    timestamp: float

@dataclass
class OTADeploymentEvent:
    package_id: str
    version: str
    status: str # PENDING, VALIDATING, DEPLOYING, SUCCESS, FAILED, ROLLBACK
    progress: float
    message: str
    timestamp: float
