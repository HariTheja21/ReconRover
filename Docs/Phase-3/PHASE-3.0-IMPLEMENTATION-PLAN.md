# Phase 3.0: Runtime Integration & System Orchestrator - Implementation Plan

## Goal Description
Build the Runtime Integration & System Orchestrator for Recon Rover V2. As Phase 2 is now complete, we possess numerous decoupled sub-systems (Config, Safety, Mode, Sensors, Actuation, etc.) that communicate via the EventBus. Phase 3.0 introduces a centralized supervisor that manages the exact deterministic boot sequence, handles graceful teardowns, actively monitors module heartbeats, and safely orchestrates restart procedures in case a sub-system panics or dies. 

Crucially, this module possesses NO AI, NO SLAM, and NO Navigation. It acts purely as a "Systemd" equivalent for the Python process, orchestrating the lifecycles of all other nodes.

## Proposed Changes

### 1. Runtime Events (`core/runtime/`)
[NEW] `runtime_events.py`:
- Consumes: `SystemStartRequest`, `SystemShutdownRequest`, `ModuleFailure`, `HeartbeatTimeout`.
- Publishes: `SystemStarted`, `SystemStopped`, `ModuleStarted`, `ModuleStopped`, `ModuleRestarted`, `RuntimeHealthy`, `RuntimeFault`.

### 2. Lifecycle & Dependency Management (`core/runtime/`)
[NEW] `lifecycle_manager.py`: Base definitions for module states (INIT, STARTING, RUNNING, STOPPING, FAULT).
[NEW] `dependency_manager.py`: Represents the DAG (Directed Acyclic Graph) of module dependencies. Enforces the strict startup order.
[NEW] `startup_manager.py`: Traverses the dependency graph, injecting the EventBus, and calling `.start()` on modules sequentially.
[NEW] `shutdown_manager.py`: Safely reverses the startup order, calling `.stop()` and yielding until clean teardown.

### 3. Orchestration & Supervision (`core/runtime/`)
[NEW] `system_orchestrator.py`: The highest level object in the Python application. Initializes the `EventBus` first, then instantiates the Runtime layers.
[NEW] `runtime_manager.py`: Glues the Startup, Shutdown, and Supervisor modules together. Listens to `SystemStartRequest` and `SystemShutdownRequest`.
[NEW] `module_supervisor.py`: Pings registered modules for heartbeats. If `HeartbeatTimeout` or `ModuleFailure` is detected, it triggers isolated module teardown and restart procedures.

### 4. Telemetry & Health (`core/runtime/`)
[NEW] `runtime_health.py`: Collects system-wide status flags across all supervised modules and publishes `RuntimeHealthy` or `RuntimeFault`.
[NEW] `runtime_statistics.py`: Thread-safe tracking of restarts, uptime, and state transitions.

### 5. Documentation
[NEW] `docs/Phase-3/PHASE-3.0-IMPLEMENTATION-PLAN.md` (This file natively)
[NEW] `docs/Phase-3/PHASE-3.0.md`
[MODIFY] `ENGINEERING-CHANGELOG.md`

## Startup Order Verification
The strict startup order implemented in `dependency_manager.py` will be:
1. EventBus
2. Configuration Manager
3. Mode Manager
4. Safety Manager
5. HAL (Hardware Abstraction Layer)
6. Telemetry
7. Sensors
8. Camera
9. Actuation
10. Input
11. Future AI Modules (Deferred to subsequent phases)

## Verification Plan
### Internal Tests
- Write `scratch/test_runtime.py`.
- Mock 5 dummy modules matching the dependency DAG.
- Fire `SystemStartRequest`.
- Verify the `startup_manager.py` boots them sequentially strictly adhering to dependency rules.
- Simulate a `HeartbeatTimeout` for one module. Verify `module_supervisor.py` catches it, stops the module, and re-triggers its startup.
- Fire `SystemShutdownRequest` and verify `shutdown_manager.py` cleanly tears them down in reverse order.

## User Review Required
> [!IMPORTANT]  
> Bypassing standard artifacts per your Mandatory Documentation Policy. Once approved, I will implement all 10 orchestration files under `core/runtime/` and write a comprehensive deterministic internal test script before generating the final Phase 3.0 report.
