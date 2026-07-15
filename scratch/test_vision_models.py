import asyncio
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'MAIN CODE', 'RASPBERRY_PI'))

from core.ai.runtime.vision.vision_runtime import VisionRuntime

class MockEventBus:
    def publish(self, topic, payload):
        print(f"[EventBus] {topic}: {payload}")

async def main():
    print("Initializing Vision Runtime...")
    bus = MockEventBus()
    runtime = VisionRuntime(bus)
    
    await runtime.initialize()
    
    print("\nLoading YOLO11...")
    success = runtime.loader.load_model("yolo11", "/tmp/yolo.onnx", "cpu")
    print(f"YOLO11 Loaded: {success}")
    
    print("\nRunning Inference...")
    mock_frame = "image_data"
    res = runtime.inference.execute("yolo11", mock_frame, "detection")
    
    if res:
        print(f"Detections: {res.detections}")
        print(f"Latency: {res.latency_ms:.2f}ms")
        runtime.bridge.publish_event("ObjectDetectionUpdated", {
            "detections": res.detections,
            "timestamp": 0.0
        })
        
    print("\nSwitching to Depth Anything...")
    runtime.loader.unload_model("yolo11")
    runtime.loader.load_model("depth_anything", "/tmp/depth.pt", "cpu")
    
    res = runtime.inference.execute("depth_anything", mock_frame, "depth")
    print(f"Depth Inference Latency: {res.latency_ms:.2f}ms")
    
    print("\nTest Complete.")

if __name__ == "__main__":
    asyncio.run(main())
