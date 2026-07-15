# Phase 8.3: LLM Provider Integration - Verification Plan

## Executive Summary
This document outlines the verification strategy for Phase 8.3. The objective is to validate that the LLM Integration layer securely manages API keys, maintains cross-provider conversation history, streams outputs asynchronously, and reliably executes failovers from cloud to local endpoints without starving the underlying OS event loop.

## Verification Objectives
- Validate `ProviderManager` accurately caches and applies API keys via `AuthenticationManager` upon provider activation.
- Confirm `LLMScheduler` correctly handles concurrent async generation requests.
- Verify `ProviderFailover` correctly catches generated exceptions (e.g., TimeoutError) and reroutes the context seamlessly to the next defined fallback provider.
- Prove `SessionManager` securely segregates context buffers by `session_id`.
- Ensure `StreamingManager` yields tokens progressively without locking the main thread.
- Validate `LLMBridge` correctly routes all JSON payloads to `llm.inference` and `llm.telemetry`.

## Verification Scope
The scope encompasses all 26 LLM integration modules located in `MAIN CODE/RASPBERRY_PI/core/ai/runtime/llm/` and the integration script `scratch/test_llm_providers.py`.

## Audit Strategy
1. **Model Loading & Auth Audit:** Instruct `ProviderManager` to load OpenAI. Check if `is_authenticated` flips to true only after reading the valid mock key.
2. **Context Persistence Audit:** Submit a prompt. Ensure the `ResponseParser` output is automatically appended back into the `SessionManager` arrays, preserving the LLM's memory.
3. **Failover Logic Audit:** Mock an exception in the primary provider. Verify `execute_with_failover` automatically catches it and returns the output from the secondary provider.
4. **Asynchronous Streaming Audit:** Check if the `BaseProvider.stream()` implementations utilize `async yield`, allowing the event loop to breathe between token generation.
5. **Event Routing Audit:** Monitor the MockEventBus for the exact presence of `LLMResponseReceived` and `ProviderChanged`.

## Runtime Audit
- Ensure that `LLMScheduler` utilizes an `asyncio.Queue`, processing inferences asynchronously to prevent a 2-second cloud API call from freezing the robot's hardware controllers.

## Memory Audit
- Verify the `SessionManager` allows for eventual context truncation, ensuring the `[{"role": "user"}]` array doesn't exponentially leak RAM over a 10-hour deployment.

## Internal Test Matrix
1. **Valid Initialization:** Run `test_llm_providers.py`. (Expect Success).
2. **Authentication:** Set key for OpenAI. (Expect True).
3. **Queue Submission:** Submit prompt to Scheduler. (Expect Queue Size > 0).
4. **Generation & Memory:** Process queue. (Expect Session updated with Response).
5. **Failover Simulation:** Trigger fake timeout. (Expect output from Ollama).
6. **Streaming Simulation:** Trigger stream. (Expect progressive chunks).

## PASS / FAIL Criteria
- **PASS:** The LLM Runtime flawlessly abstracts 7 different inference backends. Failovers occur silently. Context is perfectly maintained. The thread never blocks.
- **FAIL:** The `SessionManager` mixes context between IDs. A network timeout freezes the robot. The EventBus receives malformed JSON.

## Expected Deliverables
- `PHASE-8.3-VERIFICATION-PLAN.md`
- `PHASE-8.3-VERIFICATION.md`
- Updates to `ENGINEERING-CHANGELOG.md`
