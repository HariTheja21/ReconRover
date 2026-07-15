import asyncio
from typing import Callable, Any

class LLMEngine:
    def __init__(self, registry, conv_manager, session_manager, token_manager,
                 safety_manager, response_gen, streaming_manager, stats, publish: Callable):
        self.registry = registry
        self.cm = conv_manager
        self.sm = session_manager
        self.tm = token_manager
        self.safety = safety_manager
        self.rg = response_gen
        self.stream = streaming_manager
        self.stats = stats
        self.publish = publish
        
    async def process_prompt(self, user_input: str) -> str:
        if not self.safety.validate_prompt(user_input):
            self.stats.errors_encountered += 1
            return "Error: Prompt failed safety validation."
            
        session_id = self.sm.get_session()
        self.publish("ReasoningStarted", {"session_id": session_id, "timestamp": asyncio.get_event_loop().time()})
        
        self.cm.add_user_message(user_input)
        history = self.tm.truncate_history(self.cm.get_history())
        
        response = await self.rg.generate(user_input, history)
        
        if not self.safety.validate_response(response):
            self.stats.errors_encountered += 1
            return "Error: Response failed safety validation."
            
        self.cm.add_assistant_message(response)
        self.publish("ReasoningCompleted", {"session_id": session_id, "result": response, "timestamp": asyncio.get_event_loop().time()})
        
        self.publish("ConversationUpdated", {
            "session_id": session_id, 
            "messages_count": len(self.cm.get_history()),
            "timestamp": asyncio.get_event_loop().time()
        })
        
        return response
