class RAGManager:
    def __init__(self, indexer, engine, knowledge, memory, context):
        self.indexer = indexer
        self.engine = engine
        self.knowledge = knowledge
        self.memory = memory
        self.context = context
