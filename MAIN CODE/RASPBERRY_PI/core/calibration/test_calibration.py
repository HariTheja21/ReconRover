import asyncio
import os
import unittest
from unittest.mock import patch

from core.calibration.calibration_manager import CalibrationManager

class TestCalibrationSystem(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self.events_published = []
        def mock_publish(event_name, event_data):
            self.events_published.append((event_name, event_data))
        self.manager = CalibrationManager(mock_publish)

    async def test_full_calibration_success(self):
        success = await self.manager.run_calibration()
        
        self.assertTrue(success)
        self.assertTrue(self.manager.engine.health.is_calibrated)
        self.assertFalse(self.manager.engine.health.critical_failure)
        
        event_names = [e[0] for e in self.events_published]
        self.assertIn("CalibrationStartedEvent", event_names)
        self.assertIn("CalibrationCompletedEvent", event_names)
        
        mapped_events = [e for e in self.events_published if e[0] == "DeviceMappedEvent"]
        self.assertEqual(len(mapped_events), 3) # esp32, camera, lidar
        
        calib_events = [e for e in self.events_published if e[0] == "ComponentCalibratedEvent"]
        self.assertEqual(len(calib_events), 6) # serial, camera, imu, motor, servo, battery

        # Verify file creation
        self.assertTrue(os.path.exists("/tmp/recon_rover_calibration.json"))

    @patch("core.calibration.motor_calibrator.MotorCalibrator.calibrate")
    async def test_calibration_failure(self, mock_motor):
        mock_motor.side_effect = Exception("Motor overcurrent detected")
        
        success = await self.manager.run_calibration()
        
        self.assertFalse(success)
        self.assertFalse(self.manager.engine.health.is_calibrated)
        self.assertTrue(self.manager.engine.health.critical_failure)
        
        event_names = [e[0] for e in self.events_published]
        self.assertIn("CalibrationFailedEvent", event_names)
        self.assertNotIn("CalibrationCompletedEvent", event_names)

if __name__ == "__main__":
    unittest.main()
