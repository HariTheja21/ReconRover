"""
integration_validator.py
Recon Rover V1 - Full System Integration

Validates that all required modules actually started and exist in the registry.
"""

import logging
from typing import Dict
from .dependency_graph import DependencyGraph
from .lifecycle_manager import BaseModule

class IntegrationValidator:
    def __init__(self, modules: Dict[str, BaseModule]):
        self.log = logging.getLogger("IntegrationValidator")
        self.modules = modules
        self.required = DependencyGraph.get_startup_sequence()
        
    def validate_integration(self) -> bool:
        """
        Runs a final pre-flight check after startup.
        Returns True if the system is fully integrated.
        """
        self.log.info("Running Final Integration Validation...")
        missing = []
        for req in self.required:
            if req not in self.modules:
                missing.append(req)
                
        if missing:
            self.log.critical(f"Integration Validation FAILED. Missing modules: {missing}")
            return False
            
        self.log.info("Integration Validation PASSED. All modules present.")
        return True
