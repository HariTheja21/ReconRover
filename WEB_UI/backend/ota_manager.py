import asyncio
import time
import os
import uuid
from typing import Callable, Tuple

from .ota_validator import OTAValidator
from .ota_deployer import OTADeployer
from .ota_bridge import OTABridge
from .configuration_statistics import ConfigurationStatistics
from .configuration_health import ConfigurationHealth
from .configuration_events import OTADeploymentEvent

class OTAManager:
    def __init__(self, publish_callback: Callable, stats: ConfigurationStatistics, health: ConfigurationHealth):
        self.stats = stats
        self.health = health
        self.bridge = OTABridge(publish_callback)
        self.validator = OTAValidator()
        self.deployer = OTADeployer(self.bridge)
        
        self.upload_dir = "data/ota_uploads"
        if not os.path.exists(self.upload_dir):
            os.makedirs(self.upload_dir, exist_ok=True)
            
        self.active_deployment = False

    async def process_ota_upload(self, file_content: bytes, filename: str, expected_checksum: str, version: str) -> Tuple[bool, str]:
        if self.active_deployment:
            return False, "Deployment already in progress."
            
        package_id = str(uuid.uuid4())
        filepath = os.path.join(self.upload_dir, f"{package_id}_{filename}")
        
        # 1. Save uploaded file
        try:
            with open(filepath, 'wb') as f:
                f.write(file_content)
        except Exception as e:
            self.health.set_ota_error(f"Failed to save upload: {str(e)}")
            return False, "Failed to save file."
            
        self.stats.total_ota_packages_uploaded += 1
        
        # 2. Validate checksum
        self.bridge.broadcast_status(OTADeploymentEvent(
            package_id=package_id, version=version, status="VALIDATING", progress=0.0,
            message="Verifying package integrity...", timestamp=time.time()
        ))
        
        is_valid = self.validator.validate_package(filepath, expected_checksum)
        if not is_valid:
            self.bridge.broadcast_status(OTADeploymentEvent(
                package_id=package_id, version=version, status="FAILED", progress=0.0,
                message="Checksum validation failed.", timestamp=time.time()
            ))
            self.stats.total_ota_deployments_failed += 1
            os.remove(filepath)
            return False, "Checksum mismatch."
            
        # 3. Deploy
        self.active_deployment = True
        try:
            success = await self.deployer.deploy_package(package_id, filepath, version)
            if success:
                self.stats.total_ota_deployments_successful += 1
                return True, "Deployment successful."
            else:
                self.stats.total_ota_deployments_failed += 1
                return False, "Deployment failed during flashing."
        finally:
            self.active_deployment = False
