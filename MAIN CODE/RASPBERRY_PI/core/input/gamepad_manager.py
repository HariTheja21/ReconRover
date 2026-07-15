"""
Gamepad Manager Module
Recon Rover V2 - Phase 2.6

Provides an abstraction over OS-level generic USB HID controllers (e.g. pygame.joystick).
Designed to degrade gracefully if no controller is present.
"""

from typing import Callable, Any

class GamepadManager:
    """Interfaces with OS gamepad drivers and emits basic callback events."""
    
    def __init__(self):
        self.is_connected = False
        self.device_name = "None"
        
        self.on_axis_moved: Callable[[int, float], None] = lambda axis, val: None
        self.on_button_pressed: Callable[[int], None] = lambda btn: None
        self.on_button_released: Callable[[int], None] = lambda btn: None

    def connect(self) -> bool:
        """
        Attempts to bind to the first available USB controller.
        In a real deployment, this might init pygame.joystick.
        Returns True if a device is captured.
        """
        # We simulate no hardware by default, avoiding hardware dependency crashes
        self.is_connected = False
        return self.is_connected

    def poll(self):
        """
        Reads OS event queues and fires callbacks.
        In a real deployment, this would be a loop calling pygame.event.get().
        """
        if not self.is_connected:
            return
        pass

    # --- Methods for injecting mock data during internal testing ---
    def mock_axis(self, axis_id: int, value: float):
        self.on_axis_moved(axis_id, value)
        
    def mock_button(self, button_id: int):
        self.on_button_pressed(button_id)
        # Assuming an instant release for simple test
        self.on_button_released(button_id)
