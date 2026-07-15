from typing import Callable, Tuple, Dict, Any, Optional

from .configuration_storage import ConfigurationStorage
from .configuration_validator import ConfigurationValidator
from .profile_manager import ProfileManager
from .configuration_statistics import ConfigurationStatistics
from .configuration_health import ConfigurationHealth
from .configuration_events import ConfigurationUpdatedEvent
import time

class ConfigurationEngine:
    def __init__(self, publish_callback: Callable):
        self.stats = ConfigurationStatistics()
        self.health = ConfigurationHealth()
        self.storage = ConfigurationStorage()
        self.validator = ConfigurationValidator()
        self.profile_manager = ProfileManager(self.storage)
        self.publish = publish_callback
        
    def get_current_configuration(self) -> Dict[str, Any]:
        cfg = self.storage.load_configuration("active_config")
        if not cfg:
            # Return sensible defaults if nothing active
            cfg = {
                "motion_limits": {"max_velocity": 1.0, "max_acceleration": 0.5},
                "safety_thresholds": {"obstacle_distance_m": 0.5, "battery_critical_v": 10.5},
                "communication": {"heartbeat_interval_ms": 1000},
                "camera": {"fps": 30, "resolution": "640x480"}
            }
        return cfg

    def update_configuration(self, config_data: Dict[str, Any]) -> Tuple[bool, str]:
        is_valid, msg = self.validator.validate_configuration(config_data)
        if not is_valid:
            return False, msg
            
        try:
            # Backup before replacing
            self.storage.backup_configuration("active_config", f"backup_{int(time.time())}")
            self.storage.save_configuration("active_config", config_data)
            
            # Publish to EventBus so system components can react
            event = ConfigurationUpdatedEvent("active_config", config_data, time.time())
            self.publish("ConfigurationUpdatedEvent", event)
            return True, "Configuration updated successfully"
        except Exception as e:
            self.health.set_storage_error(str(e))
            return False, f"Failed to update config: {str(e)}"

    def backup_active(self, backup_id: str) -> bool:
        return self.storage.backup_configuration("active_config", backup_id)

    def restore_backup(self, backup_id: str) -> bool:
        if self.storage.restore_configuration("active_config", backup_id):
            cfg = self.get_current_configuration()
            self.publish("ConfigurationUpdatedEvent", ConfigurationUpdatedEvent("active_config", cfg, time.time()))
            return True
        return False
