from typing import Any

from .tool_health import ToolHealth
from .tool_statistics import ToolStatistics
from .tool_bridge import ToolBridge

from .tool_registry import ToolRegistry
from .tool_validator import ToolValidator
from .tool_permissions import ToolPermissions
from .tool_context import ToolContext
from .tool_result import ToolResult
from .tool_serializer import ToolSerializer
from .tool_timeout import ToolTimeout
from .tool_retry import ToolRetry
from .tool_audit import ToolAudit

from .tool_executor import ToolExecutor
from .tool_dispatcher import ToolDispatcher
from .tool_manager import ToolManager
from .tool_scheduler import ToolScheduler

from .providers.system_tool import SystemTool
from .providers.navigation_tool import NavigationTool
from .providers.vision_tool import VisionTool
from .providers.speech_tool import SpeechTool
from .providers.memory_tool import MemoryTool
from .providers.diagnostics_tool import DiagnosticsTool

class ToolRuntime:
    def __init__(self, event_bus: Any):
        self.health = ToolHealth()
        self.stats = ToolStatistics()
        self.bridge = ToolBridge(event_bus)
        
        self.registry = ToolRegistry()
        self.validator = ToolValidator()
        self.permissions = ToolPermissions()
        self.context = ToolContext()
        self.serializer = ToolSerializer()
        self.timeout = ToolTimeout(default_timeout=10.0)
        self.retry = ToolRetry(max_retries=2)
        self.audit = ToolAudit()
        
        self.executor = ToolExecutor(
            validator=self.validator,
            permissions=self.permissions,
            timeout=self.timeout,
            retry=self.retry
        )
        
        self.dispatcher = ToolDispatcher(
            registry=self.registry,
            executor=self.executor,
            audit=self.audit,
            publish=self.bridge.publish_event
        )
        
        self.manager = ToolManager(self.registry, self.dispatcher, self.context)
        self.scheduler = ToolScheduler(self.dispatcher)
        
    async def initialize(self):
        default_tools = [
            SystemTool(),
            NavigationTool(),
            VisionTool(),
            SpeechTool(),
            MemoryTool(),
            DiagnosticsTool()
        ]
        self.manager.register_default_tools(default_tools)
        return True
