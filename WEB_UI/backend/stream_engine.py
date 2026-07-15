import asyncio
import time
from typing import Callable, Awaitable

from .frame_encoder import FrameEncoder
from .stream_session_manager import StreamSessionManager
from .stream_router import StreamRouter
from .stream_statistics import StreamStatistics
from .stream_health import StreamHealth
from .stream_events import FrameBroadcastEvent

class StreamEngine:
    def __init__(self, broadcast_callback: Callable[[bytes], Awaitable[None]]):
        self.stats = StreamStatistics()
        self.health = StreamHealth()
        self.encoder = FrameEncoder(self.stats)
        self.sessions = StreamSessionManager()
        self.router = StreamRouter(broadcast_callback)
        
        self.last_frame_time = time.time()
        self.frame_count = 0

    def add_viewer(self, client_id: str):
        self.sessions.add_viewer(client_id)
        self.stats.active_viewers = self.sessions.get_active_count()

    def remove_viewer(self, client_id: str):
        self.sessions.remove_viewer(client_id)
        self.stats.active_viewers = self.sessions.get_active_count()

    def set_quality(self, quality: int, resolution: tuple):
        self.encoder.set_quality(quality, resolution)

    async def process_raw_frame(self, frame):
        """
        Receives raw numpy frame from the EventBus (Camera Pipeline)
        """
        if not self.sessions.has_viewers():
            return # Don't burn CPU encoding if nobody is watching

        encoded_bytes = self.encoder.encode(frame)
        if encoded_bytes:
            event = FrameBroadcastEvent(
                frame_data=encoded_bytes,
                timestamp=time.time(),
                width=self.encoder.target_resolution[0],
                height=self.encoder.target_resolution[1],
                format='jpeg'
            )
            await self.router.route_frame(event)
            
            # Update FPS calculation
            self.frame_count += 1
            now = time.time()
            if now - self.last_frame_time >= 1.0:
                self.stats.current_fps = self.frame_count / (now - self.last_frame_time)
                self.frame_count = 0
                self.last_frame_time = now
