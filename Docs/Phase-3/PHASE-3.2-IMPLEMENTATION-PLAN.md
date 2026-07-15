# Phase 3.2: Sensor Fusion Engine - Implementation Plan

## Executive Summary
Recon Rover V2's perception capabilities are expanding via Phase 3.2 (Sensor Fusion Engine). This module resolves contradictory sensory data (e.g., ultrasonic vs. LiDAR) into a single, highly reliable semantic truth. By isolating fusion math from both raw hardware drivers and the downstream World Model database, the system can gracefully handle sensor hardware faults, blind spots, and noisy measurements.

## Objectives
- Cross-check overlapping modalities (VL53L0X, HC-SR04, LiDAR).
- Maintain dynamic confidence values for every individual sensor.
- Resolve conflicting distance observations algorithmically.
- Publish `FusedDistance` and `FusedObstacle` abstractions for World Model ingestion.

## Repository Analysis
Phase 3.1 established the `WorldModel`, an agnostic consumer of semantic abstractions. Phase 3.2 acts as the intelligent intermediary filter sitting between raw EventBus telemetry and the World Model.

## Proposed Architecture
The `FusionManager` instantiates the `FusionEngine`. 
- `fusion_state.py` caches raw measurements.
- `sensor_correlator.py` detects statistical outliers and contradictory readings.
- `sensor_confidence.py` penalizes hardware that frequently contradicts consensus.
- `fusion_rules.py` executes stateless logic to pick the safest, highest-confidence measurement (typically shortest-distance).

## Folder Structure
```
core/fusion/
  ├── fusion_manager.py
  ├── fusion_engine.py
  ├── fusion_rules.py
  ├── fusion_state.py
  ├── fusion_events.py
  ├── fusion_health.py
  ├── fusion_statistics.py
  ├── sensor_confidence.py
  └── sensor_correlator.py
```

## Public APIs
The `FusionManager` publishes cyclic 10Hz updates resolving all collected distance payloads into `FusedDistance` and `FusedObstacle`. It also dynamically broadcasts `SensorConfidenceUpdated` whenever it detects an outlier.

## EventBus Integration
**Consumes:** `IMUUpdated`, `DistanceUpdated`, `ObstacleDetected`
**Publishes:** `FusedObstacle`, `FusedDistance`, `SensorConfidenceUpdated`, `EnvironmentUpdated`, `FusionHealthUpdated`

## Memory Strategy
`fusion_state.py` relies strictly on Time-To-Live (TTL = 1.0s) parameters. No array appending. Data older than 1.0 seconds is ignored during fusion and discarded on subsequent cycles.

## CPU Strategy
The `detect_conflicts` logic relies on highly optimized $O(N \log N)$ sorting for median isolation. Since $N$ (number of sensors) is $<10$, this computes in micro-seconds.

## Risks
- Extreme edge-case where *all* sensors hallucinate simultaneously.
- Mitigation: Requires multi-modal correlation (future vision overlap).

## Engineering Recommendation
Proceed immediately to establish the statistical noise filter needed before running true cognitive AI operations.
