from typing import List, Callable, Dict, Any

class WebsocketManager:
    def __init__(self, publish_callback: Callable):
        self.publish = publish_callback
        self.active_connections: List[Any] = [] # In real FastAPI, List[WebSocket]

    async def connect(self, websocket: Any, client_id: str):
        # await websocket.accept()
        self.active_connections.append(websocket)
        self.publish("ClientConnectedEvent", {"client_id": client_id})

    def disconnect(self, websocket: Any, client_id: str):
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)
            self.publish("ClientDisconnectedEvent", {"client_id": client_id})

    async def broadcast(self, topic: str, data: dict):
        payload = {"topic": topic, "data": data}
        # for connection in self.active_connections:
        #     await connection.send_json(payload)
        self.publish("WebsocketBroadcast", payload)
        
    async def route_incoming_message(self, client_id: str, message: dict):
        # Routes commands from WS to the EventBus
        cmd = message.get("command")
        payload = message.get("payload", {})
        if cmd:
            self.publish("CommandReceivedEvent", {"client_id": client_id, "command": cmd, "payload": payload})
