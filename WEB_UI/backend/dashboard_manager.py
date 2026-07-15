import asyncio
from .dashboard_engine import DashboardEngine

class DashboardManager:
    def __init__(self, publish_callback):
        self.publish = publish_callback
        self.engine = DashboardEngine(publish_callback)

    async def start_dashboard(self):
        """
        Entry point to start the Ground Station Web UI Backend.
        """
        await self.engine.start()
