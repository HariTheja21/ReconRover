class ProviderFailover:
    def __init__(self, manager, publish):
        self.manager = manager
        self.publish = publish
        self.fallback_chain = ["openai", "gemini", "ollama"]
        
    async def execute_with_failover(self, prompt: str, initial_provider: str):
        current = initial_provider
        for provider_name in self.fallback_chain:
            try:
                if current != provider_name:
                    self.publish("ProviderChanged", {
                        "old_provider": current,
                        "new_provider": provider_name,
                        "reason": "Failover",
                        "timestamp": 0.0
                    })
                    current = provider_name
                    
                provider = await self.manager.activate(current)
                if not provider:
                    continue
                    
                result = await provider.generate(prompt)
                return result, current
            except Exception:
                continue
        return None, None
