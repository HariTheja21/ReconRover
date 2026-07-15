# Phase 8.2: Speech & Audio AI Integration - Implementation Plan

## Executive Summary
Phase 8.2 introduces the Speech & Audio AI Integration layer to Recon Rover V2. Building on the core AI Runtime, this phase implements audio stream processing for real-time human-robot interaction. It abstracts away the complexities of Wake Word engines, Speech-to-Text (STT) models like Whisper, and Text-to-Speech (TTS) synthesizers like Piper. The architecture allows continuous non-blocking microphone sampling while pushing parsed intents to the EventBus.

## Objectives
- Build `AudioRuntime`, `AudioRegistry`, and `AudioLoader` for dynamic audio model injection.
- Implement `MicrophoneManager`, `AudioStream`, and `AudioBuffer` for thread-safe ALSA/PulseAudio hardware interfacing.
- Construct `VoiceActivityDetector` (VAD) to filter silence, and `WakeWordDetector` to trigger active listening states.
- Develop `SpeechRecognition` to transcribe bytes into text using `WhisperProvider` or `OpenAI_STTProvider`.
- Create `TextToSpeech` to synthesize voice feedback using `PiperProvider`.
- Build `CommandParser` to do simple regex/intent mapping before hitting the LLM (for basic override commands).
- Wire `AudioBridge` to broadcast `WakeWordDetected`, `SpeechRecognized`, and `TextToSpeechCompleted` to the EventBus.

## Architecture
- **Continuous Loop:** `AudioScheduler` constantly requests chunks from `AudioStream`.
- **Filtering:** Chunks pass through `VoiceActivityDetector`. If silent, they are discarded to save CPU.
- **Wake Word:** If speech is detected, it hits `WakeWordDetector`.
- **Transcription:** Upon wake, the `AudioBuffer` is sent to `SpeechRecognition`.
- **Feedback:** Text responses from the system hit `TextToSpeech` and play out the speaker.

## Safety & Constraints
- **Bandwidth:** Continuous local VAD prevents sending 24/7 audio to cloud STT APIs.
- **Async Streaming:** Audio loops run asynchronously, preventing blocking of the vision or executive threads.
