"""
telemetry_cache.py
Recon Rover V1 - Hardware Interface

Maintains a constant-memory $O(1)$ cache to prevent EventBus flooding.
"""

class TelemetryCache:
    def __init__(self):
        # We only store the latest value for each sensor key
        self._cache = {}
        
    def has_changed(self, sensor_id: str, new_value: any, tolerance: float = 0.0) -> bool:
        """
        Returns True if the sensor value has changed beyond the tolerance limit.
        """
        old_value = self._cache.get(sensor_id)
        
        if old_value is None:
            self._cache[sensor_id] = new_value
            return True
            
        if isinstance(new_value, (int, float)) and isinstance(old_value, (int, float)):
            if abs(new_value - old_value) > tolerance:
                self._cache[sensor_id] = new_value
                return True
            return False
            
        if old_value != new_value:
            self._cache[sensor_id] = new_value
            return True
            
        return False
