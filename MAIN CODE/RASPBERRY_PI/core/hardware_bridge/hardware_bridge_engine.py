"""
Hardware Bridge Engine Module
Recon Rover V2 - Phase 4.2
"""
import threading
from typing import Tuple, Optional
from .hardware_bridge_state import HardwareBridgeState
from .packet_validator import PacketValidator
from .command_encoder import CommandEncoder
from .packet_builder import PacketBuilder

class HardwareBridgeEngine:
    """Core translation from wheel speeds to binary protocol packets."""
    def __init__(self, stats):
        self._lock = threading.RLock()
        self.stats = stats
        self.state = HardwareBridgeState()
        
        self.validator = PacketValidator()
        self.encoder = CommandEncoder()
        self.builder = PacketBuilder()
        
        self.sequence_number = 0
        
    def _next_seq(self) -> int:
        self.sequence_number = (self.sequence_number + 1) % 256
        return self.sequence_number
        
    def set_estop(self):
        self.state.set(HardwareBridgeState.ESTOP)
        
    def clear_estop(self):
        self.state.set(HardwareBridgeState.IDLE)
        
    def create_stop_packet(self) -> Tuple[int, bytes]:
        with self._lock:
            seq = self._next_seq()
            # Stop is just velocity 0,0
            enc_l, enc_r = self.encoder.encode_speeds(0.0, 0.0)
            packet = self.builder.build_velocity_packet(seq, enc_l, enc_r)
            self.stats.increment_encoded()
            return seq, packet
            
    def evaluate(self, left: float, right: float) -> Tuple[Optional[int], Optional[bytes]]:
        """
        Returns (seq_num, packet_bytes) if valid.
        """
        with self._lock:
            if self.state.get() == HardwareBridgeState.ESTOP:
                return None, None
                
            if not self.validator.is_valid(left, right):
                self.stats.increment_invalid()
                return None, None
                
            self.state.set(HardwareBridgeState.ACTIVE)
            
            enc_l, enc_r = self.encoder.encode_speeds(left, right)
            seq = self._next_seq()
            packet = self.builder.build_velocity_packet(seq, enc_l, enc_r)
            
            self.stats.increment_encoded()
            return seq, packet
