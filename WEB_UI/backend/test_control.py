import unittest
import time
from backend.control_manager import ControlManager

class TestControlSystem(unittest.TestCase):
    def setUp(self):
        self.events_published = []
        def mock_publish(event_name, event_data):
            self.events_published.append((event_name, event_data))
        self.manager = ControlManager(mock_publish)

    def test_valid_command_routing(self):
        success = self.manager.process_incoming_command("client_1", "DRIVE_FORWARD", {"throttle": 50})
        self.assertTrue(success)
        self.assertEqual(len(self.events_published), 1)
        self.assertEqual(self.events_published[0][0], "OperatorCommandEvent")
        self.assertEqual(self.manager.stats.commands_routed, 1)

    def test_invalid_command_rejection(self):
        # Invalid command name
        success = self.manager.process_incoming_command("client_1", "FLY_UP", {"throttle": 50})
        self.assertFalse(success)
        
        # Invalid payload (throttle out of bounds)
        success = self.manager.process_incoming_command("client_1", "DRIVE_FORWARD", {"throttle": 150})
        self.assertFalse(success)
        
        self.assertEqual(self.manager.stats.commands_rejected, 2)

    def test_control_ownership(self):
        # Client 1 takes control
        self.manager.process_incoming_command("client_1", "DRIVE_FORWARD", {"throttle": 50})
        self.assertEqual(self.manager.router.active_controller_id, "client_1")
        
        # Client 2 tries to control
        success = self.manager.process_incoming_command("client_2", "DRIVE_REVERSE", {"throttle": 50})
        self.assertFalse(success) # Rejected due to ownership

    def test_rate_limiting(self):
        # Fire 30 commands instantly (limit is 20/sec)
        for _ in range(30):
            self.manager.process_incoming_command("client_1", "DRIVE_FORWARD", {"throttle": 50})
            
        self.assertTrue(self.manager.stats.commands_rate_limited > 0)
        self.assertTrue(self.manager.stats.commands_routed <= 20)

    def test_emergency_stop_bypass(self):
        # Client 1 takes control
        self.manager.process_incoming_command("client_1", "DRIVE_FORWARD", {"throttle": 50})
        
        # Client 2 issues ESTOP (should bypass ownership and rate limits)
        success = self.manager.process_incoming_command("client_2", "EMERGENCY_STOP", {})
        self.assertTrue(success)
        
        estop_events = [e for e in self.events_published if e[0] == "EmergencyStopEvent"]
        self.assertEqual(len(estop_events), 1)

    def test_disconnect_safety(self):
        # Client 1 takes control
        self.manager.process_incoming_command("client_1", "DRIVE_FORWARD", {"throttle": 50})
        
        # Client 1 disconnects
        self.manager.handle_client_disconnect("client_1")
        
        estop_events = [e for e in self.events_published if e[0] == "EmergencyStopEvent"]
        self.assertEqual(len(estop_events), 1)
        self.assertEqual(estop_events[0][1].reason, "Driver Disconnected")
        self.assertIsNone(self.manager.router.active_controller_id)

if __name__ == "__main__":
    unittest.main()
