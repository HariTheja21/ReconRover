class ToolManager:
    def __init__(self, registry, dispatcher, context):
        self.registry = registry
        self.dispatcher = dispatcher
        self.context = context
        
    def register_default_tools(self, tools: list):
        for tool in tools:
            self.registry.register(tool)
