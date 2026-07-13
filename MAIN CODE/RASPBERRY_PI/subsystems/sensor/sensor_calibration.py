"""
sensor_calibration.py
Recon Rover V1 - Sensor Fusion Layer

Loads, stores, and applies static offsets to raw telemetry.
"""

from dataclasses import dataclass
from typing import Dict

@dataclass
class CalibrationOffsets:
    imu_pitch_offset: float = 0.0
    imu_roll_offset: float = 0.0
    imu_yaw_offset: float = 0.0
    mq2_baseline: float = 0.0
    ina219_current_offset: float = 0.0
    servo_pan_offset: float = 0.0
    servo_tilt_offset: float = 0.0

class SensorCalibration:
    def __init__(self):
        # In the future, this will load from a YAML config file.
        # Hardcoding defaults for now.
        self.offsets = CalibrationOffsets(
            imu_pitch_offset=0.0,
            imu_roll_offset=0.0,
            imu_yaw_offset=0.0,
            mq2_baseline=0.0,
            ina219_current_offset=0.0,
            servo_pan_offset=0.0,
            servo_tilt_offset=0.0
        )

    def apply_imu(self, pitch: float, roll: float, yaw: float) -> tuple[float, float, float]:
        return (
            pitch - self.offsets.imu_pitch_offset,
            roll - self.offsets.imu_roll_offset,
            yaw - self.offsets.imu_yaw_offset
        )

    def apply_gas(self, raw_gas: float) -> float:
        return max(0.0, raw_gas - self.offsets.mq2_baseline)

    def apply_power(self, raw_current: float) -> float:
        return raw_current - self.offsets.ina219_current_offset
