"""
telemetry_validator.py
Recon Rover V1 - Hardware Interface

Validates incoming packet data sanity before publishing.
"""

class TelemetryValidator:
    def validate(self, packet_data: dict) -> bool:
        """
        Returns True if the packet conforms to basic physical reality.
        (e.g., ultrasonic values can't be negative).
        """
        # Example validation rule for ultrasonic
        if "ultrasonic" in packet_data:
            if packet_data["ultrasonic"] < 0:
                return False
                
        # Example validation rule for battery
        if "battery" in packet_data:
            if packet_data["battery"] < 0 or packet_data["battery"] > 100:
                return False
                
        return True
