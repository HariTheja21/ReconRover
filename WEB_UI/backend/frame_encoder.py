import cv2
import time
from typing import Optional, Tuple
from .stream_statistics import StreamStatistics

class FrameEncoder:
    def __init__(self, stats: StreamStatistics):
        self.stats = stats
        self.quality = 80 # JPEG quality
        self.target_resolution = (640, 480)

    def set_quality(self, quality: int, resolution: Tuple[int, int]):
        self.quality = max(10, min(100, quality))
        self.target_resolution = resolution

    def encode(self, frame) -> Optional[bytes]:
        start = time.perf_counter()
        try:
            # Resize
            resized = cv2.resize(frame, self.target_resolution)
            
            # Encode
            encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), self.quality]
            result, encimg = cv2.imencode('.jpg', resized, encode_param)
            
            if not result:
                self.stats.frames_dropped += 1
                return None
                
            self.stats.frames_encoded += 1
            self.stats.encoding_latency_ms = (time.perf_counter() - start) * 1000
            
            byte_data = encimg.tobytes()
            self.stats.total_bytes_sent += len(byte_data)
            return byte_data
            
        except Exception:
            self.stats.frames_dropped += 1
            return None
