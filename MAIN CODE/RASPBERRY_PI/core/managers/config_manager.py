"""
Config Manager Module
Recon Rover V2 - Phase 2.3

Provides a centralized, thread-safe runtime configuration API.
Subscribes to Configuration requests over the EventBus and manages in-memory config states.
"""

import threading
import asyncio
from typing import Dict, Any

from .configuration_loader import ConfigurationLoader
from .config_events import ConfigurationRequest, ConfigurationUpdate, ConfigurationUpdated

class ConfigManager:
    """
    Manages runtime configuration, enforcing thread-safe reads and asynchronous updates.
    """
    
    def __init__(self, event_bus: Any):
        self._bus = event_bus
        self._loader = ConfigurationLoader()
        self._lock = threading.RLock()
        
        # Load initial state
        self._current_config = self._loader.load()
        
        # Subscribe to EventBus
        self._bus.subscribe(ConfigurationRequest, self._handle_config_request)
        self._bus.subscribe(ConfigurationUpdate, self._handle_config_update)
        
    def get(self, section: str, key: str = None) -> Any:
        """
        Thread-safe getter for configuration values.
        """
        with self._lock:
            sec = self._current_config.get(section, {})
            if key is None:
                return sec
            return sec.get(key)
            
    async def _handle_config_request(self, event: ConfigurationRequest) -> None:
        """
        Fired when a module requests the current config.
        We broadcast the full config back.
        """
        with self._lock:
            # We copy to prevent reference mutation by the receiver
            cfg_copy = dict(self._current_config)
            
        self._bus.publish(ConfigurationUpdated(current_config=cfg_copy, changed_keys=[]))
        
    async def _handle_config_update(self, event: ConfigurationUpdate) -> None:
        """
        Fired when a request to mutate the config occurs.
        """
        changed_keys = []
        with self._lock:
            for compound_key, new_value in event.updates.items():
                # Expecting 'section.key' format
                parts = compound_key.split('.')
                if len(parts) == 2:
                    section, key = parts[0], parts[1]
                    if section in self._current_config:
                        # Simple type validation based on existing type
                        existing = self._current_config[section].get(key)
                        if existing is not None and type(existing) == type(new_value):
                            self._current_config[section][key] = new_value
                            changed_keys.append(compound_key)
                        elif existing is None:
                            # Allow new keys if they were dynamically requested
                            self._current_config[section][key] = new_value
                            changed_keys.append(compound_key)
            
            # Save to disk if changes occurred
            if changed_keys:
                self._loader.save(self._current_config)
                cfg_copy = dict(self._current_config)
                
        if changed_keys:
            self._bus.publish(ConfigurationUpdated(current_config=cfg_copy, changed_keys=changed_keys))
