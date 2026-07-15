"""
Frame Buffer Module
Recon Rover V2 - Phase 2.7

Provides a bounded ring buffer for raw image frames to prevent memory overflow
during high capture rates or slow syndication.
"""

import collections
import threading
from typing import Tuple, Any, Optional

class FrameBuffer:
    """Thread-safe Ring Buffer for camera frames."""
    
    def __init__(self, max_size: int = 10):
        # Using deque with maxlen natively drops the oldest item when full
        self._buffer = collections.deque(maxlen=max_size)
        self._lock = threading.Lock()
        
    def push(self, frame_id: int, timestamp_ms: int, frame_data: Any) -> bool:
        """
        Pushes a frame to the buffer.
        Returns True if a frame was dropped to make room.
        """
        dropped = False
        with self._lock:
            if len(self._buffer) == self._buffer.maxlen:
                dropped = True
            self._buffer.append((frame_id, timestamp_ms, frame_data))
        return dropped

    def pop(self) -> Optional[Tuple[int, int, Any]]:
        """
        Pops the oldest frame from the buffer.
        Returns None if buffer is empty.
        """
        with self._lock:
            if not self._buffer:
                return None
            return self._buffer.popleft()
            
    def qsize(self) -> int:
        with self._lock:
            return len(self._buffer)
