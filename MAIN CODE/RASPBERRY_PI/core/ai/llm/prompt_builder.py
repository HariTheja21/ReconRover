class PromptBuilder:
    def __init__(self, context_builder, memory_retriever):
        self.cb = context_builder
        self.mr = memory_retriever
        
    def build(self, user_input: str, conversation_history: list) -> list:
        mem = self.mr.retrieve_relevant(user_input)
        sys_ctx = self.cb.build_context(mem, "Stubbed Spatial Context")
        return sys_ctx + conversation_history + [{"role": "user", "content": user_input}]
