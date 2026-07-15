import asyncio
from typing import Callable, Awaitable
from .stream_events import FrameBroadcastEvent

class StreamRouter:
    def __init__(self, broadcast_callback: Callable[[bytes], Awaitable[None]]):
        self.broadcast = broadcast_callback

    async def route_frame(self, frame_event: FrameBroadcastEvent):
        # The broadcast_callback represents pushing data down the websocket to all connected clients
        await self.broadcast(frame_event.frame_data)
