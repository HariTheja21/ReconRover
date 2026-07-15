# Phase 7.3: Speech AI - Implementation Plan

## Executive Summary
Phase 7.3 introduces the Speech AI subsystem into the Recon Rover V2 AI Runtime. This module will allow operators to interact with the rover via voice commands. The subsystem encompasses an end-to-end audio processing pipeline: wake-word detection, speech-to-text (STT), text-to-speech (TTS), and conversation state management. It is designed to be completely model-agnostic, supporting offline Edge models (e.g., Vosk, Whisper.cpp, Piper).

## Objectives
- Build `SpeechRuntime` and `SpeechManager` to orchestrate audio ingestion and TTS output.
- Implement `AudioCapture` to stream microphone bytes asynchronously.
- Develop the inbound audio pipeline: `AudioPreprocessor` -> `WakeWordDetector` -> `VoiceActivityDetector` (VAD) -> `SpeechRecognizer`.
- Develop the conversational memory: `TranscriptManager` and `ConversationContext`.
- Develop the outbound audio pipeline: `TextToSpeech` -> `AudioPostprocessor`.
- Construct `CommandParser` as a fast local fallback to parse rigid commands (e.g., "stop") prior to LLM integration.
- Ensure strict EventBus integration via `SpeechBridge` to route parsed commands to the autonomy stack.

## Architecture
- **Inbound State Machine:** The `SpeechEngine` implements a passive vs active listening state. Initially in passive mode, audio chunks are evaluated by `WakeWordDetector`. Upon detection, it enters active listening, where `VoiceActivityDetector` monitors for the end of the user's sentence before triggering `SpeechRecognizer`.
- **Event Routing:** STT telemetry (latency) goes to `telemetry.speech`. `TranscriptGenerated` and `SpeechCommandParsed` events are routed to `speech.commands` for downstream processing.

## Safety & Constraints
- **Asynchronous Execution:** Heavy models (Whisper/Piper) must not block the main robotic control loop. `SpeechScheduler` manages `audio_queue` and `tts_queue` using Python `asyncio`.
- **Thread Safety:** Audio buffer manipulation is confined to the specific async task handling the engine logic to prevent data corruption.
