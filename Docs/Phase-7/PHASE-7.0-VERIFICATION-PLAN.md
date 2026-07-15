# Phase 7.0: AI Runtime Framework - Verification Plan

## Executive Summary
This document outlines the verification strategy for Phase 7.0. The objective is to validate the architectural integrity, memory safety, and logical correctness of the AI Runtime Framework on the Raspberry Pi before integrating live AI models in subsequent phases.

## Verification Objectives
- Validate `AIRuntime` and `AIManager` initialization sequences.
- Confirm `MemoryManager` strictly bounds memory allocations and rejects requests exceeding the 4096MB limit.
- Verify `GPUResourceManager` correctly acquires and releases mocked TPU/GPU locks.
- Ensure `InferenceScheduler` maintains priority queue order (lower integer = higher priority).
- Prove `PromptManager` successfully amalgamates System, Mission, and Vision contexts with Conversation history.
- Validate `ToolExecutor` successfully runs mocked async functions and publishes telemetry.
- Verify `AIBridge` correctly routes generated AI events to the central EventBus.

## Verification Scope
The scope encompasses all 17 modules created within `MAIN CODE/RASPBERRY_PI/core/ai/` and the scratch test suite `scratch/test_ai_runtime.py`.

## Audit Strategy
1. **Resource Bounding Audit:** Register a mock model requiring 5000MB of RAM. Attempt to load it. Verify `ModelManager.load_model()` returns `False` and emits a `FAILED` event without crashing.
2. **Priority Queue Audit:** Push three inference requests with priorities 3, 1, and 2. Pop them from the `InferenceScheduler`. Verify execution order is 1, 2, 3.
3. **Context Assembly Audit:** Update system battery to 50% and vision context to "Person detected". Generate a prompt. Verify both data points are present in the final prompt string.
4. **Tool Execution Audit:** Register a tool that sleeps for 100ms. Execute it. Verify the `ToolExecutionEvent` registers a latency of approximately 100ms.

## Runtime Audit
- Ensure that the `ToolExecutor` wraps callbacks in `asyncio` to prevent long-running AI tools (e.g., motor commands) from blocking the main thread.
- Verify event publication does not throw exceptions if the EventBus is disconnected or saturated.

## Memory Audit
- Verify the `MemoryManager` accurately frees memory when a model is unloaded, returning the allocated count back to 0.

## Internal Test Matrix
1. **Valid Initialization:** Run `test_ai_runtime.py`. (Expect Success).
2. **OOM Simulation:** Request 5GB RAM model. (Expect Clean Failure).
3. **Missing Tool:** Request execution of an unregistered tool. (Expect ValueError).
4. **Context Overflow:** Add 60 messages to Conversation history (Limit 50). (Expect oldest 10 dropped).

## PASS / FAIL Criteria
- **PASS:** The framework successfully guards against memory overallocation, prioritizes inference correctly, and builds accurate context prompts.
- **FAIL:** Memory allocation allows OOM. Tool execution blocks the event loop. The scheduler queue ignores priority.

## Expected Deliverables
- `PHASE-7.0-VERIFICATION-PLAN.md`
- `PHASE-7.0-VERIFICATION.md`
- Updates to `ENGINEERING-CHANGELOG.md`
