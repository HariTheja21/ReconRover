import json
import os
from typing import Dict

class DeviceMapper:
    def __init__(self):
        self.rules_path = "/etc/udev/rules.d/99-recon-rover.rules"

    def generate_udev_rules(self) -> str:
        # Template for static udev rules
        rules = [
            'SUBSYSTEM=="tty", ATTRS{idVendor}=="10c4", ATTRS{idProduct}=="ea60", SYMLINK+="esp32"',
            'SUBSYSTEM=="video4linux", ATTRS{name}=="mmal service 16.1", SYMLINK+="camera"',
            'SUBSYSTEM=="tty", ATTRS{idVendor}=="10c4", ATTRS{idProduct}=="ea60", SYMLINK+="lidar"' # Example
        ]
        return "\n".join(rules)
    
    def simulate_mapping(self) -> Dict[str, str]:
        # During dev, simulate the resulting symlinks
        return {
            "esp32": "/dev/esp32",
            "camera": "/dev/camera",
            "lidar": "/dev/lidar"
        }
