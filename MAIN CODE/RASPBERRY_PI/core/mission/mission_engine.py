"""
Mission Engine Module
Recon Rover V2 - Phase 3.9
"""
import threading
import time
from typing import Any
from .mission_events import (MissionStarted, MissionCompleted, MissionFailed, MissionCancelled, 
                           TaskStarted, TaskCompleted, TaskFailed)
from .task_executor import TaskExecutor

class MissionEngine:
    """Manages the lifecycle of a single active mission."""
    def __init__(self, event_bus: Any, stats: Any):
        self._lock = threading.RLock()
        self.bus = event_bus
        self.stats = stats
        self.executor = TaskExecutor(self.bus)
        
        self.active_mission = None
        self.tasks = []
        self.current_task_index = 0
        self.state = "IDLE" # IDLE, RUNNING, PAUSED
        
    def load_mission(self, mission: dict):
        with self._lock:
            self.active_mission = mission
            self.tasks = mission.get('tasks', [])
            self.current_task_index = 0
            self.state = "IDLE"
            
    def start(self):
        with self._lock:
            if not self.active_mission or not self.tasks:
                return
            self.state = "RUNNING"
            now = time.time()
            mid = self.active_mission['mission_id']
            self.bus.publish(MissionStarted(timestamp=now, mission_id=mid))
            self._start_current_task()
            
    def pause(self):
        with self._lock:
            if self.state == "RUNNING":
                self.state = "PAUSED"
                
    def resume(self):
        with self._lock:
            if self.state == "PAUSED":
                self.state = "RUNNING"
                
    def abort(self, reason: str):
        with self._lock:
            if self.active_mission:
                now = time.time()
                mid = self.active_mission['mission_id']
                self.bus.publish(MissionFailed(timestamp=now, mission_id=mid, reason=reason))
                self.stats.increment_mission_failed()
                self._clear()
                
    def cancel(self):
        with self._lock:
            if self.active_mission:
                now = time.time()
                mid = self.active_mission['mission_id']
                self.bus.publish(MissionCancelled(timestamp=now, mission_id=mid))
                self._clear()
                
    def _clear(self):
        self.active_mission = None
        self.tasks = []
        self.current_task_index = 0
        self.state = "IDLE"
        self.executor.clear()
        
    def _start_current_task(self):
        if self.current_task_index < len(self.tasks):
            task_def = self.tasks[self.current_task_index]
            mid = self.active_mission['mission_id']
            
            if self.executor.start_task(task_def, mid, self.current_task_index):
                now = time.time()
                self.bus.publish(TaskStarted(timestamp=now, mission_id=mid, 
                                           task_index=self.current_task_index, 
                                           task_type=task_def['type']))
            else:
                self.abort(f"Failed to start task {self.current_task_index}")
        else:
            # Mission complete
            now = time.time()
            mid = self.active_mission['mission_id']
            self.bus.publish(MissionCompleted(timestamp=now, mission_id=mid))
            self.stats.increment_mission_completed()
            self._clear()
            
    def tick(self, context: Any):
        """Called periodically by the Manager to monitor task progress."""
        with self._lock:
            if self.state != "RUNNING" or not self.active_mission:
                return
                
            status = self.executor.tick(context)
            mid = self.active_mission['mission_id']
            now = time.time()
            
            if status == "COMPLETED":
                self.bus.publish(TaskCompleted(timestamp=now, mission_id=mid, task_index=self.current_task_index))
                self.stats.increment_task_completed()
                self.current_task_index += 1
                self._start_current_task()
            elif status == "FAILED":
                self.bus.publish(TaskFailed(timestamp=now, mission_id=mid, task_index=self.current_task_index, reason="Task execution failed"))
                self.abort(f"Task {self.current_task_index} failed")
