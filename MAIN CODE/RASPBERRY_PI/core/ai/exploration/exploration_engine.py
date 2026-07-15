import asyncio
from typing import Callable, Any
from .exploration_events import (
    FrontierDetected, ExplorationGoalSelected, ExplorationMissionGenerated,
    CoverageUpdated, DeadlockDetected, RecoveryRequested, ExplorationStateUpdated
)

class ExplorationEngine:
    def __init__(self, frontier_detector, clusterer, ranker, selector, 
                 cov_tracker, cov_map, state, mission_gen, recovery, 
                 deadlock, optimizer, stats, publish: Callable):
        self.fd = frontier_detector
        self.fc = clusterer
        self.fr = ranker
        self.gs = selector
        self.cov_tracker = cov_tracker
        self.cov_map = cov_map
        self.state = state
        self.mg = mission_gen
        self.rm = recovery
        self.dd = deadlock
        self.opt = optimizer
        self.stats = stats
        self.publish = publish
        
        self.robot_pose = (0.0, 0.0)
        
    async def process_grid_update(self, grid: Any, resolution: float, origin: tuple):
        # 1. Update coverage map
        self.cov_map.update(grid, resolution, origin)
        area, pct = self.cov_tracker.calculate_coverage(resolution)
        self.stats.total_coverage_m2 = area
        self.publish("CoverageUpdated", {"area": area, "pct": pct, "ts": asyncio.get_event_loop().time()})
        
        if self.state.get_state() != "EXPLORING":
            return
            
        # 2. Deadlock Detection
        if self.dd.update(self.robot_pose):
            self.state.transition("RECOVERING")
            self.stats.deadlocks_resolved += 1
            reason = self.dd.get_deadlock_reason()
            self.publish("DeadlockDetected", {"reason": reason, "time": 0.0, "ts": asyncio.get_event_loop().time()})
            
            strat, rx, ry = self.rm.plan_recovery(self.robot_pose)
            self.publish("RecoveryRequested", {"strategy": strat, "x": rx, "y": ry, "ts": asyncio.get_event_loop().time()})
            return
            
        # 3. Frontier Detection & Clustering
        points = self.fd.detect(grid)
        if not points:
            self.state.transition("COMPLETED")
            self.publish("ExplorationStateUpdated", {"state": "COMPLETED", "ts": asyncio.get_event_loop().time()})
            return
            
        clusters = self.fc.cluster(points)
        self.stats.frontiers_detected += len(clusters)
        self.publish("FrontierDetected", {"count": len(clusters), "ts": asyncio.get_event_loop().time()})
        
        # 4. Ranking & Goal Selection
        ranked = self.fr.rank(clusters, self.robot_pose)
        tx, ty, score = self.gs.select_best(ranked)
        
        if score > 0:
            tx, ty = self.opt.optimize_goal(tx, ty)
            self.stats.goals_selected += 1
            self.publish("ExplorationGoalSelected", {"x": tx, "y": ty, "score": score, "ts": asyncio.get_event_loop().time()})
            
            # 5. Mission Generation
            mid, prio = self.mg.create_mission(tx, ty)
            self.stats.missions_generated += 1
            self.publish("ExplorationMissionGenerated", {"id": mid, "x": tx, "y": ty, "prio": prio, "ts": asyncio.get_event_loop().time()})
            
    def update_pose(self, x: float, y: float):
        self.robot_pose = (x, y)
