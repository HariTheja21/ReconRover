import asyncio
from typing import Any
from .ai_health import AIHealth
from .ai_statistics import AIStatistics
from .ai_bridge import AIBridge
from .memory_manager import MemoryManager
from .gpu_resource_manager import GPUResourceManager
from .model_registry import ModelRegistry
from .model_manager import ModelManager
from .inference_scheduler import InferenceScheduler
from .context_manager import ContextManager
from .conversation_manager import ConversationManager
from .prompt_manager import PromptManager
from .tool_registry import ToolRegistry
from .tool_executor import ToolExecutor
from .reasoning_engine import ReasoningEngine

class AIManager:
    def __init__(self, event_bus: Any):
        self.health = AIHealth()
        self.stats = AIStatistics()
        self.bridge = AIBridge(event_bus)
        
        # Resource Layer
        self.memory = MemoryManager(max_memory_mb=4096)
        self.gpu = GPUResourceManager()
        
        # Model Layer
        self.model_registry = ModelRegistry()
        self.model_manager = ModelManager(self.model_registry, self.memory, self.gpu, self.stats, self.bridge.publish_event)
        self.scheduler = InferenceScheduler(self.stats, self.bridge.publish_event)
        
        # Context Layer
        self.context = ContextManager()
        self.conversation = ConversationManager()
        self.prompt = PromptManager(self.context, self.conversation)
        
        # Tool Layer
        self.tool_registry = ToolRegistry()
        self.tool_executor = ToolExecutor(self.tool_registry, self.stats, self.bridge.publish_event)
        
        # Reasoning Layer
        self.reasoning = ReasoningEngine(self.prompt, self.scheduler, self.tool_executor, self.tool_registry)
        
    async def start(self):
        # Start async background tasks like the scheduler loop
        asyncio.create_task(self.scheduler.process_queue())
