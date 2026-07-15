# Phase 7.4: Autonomous Exploration Engine - Implementation Plan

## Executive Summary
Phase 7.4 introduces the Autonomous Exploration Engine into the AI Runtime Framework. This module is responsible for analyzing the environment (OccupancyGrid), identifying unexplored boundaries (Frontiers), selecting optimal exploration targets, generating mission commands, and safely managing exploration state (including deadlock recovery). It operates purely at the planning level and issues semantic goals, remaining fully decoupled from direct motor control.

## Objectives
- Build `ExplorationRuntime` and `ExplorationManager` as the core orchestrators for autonomous discovery.
- Implement `FrontierDetector` and `FrontierCluster` to process the SLAM occupancy grid and isolate unexplored boundaries.
- Develop `FrontierRanker` and `GoalSelector` to score potential targets based on distance and cluster size.
- Construct `CoverageTracker` and `CoverageMap` to monitor the total square meters explored.
- Build `DeadlockDetector` and `RecoveryManager` to prevent the rover from getting stuck in confined spaces.
- Create `MissionGenerator` and `ExplorationState` to manage the lifecycle of a discovery mission.
- Ensure strict EventBus integration via `ExplorationBridge` to communicate targets to the Navigation stack.

## Architecture
- **Exploration Pipeline:** Grid Updated -> Update Coverage -> Detect Deadlock -> Detect Frontiers -> Cluster Frontiers -> Rank Clusters -> Select Goal -> Generate Mission.
- **State Machine:** Governed by `ExplorationState` (IDLE, EXPLORING, RECOVERING, COMPLETED, PAUSED).
- **Event Routing:** The `ExplorationBridge` emits `ExplorationMissionGenerated` and `RecoveryRequested` to the `exploration.missions` topic.

## Safety & Constraints
- **Asynchronous Scheduler:** The `ExplorationScheduler` uses a bounded `asyncio.Queue` (maxsize=10) to process heavy grid arrays. If grid updates outpace processing, older grids are dropped to prevent memory exhaustion.
- **Thread Safety:** Grid parsing and state management are strictly synchronous within the async worker loop, avoiding race conditions.
