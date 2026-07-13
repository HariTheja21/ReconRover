"""
telemetry_receiver.py
Recon Rover V1 - Hardware Interface

Receives raw packets, parses them, validates them, and pushes them to the EventBus.
"""

import json
from event_bus import EventBus, TelemetryReceived, SensorStateUpdated
from .telemetry_validator import TelemetryValidator
from .telemetry_cache import TelemetryCache

class TelemetryReceiver:
    def __init__(self, event_bus: EventBus):
        self.event_bus = event_bus
        self.validator = TelemetryValidator()
        self.cache = TelemetryCache()
        
    def process_raw_packet(self, raw_bytes: bytes):
        """Deserializes and validates raw bytes into EventBus events."""
        try:
            # We assume JSON framing for now as defined by the protocol
            text = raw_bytes.decode('utf-8').strip()
            if not text:
                return
                
            data = json.loads(text)
            
            # 1. Broad Telemetry event
            self.event_bus.publish(TelemetryReceived(raw_data=text))
            
            # 2. Validation
            if not self.validator.validate(data):
                return
                
            # 3. Deduplication and Sensor Events
            if data.get("type") == "sensor":
                # E.g., data = {"type": "sensor", "sensor": "ultrasonic", "value": 45}
                sensor_id = data.get("sensor")
                value = data.get("value")
                
                if sensor_id and value is not None:
                    if self.cache.has_changed(sensor_id, value, tolerance=2.0):
                        self.event_bus.publish(SensorStateUpdated(
                            sensor_id=sensor_id,
                            state=value
                        ))
                        
        except json.JSONDecodeError:
            pass # Invalid JSON frame, drop it.
        except Exception:
            pass
