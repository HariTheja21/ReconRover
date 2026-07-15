import asyncio
from typing import Any
from .semantic_health import SemanticHealth
from .semantic_statistics import SemanticStatistics
from .semantic_bridge import SemanticBridge
from .persistent_storage import PersistentStorage
from .semantic_database import SemanticDatabase
from .landmark_manager import LandmarkManager
from .location_manager import LocationManager
from .object_memory import ObjectMemory
from .room_classifier import RoomClassifier
from .scene_memory import SceneMemory
from .entity_linker import EntityLinker
from .knowledge_graph import KnowledgeGraph
from .memory_optimizer import MemoryOptimizer
from .semantic_query import SemanticQuery
from .semantic_engine import SemanticEngine
from .semantic_scheduler import SemanticScheduler

class SemanticManager:
    def __init__(self, event_bus: Any, db_path: str = ":memory:"):
        self.health = SemanticHealth()
        self.stats = SemanticStatistics()
        self.bridge = SemanticBridge(event_bus)
        
        # Database & Storage
        self.storage = PersistentStorage(db_path)
        self.db = SemanticDatabase(self.storage)
        
        # Subcomponents
        self.lm = LandmarkManager(self.db)
        self.loc = LocationManager()
        self.obj_mem = ObjectMemory(self.db)
        self.room_c = RoomClassifier()
        self.scene_m = SceneMemory()
        self.linker = EntityLinker()
        self.kg = KnowledgeGraph()
        self.opt = MemoryOptimizer()
        self.query = SemanticQuery(self.db)
        
        # Assembly
        self.engine = SemanticEngine(
            self.db, self.lm, self.loc, self.obj_mem, self.room_c, 
            self.scene_m, self.linker, self.kg, self.opt, self.query, 
            self.stats, self.bridge.publish_event
        )
        
        self.scheduler = SemanticScheduler(self.engine)
        
    async def start(self):
        self.storage.connect()
        self.health.db_connected = True
        asyncio.create_task(self.scheduler.run_scene_loop())
        asyncio.create_task(self.scheduler.run_landmark_loop())
        
    def stop(self):
        self.storage.close()
        self.health.db_connected = False
