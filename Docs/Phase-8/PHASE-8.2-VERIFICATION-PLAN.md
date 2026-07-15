# Phase 8.2: Speech & Audio AI Integration - Verification Plan

## Executive Summary
This document outlines the verification strategy for Phase 8.2. The objective is to validate that the Speech & Audio Integration layer effectively streams, processes, and serializes audio data without starving system resources. The pipeline must filter out silence (VAD), accurately detect wake words, transcribe speech, parse intents, and synthesize Text-to-Speech (TTS) responses asynchronously.

## Verification Objectives
- Validate `VoiceActivityDetector` correctly filters silent chunks, preventing the pipeline from sending empty data to transcription models.
- Confirm `WakeWordDetector` accurately triggers the active listening state and broadcasts `WakeWordDetected`.
- Verify `SpeechRecognition` successfully routes buffered audio to dynamically loaded providers (e.g., `WhisperCPPProvider`).
- Prove `TextToSpeech` successfully routes text to `PiperProvider` for local synthesis.
- Ensure `AudioScheduler` runs continuously but yields to the async event loop to maintain thread safety.
- Validate `AudioBridge` correctly routes all JSON payloads to `audio.input`, `audio.output`, and `audio.telemetry`.

## Verification Scope
The scope encompasses all 23 audio integration modules located in `MAIN CODE/RASPBERRY_PI/core/ai/runtime/audio/` and the integration script `scratch/test_audio_runtime.py`.

## Audit Strategy
1. **Model Loading Audit:** Check `AudioLoader` to ensure both STT (Whisper) and TTS (Piper) models can be loaded into memory simultaneously without conflict.
2. **Audio Streaming Audit:** Trigger `MicrophoneManager.start_stream()`. Verify the `AudioStream.read_chunk()` method continuously yields bytes.
3. **Pipeline Logic Audit:** Inject a mock audio chunk containing speech. Ensure it successfully passes `VAD -> Wake Word -> Buffer -> STT`.
4. **Latency Audit:** Verify the time taken for the STT and TTS forward passes are reasonably bounded (simulated in the stubs) so they do not hang the system.
5. **Event Routing Audit:** Monitor the MockEventBus for the exact presence of `WakeWordDetected`, `SpeechRecognized`, and `TextToSpeechCompleted`.

## Runtime Audit
- Ensure that `AudioScheduler.run_audio_loop()` employs `asyncio.sleep()` correctly, proving the microphone polling loop yields control to other systems running on the Pi.

## Memory Audit
- Verify the `AudioBuffer` implements a `.clear()` function that is called after transcription, preventing the buffer from expanding infinitely over a long session.

## Internal Test Matrix
1. **Valid Initialization:** Run `test_audio_runtime.py`. (Expect Success).
2. **Provider Loading:** Load WhisperCPP and Piper. (Expect True).
3. **VAD Filtering:** Inject silence / inject speech. (Expect False / True).
4. **Wake Word Trigger:** Simulate 'recon' phrase. (Expect Wake event).
5. **STT & Parsing:** Transcribe chunk. (Expect SpeechRecognized event).
6. **TTS Synthesis:** Synthesize response. (Expect TextToSpeechCompleted event).

## PASS / FAIL Criteria
- **PASS:** The Audio Runtime flawlessly abstracts microphone IO and ML inference. Silence is filtered, speech is transcribed, and audio is synthesized safely in the background.
- **FAIL:** The `AudioBuffer` leaks memory. The microphone polling blocks the async thread. The EventBus receives malformed JSON.

## Expected Deliverables
- `PHASE-8.2-VERIFICATION-PLAN.md`
- `PHASE-8.2-VERIFICATION.md`
- Updates to `ENGINEERING-CHANGELOG.md`
