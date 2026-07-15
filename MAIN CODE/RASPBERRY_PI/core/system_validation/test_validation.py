import asyncio
import unittest
from unittest.mock import patch

from core.system_validation.validation_manager import ValidationManager

class TestValidationSystem(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self.events_published = []
        def mock_publish(event_name, event_data):
            self.events_published.append((event_name, event_data))
        self.manager = ValidationManager(mock_publish)

    async def test_full_validation_success(self):
        success = await self.manager.run_validation()
        
        self.assertTrue(success)
        self.assertTrue(self.manager.engine.health.is_validated)
        self.assertFalse(self.manager.engine.health.critical_failure)
        
        event_names = [e[0] for e in self.events_published]
        self.assertIn("ValidationStartedEvent", event_names)
        self.assertIn("TestCompletedEvent", event_names)
        self.assertIn("ValidationCompletedEvent", event_names)
        
        completed_events = [e for e in self.events_published if e[0] == "TestCompletedEvent"]
        self.assertEqual(len(completed_events), 5) # 5 scenarios

    @patch("core.system_validation.test_scenarios.TestScenarios.run_command_round_trip")
    async def test_validation_failure(self, mock_scenario):
        mock_scenario.return_value = {"passed": False, "error": "Timeout waiting for ACK", "latency_ms": 500}
        
        success = await self.manager.run_validation()
        
        self.assertFalse(success)
        self.assertFalse(self.manager.engine.health.is_validated)
        self.assertTrue(self.manager.engine.health.critical_failure)
        
        event_names = [e[0] for e in self.events_published]
        self.assertIn("ValidationFailedEvent", event_names)
        self.assertNotIn("ValidationCompletedEvent", event_names)

if __name__ == "__main__":
    unittest.main()
