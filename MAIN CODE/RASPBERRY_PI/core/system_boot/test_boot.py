import asyncio
import os
import unittest
from unittest.mock import patch

from core.system_boot.boot_manager import BootManager

class TestBootSystem(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self.events_published = []
        def mock_publish(event_name, event_data):
            self.events_published.append((event_name, event_data))
        self.manager = BootManager(mock_publish)

    @patch("core.system_boot.hardware_discovery.os.path.exists")
    async def test_cold_boot_success(self, mock_exists):
        # Mock /dev/ttyUSB0 and /dev/video0 existing
        mock_exists.side_effect = lambda x: True
        
        success = await self.manager.start_system()
        
        self.assertTrue(success)
        self.assertTrue(self.manager.engine.health.is_booted)
        self.assertFalse(self.manager.engine.health.critical_failure)
        
        # Verify events
        event_names = [e[0] for e in self.events_published]
        self.assertIn("BootStartedEvent", event_names)
        self.assertIn("BootCompletedEvent", event_names)
        
        # Total sequence length is 16
        started_events = [e for e in self.events_published if e[0] == "SubsystemStartedEvent"]
        self.assertEqual(len(started_events), 16)

    @patch("core.system_boot.hardware_discovery.os.path.exists")
    async def test_esp32_disconnected(self, mock_exists):
        # Mock /dev/ttyUSB0 missing, but /dev/video0 existing
        mock_exists.side_effect = lambda x: x == "/dev/video0"
        
        success = await self.manager.start_system()
        
        self.assertFalse(success)
        self.assertFalse(self.manager.engine.health.is_booted)
        self.assertTrue(self.manager.engine.health.critical_failure)
        
        event_names = [e[0] for e in self.events_published]
        self.assertIn("BootFailedEvent", event_names)
        self.assertNotIn("BootCompletedEvent", event_names)

    @patch("core.system_boot.hardware_discovery.os.path.exists")
    async def test_camera_disconnected(self, mock_exists):
        # Mock /dev/ttyUSB0 existing, but /dev/video0 missing
        mock_exists.side_effect = lambda x: x == "/dev/ttyUSB0"
        
        success = await self.manager.start_system()
        
        self.assertFalse(success)
        self.assertFalse(self.manager.engine.health.is_booted)
        self.assertTrue(self.manager.engine.health.critical_failure)
        
        event_names = [e[0] for e in self.events_published]
        self.assertIn("BootFailedEvent", event_names)
        self.assertNotIn("BootCompletedEvent", event_names)

if __name__ == "__main__":
    unittest.main()
