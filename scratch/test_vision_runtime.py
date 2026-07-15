import asyncio
import sys
import os
import numpy as np

# Adjust path to import from core
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'MAIN CODE', 'RASPBERRY_PI'))

from core.ai.vision.vision_runtime import VisionRuntime

class MockEventBus:
    def publish(self, topic, payload):
        print(f"[EventBus] {topic}: {payload}")

async def main():
    print("Initializing Vision AI Runtime...")
    bus = MockEventBus()
    runtime = VisionRuntime(bus)
    await runtime.initialize()
    
    print("\nLoading YOLOv11 Mock Model...")
    success = runtime.load_model("/models/yolov11n.onnx", "YOLOv11-Nano")
    print(f"Load Success: {success}")
    
    print("\nConfiguring Filters...")
    runtime.set_allowed_classes(["person", "laptop"])
    runtime.set_confidence_threshold(0.6)
    
    print("\nSimulating Camera Feed (3 Frames)...")
    for i in range(3):
        # Create a mock 640x480 RGB frame
        mock_frame = np.zeros((480, 640, 3), dtype=np.uint8)
        print(f"\nProcessing Frame {i+1}...")
        await runtime.process_frame(mock_frame, "YOLOv11-Nano")
        await asyncio.sleep(0.1) # Let the async scheduler process it
        
    print("\nVision Statistics:")
    print(runtime.manager.stats.__dict__)
    
    print("\nUnloading Model...")
    runtime.unload_model()
    
    print("\nTest Complete.")

if __name__ == "__main__":
    asyncio.run(main())
