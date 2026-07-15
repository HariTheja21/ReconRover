# Phase 5.0: Hardware Bring-up & System Boot Framework - Verification Plan

## Executive Summary
This document defines the verification strategy for Phase 5.0 (Hardware Bring-up & System Boot Framework). The objective is to formally audit the Python AsyncIO architecture to guarantee that the system executes the 16-step boot sequence deterministically, accurately detects missing Linux hardware peripherals (e.g., `/dev/ttyUSB0`), strictly enforces downstream logical dependencies, and safely halts execution upon catastrophic failure.

## Verification Objectives
- Validate the static topological mapping of the `BootSequence`.
- Ensure the `DependencyChecker` strictly blocks downstream modules if an upstream module fails or is bypassed.
- Verify `HardwareDiscovery` relies on physical OS-level indicators rather than logical assumptions.
- Prove that `BootEngine` executes non-blockingly, respecting `asyncio.sleep` to decouple from the main event loop.
- Confirm the `StartupValidator` emits an unequivocal `PASS/FAIL` Boolean that can be used by `main.py` to enter Mission mode or Safe mode.

## Verification Scope
The scope is entirely focused on the `core/system_boot/` module on the Raspberry Pi. This involves validating logical state machines; physical integration with external devices is deferred to Phase 5.1.

## Audit Strategy
1. **Dependency Graph Audit:** Mathematically review the sequence list to ensure no circular dependencies exist (e.g., Navigation requires SLAM, SLAM requires Mapping, Mapping requires Camera).
2. **Logic Emulation:** Run the `unittest` suite (`test_boot.py`) utilizing `unittest.mock` to forcefully break OS paths (`os.path.exists`) and observe the engine's reaction.
3. **Event Observation:** Validate that every sequence step emits the correct `SubsystemStartedEvent` or `SubsystemFailedEvent` prior to the final `BootCompletedEvent`.

## AsyncIO Audit
- Ensure that `await asyncio.sleep()` or similar `await` yielding occurs between subsystem instantiations, preventing CPU starvation for background threads (like the EventBus).

## Runtime Audit
- Verify $O(N)$ execution time relative to the sequence length. Boot should resolve as fast as the hardware allows.

## Memory Audit
- Confirm that the `BootManager` holds only state statistics and simple strings, avoiding massive object instantiations that could spike memory during startup.

## Internal Test Matrix
1. **Cold Boot Success:** Mock all `/dev/` files as present. Assert all 16 subsystems boot and `BootCompletedEvent` is fired.
2. **Missing Dependency:** Manually inject a failure into step 3 (EventBus). Assert that step 4 (Runtime) and all subsequent steps instantly fail validation.
3. **ESP32 Disconnected:** Mock `/dev/ttyUSB0` as missing. Assert that the `HardwareDiscovery` catches it, fails the sequence, and prevents Telemetry from starting.
4. **Camera Disconnected:** Mock `/dev/video0` as missing. Assert that the sequence hard-fails before Mapping or SLAM can initialize with null buffers.

## PASS / FAIL Criteria
- **PASS:** 100% test success, complete topological compliance, strict failure halting on missing hardware.
- **FAIL:** Silent failures, circular dependencies, blocking I/O calls without `await`, or starting SLAM/Navigation without physical hardware verification.

## Expected Deliverables
- `PHASE-5.0-VERIFICATION-PLAN.md`
- `PHASE-5.0-VERIFICATION.md`
- Updates to `ENGINEERING-CHANGELOG.md`
