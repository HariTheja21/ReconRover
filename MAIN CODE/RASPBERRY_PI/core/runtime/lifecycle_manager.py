"""
Lifecycle Manager Module
Recon Rover V2 - Phase 3.0
"""
from enum import Enum

class ModuleState(Enum):
    INIT = 1
    STARTING = 2
    RUNNING = 3
    STOPPING = 4
    STOPPED = 5
    FAULT = 6

class LifecycleManager:
    """Tracks the state of all registered modules."""
    
    def __init__(self):
        self.module_states = {}
        
    def register_module(self, module_name: str):
        if module_name not in self.module_states:
            self.module_states[module_name] = ModuleState.INIT
            
    def set_state(self, module_name: str, state: ModuleState):
        if module_name in self.module_states:
            self.module_states[module_name] = state
            
    def get_state(self, module_name: str) -> ModuleState:
        return self.module_states.get(module_name, ModuleState.INIT)
