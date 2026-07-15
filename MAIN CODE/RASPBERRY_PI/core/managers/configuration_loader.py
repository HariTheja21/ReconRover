"""
Configuration Loader Module
Recon Rover V2 - Phase 2.3

Handles disk I/O for JSON configuration files and provides robust fallbacks
using the Shared Definitions Framework constants if files are missing or corrupt.
"""

import os
import json
import sys
from typing import Dict, Any

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..', 'SHARED', 'python')))
try:
    from constants import SystemConstants, CommunicationConstants, SafetyConstants, MotionConstants
except ImportError:
    # Dummy fallbacks if shared definitions are unreachable
    class SafetyConstants: CRITICAL_BATTERY_V = 6.8; WARNING_BATTERY_V = 7.2
    class SystemConstants: PROTOCOL_VERSION = 2; DEFAULT_TICK_RATE_HZ = 50
    class MotionConstants: DEFAULT_SPEED = 150
    class CommunicationConstants: BAUD_RATE = 115200

class ConfigurationLoader:
    """
    Manages loading and saving of the runtime configuration JSON profile.
    """
    
    DEFAULT_PROFILE_PATH = os.path.join(os.path.dirname(__file__), '..', '..', 'config', 'rover_profile.json')
    
    @staticmethod
    def get_default_config() -> Dict[str, Any]:
        """
        Builds the fallback dictionary using the strongly-typed SHARED constants.
        """
        return {
            "system": {
                "protocol_version": getattr(SystemConstants, 'PROTOCOL_VERSION', 2),
                "tick_rate_hz": getattr(SystemConstants, 'DEFAULT_TICK_RATE_HZ', 50)
            },
            "safety": {
                "critical_battery_v": getattr(SafetyConstants, 'CRITICAL_BATTERY_V', 6.8),
                "warning_battery_v": getattr(SafetyConstants, 'WARNING_BATTERY_V', 7.2)
            },
            "motion": {
                "default_speed": getattr(MotionConstants, 'DEFAULT_SPEED', 150)
            },
            "communication": {
                "baud_rate": getattr(CommunicationConstants, 'BAUD_RATE', 115200)
            }
        }
        
    def load(self, file_path: str = None) -> Dict[str, Any]:
        """
        Loads the config from disk. If missing or corrupt, returns the defaults.
        """
        path = file_path or self.DEFAULT_PROFILE_PATH
        defaults = self.get_default_config()
        
        if not os.path.exists(path):
            self.save(defaults, path)
            return defaults
            
        try:
            with open(path, 'r') as f:
                disk_config = json.load(f)
                
            # Merge disk config with defaults to ensure missing keys are populated
            return self._merge_configs(defaults, disk_config)
            
        except (json.JSONDecodeError, IOError):
            return defaults
            
    def save(self, config: Dict[str, Any], file_path: str = None) -> bool:
        """
        Saves the config dictionary to disk safely.
        """
        path = file_path or self.DEFAULT_PROFILE_PATH
        
        # Ensure directory exists
        os.makedirs(os.path.dirname(path), exist_ok=True)
        
        try:
            with open(path, 'w') as f:
                json.dump(config, f, indent=4)
            return True
        except IOError:
            return False

    def _merge_configs(self, default: Dict[str, Any], override: Dict[str, Any]) -> Dict[str, Any]:
        """
        Recursively merges the override dict into the default dict.
        """
        merged = default.copy()
        for k, v in override.items():
            if k in merged and isinstance(merged[k], dict) and isinstance(v, dict):
                merged[k] = self._merge_configs(merged[k], v)
            else:
                merged[k] = v
        return merged
