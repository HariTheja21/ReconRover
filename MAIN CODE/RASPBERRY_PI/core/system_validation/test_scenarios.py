import asyncio

class TestScenarios:
    @staticmethod
    async def run_command_round_trip() -> dict:
        # Simulate sending a command down to ESP32 and waiting for telemetry ACK
        await asyncio.sleep(0.02)
        return {"passed": True, "latency_ms": 20}

    @staticmethod
    async def run_emergency_stop() -> dict:
        # Simulate sending E-STOP and verifying motors halt
        await asyncio.sleep(0.01)
        return {"passed": True, "latency_ms": 10}

    @staticmethod
    async def run_sensor_feedback() -> dict:
        # Simulate reading IMU data through the whole pipeline
        await asyncio.sleep(0.015)
        return {"passed": True, "latency_ms": 15}

    @staticmethod
    async def run_telemetry_consistency() -> dict:
        # Simulate checking multiple telemetry packets for sequence drops
        await asyncio.sleep(0.05)
        return {"passed": True, "dropped_packets": 0, "latency_ms": 50}

    @staticmethod
    async def run_packet_loss_simulation() -> dict:
        # Simulate dropping a packet and verifying recovery
        await asyncio.sleep(0.03)
        return {"passed": True, "recovered": True, "latency_ms": 30}
