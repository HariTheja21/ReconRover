import asyncio
from typing import Any

from .rag_health import RAGHealth
from .rag_statistics import RAGStatistics
from .rag_bridge import RAGBridge
from .rag_manager import RAGManager
from .rag_scheduler import RAGScheduler

from .embedding_provider import EmbeddingProvider
from .providers.sentence_transformer_provider import SentenceTransformerProvider
from .embedding_manager import EmbeddingManager

from .vector_database import VectorDatabase
from .providers.chromadb_provider import ChromaDBProvider
from .providers.faiss_provider import FAISSProvider

from .document_store import DocumentStore
from .document_loader import DocumentLoader
from .chunk_manager import ChunkManager
from .document_indexer import DocumentIndexer

from .query_optimizer import QueryOptimizer
from .semantic_search import SemanticSearch
from .hybrid_search import HybridSearch
from .reranker import Reranker
from .retrieval_ranker import RetrievalRanker
from .retrieval_engine import RetrievalEngine

from .knowledge_retriever import KnowledgeRetriever
from .memory_retriever import MemoryRetriever
from .context_builder import ContextBuilder

class RAGRuntime:
    def __init__(self, event_bus: Any):
        self.health = RAGHealth()
        self.stats = RAGStatistics()
        self.bridge = RAGBridge(event_bus)
        
        # Init Providers
        self.embedder = SentenceTransformerProvider()
        self.embedding_manager = EmbeddingManager(self.embedder)
        
        self.vdb = ChromaDBProvider()
        
        # Init Indexing Pipeline
        self.doc_store = DocumentStore()
        self.doc_loader = DocumentLoader()
        self.chunker = ChunkManager()
        self.indexer = DocumentIndexer(self.chunker, self.embedding_manager, self.vdb, self.doc_store)
        
        # Init Retrieval Pipeline
        self.optimizer = QueryOptimizer()
        self.semantic_search = SemanticSearch(self.embedding_manager, self.vdb)
        self.hybrid_search = HybridSearch(self.semantic_search, None) # Mock keyword search
        self.reranker = Reranker()
        self.ranker = RetrievalRanker(self.reranker)
        
        self.engine = RetrievalEngine(self.optimizer, self.hybrid_search, self.ranker, self.bridge.publish_event)
        
        # Specific Retrievers
        self.knowledge = KnowledgeRetriever(self.engine, self.bridge.publish_event)
        self.memory = MemoryRetriever(self.engine, self.bridge.publish_event)
        self.context = ContextBuilder(self.bridge.publish_event)
        
        # Orchestrator
        self.manager = RAGManager(self.indexer, self.engine, self.knowledge, self.memory, self.context)
        self.scheduler = RAGScheduler(self.manager)
        
    async def initialize(self):
        return True
