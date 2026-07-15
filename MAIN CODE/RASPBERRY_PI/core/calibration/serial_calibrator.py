class SerialCalibrator:
    async def calibrate(self) -> dict:
        # Simulates pinging the ESP32 and calculating latency
        return {"latency_ms": 12, "baud_rate": 115200, "status": "ok"}
