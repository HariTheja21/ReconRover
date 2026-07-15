"""
Command Encoder Module
Recon Rover V2 - Phase 4.2
"""
import threading

class CommandEncoder:
    """Encodes normalized [-1.0, 1.0] speeds into protocol integer bounds."""
    def __init__(self):
        self._lock = threading.RLock()
        # Assume protocol uses 16-bit signed ints for speed commands: -32767 to 32767
        self.MAX_INT = 32767
        
    def encode_speeds(self, left: float, right: float) -> tuple:
        with self._lock:
            # Map [-1.0, 1.0] to [-32767, 32767]
            enc_l = int(left * self.MAX_INT)
            enc_r = int(right * self.MAX_INT)
            
            # Final safety clamp
            enc_l = max(-self.MAX_INT, min(self.MAX_INT, enc_l))
            enc_r = max(-self.MAX_INT, min(self.MAX_INT, enc_r))
            
            return enc_l, enc_r
