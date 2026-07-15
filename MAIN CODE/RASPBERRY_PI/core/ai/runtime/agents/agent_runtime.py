from typing import Any
import asyncio

from .agent_events import AgentExecutionStarted, AgentExecutionCompleted, BlackboardUpdated
from .agent_bridge import AgentBridge
from .agent_health import AgentHealth
from .agent_statistics import AgentStatistics
from .agent_metrics import AgentMetrics

from .agent_registry import AgentRegistry
from .agent_mailbox import AgentMailbox
from .blackboard_runtime import BlackboardRuntime
from .shared_context_runtime import SharedContextRuntime
from .conflict_manager import ConflictManager
from .consensus_manager import ConsensusManager
from .coordination_manager import CoordinationManager

from .agent_executor import AgentExecutor
from .agent_dispatcher import AgentDispatcher
from .agent_queue import AgentQueue
from .agent_supervisor import AgentSupervisor
from .agent_manager import AgentManager
from .agent_scheduler import AgentScheduler

from .providers.planner_agent import PlannerAgent
from .providers.vision_agent import VisionAgent
from .providers.speech_agent import SpeechAgent
from .providers.memory_agent import MemoryAgent
from .providers.navigation_agent import NavigationAgent
from .providers.exploration_agent import ExplorationAgent
from .providers.diagnostics_agent import DiagnosticsAgent

class AgentRuntime:
    def __init__(self, event_bus: Any):
        self.bridge = AgentBridge(event_bus)
        self.health = AgentHealth()
        self.stats = AgentStatistics()
        self.metrics = AgentMetrics(self.stats, self.bridge.publish_event)
        
        self.registry = AgentRegistry()
        self.mailbox = AgentMailbox()
        self.blackboard = BlackboardRuntime(self.bridge.publish_event)
        self.shared_context = SharedContextRuntime(self.blackboard)
        
        self.conflict = ConflictManager(self.bridge.publish_event)
        self.consensus = ConsensusManager(self.bridge.publish_event)
        self.coordinator = CoordinationManager(self.conflict, self.consensus)
        
        self.executor = AgentExecutor(self.metrics, self.bridge.publish_event)
        self.dispatcher = AgentDispatcher(self.registry, self.executor, self.mailbox)
        self.queue = AgentQueue()
        self.supervisor = AgentSupervisor(self.health, self.bridge.publish_event)
        
        self.manager = AgentManager(self.registry, self.mailbox, self.blackboard)
        self.scheduler = AgentScheduler(self.queue, self.dispatcher)
        
    async def initialize(self):
        agents = [
            PlannerAgent(), VisionAgent(), SpeechAgent(), 
            MemoryAgent(), NavigationAgent(), ExplorationAgent(), DiagnosticsAgent()
        ]
        self.manager.register_agents(agents)
        return True
