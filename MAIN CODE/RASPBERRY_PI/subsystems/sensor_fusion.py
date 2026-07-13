"""
sensor_fusion.py
Recon Rover V1 - Cognitive Layer

Integrates ESP32 telemetry into the world model.
Acts as the single source of truth for the physical state of the rover.
"""

import time
from lifecycle_manager import BaseModule
from event_bus import (
    EventBus, TelemetryReceived, SensorStateUpdated, 
    ObstacleDetected, BatteryLow, GasDetected
)
from sensor.sensor_models import WorldSensorState
from sensor.sensor_filters import SensorFilters
from sensor.sensor_calibration import SensorCalibration
from sensor.sensor_health import SensorHealthMonitor

class SensorFusion(BaseModule):
    """
    Consumes raw telemetry, applies filters/calibration, handles conflicts, 
    and publishes a unified WorldSensorState at 20Hz.
    """
    def __init__(self, event_bus: EventBus):
        super().__init__()
        self.event_bus = event_bus
        self.state = WorldSensorState()
        self.filters = SensorFilters()
        self.calibration = SensorCalibration()
        self.health = SensorHealthMonitor(timeout_ms=1000)

    async def initialize(self):
        self.event_bus.subscribe(TelemetryReceived, self._on_telemetry)
        self.log.info("SensorFusion initialized.")

    async def start(self):
        self.log.info("SensorFusion started.")

    async def stop(self):
        self.log.info("SensorFusion stopped.")

    def health(self) -> str:
        # Evaluate module health based on internal state
        if not self.state.health.imu_ok and not self.state.health.tof_ok:
            return "DEGRADED_SENSORS"
        return "OK"

    async def _on_telemetry(self, event: TelemetryReceived):
        """Reacts to incoming raw telemetry, processes it, and publishes the fused state."""
        raw = event.data
        now = int(time.time() * 1000)
        self.state.timestamp_ms = now
        conflicts = 0

        # --- Process IMU ---
        if "imu" in raw:
            self.health.update_timestamp("imu", now)
            imu = raw["imu"]
            p, r, y = self.calibration.apply_imu(imu.get("p", 0.0), imu.get("r", 0.0), imu.get("y", 0.0))
            self.state.imu.pitch = self.filters.imu_pitch.update(p)
            self.state.imu.roll = self.filters.imu_roll.update(r)
            self.state.imu.yaw = self.filters.imu_yaw.update(y)
            self.state.imu.accel_x = imu.get("ax", 0.0)
            self.state.imu.accel_y = imu.get("ay", 0.0)
            self.state.imu.accel_z = imu.get("az", 0.0)

        # --- Process Obstacles (ToF & Ultrasonic) ---
        has_tof = "tof" in raw
        has_us = "us" in raw
        
        if has_tof:
            self.health.update_timestamp("tof", now)
            tof = raw["tof"]
            self.state.obstacle_map.front_tof = self.filters.front_tof.update(tof.get("f", -1.0))
            self.state.obstacle_map.front_scan_distance = tof.get("s", -1.0)
            
        if has_us:
            self.health.update_timestamp("ultrasonic", now)
            us = raw["us"]
            self.state.obstacle_map.front_ultrasonic = self.filters.front_ultrasonic.update(us.get("f", -1.0))
            self.state.obstacle_map.left_ultrasonic = self.filters.left_ultrasonic.update(us.get("l", -1.0))
            self.state.obstacle_map.right_ultrasonic = self.filters.right_ultrasonic.update(us.get("r", -1.0))
            self.state.obstacle_map.rear_ultrasonic = self.filters.rear_ultrasonic.update(us.get("b", -1.0))

        # Conflict Resolution (Front ToF vs Front Ultrasonic)
        # ToF has shorter range (~120cm) but higher accuracy. Ultrasonic has longer range (~400cm).
        if has_tof and has_us:
            f_tof = self.state.obstacle_map.front_tof
            f_us = self.state.obstacle_map.front_ultrasonic
            
            if 0 < f_tof < 100 and f_us > 150:
                # ToF sees something close, Ultrasonic misses it (e.g. soft material or small object)
                conflicts += 1
                self.log.debug(f"Sensor conflict: ToF={f_tof:.1f}, US={f_us:.1f}")

        # Publish specific threshold events
        if self.state.obstacle_map.front_tof > 0 and self.state.obstacle_map.front_tof < 30.0:
            self.event_bus.publish(ObstacleDetected(location="front", distance_cm=self.state.obstacle_map.front_tof))

        # --- Process Environment (Gas) ---
        if "gas" in raw:
            self.health.update_timestamp("gas", now)
            raw_gas = raw["gas"].get("v", 0.0)
            calibrated_gas = self.calibration.apply_gas(raw_gas)
            
            if calibrated_gas > 500.0: # Arbitrary threshold
                self.state.environment.gas_detected = True
                self.state.environment.gas_confidence = min(1.0, calibrated_gas / 1024.0)
                self.event_bus.publish(GasDetected(gas_level=calibrated_gas, confidence=self.state.environment.gas_confidence))
            else:
                self.state.environment.gas_detected = False

        # --- Process Battery (INA219) ---
        if "bat" in raw:
            self.health.update_timestamp("battery", now)
            bat = raw["bat"]
            v = self.filters.battery_voltage.update(bat.get("v", 0.0))
            c = self.filters.battery_current.update(self.calibration.apply_power(bat.get("c", 0.0)))
            
            # LiPo 3S approx mapping (10.5V to 12.6V)
            pct = max(0.0, min(100.0, (v - 10.5) / (12.6 - 10.5) * 100.0))
            
            self.state.battery.voltage = v
            self.state.battery.current = c
            self.state.battery.power = v * (c / 1000.0)
            self.state.battery.percentage = pct
            
            if pct < 15.0:
                self.event_bus.publish(BatteryLow(voltage=v, percentage=pct))

        # --- Finalize Health and Confidence ---
        self.state.health = self.health.evaluate_health(now)
        self.state.confidence_score = self.health.compute_confidence(conflicts)

        # Broadcast the unified state
        self.event_bus.publish(SensorStateUpdated(state=self.state))
