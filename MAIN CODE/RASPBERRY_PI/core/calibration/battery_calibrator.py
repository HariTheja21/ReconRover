class BatteryCalibrator:
    async def calibrate(self) -> dict:
        # Simulates reading raw ADC value and applying multiplier
        return {"voltage_multiplier": 0.024, "measured_v": 11.8, "status": "ok"}
