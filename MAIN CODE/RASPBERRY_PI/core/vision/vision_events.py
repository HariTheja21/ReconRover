"""
Vision Events Module
Recon Rover V2 - Phase 2.7

Defines asynchronous events for camera lifecycle and frame syndication.
"""

from dataclasses import dataclass
from typing import Any, Optional
import time

try:
    from core.event_bus import Event
except ImportError:
    @dataclass
    class Event: pass

# =============================================================================
# HARDWARE / LIFECYCLE EVENTS
# =============================================================================

@dataclass
class CameraStartRequest(Event):
    """Requests the camera pipeline to initialize and begin capturing."""
    resolution: tuple = (640, 480)
    fps: int = 30

@dataclass
class CameraStopRequest(Event):
    """Requests the camera pipeline to gracefully shutdown."""
    reason: str = "Requested by system"

@dataclass
class CameraStarted(Event):
    """Broadcast when camera hardware is successfully bound and streaming."""
    resolution: tuple
    fps: int

@dataclass
class CameraStopped(Event):
    """Broadcast when camera hardware is successfully released."""
    reason: str

@dataclass
class CameraConfigurationUpdate(Event):
    """Requests a runtime change to camera parameters (if supported)."""
    resolution: Optional[tuple] = None
    fps: Optional[int] = None

# =============================================================================
# DATA / FRAME EVENTS
# =============================================================================

@dataclass
class FrameCaptured(Event):
    """Internal event denoting a raw frame successfully pulled from hardware."""
    frame_id: int
    timestamp_ms: int

@dataclass
class FrameDropped(Event):
    """Internal event denoting a frame was discarded (e.g. RingBuffer full)."""
    frame_id: int
    reason: str

@dataclass
class FrameAvailable(Event):
    """
    Public event syndicating a new frame to the rest of the cognitive layer.
    Subscribers (like AI/Navigation) consume this.
    """
    frame_id: int
    timestamp_ms: int
    frame_data: Any  # Numpy array (cv2 image)

# =============================================================================
# TELEMETRY EVENTS
# =============================================================================

@dataclass
class CameraStatisticsUpdated(Event):
    """Periodic telemetry containing FPS and drop rates."""
    current_fps: float
    total_frames: int
    dropped_frames: int

@dataclass
class CameraHealthUpdated(Event):
    """Periodic telemetry containing pipeline stability and hardware status."""
    is_connected: bool
    status_msg: str
