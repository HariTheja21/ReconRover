class TelemetryBridge:
    def __init__(self, websocket_manager):
        self.ws_manager = websocket_manager

    async def forward_eventbus_telemetry(self, telemetry_data: dict):
        """
        Takes hardware telemetry from the EventBus and broadcasts it to the browser.
        """
        await self.ws_manager.broadcast("Telemetry", telemetry_data)

    async def forward_system_health(self, health_data: dict):
        """
        Forwards CPU, Memory, and Subsystem status to the browser.
        """
        await self.ws_manager.broadcast("System Health", health_data)
