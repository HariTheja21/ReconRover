import asyncio
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'MAIN CODE', 'RASPBERRY_PI'))

from core.ai.runtime.rag.rag_runtime import RAGRuntime

class MockEventBus:
    def publish(self, topic, payload):
        print(f"[EventBus] {topic}: {payload}")

async def main():
    print("Initializing RAG Runtime...")
    bus = MockEventBus()
    runtime = RAGRuntime(bus)
    
    await runtime.initialize()
    
    print("\nLoading and Indexing Documents...")
    docs = runtime.doc_loader.load("mock_source")
    runtime.indexer.index(docs)
    print("Documents Indexed.")
    
    print("\nPerforming Semantic Retrieval...")
    query = "Find information about Recon Rover"
    results = runtime.engine.retrieve(query)
    print(f"Results: {results}")
    
    print("\nTesting Specialized Retrievers...")
    mem_res = runtime.memory.get_memory("recent paths")
    print(f"Memory Retrieval: {mem_res}")
    
    print("\nBuilding Context...")
    context = runtime.context.build("session-123", results)
    print(f"Built Context:\n{context}")
    
    print("\nTest Complete.")

if __name__ == "__main__":
    asyncio.run(main())
