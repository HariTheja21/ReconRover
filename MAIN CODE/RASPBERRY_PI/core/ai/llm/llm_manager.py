import asyncio
from typing import Any
from .llm_health import LLMHealth
from .llm_statistics import LLMStatistics
from .llm_bridge import LLMBridge
from .model_registry import ModelRegistry
from .conversation_manager import ConversationManager
from .context_builder import ContextBuilder
from .memory_retriever import MemoryRetriever
from .prompt_builder import PromptBuilder
from .tool_executor import ToolExecutor
from .agent_orchestrator import AgentOrchestrator
from .reasoning_engine import ReasoningEngine
from .response_generator import ResponseGenerator
from .streaming_manager import StreamingManager
from .token_manager import TokenManager
from .session_manager import SessionManager
from .safety_manager import SafetyManager
from .llm_engine import LLMEngine
from .llm_scheduler import LLMScheduler

class LLMManager:
    def __init__(self, event_bus: Any):
        self.health = LLMHealth()
        self.stats = LLMStatistics()
        self.bridge = LLMBridge(event_bus)
        
        # Core
        self.registry = ModelRegistry()
        self.cm = ConversationManager()
        self.sm = SessionManager()
        self.tm = TokenManager()
        self.safety = SafetyManager()
        
        # Builders & Executors
        self.cb = ContextBuilder()
        self.mr = MemoryRetriever()
        self.pb = PromptBuilder(self.cb, self.mr)
        self.te = ToolExecutor()
        self.orch = AgentOrchestrator(self.bridge.publish_event)
        
        # Engines
        self.reasoning = ReasoningEngine(self.registry, self.pb, self.te, self.orch, self.stats)
        self.rg = ResponseGenerator(self.reasoning)
        self.stream = StreamingManager()
        
        self.engine = LLMEngine(
            self.registry, self.cm, self.sm, self.tm, self.safety,
            self.rg, self.stream, self.stats, self.bridge.publish_event
        )
        
        self.scheduler = LLMScheduler(self.engine)
        
    async def start(self):
        asyncio.create_task(self.scheduler.run_llm_loop())
