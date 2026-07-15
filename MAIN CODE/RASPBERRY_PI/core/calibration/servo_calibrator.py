class ServoCalibrator:
    async def calibrate(self) -> dict:
        # Simulates moving servos to theoretical center and reading actual position if feedback exists
        return {"pan_center": 90, "tilt_center": 90, "status": "ok"}
