import asyncio
import unittest
from unittest.mock import patch

from backend.dashboard_manager import DashboardManager

class TestDashboardSystem(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self.events_published = []
        def mock_publish(event_name, event_data):
            self.events_published.append((event_name, event_data))
        self.manager = DashboardManager(mock_publish)

    async def test_authentication_and_session(self):
        await self.manager.start_dashboard()
        
        # Test valid login
        req = {"username": "admin", "password": "recon_rover_2026"}
        res = await self.manager.engine.process_login(req, "192.168.1.100")
        
        self.assertTrue(res["success"])
        self.assertIn("token", res)
        self.assertEqual(self.manager.engine.stats.active_sessions, 1)
        
        # Test API access with token
        status = self.manager.engine.api_server.get_status(res["token"])
        self.assertEqual(status["status"], "online")
        
        # Test invalid login
        bad_req = {"username": "admin", "password": "wrong"}
        bad_res = await self.manager.engine.process_login(bad_req, "192.168.1.101")
        
        self.assertFalse(bad_res["success"])
        self.assertEqual(self.manager.engine.stats.failed_logins, 1)
        
        # Test API access without token
        bad_status = self.manager.engine.api_server.get_status("invalid_token")
        self.assertIn("error", bad_status)

    async def test_websocket_routing(self):
        await self.manager.start_dashboard()
        
        # Simulate WS Connect
        await self.manager.engine.ws_manager.connect("mock_ws", "client_1")
        self.assertEqual(len(self.manager.engine.ws_manager.active_connections), 1)
        
        # Simulate incoming command
        msg = {"command": "DRIVE_FORWARD", "payload": {"speed": 50}}
        await self.manager.engine.ws_manager.route_incoming_message("client_1", msg)
        
        # Verify it was published to EventBus wrapper
        cmd_events = [e for e in self.events_published if e[0] == "CommandReceivedEvent"]
        self.assertEqual(len(cmd_events), 1)
        self.assertEqual(cmd_events[0][1]["command"], "DRIVE_FORWARD")
        
        # Simulate WS Disconnect
        self.manager.engine.ws_manager.disconnect("mock_ws", "client_1")
        self.assertEqual(len(self.manager.engine.ws_manager.active_connections), 0)

    async def test_telemetry_bridging(self):
        await self.manager.start_dashboard()
        
        telem_data = {"battery_v": 11.5, "speed": 1.2}
        await self.manager.engine.telemetry_bridge.forward_eventbus_telemetry(telem_data)
        
        bc_events = [e for e in self.events_published if e[0] == "WebsocketBroadcast"]
        self.assertEqual(len(bc_events), 1)
        self.assertEqual(bc_events[0][1]["topic"], "Telemetry")
        self.assertEqual(bc_events[0][1]["data"]["battery_v"], 11.5)

if __name__ == "__main__":
    unittest.main()
