"""
Camera Manager Module
Recon Rover V2 - Phase 2.7

The master orchestrator for the local vision node.
Listens to Start/Stop requests, instantiates the pipeline, and oversees distribution.
"""

from typing import Any
from .vision_events import CameraStartRequest, CameraStopRequest, CameraStarted, CameraStopped
from .frame_buffer import FrameBuffer
from .camera_statistics import CameraStatistics
from .camera_health import CameraHealth
from .camera_pipeline import CameraPipeline
from .frame_distributor import FrameDistributor

class CameraManager:
    """Master node for the Vision subsystem."""
    
    def __init__(self, event_bus: Any):
        self._bus = event_bus
        self.stats = CameraStatistics()
        self.health = CameraHealth(self._bus, self.stats)
        
        # Keep ring buffer small to prevent memory leaks from stale frames
        self.buffer = FrameBuffer(max_size=10)
        self.distributor = FrameDistributor(self._bus, self.buffer)
        
        self.pipeline = None
        self._subscribe_events()
        
    def _subscribe_events(self):
        self._bus.subscribe(CameraStartRequest, self._handle_start_req)
        self._bus.subscribe(CameraStopRequest, self._handle_stop_req)
        
    async def _handle_start_req(self, event: CameraStartRequest):
        """Asynchronously starts the vision pipeline."""
        if self.pipeline and self.pipeline._running:
            return # Already running
            
        self.pipeline = CameraPipeline(
            event_bus=self._bus,
            frame_buffer=self.buffer,
            stats=self.stats,
            resolution=event.resolution,
            fps=event.fps
        )
        
        if self.pipeline.start():
            self.distributor.start()
            self.health.is_connected = True
            self.health.status_msg = "Streaming"
            self.health.start()
            
            self._bus.publish(CameraStarted(
                resolution=event.resolution,
                fps=event.fps
            ))
        else:
            self.health.is_connected = False
            self.health.status_msg = "Failed to open camera hardware"
            self._bus.publish(CameraStopped(reason="Hardware Failure"))
            
    async def _handle_stop_req(self, event: CameraStopRequest):
        """Asynchronously stops the vision pipeline."""
        if self.pipeline:
            self.pipeline.stop()
            self.pipeline = None
            
        self.distributor.stop()
        self.health.stop()
        self.health.is_connected = False
        self.health.status_msg = "Offline"
        
        self._bus.publish(CameraStopped(reason=event.reason))
