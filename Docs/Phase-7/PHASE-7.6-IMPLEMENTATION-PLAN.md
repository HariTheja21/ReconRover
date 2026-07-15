# Phase 7.6: Task Planner & Behavior Tree Engine - Implementation Plan

## Executive Summary
Phase 7.6 introduces the Task Planner & Behavior Tree Engine into the AI Runtime Framework. This module is the cognitive executive for the rover. It receives high-level semantic or geometric missions (e.g., "Explore living room") and decomposes them into discrete, executable tasks using a classic Behavior Tree (BT) architecture. It also serves as the failure recovery orchestrator, monitoring task progression and dynamically re-planning via the `RecoveryPlanner` if a sub-task fails.

## Objectives
- Build `TaskPlannerRuntime` and `TaskPlannerManager` as the core orchestrators for task sequencing.
- Implement a modular Behavior Tree framework (`behavior_tree.py`, `behavior_nodes.py`, `behavior_executor.py`) to manage task hierarchy.
- Develop `MissionManager` and `TaskQueue` to store and prioritize broken-down tasks.
- Construct `TaskExecutor` and `TaskMonitor` to track the state of currently executing hardware/navigation tasks.
- Build `FailureManager` and `RecoveryPlanner` to detect stalled tasks and generate evasive/corrective maneuvers.
- Create `PlanOptimizer` to sort queues efficiently (e.g., shortest path first).
- Ensure strict EventBus integration via `PlannerBridge`.

## Architecture
- **Decomposition Pipeline:** MissionCreated -> `MissionManager` -> `PlanOptimizer` -> `TaskQueue`.
- **Execution Pipeline:** `TaskScheduler` pops from `TaskQueue` -> `TaskExecutor` starts task -> `TaskMonitor` checks state -> Success or Failure.
- **Recovery Pipeline:** `TaskFailed` -> `FailureManager` logs -> If fatal, `RecoveryPlanner` generates backup task -> `TaskQueue`.
- **Event Routing:** The `PlannerBridge` emits `TaskStarted`, `TaskCompleted`, and `TaskFailed` to the `planner.tasks` topic.

## Safety & Constraints
- **Asynchronous Scheduler:** The `TaskScheduler` uses bounded `asyncio.Queue` structures to process missions. The task loop is safely throttled (`asyncio.sleep`) to prevent infinite spinning when the task queue is empty.
- **Thread Safety:** Goal and task states are strictly managed within the event loop to avoid concurrent state mutation.
