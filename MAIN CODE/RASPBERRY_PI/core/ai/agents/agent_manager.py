import asyncio
from typing import Any
from .agent_health import AgentHealth
from .agent_statistics import AgentStatistics
from .agent_bridge import AgentBridge
from .agent_registry import AgentRegistry
from .blackboard import Blackboard
from .shared_context import SharedContext
from .message_bus import MessageBus
from .priority_resolver import PriorityResolver
from .conflict_resolver import ConflictResolver
from .task_dispatcher import TaskDispatcher
from .coordination_engine import CoordinationEngine
from .agent_scheduler import AgentScheduler

# Agents
from .vision_agent import VisionAgent, SpeechAgent, NavigationAgent, ExplorationAgent, MemoryAgent, PlannerAgent, DiagnosticsAgent

class AgentManager:
    def __init__(self, event_bus: Any):
        self.health = AgentHealth()
        self.stats = AgentStatistics()
        self.bridge = AgentBridge(event_bus)
        
        # Core Infrastructure
        self.registry = AgentRegistry()
        self.bb = Blackboard()
        self.ctx = SharedContext()
        self.msg_bus = MessageBus(self.registry)
        
        # Resolvers & Dispatchers
        self.priority_res = PriorityResolver()
        self.conflict_res = ConflictResolver(self.bridge.publish_event)
        self.task_disp = TaskDispatcher(self.msg_bus)
        
        # Engine
        self.engine = CoordinationEngine(
            self.registry, self.bb, self.ctx, self.msg_bus,
            self.conflict_res, self.priority_res, self.task_disp,
            self.stats, self.bridge.publish_event
        )
        
        self.scheduler = AgentScheduler(self.engine, self.registry)
        
    def register_default_agents(self):
        self.registry.register(VisionAgent())
        self.registry.register(SpeechAgent())
        self.registry.register(NavigationAgent())
        self.registry.register(ExplorationAgent())
        self.registry.register(MemoryAgent())
        self.registry.register(PlannerAgent())
        self.registry.register(DiagnosticsAgent())
        
    async def start(self):
        self.register_default_agents()
        asyncio.create_task(self.scheduler.run_coordination_loop())
        # Not awaiting gather here to prevent blocking
        asyncio.create_task(self.scheduler.run_agent_loops())
