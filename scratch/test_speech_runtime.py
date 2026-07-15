import asyncio
import sys
import os

# Adjust path to import from core
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'MAIN CODE', 'RASPBERRY_PI'))

from core.ai.speech.speech_runtime import SpeechRuntime

class MockEventBus:
    def publish(self, topic, payload):
        print(f"[EventBus] {topic}: {payload}")

async def main():
    print("Initializing Speech AI Runtime...")
    bus = MockEventBus()
    runtime = SpeechRuntime(bus)
    await runtime.initialize()
    
    print("\nSimulating Voice Interaction...")
    
    # 1. Simulate Wake Word audio
    print("\n--- Sending Wake Word ---")
    # By default, mock WakeWordDetector returns True
    runtime.inject_mock_audio(b"mock_wake_word_audio")
    await asyncio.sleep(0.1) # Let async process
    
    # 2. Simulate Command audio
    print("\n--- Sending Command ---")
    runtime.inject_mock_audio(b"mock_command_audio_move_forward")
    await asyncio.sleep(0.2)
    
    # 3. Simulate TTS Request
    print("\n--- Requesting Speech Synthesis ---")
    await runtime.request_speech("Moving forward five meters.", "default")
    await asyncio.sleep(0.2)
    
    print("\nSpeech Statistics:")
    print(runtime.manager.stats.__dict__)
    
    print("\nRecent Transcripts:")
    for t in runtime.manager.transcript.get_recent():
        print(f"[{t['speaker']}] {t['text']}")
        
    print("\nTest Complete.")

if __name__ == "__main__":
    asyncio.run(main())
