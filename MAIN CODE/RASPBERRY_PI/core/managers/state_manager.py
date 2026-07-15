"""
State Manager Module
Recon Rover V2 - Phase 2.2

Thread-safe, centralized data store holding the current runtime state.
Tracks OperatingMode, MissionMode, SafetyState, and lockouts.
Provides read-only access for other modules.
"""

import sys
import os
import threading

# Add SHARED to path dynamically for robustness
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..', 'SHARED', 'python')))
try:
    from enums import OperatingMode, MissionMode, SafetyState, HealthState
except ImportError:
    # Fallbacks for syntax parsing if path fails during linting
    class OperatingMode: STANDBY = 0
    class MissionMode: IDLE = 0
    class SafetyState: SAFE = 0


class StateManager:
    """
    Central repository for Rover state. All writes should be guarded by threading locks
    to ensure atomic updates from the EventBus callbacks.
    """
    
    def __init__(self):
        """Initializes the state manager with default safe states."""
        self._lock = threading.RLock()
        
        # Primary Modes
        self._operating_mode: int = OperatingMode.STANDBY
        self._mission_mode: int = MissionMode.IDLE
        
        # Safety & Lockouts
        self._safety_state: int = SafetyState.SAFE
        self._system_locked: bool = False
        self._lock_reason: str = ""
        
        # Environment Requirements flags (managed by telemetry/health updates)
        self._laptop_connected: bool = False
        self._wifi_connected: bool = False
        self._sensors_healthy: bool = True
        
    # ---------------------------------------------------------
    # GETTERS (Thread-Safe)
    # ---------------------------------------------------------
    
    @property
    def operating_mode(self) -> int:
        """Returns the current OperatingMode."""
        with self._lock:
            return self._operating_mode
            
    @property
    def mission_mode(self) -> int:
        """Returns the current MissionMode."""
        with self._lock:
            return self._mission_mode
            
    @property
    def safety_state(self) -> int:
        """Returns the current SafetyState."""
        with self._lock:
            return self._safety_state
            
    @property
    def is_locked(self) -> bool:
        """Returns True if the system is securely locked."""
        with self._lock:
            return self._system_locked
            
    @property
    def lock_reason(self) -> str:
        """Returns the reason the system was locked."""
        with self._lock:
            return self._lock_reason

    @property
    def laptop_connected(self) -> bool:
        """Returns True if the Legend AI laptop is currently communicating."""
        with self._lock:
            return self._laptop_connected

    @property
    def wifi_connected(self) -> bool:
        """Returns True if WiFi is connected."""
        with self._lock:
            return self._wifi_connected

    @property
    def sensors_healthy(self) -> bool:
        """Returns True if critical mission sensors are healthy."""
        with self._lock:
            return self._sensors_healthy

    # ---------------------------------------------------------
    # SETTERS (Thread-Safe)
    # ---------------------------------------------------------

    def set_operating_mode(self, mode: int) -> None:
        """
        Sets a new operating mode.
        Args:
            mode (int): The new OperatingMode to set.
        """
        with self._lock:
            self._operating_mode = mode

    def set_mission_mode(self, mode: int) -> None:
        """
        Sets a new mission mode.
        Args:
            mode (int): The new MissionMode to set.
        """
        with self._lock:
            self._mission_mode = mode

    def set_safety_state(self, state: int) -> None:
        """
        Sets the safety state.
        Args:
            state (int): The new SafetyState.
        """
        with self._lock:
            self._safety_state = state

    def lock_system(self, reason: str) -> None:
        """
        Locks the system, preventing mode transitions.
        Args:
            reason (str): Context for the lockdown.
        """
        with self._lock:
            self._system_locked = True
            self._lock_reason = reason
            
    def unlock_system(self) -> None:
        """Unlocks the system."""
        with self._lock:
            self._system_locked = False
            self._lock_reason = ""

    def update_environment_flags(self, laptop: bool = None, wifi: bool = None, sensors: bool = None) -> None:
        """
        Updates internal environment capability flags.
        Args:
            laptop (bool, optional): Connection status of Legend AI laptop.
            wifi (bool, optional): Connection status of WiFi.
            sensors (bool, optional): Overall sensor health.
        """
        with self._lock:
            if laptop is not None:
                self._laptop_connected = laptop
            if wifi is not None:
                self._wifi_connected = wifi
            if sensors is not None:
                self._sensors_healthy = sensors
