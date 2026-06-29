"""
module_loader.py
Recon Rover V1 - System Orchestrator

Responsible for instantiating and registering modules.
"""

from logger import Logger
from .module_registry import ModuleRegistry
from .dependency_container import DependencyContainer
from .application_state import LifecycleState
import asyncio

class ModuleLoader:
    def __init__(self, container: DependencyContainer):
        self.container = container
        self.log = Logger.get("ModuleLoader")

    def load(self, name: str, cls, *args, **kwargs):
        """
        Instantiates a module, resolving any dependencies from the container,
        and registers it with the ModuleRegistry.
        """
        try:
            # We assume most modules take event_bus, which can be injected directly
            # or passed explicitly in args/kwargs.
            # To strictly follow the "do not break existing phases", we just pass args/kwargs.
            instance = cls(*args, **kwargs)
            
            ModuleRegistry.register(name, instance)
            ModuleRegistry.set_state(name, LifecycleState.REGISTERED)
            self.log.info(f"Loaded and registered module: {name}")
            return instance
            
        except Exception as e:
            self.log.critical(f"Failed to load module {name}: {e}")
            raise
