import asyncio
from typing import Callable, Any
from .behavior_nodes import NodeStatus

class TaskPlannerEngine:
    def __init__(self, behavior_executor, goal_manager, mission_manager, task_queue,
                 task_executor, task_monitor, failure_manager, recovery_planner,
                 plan_optimizer, stats, publish: Callable):
        self.be = behavior_executor
        self.gm = goal_manager
        self.mm = mission_manager
        self.tq = task_queue
        self.te = task_executor
        self.tm = task_monitor
        self.fm = failure_manager
        self.rp = recovery_planner
        self.po = plan_optimizer
        self.stats = stats
        self.publish = publish
        
    async def process_mission(self, goal: str, params: dict):
        m_id = self.mm.create_mission(goal, params)
        self.stats.missions_received += 1
        
        # Stub: Decompose mission into tasks
        tasks = [{"id": "t1", "type": "NAVIGATE", "priority": 1}]
        tasks = self.po.optimize_tasks(tasks)
        
        self.mm.assign_tasks(m_id, [t["id"] for t in tasks])
        
        for t in tasks:
            t["mission_id"] = m_id
            self.tq.add_task(t)
            self.stats.tasks_created += 1
            self.publish("TaskCreated", {
                "task_id": t["id"],
                "mission_id": m_id,
                "task_type": t["type"],
                "timestamp": asyncio.get_event_loop().time()
            })
            
    async def process_task_loop(self):
        # This will be called by the scheduler
        task = self.tq.pop_task()
        if not task:
            return
            
        t_id = task["id"]
        self.te.start_task(task)
        self.publish("TaskStarted", {"task_id": t_id, "timestamp": asyncio.get_event_loop().time()})
        
        # Stub execution result
        status = NodeStatus.SUCCESS
        
        if status == NodeStatus.SUCCESS:
            self.te.complete_task()
            self.stats.tasks_completed += 1
            self.publish("TaskCompleted", {"task_id": t_id, "result": "SUCCESS", "timestamp": asyncio.get_event_loop().time()})
        else:
            self.stats.tasks_failed += 1
            self.fm.log_failure(t_id, "Execution Error")
            self.publish("TaskFailed", {"task_id": t_id, "reason": "Execution Error", "timestamp": asyncio.get_event_loop().time()})
            
            if self.fm.check_fatal(t_id):
                # Stub recovery
                self.stats.recoveries_attempted += 1
                rec_task = self.rp.plan_recovery(t_id, "Fatal Error")
                self.tq.add_task(rec_task)
