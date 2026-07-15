"""
Hardware Router Module
Recon Rover V2 - Phase 2.8

Parses `OutgoingCommandPacket` and routes to explicit hardware controllers.
"""

from typing import Any
from .motor_controller import MotorController
from .servo_controller import ServoController
from .oled_controller import OLEDController
from .rgb_controller import RGBController
from .buzzer_controller import BuzzerController

class HardwareRouter:
    """Routes semantic commands to specific hardware constraints."""
    
    def __init__(self, event_bus: Any):
        self._bus = event_bus
        self.motor = MotorController(self._bus)
        self.servo = ServoController(self._bus)
        self.oled = OLEDController(self._bus)
        self.rgb = RGBController(self._bus)
        self.buzzer = BuzzerController(self._bus)
        
        # We will parse command IDs from the shared protocol definitions
        # Assuming constants defined in previous phases (e.g. CommandConstants)
        
    def update_config(self, config: dict):
        """Cascades configuration updates to all sub-controllers."""
        self.motor.update_config(config)
        self.servo.update_config(config)
        self.rgb.update_config(config)
        
    def route_packet(self, command_type: int, binary_payload: bytes):
        """
        Parses payload bytes based on command_type and routes to the right controller.
        This uses struct unpacking which relies on Phase 2.5/Shared knowledge.
        """
        import struct
        
        # Based on typical command definitions (mocking the ID map for simplicity here,
        # but in production this pulls from Shared Definitions).
        
        if command_type == 0x10:  # CMD_MOTOR_DRIVE
            if len(binary_payload) >= 6:
                # Int16 left, Int16 right, UInt16 duration
                left, right, dur = struct.unpack('<hhH', binary_payload[:6])
                self.motor.route_command(left, right, dur)
                
        elif command_type == 0x20: # CMD_SERVO_MOVE
            if len(binary_payload) >= 3:
                # UInt8 id, UInt16 angle
                sid, ang = struct.unpack('<BH', binary_payload[:3])
                self.servo.route_command(sid, ang)
                
        elif command_type == 0x40: # CMD_OLED_WRITE
            # String payload
            try:
                text = binary_payload.decode('utf-8').strip('\x00')
                self.oled.route_command(lines=[text])
            except UnicodeDecodeError:
                pass
                
        elif command_type == 0x50: # CMD_RGB_SET
            if len(binary_payload) >= 4:
                # R, G, B, Brightness (all UInt8)
                r, g, b, bright = struct.unpack('<BBBB', binary_payload[:4])
                self.rgb.route_command(r, g, b, bright)
                
        elif command_type == 0x60: # CMD_BUZZER_TONE
            if len(binary_payload) >= 4:
                # UInt16 freq, UInt16 dur
                freq, dur = struct.unpack('<HH', binary_payload[:4])
                self.buzzer.route_command(freq, dur)
