# Phase 7.3: Speech AI - Verification Plan

## Executive Summary
This document defines the verification strategy for Phase 7.3. The objective is to validate the architectural integrity, streaming performance, and logic of the Speech AI Engine, ensuring the `SpeechPipeline` effectively handles continuous audio ingestion, state machine transitions, and text-to-speech synthesis asynchronously without blocking the event loop.

## Verification Objectives
- Validate `SpeechRuntime` initialization and capture callback registration.
- Confirm the `SpeechEngine` accurately transitions from passive listening (Wake Word) to active listening (VAD).
- Verify `TranscriptManager` correctly stores and retrieves chronological conversation history.
- Prove the `CommandParser` successfully matches deterministic keywords (e.g., "stop") and emits a high-confidence parse.
- Validate `SpeechScheduler` correctly queues audio chunks and TTS requests, dropping packets under high load.
- Ensure `SpeechBridge` correctly segregates semantic commands from general telemetry.

## Verification Scope
The scope encompasses all 19 Speech modules located in `MAIN CODE/RASPBERRY_PI/core/ai/speech/` and the scratch test `scratch/test_speech_runtime.py`.

## Audit Strategy
1. **State Machine Audit:** Inject 5 mock audio chunks. Ensure chunks 1-2 trigger `WakeWordDetector` but not STT. Ensure chunk 3 triggers the wake word, transitioning the engine to active mode. Ensure chunk 5 triggers STT after VAD detects silence.
2. **Conversation Context Audit:** Inject an utterance ("move forward"), then synthesize a TTS response ("Moving"). Verify the `TranscriptManager` contains both in exact chronological order with correct speaker IDs ("user" and "rover").
3. **Command Parser Audit:** Pass the string "Please execute an emergency stop immediately" to the `CommandParser`. Verify it correctly extracts the "emergency_stop" command.
4. **Queue Saturation Audit:** Rapidly push 60 audio chunks into the `SpeechScheduler` (maxsize=50). Verify the oldest chunks are dropped without throwing fatal exceptions.

## Runtime Audit
- Ensure that mock latency inside `SpeechRecognizer` and `TextToSpeech` (`time.sleep`) correctly simulates blocking STT/TTS workloads, and that the `asyncio` loop manages them without starving other tasks.

## Memory Audit
- Verify the `audio_queue` size cap (maxsize=50) prevents infinite memory accumulation if the STT engine completely hangs.
- Verify `TranscriptManager` correctly implements a rolling window (e.g., max 50 utterances) to prevent memory leaks during long-running sessions.

## Internal Test Matrix
1. **Valid Initialization:** Run `test_speech_runtime.py`. (Expect Success).
2. **Wake Word Trigger:** Pass mock audio. (Expect State Change).
3. **Queue Overflow:** Inject 100 chunks instantly. (Expect Drops).
4. **Deterministic Parse:** Pass "move forward five meters". (Expect `drive_forward`).

## PASS / FAIL Criteria
- **PASS:** The engine transitions states correctly, tracks transcripts chronologically, parses deterministic commands, and limits memory via bounded queues.
- **FAIL:** The engine runs STT on all audio (missing wake word logic). The event loop hangs during TTS. The transcript grows infinitely.

## Expected Deliverables
- `PHASE-7.3-VERIFICATION-PLAN.md`
- `PHASE-7.3-VERIFICATION.md`
- Updates to `ENGINEERING-CHANGELOG.md`
