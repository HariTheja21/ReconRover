from dataclasses import dataclass

@dataclass
class ConfigurationStatistics:
    total_profiles_saved: int = 0
    total_profiles_loaded: int = 0
    total_configs_exported: int = 0
    total_ota_packages_uploaded: int = 0
    total_ota_deployments_successful: int = 0
    total_ota_deployments_failed: int = 0
    total_ota_rollbacks: int = 0
