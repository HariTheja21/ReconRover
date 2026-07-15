import json
import os
import shutil
from typing import Dict, Optional

class ConfigurationStorage:
    def __init__(self, storage_dir: str = "data/config"):
        self.storage_dir = storage_dir
        self.backup_dir = os.path.join(storage_dir, "backups")
        if not os.path.exists(self.storage_dir):
            os.makedirs(self.storage_dir, exist_ok=True)
        if not os.path.exists(self.backup_dir):
            os.makedirs(self.backup_dir, exist_ok=True)
            
    def _get_filepath(self, config_id: str) -> str:
        return os.path.join(self.storage_dir, f"{config_id}.json")

    def save_configuration(self, config_id: str, config_data: dict) -> bool:
        filepath = self._get_filepath(config_id)
        with open(filepath, 'w') as f:
            json.dump(config_data, f, indent=4)
        return True

    def load_configuration(self, config_id: str) -> Optional[dict]:
        filepath = self._get_filepath(config_id)
        if not os.path.exists(filepath):
            return None
        with open(filepath, 'r') as f:
            return json.load(f)

    def backup_configuration(self, config_id: str, backup_id: str) -> bool:
        src = self._get_filepath(config_id)
        dst = os.path.join(self.backup_dir, f"{backup_id}.json")
        if os.path.exists(src):
            shutil.copy2(src, dst)
            return True
        return False

    def restore_configuration(self, config_id: str, backup_id: str) -> bool:
        src = os.path.join(self.backup_dir, f"{backup_id}.json")
        dst = self._get_filepath(config_id)
        if os.path.exists(src):
            shutil.copy2(src, dst)
            return True
        return False
