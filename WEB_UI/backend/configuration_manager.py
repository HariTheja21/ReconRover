from typing import Callable, Dict, Any, Tuple
from .configuration_engine import ConfigurationEngine
from .ota_manager import OTAManager

class ConfigurationManager:
    """
    Main entry point for the Ground Station Backend for handling Configuration & OTA.
    Integrates with FastAPI routes and WebSocket bridges.
    """
    def __init__(self, publish_callback: Callable):
        self.engine = ConfigurationEngine(publish_callback)
        self.ota_manager = OTAManager(publish_callback, self.engine.stats, self.engine.health)

    def get_config(self) -> Dict[str, Any]:
        return self.engine.get_current_configuration()

    def update_config(self, config_data: Dict[str, Any]) -> Tuple[bool, str]:
        return self.engine.update_configuration(config_data)

    def backup_config(self, backup_id: str) -> bool:
        return self.engine.backup_active(backup_id)

    def restore_config(self, backup_id: str) -> bool:
        return self.engine.restore_backup(backup_id)

    async def handle_ota_upload(self, file_content: bytes, filename: str, expected_checksum: str, version: str) -> Tuple[bool, str]:
        return await self.ota_manager.process_ota_upload(file_content, filename, expected_checksum, version)
