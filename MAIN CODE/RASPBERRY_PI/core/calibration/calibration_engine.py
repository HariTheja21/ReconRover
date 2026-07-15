import asyncio
import time
import json
import os
from typing import Callable, Dict

from .calibration_events import (
    CalibrationStartedEvent, DeviceMappedEvent, ComponentCalibratedEvent,
    CalibrationFailedEvent, CalibrationCompletedEvent
)
from .calibration_statistics import CalibrationStatistics
from .calibration_health import CalibrationHealth
from .device_mapper import DeviceMapper
from .serial_calibrator import SerialCalibrator
from .camera_calibrator import CameraCalibrator
from .imu_calibrator import ImuCalibrator
from .motor_calibrator import MotorCalibrator
from .servo_calibrator import ServoCalibrator
from .battery_calibrator import BatteryCalibrator
from .system_validator import SystemValidator

class CalibrationEngine:
    def __init__(self, publish_callback: Callable):
        self.publish = publish_callback
        self.stats = CalibrationStatistics()
        self.health = CalibrationHealth()
        self.mapper = DeviceMapper()
        self.validator = SystemValidator()
        self.profile = {}
        
        # Instantiate calibrators
        self.calibrators = {
            "serial": SerialCalibrator(),
            "camera": CameraCalibrator(),
            "imu": ImuCalibrator(),
            "motor": MotorCalibrator(),
            "servo": ServoCalibrator(),
            "battery": BatteryCalibrator()
        }

    async def execute_calibration(self) -> bool:
        start_time = time.time()
        self.publish("CalibrationStartedEvent", CalibrationStartedEvent(timestamp=start_time))

        # 1. Device Mapping (udev rules simulation)
        mappings = self.mapper.simulate_mapping()
        for logic_name, phys_path in mappings.items():
            self.publish("DeviceMappedEvent", DeviceMappedEvent(logic_name, phys_path))
            self.stats.devices_mapped += 1

        # 2. Component Calibration
        for name, calibrator in self.calibrators.items():
            try:
                result = await calibrator.calibrate()
                self.profile[name] = result
                self.publish("ComponentCalibratedEvent", ComponentCalibratedEvent(name, result))
                self.stats.calibrations_completed += 1
            except Exception as e:
                self.publish("CalibrationFailedEvent", CalibrationFailedEvent(name, str(e)))
                self.stats.calibrations_failed += 1
                self.health.mark_failure(f"Calibration of {name} failed: {e}")
                return False

        # 3. System Validation
        if self.validator.validate_profile(self.profile):
            self.health.mark_calibrated()
            
            # Save profile
            profile_path = "/tmp/recon_rover_calibration.json"
            with open(profile_path, "w") as f:
                json.dump(self.profile, f, indent=4)
                
            total_time_ms = int((time.time() - start_time) * 1000)
            self.stats.total_time_ms = total_time_ms
            self.publish("CalibrationCompletedEvent", CalibrationCompletedEvent(profile_path, total_time_ms))
            return True
        else:
            self.health.mark_failure("Final profile validation failed.")
            return False
