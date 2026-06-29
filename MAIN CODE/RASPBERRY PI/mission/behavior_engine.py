"""
behavior_engine.py
Recon Rover V1 - Behavior Engine

Core module executing the behavior trees based on the active mission.
"""

import asyncio
from system.lifecycle_manager import BaseModule
from event_bus import (
    EventBus, MissionStarted, MissionCompleted, MissionFailed, MissionCancelled,
    MovementRequestEvent, CameraRequestEvent, ExpressionRequestEvent, BehaviorStateChanged,
    ObstacleAppeared
)
from logger import Logger
from .state_machine import BehaviorStateMachine, RobotBehaviorState
from .recovery_manager import RecoveryManager
from .mission_factory import MissionFactory
from .behavior_tree import NodeStatus

class BehaviorEngine(BaseModule):
    def __init__(self, event_bus: EventBus):
        super().__init__()
        self.event_bus = event_bus
        self.state_machine = BehaviorStateMachine()
        self.recovery = RecoveryManager(self.event_bus)
        self.factory = MissionFactory(self.event_bus, self.state_machine)
        
        self.active_tree = None
        self.active_mission_id = None
        self._running = False
        self._task = None
        self._last_state = None

    async def initialize(self):
        # Listen for mission lifecycle changes
        self.event_bus.subscribe(MissionStarted, self._on_mission_started)
        self.event_bus.subscribe(MissionCompleted, self._on_mission_ended)
        self.event_bus.subscribe(MissionFailed, self._on_mission_ended)
        self.event_bus.subscribe(MissionCancelled, self._on_mission_ended)
        
        # Listen for environmental events
        self.event_bus.subscribe(ObstacleAppeared, self._on_obstacle)
        
        self.log.info("BehaviorEngine initialized.")

    async def start(self):
        self._running = True
        self._task = asyncio.create_task(self._engine_loop())
        self.log.info("BehaviorEngine started.")

    async def stop(self):
        self._running = False
        if self._task:
            self._task.cancel()
        self.log.info("BehaviorEngine stopped.")

    # --- Event Handlers ---
    async def _on_mission_started(self, event: MissionStarted):
        self.log.info(f"Received new mission: {event.mission_type} [ID: {event.mission_id}]")
        self.active_mission_id = event.mission_id
        # Build the behavior tree corresponding to this mission
        self.active_tree = self.factory.build_tree(event.mission_type)

    async def _on_mission_ended(self, event):
        if hasattr(event, 'mission_id') and event.mission_id == self.active_mission_id:
            self.log.info(f"Active mission ended: {type(event).__name__}")
            self.active_tree = None
            self.active_mission_id = None
            self.state_machine.set_state(RobotBehaviorState.IDLE)

    async def _on_obstacle(self, event: ObstacleAppeared):
        # E.g. Set an internal flag the condition nodes can read, or forcibly inject an AVOIDING state
        self.log.info("Obstacle detected by Behavior Engine.")

    # --- Core Loop ---
    async def _engine_loop(self):
        while self._running:
            try:
                # 1. Execute behavior tree if active
                if self.active_tree:
                    status = self.active_tree.tick()
                    if status == NodeStatus.SUCCESS:
                        self.log.info("Behavior Tree completed successfully.")
                        self.event_bus.publish(MissionCompleted(mission_id=self.active_mission_id))
                        self.active_tree = None
                    elif status == NodeStatus.FAILURE:
                        self.log.warning("Behavior Tree failed.")
                        self.event_bus.publish(MissionFailed(mission_id=self.active_mission_id, reason="Tree Failure"))
                        self.active_tree = None

                # 2. Monitor recovery
                is_stuck = (self.state_machine.current_state == RobotBehaviorState.AVOIDING)
                self.recovery.tick(is_stuck)

                # 3. Publish state changes
                if self._last_state != self.state_machine.current_state:
                    self.event_bus.publish(BehaviorStateChanged(state=self.state_machine.current_state.name))
                    self._last_state = self.state_machine.current_state

                # Typical tick rate for a behavior tree is around 10Hz
                await asyncio.sleep(0.1)
                
            except asyncio.CancelledError:
                break
            except Exception as e:
                self.log.error(f"BehaviorEngine loop error: {e}")
                await asyncio.sleep(1.0)
