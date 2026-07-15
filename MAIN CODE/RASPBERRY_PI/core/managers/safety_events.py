"""
Safety Events Module
Recon Rover V2 - Phase 2.2

Defines strongly-typed events consumed and published by the Mode Manager and Safety Manager.
These events leverage the Shared Definitions Framework.
"""

from dataclasses import dataclass
from typing import Optional, Dict, Any

# We import the base Event class from the central EventBus
# Assuming RASPBERRY_PI is in the Python Path or using relative imports.
# For flexibility in this architecture, we will use an absolute import assuming RASPBERRY_PI is root,
# or we can just define a lightweight placeholder Event if it fails.
try:
    from core.event_bus import Event
except ImportError:
    @dataclass
    class Event:
        pass


# ---------------------------------------------------------
# CONSUMED EVENTS (Incoming to Managers)
# ---------------------------------------------------------

@dataclass
class SystemHealthUpdated(Event):
    """
    Published by various modules to report their health.
    
    Attributes:
        module_id (int): The ID of the module reporting health (from SHARED.enums.ModuleID).
        health_state (int): The current health state (from SHARED.enums.HealthState).
        details (str): Optional text providing context (e.g., error trace).
    """
    module_id: int
    health_state: int
    details: str = ""


@dataclass
class BatteryUpdated(Event):
    """
    Published by the Battery/Power monitor when reading new voltages.
    
    Attributes:
        voltage (float): Current battery voltage.
        percentage (float): Current battery percentage (0.0 to 100.0).
        current_ma (float): Current draw in milliamps.
    """
    voltage: float
    percentage: float
    current_ma: float = 0.0


@dataclass
class TelemetryUpdated(Event):
    """
    Published when new telemetry (IMU, distance) arrives.
    
    Attributes:
        telemetry_type (int): Type of telemetry (from SHARED.enums.TelemetryType).
        data (Dict[str, Any]): The raw telemetry payload.
    """
    telemetry_type: int
    data: Dict[str, Any]


@dataclass
class EmergencyButtonPressed(Event):
    """
    Published when a hardware or software Emergency Stop button is pressed.
    
    Attributes:
        source (str): The origin of the E-Stop (e.g., "HARDWARE", "WEB_UI").
    """
    source: str


@dataclass
class RemoteModeRequest(Event):
    """
    Request to transition to REMOTE operating mode.
    """
    pass


@dataclass
class BrowserModeRequest(Event):
    """
    Request to transition to SMART_CONTROL (Browser) operating mode.
    """
    pass


@dataclass
class LegendModeRequest(Event):
    """
    Request to transition to LEGEND_AI operating mode.
    """
    pass


@dataclass
class MissionModeRequest(Event):
    """
    Request to transition to a specific Mission Mode.
    
    Attributes:
        target_mission (int): The requested mission (from SHARED.enums.MissionMode).
    """
    target_mission: int


# ---------------------------------------------------------
# PUBLISHED EVENTS (Outgoing from Managers)
# ---------------------------------------------------------

@dataclass
class OperatingModeChanged(Event):
    """
    Published when the Operating Mode successfully changes.
    
    Attributes:
        new_mode (int): The new operating mode (from SHARED.enums.OperatingMode).
        previous_mode (int): The old operating mode.
    """
    new_mode: int
    previous_mode: int


@dataclass
class MissionModeChanged(Event):
    """
    Published when the Mission Mode successfully changes.
    
    Attributes:
        new_mission (int): The new mission mode (from SHARED.enums.MissionMode).
        previous_mission (int): The old mission mode.
    """
    new_mission: int
    previous_mission: int


@dataclass
class EmergencyStopActivated(Event):
    """
    Published when the Safety Manager triggers an Emergency Stop.
    
    Attributes:
        reason (str): The reason for the E-Stop.
    """
    reason: str


@dataclass
class SafetyStateChanged(Event):
    """
    Published when the overarching Safety State changes.
    
    Attributes:
        new_state (int): The new safety state (from SHARED.enums.SafetyState).
        reason (str): Context for the transition.
    """
    new_state: int
    reason: str


@dataclass
class ModeTransitionRejected(Event):
    """
    Published when a mode transition request violates a constraint.
    
    Attributes:
        requested_mode (int): The mode that was requested (Operating or Mission).
        reason (str): Why the transition was rejected.
    """
    requested_mode: int
    reason: str


@dataclass
class SystemLocked(Event):
    """
    Published when the system is locked down due to severe safety violations.
    
    Attributes:
        reason (str): The reason for the system lock.
    """
    reason: str
