# Phase 7.8: LLM Intelligence Engine - Verification Plan

## Executive Summary
This document establishes the verification strategy for Phase 7.8. The objective is to validate that the LLM Intelligence Engine accurately retrieves contextual memory, processes prompts asynchronously through abstracted model providers, truncates context safely, and effectively triggers downstream tools or agent dispatches without blocking the core robotic operating system.

## Verification Objectives
- Validate `ModelRegistry` successfully isolates proprietary LLM APIs from the core runtime via the `ModelProvider` abstraction.
- Confirm `PromptBuilder` effectively synthesizes User Input + Conversation History + Memory + Spatial Context into a single RAG payload.
- Verify `TokenManager` successfully truncates lengthy conversations, preventing memory overflow or API rejection.
- Prove `SafetyManager` intercepts and flags malicious or malformed inputs and outputs.
- Validate `AgentOrchestrator` and `ToolExecutor` successfully map string-based responses into internal Python executions.
- Ensure `LLMBridge` serializes execution telemetry to the EventBus.

## Verification Scope
The scope covers the 23 LLM modules located in `MAIN CODE/RASPBERRY_PI/core/ai/llm/` and the integration script `scratch/test_llm_runtime.py`.

## Audit Strategy
1. **Model Abstraction Audit:** Instantiate a `MockProvider`, register it in the `ModelRegistry`, and verify `LLMEngine` executes it without throwing errors regarding missing OpenAI/Ollama libraries.
2. **Context Window Audit:** Inject 50 messages into the `ConversationManager`. Call `TokenManager.truncate_history()` and verify only the latest `N` messages are retained.
3. **Safety Audit:** Send a prompt that intentionally triggers `SafetyManager.validate_prompt(text) == False`. Verify the engine rejects the prompt and increments `stats.errors_encountered`.
4. **Tool Execution Audit:** Register a stub tool `get_battery()` in `ToolExecutor`. Call `execute("get_battery", {})` and verify it fires correctly.
5. **Event Routing Audit:** Submit a prompt to the runtime and verify the mock EventBus receives `ReasoningStarted` and `ReasoningCompleted` JSON payloads.

## Runtime Audit
- Ensure `LLMScheduler.run_llm_loop()` properly awaits `asyncio.Queue.get()`, preventing the thread from spinning at 100% CPU when no user prompts are active.

## Memory Audit
- Verify the `SessionManager` and `ConversationManager` successfully release memory when `clear_conversation()` is called, preventing long-term memory leaks.

## Internal Test Matrix
1. **Valid Initialization:** Run `test_llm_runtime.py`. (Expect Success).
2. **Safety Rejection:** Trigger `SafetyManager` fail. (Expect Error string).
3. **Token Truncation:** Overload history. (Expect Truncated array).
4. **Tool Invocation:** Execute mock tool. (Expect Execution result).

## PASS / FAIL Criteria
- **PASS:** The RAG pipeline builds successfully, the provider processes the text asynchronously, the conversation history updates, memory bounds are respected, and events are published.
- **FAIL:** The `LLMEngine` blocks the `asyncio` event loop during generation. The `TokenManager` fails to truncate, causing memory explosion. The `ModelRegistry` enforces proprietary API lock-in.

## Expected Deliverables
- `PHASE-7.8-VERIFICATION-PLAN.md`
- `PHASE-7.8-VERIFICATION.md`
- Updates to `ENGINEERING-CHANGELOG.md`
