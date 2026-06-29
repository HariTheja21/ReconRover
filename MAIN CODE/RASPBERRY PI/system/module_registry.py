"""
module_registry.py
Recon Rover V1 - System Orchestrator

Advanced module registry tracking instances, states, and metadata.
"""

from typing import Dict, Any, List
from dataclasses import dataclass
from .application_state import LifecycleState

@dataclass
class ModuleRecord:
    name: str
    instance: Any
    state: LifecycleState = LifecycleState.REGISTERED

class ModuleRegistry:
    """
    Central registry for all active modules.
    Now supports states and advanced queries.
    """
    _records: Dict[str, ModuleRecord] = {}

    @classmethod
    def register(cls, name: str, instance: Any):
        if name in cls._records:
            raise ValueError(f"Module {name} already registered.")
        cls._records[name] = ModuleRecord(name=name, instance=instance)

    @classmethod
    def get(cls, name: str) -> Any:
        if name not in cls._records:
            raise KeyError(f"Module {name} not found in registry.")
        return cls._records[name].instance
        
    @classmethod
    def get_record(cls, name: str) -> ModuleRecord:
        if name not in cls._records:
            raise KeyError(f"Module {name} not found in registry.")
        return cls._records[name]

    @classmethod
    def all_modules(cls) -> Dict[str, Any]:
        """Backward compatibility"""
        return {name: record.instance for name, record in cls._records.items()}
        
    @classmethod
    def set_state(cls, name: str, state: LifecycleState):
        if name in cls._records:
            cls._records[name].state = state
            
    @classmethod
    def get_modules_in_state(cls, state: LifecycleState) -> List[str]:
        return [name for name, record in cls._records.items() if record.state == state]
        
    @classmethod
    def clear(cls):
        cls._records.clear()
