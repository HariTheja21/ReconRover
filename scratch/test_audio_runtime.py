import asyncio
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'MAIN CODE', 'RASPBERRY_PI'))

from core.ai.runtime.audio.audio_runtime import AudioRuntime

class MockEventBus:
    def publish(self, topic, payload):
        print(f"[EventBus] {topic}: {payload}")

async def main():
    print("Initializing Audio Runtime...")
    bus = MockEventBus()
    runtime = AudioRuntime(bus)
    
    await runtime.initialize()
    
    print("\nLoading WhisperCPP...")
    success = runtime.loader.load_model("whispercpp", "/tmp/whisper.bin", "cpu")
    print(f"WhisperCPP Loaded: {success}")
    
    print("\nLoading Piper TTS...")
    success = runtime.loader.load_model("piper", "/tmp/piper.onnx", "cpu")
    print(f"Piper TTS Loaded: {success}")
    
    print("\nSimulating Audio Stream...")
    chunk = runtime.stream.read_chunk()
    is_speech = runtime.vad.is_speaking(chunk)
    print(f"VAD Detected Speech: {is_speech}")
    
    wake_detected = runtime.wake.detect(chunk)
    if wake_detected:
        print("Wake Word detected, transcribing...")
        text = runtime.speech.recognize("whispercpp", chunk)
        print(f"Transcription: {text}")
        
        runtime.parser.parse(text)
        
        print("\nSynthesizing TTS response...")
        runtime.tts.speak("Command received", "piper")
    
    print("\nTest Complete.")

if __name__ == "__main__":
    asyncio.run(main())
