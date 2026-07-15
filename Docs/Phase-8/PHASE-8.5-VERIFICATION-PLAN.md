# Phase 8.5: Tool Calling & Function Execution Runtime - Verification Plan

## Executive Summary
This document outlines the verification strategy for Phase 8.5. The objective is to validate that the Tool Calling layer perfectly bridges LLM outputs with the rover's physical capabilities in a secure, validated, and highly resilient manner, immune to hallucinations and hardware timeouts.

## Verification Objectives
- Validate `ToolRegistry` correctly dynamically constructs OpenAPI-style JSON schemas from all registered `BaseTool` objects.
- Confirm `ToolPermissions` strictly rejects unauthenticated roles.
- Verify `ToolValidator` correctly catches malformed arguments before passing them to the executor.
- Prove `ToolTimeout` terminates hanging coroutines and returns structured errors instead of crashing the thread.
- Ensure `ToolRetry` successfully catches transient exceptions and re-attempts the command up to `max_retries`.
- Validate `ToolBridge` reliably broadcasts `ToolExecutionStarted`, `ToolExecutionCompleted`, and `ToolExecutionFailed`.

## Verification Scope
The scope encompasses all 25 Tool Runtime modules located in `MAIN CODE/RASPBERRY_PI/core/ai/runtime/tools/` and the integration script `scratch/test_tool_runtime.py`.

## Audit Strategy
1. **Registration & Discovery Audit:** Instantiate `ToolRuntime` and query `registry.get_all_schemas()`. Verify exactly 6 standard tools are returned with properly formed JSON schema parameter blocks.
2. **Permission Audit:** Dispatch a `SystemTool` command using a `"guest"` role. Verify `ToolPermissions` blocks it.
3. **Execution Pipeline Audit:** Dispatch a valid `NavigationTool` command using a `"planner"` role. Verify the command successfully traverses `ToolValidator`, `ToolTimeout`, and `ToolRetry`, generating a valid `ToolResult`.
4. **Audit Logging Audit:** Check the `ToolAudit.logs` array. Verify that both the successful and failed invocations were immutably recorded with their arguments and final results.
5. **Event Routing Audit:** Monitor the MockEventBus for the exact presence of `ToolExecutionStarted` and `ToolExecutionCompleted` / `Failed`.

## Runtime Audit
- Ensure that `ToolScheduler` utilizes an `asyncio.Queue` and dispatches execution tasks concurrently to prevent one slow tool from blocking another.

## Memory Audit
- Verify the `ToolAudit` array does not leak memory. Ensure it contains logic to truncate the log or rotate to disk if it exceeds bounds.

## Internal Test Matrix
1. **Valid Initialization:** Run `test_tool_runtime.py`. (Expect Success).
2. **Schema Generation:** Query schemas. (Expect standard JSON format).
3. **RBAC Rejection:** Dispatch unauthorized tool. (Expect Failure - Permission).
4. **Valid Execution:** Dispatch authorized tool. (Expect Success - Result generated).
5. **Audit Trail:** Check memory logs. (Expect chronological action records).
6. **Telemetry:** Check stdout. (Expect EventBus logs).

## PASS / FAIL Criteria
- **PASS:** The Tool Runtime strictly isolates execution. Unauthorized or malformed calls fail gracefully. Hardware hangs are caught by the timeout wrapper. The main event loop remains unblocked.
- **FAIL:** An invalid JSON payload crashes the executor. A hanging tool freezes the async loop. EventBus telemetry is missing.

## Expected Deliverables
- `PHASE-8.5-VERIFICATION-PLAN.md`
- `PHASE-8.5-VERIFICATION.md`
- Updates to `ENGINEERING-CHANGELOG.md`
