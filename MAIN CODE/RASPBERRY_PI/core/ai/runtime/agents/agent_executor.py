class AgentExecutor:
    def __init__(self, metrics, publish):
        self.metrics = metrics
        self.publish = publish
        
    async def execute(self, agent, task: dict) -> dict:
        self.publish("AgentExecutionStarted", {
            "agent_id": agent.agent_id,
            "task_id": task.get("id", "unknown"),
            "timestamp": 0.0
        })
        
        try:
            result = await agent.process_task(task)
            self.metrics.record_task(True, 10.0)
            self.publish("AgentExecutionCompleted", {
                "agent_id": agent.agent_id,
                "task_id": task.get("id", "unknown"),
                "result": result,
                "latency_ms": 10.0,
                "timestamp": 0.0
            })
            return result
        except Exception as e:
            self.metrics.record_task(False, 10.0)
            return {"status": "error", "message": str(e)}
