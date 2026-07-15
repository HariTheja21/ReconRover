"""
Packet Sender Module
Recon Rover V2 - Phase 4.3
"""
import queue
import threading

class PacketSender:
    """Thread-safe outgoing packet queue."""
    def __init__(self, max_size=100):
        self._queue = queue.Queue(maxsize=max_size)
        self._lock = threading.RLock()
        
    def queue_packet(self, data: bytes, force_front=False):
        """Adds packet to queue. Drops oldest if full."""
        with self._lock:
            if self._queue.full():
                try:
                    self._queue.get_nowait() # Drop oldest
                except queue.Empty:
                    pass
            
            # Python queue doesn't have prepend. 
            # If force_front is True, we rebuild the queue.
            if force_front:
                items = []
                while not self._queue.empty():
                    items.append(self._queue.get_nowait())
                self._queue.put_nowait(data)
                for item in items:
                    if not self._queue.full():
                        self._queue.put_nowait(item)
            else:
                self._queue.put_nowait(data)
                
    def get_next(self) -> bytes:
        try:
            return self._queue.get_nowait()
        except queue.Empty:
            return None
            
    def clear(self):
        with self._lock:
            while not self._queue.empty():
                try:
                    self._queue.get_nowait()
                except queue.Empty:
                    break
