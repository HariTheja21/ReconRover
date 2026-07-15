# Phase 5.1: Real-World Hardware Integration & Calibration - Verification Plan

## Executive Summary
This document defines the verification strategy for Phase 5.1 (Real-World Hardware Integration & Calibration). The objective is to formally audit the physical integration layer, ensuring that the software pipeline accurately interacts with OS-level hardware configurations, successfully executes diagnostic queries against all physical peripherals, and safely generates a validated configuration profile.

## Verification Objectives
- Validate the logic of the `DeviceMapper` for generating correct Linux `udev` syntax.
- Ensure the `CalibrationEngine` orchestrates all 6 sub-calibrators asynchronously without blocking.
- Verify the strict isolation of hardware-specific diagnostic logic within individual classes (`MotorCalibrator`, `ImuCalibrator`, etc.).
- Prove that the `SystemValidator` correctly rejects profiles missing critical hardware data.
- Confirm that the `CalibrationManager` accurately reports the final Boolean success state.

## Verification Scope
The scope encompasses the `core/calibration/` module on the Raspberry Pi. This involves validating logical orchestrations and API schemas for physical calibration interactions.

## Audit Strategy
1. **Device Mapping Audit:** Review the generated `udev` templates for correct syntax matching `idVendor` and `idProduct`.
2. **Logic Emulation:** Run the `test_calibration.py` suite utilizing `unittest.mock` to forcefully inject hardware failures (e.g., motor overcurrent) and observe the engine's fault handling.
3. **Data Integrity:** Verify the resulting `recon_rover_calibration.json` profile contains all required fields (`latency_ms`, `offset_x`, `pan_center`, etc.) formatted correctly.

## AsyncIO Audit
- Ensure that `await` calls are correctly applied to every calibrator step, as real-world sensor reads (especially IMU sampling) are inherently time-consuming and must yield to the event loop.

## Runtime Audit
- Verify the orchestration layer executes sequentially without leaking tasks.

## Memory Audit
- Confirm that temporary data sampled during calibration (e.g., 100 IMU data points) is allowed to garbage collect after calculating the final zero-bias offset.

## Internal Test Matrix
1. **Full Calibration Success:** Execute the engine, assert all calibrators pass, assert `recon_rover_calibration.json` is generated.
2. **Motor Failure:** Mock a thrown exception inside `MotorCalibrator`. Assert the engine catches it, halts subsequent calibrations, and aborts profile generation.
3. **Validator Failure:** Return an empty dictionary from a mock calibrator. Assert `SystemValidator` rejects the incomplete profile.

## PASS / FAIL Criteria
- **PASS:** 100% test success, correct `udev` string formatting, strict fail-safe halting on hardware errors, flawless JSON schema validation.
- **FAIL:** Silent failures, unhandled async exceptions, profile generation despite hardware errors.

## Expected Deliverables
- `PHASE-5.1-VERIFICATION-PLAN.md`
- `PHASE-5.1-VERIFICATION.md`
- Updates to `ENGINEERING-CHANGELOG.md`
