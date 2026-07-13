"""
mission_executor.py
Recon Rover V1 - Mission Manager

Handles lifecycle transitions and EventBus publishing.
"""

from logger import Logger
from event_bus import (
    EventBus, MissionStarted, MissionCompleted, MissionFailed,
    MissionCancelled, MissionTimedOut, MissionPaused, MissionResumed,
    MissionStatusUpdated, MissionOwnershipChanged, EmergencyMissionStarted
)
from .mission_context import MissionStore, MissionContext
from .mission_state import MissionStateMachine, MissionLifecycle
import time

class MissionExecutor:
    def __init__(self, store: MissionStore, state_machine: MissionStateMachine, event_bus: EventBus):
        self.store = store
        self.state_machine = state_machine
        self.event_bus = event_bus
        self.log = Logger.get("MissionExecutor")

    def execute_new_mission(self, new_mission: MissionContext):
        """Cancels any active mission and starts the new one."""
        if self.store.active_mission and not self.store.active_mission.is_terminal:
            self.cancel_mission("Preempted by higher priority mission")
            
        self.store.previous_mission = self.store.active_mission
        self.store.active_mission = new_mission
        self.state_machine._state = MissionLifecycle.CREATED # Reset state machine
        
        # Fast-forward to RUNNING
        self.state_machine.transition(MissionLifecycle.READY)
        self.state_machine.transition(MissionLifecycle.RUNNING)
        self.store.active_mission.state = MissionLifecycle.RUNNING
        self.store.active_mission.start_time_ms = int(time.time() * 1000)
        
        self.log.info(f"Started Mission: {new_mission.mission_type} [ID: {new_mission.mission_id}]")
        
        if new_mission.mission_type == "Emergency Stop":
            self.event_bus.publish(EmergencyMissionStarted(mission_id=new_mission.mission_id))
        else:
            self.event_bus.publish(MissionStarted(
                mission_id=new_mission.mission_id,
                mission_type=new_mission.mission_type,
                owner=new_mission.owner
            ))
            
        self.event_bus.publish(MissionOwnershipChanged(
            mission_id=new_mission.mission_id,
            new_owner=new_mission.owner
        ))

    def cancel_mission(self, reason: str = "Cancelled"):
        if self.store.active_mission and self.state_machine.transition(MissionLifecycle.CANCELLED):
            self.store.active_mission.state = MissionLifecycle.CANCELLED
            self.log.info(f"Cancelled Mission: {self.store.active_mission.mission_type}")
            self.event_bus.publish(MissionCancelled(
                mission_id=self.store.active_mission.mission_id,
                reason=reason
            ))

    def complete_mission(self):
        if self.store.active_mission and self.state_machine.transition(MissionLifecycle.COMPLETED):
            self.store.active_mission.state = MissionLifecycle.COMPLETED
            self.log.info(f"Completed Mission: {self.store.active_mission.mission_type}")
            self.event_bus.publish(MissionCompleted(
                mission_id=self.store.active_mission.mission_id
            ))

    def fail_mission(self, reason: str):
        if self.store.active_mission and self.state_machine.transition(MissionLifecycle.FAILED):
            self.store.active_mission.state = MissionLifecycle.FAILED
            self.log.info(f"Failed Mission: {self.store.active_mission.mission_type}. Reason: {reason}")
            self.event_bus.publish(MissionFailed(
                mission_id=self.store.active_mission.mission_id,
                reason=reason
            ))

    def check_timeouts(self):
        """Called periodically to enforce mission timeouts."""
        if self.store.active_mission and self.store.active_mission.state == MissionLifecycle.RUNNING:
            if self.store.active_mission.timeout_ms > 0:
                elapsed = int(time.time() * 1000) - self.store.active_mission.start_time_ms
                if elapsed > self.store.active_mission.timeout_ms:
                    if self.state_machine.transition(MissionLifecycle.TIMED_OUT):
                        self.store.active_mission.state = MissionLifecycle.TIMED_OUT
                        self.log.warning(f"Mission Timed Out: {self.store.active_mission.mission_type}")
                        self.event_bus.publish(MissionTimedOut(
                            mission_id=self.store.active_mission.mission_id
                        ))
