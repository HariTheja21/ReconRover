"""
world_model.py
Recon Rover V1 - Cognitive Layer

Core orchestrator for the World Model. Consumes fused sensor data and 
maintains the abstract cognitive representation of the rover's environment.
"""

from lifecycle_manager import BaseModule
from event_bus import (
    EventBus, SensorStateUpdated, WorldStateUpdated,
    ObstacleAppeared, ObstacleCleared,
    HazardDetected, HazardCleared, BatteryCritical
)
from world.world_state import WorldState
from world.spatial_memory import SpatialMemory
from world.environment_model import EnvironmentModel
from world.world_health import WorldHealth
from world.threat_analyzer import ThreatAnalyzer
from world.object_models import CellState

class WorldModel(BaseModule):
    """
    Subscribes to SensorFusion output to maintain a purely passive abstract world.
    """
    def __init__(self, event_bus: EventBus):
        super().__init__()
        self.event_bus = event_bus
        
        self.state = WorldState()
        self.spatial = SpatialMemory(obstacle_threshold_cm=30.0, free_threshold_cm=50.0)
        self.environment = EnvironmentModel()
        self.health = WorldHealth(critical_battery_pct=10.0)
        self.threat_analyzer = ThreatAnalyzer(critical_distance_cm=15.0)

    async def initialize(self):
        self.event_bus.subscribe(SensorStateUpdated, self._on_sensor_state)
        self.log.info("WorldModel initialized.")

    async def start(self):
        self.log.info("WorldModel started.")

    async def stop(self):
        self.log.info("WorldModel stopped.")

    def health(self) -> str:
        return "OK" if self.state.confidence > 0.3 else "LOW_CONFIDENCE"

    async def _on_sensor_state(self, event: SensorStateUpdated):
        fused = event.state
        self.state.timestamp_ms = fused.timestamp_ms
        
        # 1. Update Pose
        self.state.pose.pitch = fused.imu.pitch
        self.state.pose.roll = fused.imu.roll
        self.state.pose.yaw = fused.imu.yaw
        
        # 2. Update Spatial Memory
        # Extract fused obstacle map
        old_grid_states = {k: v.state for k, v in self.state.spatial_grid.items()}
        
        # For simplicity, prefer ToF over ultrasonic for front if available and valid
        front_dist = fused.obstacle_map.front_tof if fused.obstacle_map.front_tof > 0 else fused.obstacle_map.front_ultrasonic
        left_dist = fused.obstacle_map.left_ultrasonic
        right_dist = fused.obstacle_map.right_ultrasonic
        rear_dist = fused.obstacle_map.rear_ultrasonic
        
        new_obstacles = self.spatial.update(
            self.state, 
            front_dist, left_dist, right_dist, rear_dist, 
            fused.confidence_score, fused.timestamp_ms
        )
        
        # Broadcast Appeared/Cleared
        for direction, cell in self.state.spatial_grid.items():
            if cell.state == CellState.OBSTACLED and old_grid_states[direction] != CellState.OBSTACLED:
                self.event_bus.publish(ObstacleAppeared(direction=direction))
            elif cell.state == CellState.FREE and old_grid_states[direction] == CellState.OBSTACLED:
                self.event_bus.publish(ObstacleCleared(direction=direction))

        # 3. Update Environment
        gas_changed = self.environment.update(
            self.state, 
            gas_detected=fused.environment.gas_detected, 
            gas_confidence=fused.environment.gas_confidence,
            timestamp_ms=fused.timestamp_ms
        )
        
        if gas_changed:
            has_gas = any(h.hazard_type == "gas" for h in self.state.active_hazards)
            if has_gas:
                self.event_bus.publish(HazardDetected(hazard_type="gas"))
            else:
                self.event_bus.publish(HazardCleared(hazard_type="gas"))

        # 4. Update Health & Confidence
        # Need to format fused battery as a dict or direct access. fused.battery is a BatteryState.
        battery_dict = {
            'percentage': fused.battery.percentage,
            'voltage': fused.battery.voltage
        }
        became_critical = self.health.update(self.state, battery_dict, fused.confidence_score)
        
        if became_critical:
            self.event_bus.publish(BatteryCritical())

        # 5. Analyze Threat Level
        old_threat = self.state.threat_level
        self.state.threat_level = self.threat_analyzer.evaluate(self.state)
        
        if old_threat != self.state.threat_level:
            self.log.info(f"Threat Level Changed: {old_threat} -> {self.state.threat_level}")

        # 6. Broadcast updated WorldState
        self.event_bus.publish(WorldStateUpdated(state=self.state))
