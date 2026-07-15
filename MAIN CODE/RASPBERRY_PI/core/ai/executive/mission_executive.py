import asyncio
from typing import Callable, Any
import uuid

class MissionExecutive:
    def __init__(self, context, state_machine, obj_manager, supervisor,
                 monitor, coordinator, allocator, policy, priority, risk,
                 logger_mod, recovery, stats, publish: Callable):
        self.ctx = context
        self.sm = state_machine
        self.om = obj_manager
        self.sup = supervisor
        self.mon = monitor
        self.coord = coordinator
        self.alloc = allocator
        self.policy = policy
        self.prio = priority
        self.risk = risk
        self.logger = logger_mod
        self.recovery = recovery
        self.stats = stats
        self.publish = publish
        
    async def start_mission(self, params: dict):
        m_id = str(uuid.uuid4())
        self.ctx.init_mission(m_id, params)
        self.sm.transition("PLANNING")
        
        self.logger.log(m_id, "Mission Initialized")
        self.publish("MissionStarted", {"mission_id": m_id, "timestamp": asyncio.get_event_loop().time()})
        self.stats.missions_executed += 1
        
        # Validate resources & policy
        if not self.alloc.check_resources(params) or not self.policy.validate_action("START_MISSION"):
            self.sm.transition("FAILED")
            self.stats.missions_failed += 1
            self.publish("MissionFailed", {"mission_id": m_id, "reason": "Policy or Resource Failure", "timestamp": asyncio.get_event_loop().time()})
            return m_id
            
        self.sm.transition("EXECUTING")
        return m_id
        
    async def abort_mission(self):
        m_id = self.ctx.mission_id
        if m_id:
            self.sm.transition("FAILED")
            self.logger.log(m_id, "Mission Aborted")
            self.publish("MissionFailed", {"mission_id": m_id, "reason": "Aborted by User", "timestamp": asyncio.get_event_loop().time()})
            
    async def update_loop(self):
        state = self.sm.get_state()
        if state == "EXECUTING":
            if self.mon.monitor_anomalies():
                self.sm.transition("RECOVERING")
                self.recovery.trigger_recovery(self.ctx.mission_id)
                self.stats.recoveries_triggered += 1
