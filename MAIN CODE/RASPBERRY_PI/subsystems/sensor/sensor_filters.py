"""
sensor_filters.py
Recon Rover V1 - Sensor Fusion Layer

Lightweight, non-blocking filters for telemetry noise reduction.
"""

import collections
import statistics

class MovingAverage:
    def __init__(self, window_size: int = 5):
        self.window = collections.deque(maxlen=window_size)

    def update(self, value: float) -> float:
        self.window.append(value)
        return sum(self.window) / len(self.window)

class ExponentialMovingAverage:
    def __init__(self, alpha: float = 0.2):
        self.alpha = alpha
        self.value = None

    def update(self, new_value: float) -> float:
        if self.value is None:
            self.value = new_value
        else:
            self.value = (self.alpha * new_value) + ((1.0 - self.alpha) * self.value)
        return self.value

class MedianFilter:
    def __init__(self, window_size: int = 3):
        self.window = collections.deque(maxlen=window_size)

    def update(self, value: float) -> float:
        self.window.append(value)
        return statistics.median(self.window)

class SensorFilters:
    """Container for all active filters used by the Fusion Engine."""
    def __init__(self):
        self.battery_voltage = MovingAverage(window_size=10)
        self.battery_current = MovingAverage(window_size=10)
        self.imu_pitch = ExponentialMovingAverage(alpha=0.3)
        self.imu_roll = ExponentialMovingAverage(alpha=0.3)
        self.imu_yaw = ExponentialMovingAverage(alpha=0.3)
        self.front_ultrasonic = MedianFilter(window_size=3)
        self.left_ultrasonic = MedianFilter(window_size=3)
        self.right_ultrasonic = MedianFilter(window_size=3)
        self.rear_ultrasonic = MedianFilter(window_size=3)
        self.front_tof = MedianFilter(window_size=3)
