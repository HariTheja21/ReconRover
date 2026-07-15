from .stream_engine import StreamEngine

class CameraStreamManager:
    def __init__(self, broadcast_callback):
        self.engine = StreamEngine(broadcast_callback)

    def handle_client_connect(self, client_id: str):
        self.engine.add_viewer(client_id)

    def handle_client_disconnect(self, client_id: str):
        self.engine.remove_viewer(client_id)

    def set_stream_quality(self, client_id: str, quality: int, resolution: tuple):
        # In a more advanced system, quality could be per-client or negotiated. 
        # Here we set global encoder quality.
        self.engine.set_quality(quality, resolution)

    async def ingest_frame(self, frame):
        """
        Subscribed to the EventBus 'CameraFrameEvent'.
        """
        await self.engine.process_raw_frame(frame)
