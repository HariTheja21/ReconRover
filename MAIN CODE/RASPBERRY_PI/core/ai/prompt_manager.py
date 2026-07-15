from typing import Dict, Any
from .context_manager import ContextManager
from .conversation_manager import ConversationManager

class PromptManager:
    def __init__(self, context_manager: ContextManager, conversation_manager: ConversationManager):
        self.context = context_manager
        self.conversation = conversation_manager
        
    def build_prompt(self, system_instruction: str, user_input: str) -> Dict[str, Any]:
        compiled_ctx = self.context.compile_context()
        ctx_str = f"System Context: {compiled_ctx['system']}\nMission Context: {compiled_ctx['mission']}\nVision Context: {compiled_ctx['vision']}"
        
        full_system = f"{system_instruction}\n\nCURRENT STATE:\n{ctx_str}"
        
        messages = [{"role": "system", "content": full_system}]
        messages.extend(self.conversation.get_history())
        messages.append({"role": "user", "content": user_input})
        
        return {"messages": messages}
