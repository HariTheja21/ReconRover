# Phase 3.2: Sensor Fusion Engine - Verification Plan

## Executive Summary
This document delineates the verification parameters for the Phase 3.2 Sensor Fusion Engine. The primary objective is to prove that the statistical fusion math accurately weeds out sensor hallucinations, penalizes faulty hardware, and emits a single, trustworthy spatial representation to the EventBus.

## Verification Objectives
- Validate the $O(N \log N)$ statistical median sorting logic in `SensorCorrelator`.
- Validate the Time-To-Live (TTL = 1.0s) observation sweeping inside `FusionState`.
- Ensure Thread Safety during rapid multi-modal telemetry ingestion.
- Confirm `FusionManager` accurately limits network congestion by down-sampling to a consistent 10Hz output loop.

## Verification Scope
Scope encompasses all `core/fusion/` components (`fusion_engine.py`, `fusion_rules.py`, `sensor_confidence.py`, etc.). The downstream `WorldModel` is out of scope.

## Audit Strategy
1. Perform static analysis on the synchronization locks in `FusionState` and `SensorConfidence`.
2. Evaluate dynamic output behavior during simulated "consensus breakage" where 1 sensor wildly diverges from 2 healthy sensors.

## Architecture Audit
- Verify that `FusionEngine` strictly decouples stateless mathematical rules (`FusionRules`) from the stateful cached observations (`FusionState`).

## Runtime Audit
- Assert that the 10Hz publication task handles empty data states gracefully without raising exceptions.

## Memory Audit
- Verify the TTL sweeps actively prevent memory drift during prolonged hardware dropouts.

## CPU Audit
- Assert negligible overhead during the cross-check operations by relying on flat dataset mapping.

## Thread Safety Audit
- Validate read/write race condition protections on high-velocity state variables like `DistanceUpdated`.

## Async Safety Audit
- Validate `asyncio.sleep()` is leveraged in the `_publish_loop` instead of blocking time functions.

## EventBus Audit
- Verify emission schema for `FusedObstacle`, `FusedDistance`, and `SensorConfidenceUpdated`.

## Internal Test Matrix
1. **Test 1 - Consensus:** Inject 3 overlapping distance readings. Expect shortest valid distance.
2. **Test 2 - Ghost Rejection:** Inject 2 overlapping distances and 1 massive outlier (e.g., 250cm vs 10cm). Expect rejection of outlier and immediate penalty assigned in `SensorConfidenceUpdated`.

## PASS / FAIL Criteria
- **PASS:** Immediate statistical quarantine of hallucinating sensor variables. Zero Python tracebacks during empty-buffer frames.
- **FAIL:** Deadlocks, CPU blocking, or merging valid measurements with ghost reflections.

## Risks
- Sensors failing at exactly the same wrong value simultaneously could hypothetically break consensus math.

## Expected Deliverables
- `PHASE-3.2-VERIFICATION-PLAN.md`
- `PHASE-3.2-VERIFICATION.md`
- Updates to `ENGINEERING-CHANGELOG.md`
