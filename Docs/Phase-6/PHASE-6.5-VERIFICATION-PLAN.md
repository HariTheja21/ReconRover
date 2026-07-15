# Phase 6.5: Configuration & OTA Management - Verification Plan

## Executive Summary
This document outlines the verification strategy for Phase 6.5 (Configuration & OTA Management). The goal is to audit both the configuration parameter hot-reload pipeline and the high-stakes OTA firmware flashing mechanism, ensuring robust validation, fault tolerance, and secure execution.

## Verification Objectives
- Validate the `ConfigurationValidator` traps out-of-bounds parameters and structural JSON flaws before persistence.
- Ensure the `ConfigurationEngine` correctly broadcasts the `ConfigurationUpdatedEvent` upon successful saves.
- Prove the `OTAValidator` accurately computes and compares SHA256 checksums to reject corrupted payloads.
- Verify the `OTAManager` enforces a strict singleton lock to prevent concurrent flash operations.
- Confirm the `OTABridge` streams accurate progress states (VALIDATING, FLASHING, SUCCESS, FAILED) back to the Ground Station UI.

## Verification Scope
The scope encompasses all Configuration and OTA scripts in `WEB_UI/backend/` and their respective UI components in `WEB_UI/frontend/js/`.

## Audit Strategy
1. **Validation Audit (Config):** Submit a payload with `max_velocity = -5` and `battery_critical = 100`. Expect rejection.
2. **Validation Audit (OTA):** Upload a dummy firmware binary with an intentionally mismatched SHA256 hash. Expect validation failure and cleanup.
3. **Concurrency Audit:** Attempt to start a second OTA upload while the first is in the "FLASHING" state. Expect immediate rejection by `OTAManager`.
4. **Rollback Audit:** Trigger a configuration backup, deliberately break the active configuration, and trigger a restore. Verify the system reverts accurately.

## Runtime Audit
- Ensure that the OTA asynchronous simulation doesn't block the FastAPI event loop, allowing telemetry and camera streams to continue (if intended) during a flash.

## Memory Audit
- Verify that `OTAManager` cleans up failed/rejected uploads from `data/ota_uploads` to prevent disk space exhaustion over time.

## Internal Test Matrix
1. **Valid Config Update:** Save valid parameters -> Check EventBus for `ConfigurationUpdatedEvent`.
2. **Invalid Config Update:** Save invalid parameters -> Check UI for error message.
3. **Valid OTA Flash:** Upload correct binary + hash -> Verify progression from 0% to 100% and UI log output.
4. **Invalid OTA Flash:** Upload corrupted binary -> Verify "Checksum mismatch" and no deployment.

## PASS / FAIL Criteria
- **PASS:** All invalid inputs are caught. Concurrent flashes are blocked. EventBus hot-reloads work.
- **FAIL:** Corrupted configuration crashes the system. Two OTA flashes run simultaneously. Temp files leak on disk.

## Expected Deliverables
- `PHASE-6.5-VERIFICATION-PLAN.md`
- `PHASE-6.5-VERIFICATION.md`
- Updates to `ENGINEERING-CHANGELOG.md`
