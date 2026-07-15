import asyncio
from typing import Any
from .exploration_health import ExplorationHealth
from .exploration_statistics import ExplorationStatistics
from .exploration_bridge import ExplorationBridge
from .frontier_detector import FrontierDetector
from .frontier_cluster import FrontierCluster
from .frontier_ranker import FrontierRanker
from .goal_selector import GoalSelector
from .coverage_tracker import CoverageTracker
from .coverage_map import CoverageMap
from .exploration_state import ExplorationState
from .mission_generator import MissionGenerator
from .recovery_manager import RecoveryManager
from .deadlock_detector import DeadlockDetector
from .exploration_optimizer import ExplorationOptimizer
from .exploration_engine import ExplorationEngine
from .exploration_scheduler import ExplorationScheduler

class ExplorationManager:
    def __init__(self, event_bus: Any):
        self.health = ExplorationHealth()
        self.stats = ExplorationStatistics()
        self.bridge = ExplorationBridge(event_bus)
        
        # Subcomponents
        self.fd = FrontierDetector()
        self.fc = FrontierCluster()
        self.fr = FrontierRanker()
        self.gs = GoalSelector()
        self.cov_map = CoverageMap()
        self.cov_tracker = CoverageTracker(self.cov_map)
        self.state = ExplorationState()
        self.mg = MissionGenerator()
        self.rm = RecoveryManager()
        self.dd = DeadlockDetector()
        self.opt = ExplorationOptimizer()
        
        # Assembly
        self.engine = ExplorationEngine(
            self.fd, self.fc, self.fr, self.gs, self.cov_tracker, self.cov_map,
            self.state, self.mg, self.rm, self.dd, self.opt, self.stats, self.bridge.publish_event
        )
        
        self.scheduler = ExplorationScheduler(self.engine)
        
    async def start(self):
        asyncio.create_task(self.scheduler.run_loop())
