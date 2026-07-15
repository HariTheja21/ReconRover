import asyncio

class LLMScheduler:
    def __init__(self, failover, session_manager, response_parser, publish):
        self.failover = failover
        self.session_manager = session_manager
        self.parser = response_parser
        self.publish = publish
        self.request_queue = asyncio.Queue()
        
    async def submit_request(self, prompt: str, session_id: str, provider: str = "openai"):
        await self.request_queue.put((prompt, session_id, provider))
        
    async def run_loop(self):
        while True:
            prompt, session_id, provider_name = await self.request_queue.get()
            
            # Simple synchronous failover generation for now
            raw_text, used_provider = await self.failover.execute_with_failover(prompt, provider_name)
            
            if raw_text:
                text = self.parser.parse(raw_text)
                self.session_manager.append_context(session_id, {"role": "assistant", "content": text})
                
                self.publish("LLMResponseReceived", {
                    "text": text,
                    "provider": used_provider,
                    "model": "default",
                    "latency_ms": 150.0,
                    "timestamp": 0.0
                })
            
            self.request_queue.task_done()
