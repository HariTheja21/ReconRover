class ImuCalibrator:
    async def calibrate(self) -> dict:
        # Simulates reading 100 samples from IMU and calculating zero-bias offsets
        return {"offset_x": 0.01, "offset_y": -0.02, "offset_z": 9.81, "status": "ok"}
