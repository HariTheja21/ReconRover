import time
from typing import Dict, Any, List, Optional
from .configuration_storage import ConfigurationStorage

class ProfileManager:
    def __init__(self, storage: ConfigurationStorage):
        self.storage = storage

    def save_profile(self, profile_name: str, config_data: Dict[str, Any]) -> str:
        profile_id = f"profile_{int(time.time())}"
        config_data["profile_name"] = profile_name
        self.storage.save_configuration(profile_id, config_data)
        return profile_id

    def load_profile(self, profile_id: str) -> Optional[Dict[str, Any]]:
        return self.storage.load_configuration(profile_id)
