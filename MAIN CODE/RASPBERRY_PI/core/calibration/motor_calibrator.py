class MotorCalibrator:
    async def calibrate(self) -> dict:
        # Simulates a brief pulse to check motor polarity/current draw
        return {"left_polarity": 1, "right_polarity": 1, "status": "ok"}
