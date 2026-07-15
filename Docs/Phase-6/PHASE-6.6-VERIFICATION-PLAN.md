# Phase 6.6: Diagnostics & Log Viewer - Verification Plan

## Executive Summary
This document defines the verification parameters for Phase 6.6 (Diagnostics & Log Viewer). The goal is to rigorously test the end-to-end telemetry pipeline, from the generation of system events on the EventBus to their persistence on disk and real-time visualization in the browser, ensuring the system remains stable under high data loads.

## Verification Objectives
- Validate that `LogManager` correctly rotates logs daily and persists `LogEvent` payloads without dropping critical data.
- Ensure `LogSearch` accurately filters large datasets by severity level, source, and regex query.
- Prove that `HealthMonitor` and `PerformanceMonitor` successfully aggregate high-frequency `EventBus` telemetry without race conditions.
- Verify that `ReportGenerator` builds a comprehensive, well-structured JSON snapshot encompassing health, logs, and performance.
- Confirm the `LogViewer` DOM correctly enforces a 1000-line FIFO buffer to prevent memory exhaustion in the browser.

## Verification Scope
The scope covers all components within `WEB_UI/backend/` related to diagnostics, logging, and performance, as well as the UI scripts in `WEB_UI/frontend/js/`.

## Audit Strategy
1. **Logging Audit:** Inject 5,000 synthetic log messages across all levels and sources in under 2 seconds. Verify that exactly 5,000 are written to disk and that the browser UI truncates to the latest 1,000.
2. **Filter Audit:** Use `LogSearch` to query for "CRITICAL" events containing the string "battery". Verify the result set precisely matches the criteria.
3. **Health Audit:** Rapidly toggle a subsystem's state between "OK" and "ERROR". Ensure the final state in the `HealthMonitor` reflects the exact last event received.
4. **Report Audit:** Trigger `ReportGenerator` while the system is under heavy logging load. Verify the output JSON is structurally sound and not corrupted by concurrent writes.

## Runtime Audit
- Ensure that File I/O operations (writing logs, saving reports) do not block the FastAPI asyncio loop.

## Memory Audit
- Verify the frontend `LogViewer` effectively garbage-collects discarded DOM nodes (log rows) when appending past the 1,000 limit.

## Internal Test Matrix
1. **High Throughput Logs:** Inject 1,000 logs/sec. (Expect PASS, no crashes).
2. **Level Filtering:** Filter frontend for ERROR. (Expect only red log lines).
3. **Report Generation:** Click "Generate Report". (Expect JSON file in `data/reports`).
4. **Log Storage Failsafe:** Make `data/logs` read-only. (Expect system to continue running, silently dropping logs or logging to stderr).

## PASS / FAIL Criteria
- **PASS:** No memory leaks. Search works perfectly. Reports generate instantly. 
- **FAIL:** High log volume crashes the EventBus. Frontend tab freezes after 10 minutes. 

## Expected Deliverables
- `PHASE-6.6-VERIFICATION-PLAN.md`
- `PHASE-6.6-VERIFICATION.md`
- Updates to `ENGINEERING-CHANGELOG.md`
