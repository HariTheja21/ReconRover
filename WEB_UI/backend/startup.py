import asyncio
import logging
from .dependency_checker import DependencyChecker
from .deployment_manager import DeploymentManager
from .release_manager import ReleaseManager

logger = logging.getLogger(__name__)

class StartupManager:
    def __init__(self):
        self.dep_checker = DependencyChecker()
        self.deploy_manager = DeploymentManager()
        self.release_manager = ReleaseManager()
        
    async def execute_startup(self) -> bool:
        v_info = self.release_manager.get_version_info()
        logger.info(f"Starting Recon Rover V2 Ground Station {v_info['version']} ({v_info['codename']})")
        
        if not self.dep_checker.check_all():
            logger.error("Dependency check failed. Cannot start.")
            return False
            
        if not self.deploy_manager.verify_deployment():
            logger.error("Deployment verification failed.")
            return False
            
        logger.info("All startup checks passed. Ground Station is OPERATIONAL.")
        return True
