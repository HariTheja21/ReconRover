from typing import List, Dict

class BootSequence:
    def __init__(self):
        self.sequence: List[Dict[str, Any]] = [
            {"name": "Configuration", "deps": []},
            {"name": "Logger", "deps": []},
            {"name": "EventBus", "deps": []},
            {"name": "Runtime", "deps": ["EventBus"]},
            {"name": "Safety", "deps": ["EventBus", "Runtime"]},
            {"name": "Serial", "deps": ["EventBus", "Safety"]},
            {"name": "ESP32", "deps": ["Serial"]},
            {"name": "Telemetry", "deps": ["ESP32"]},
            {"name": "Sensors", "deps": ["EventBus"]},
            {"name": "Camera", "deps": ["EventBus"]},
            {"name": "Localization", "deps": ["Sensors", "Telemetry"]},
            {"name": "Mapping", "deps": ["Localization", "Camera"]},
            {"name": "SLAM", "deps": ["Mapping"]},
            {"name": "Navigation", "deps": ["SLAM"]},
            {"name": "Motion", "deps": ["Navigation", "Safety"]},
            {"name": "Mission", "deps": ["Motion"]},
        ]

    def get_sequence(self) -> List[Dict[str, Any]]:
        return self.sequence
