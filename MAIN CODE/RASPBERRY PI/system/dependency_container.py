"""
dependency_container.py
Recon Rover V1 - System Orchestrator

Facilitates explicit dependency injection for all system modules.
"""

from typing import Dict, Any, Type
from logger import Logger

class DependencyContainer:
    def __init__(self):
        self._dependencies: Dict[str, Any] = {}
        self.log = Logger.get("DependencyContainer")

    def provide(self, key: str, instance: Any):
        """Registers a dependency instance."""
        if key in self._dependencies:
            self.log.warning(f"Dependency '{key}' overwritten.")
        self._dependencies[key] = instance
        self.log.debug(f"Provided dependency: {key}")

    def resolve(self, key: str) -> Any:
        """Resolves a dependency instance."""
        if key not in self._dependencies:
            raise KeyError(f"Dependency '{key}' not found in container.")
        return self._dependencies[key]
        
    def resolve_type(self, cls: Type) -> Any:
        """Helper to resolve by type name if registered as such."""
        return self.resolve(cls.__name__)
