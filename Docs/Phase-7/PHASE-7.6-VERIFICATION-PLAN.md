# Phase 7.6: Task Planner & Behavior Tree Engine - Verification Plan

## Executive Summary
This document defines the verification strategy for Phase 7.6. The objective is to validate that the Task Planner reliably decomposes abstract missions into executable tasks, governs their execution through a strict Behavior Tree framework, and flawlessly executes recovery procedures upon detecting physical or logical task failures.

## Verification Objectives
- Validate `TaskPlannerRuntime` smoothly ingests, prioritizes, and schedules incoming missions via the `TaskScheduler`.
- Confirm `BehaviorTree` executes `SequenceNode` and `SelectorNode` logic deterministically without infinite loops.
- Verify `MissionManager` decomposes high-level goals and injects properly prioritized sub-tasks into the `TaskQueue`.
- Prove `TaskExecutor` and `TaskMonitor` correctly supervise active operations without blocking the main event loop.
- Validate `FailureManager` correctly tracks failure counts and triggers `RecoveryPlanner` once the fatal threshold is met.
- Ensure `PlannerBridge` successfully routes task progression telemetry to the EventBus.

## Verification Scope
The scope encompasses all 19 task planning modules situated in `MAIN CODE/RASPBERRY_PI/core/ai/task_planner/` and the scratch test `scratch/test_task_planner.py`.

## Audit Strategy
1. **Behavior Tree Execution Audit:** Construct a mock Behavior Tree with a `SelectorNode` containing a failing `ActionNode` followed by a successful `ActionNode`. Verify the root ticks and returns `SUCCESS`, correctly demonstrating fallback behavior.
2. **Task Scheduling Audit:** Inject 3 tasks into the `TaskQueue` with priorities 1, 5, and 3. Verify `pop_task()` returns them in the order: 5, 3, 1.
3. **Failure & Recovery Audit:** Simulate a hardware failure during a "NAVIGATE" task 3 times consecutively. Verify `FailureManager.check_fatal()` returns True on the 3rd attempt, and `RecoveryPlanner` subsequently injects a "RECOVERY" task into the queue.
4. **Queue Overflow Audit:** Inject 20 mission requests into the `TaskScheduler` (maxsize=10). Verify that older missions are gracefully dropped or throttled without crashing the asynchronous pipeline.

## Runtime Audit
- Ensure the `run_task_loop` throttles itself correctly (`asyncio.sleep`) to prevent 100% CPU utilization when the `TaskQueue` is empty.

## Memory Audit
- Verify the `MissionManager` and `TaskQueue` clean up completed references, preventing memory leaks over long-duration operations involving thousands of micro-tasks.

## Internal Test Matrix
1. **Valid Initialization:** Run `test_task_planner.py`. (Expect Success).
2. **BT Fallback:** Trigger a `SelectorNode` fallback. (Expect NodeStatus.SUCCESS).
3. **Priority Queuing:** Test `TaskQueue` sorting logic. (Expect correct order).
4. **Fatal Recovery:** Trigger 3 successive task failures. (Expect Recovery Task).

## PASS / FAIL Criteria
- **PASS:** The engine accurately executes Behavior Trees, prioritizes tasks correctly, orchestrates recovery maneuvers upon fatal errors, and publishes valid JSON payloads without blocking the `asyncio` event loop.
- **FAIL:** The `run_task_loop` consumes 100% CPU. Behavior Trees enter infinite recursive ticks. The `FailureManager` fails to trigger recovery maneuvers.

## Expected Deliverables
- `PHASE-7.6-VERIFICATION-PLAN.md`
- `PHASE-7.6-VERIFICATION.md`
- Updates to `ENGINEERING-CHANGELOG.md`
