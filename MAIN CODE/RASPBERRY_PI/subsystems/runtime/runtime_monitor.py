"""
runtime_monitor.py
Recon Rover V1 - Full System Integration

Publishes system-wide health and statistics to the EventBus.
"""

import asyncio
from event_bus import EventBus, RuntimeStatisticsUpdated, SystemHealthUpdated
from .runtime_statistics import RuntimeStatistics
from .health_supervisor import HealthSupervisor

class RuntimeMonitor:
    def __init__(self, event_bus: EventBus, stats: RuntimeStatistics, supervisor: HealthSupervisor):
        self.event_bus = event_bus
        self.stats = stats
        self.supervisor = supervisor
        self._running = False
        self._task = None
        
    def start(self):
        self._running = True
        self._task = asyncio.create_task(self._monitor_loop())
        
    def stop(self):
        self._running = False
        if self._task:
            self._task.cancel()
            
    async def _monitor_loop(self):
        while self._running:
            # Publish stats
            self.event_bus.publish(RuntimeStatisticsUpdated(
                uptime=self.stats.get_uptime(),
                cpu_usage=self.stats.cpu_usage_estimate,
                ram_usage=self.stats.ram_usage_estimate,
                total_events=self.stats.events_processed
            ))
            
            # Determine global health (simplistic view: if any are FATAL, system is FATAL)
            global_health = "OK"
            for name, mod in self.supervisor.modules.items():
                st = mod.health()
                if st == "FATAL":
                    global_health = "FATAL"
                    break
                elif st.startswith("DEGRADED") and global_health != "FATAL":
                    global_health = "DEGRADED"
                    
            self.event_bus.publish(SystemHealthUpdated(status=global_health))
            
            await asyncio.sleep(5.0) # Publish every 5 seconds
