class AgentMetrics:
    def __init__(self, stats, publish):
        self.stats = stats
        self.publish = publish
        
    def record_task(self, success: bool, latency: float):
        if success:
            self.stats.tasks_completed += 1
        else:
            self.stats.tasks_failed += 1
        
        self.publish("AgentStatisticsUpdated", {
            "active_agents": self.stats.active_agents,
            "tasks_completed": self.stats.tasks_completed,
            "avg_latency_ms": latency,
            "timestamp": 0.0
        })
