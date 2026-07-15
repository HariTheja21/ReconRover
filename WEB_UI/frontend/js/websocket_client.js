class WebsocketClient {
    constructor(url, telemetryRenderer, notificationManager, widgetManager) {
        this.url = url;
        this.tr = telemetryRenderer;
        this.nm = notificationManager;
        this.wm = widgetManager;
        this.ws = null;
        this.reconnectInterval = 3000;
        
        this.connect();
    }
    
    connect() {
        this.nm.addNotification("Connecting to WebSocket...", "info");
        // In a real browser, this would be new WebSocket(this.url)
        // Simulating the connection wrapper
        this.ws = {
            send: (data) => console.log("Sent: ", data),
            close: () => { this.onClose(); }
        };
        
        // Simulate immediate connection success for testing architecture
        setTimeout(() => this.onOpen(), 500);
    }
    
    onOpen() {
        this.wm.setConnectionState(true);
        this.nm.addNotification("WebSocket Connected.", "success");
    }
    
    onClose() {
        this.wm.setConnectionState(false);
        this.nm.addNotification("WebSocket Disconnected. Reconnecting...", "warn");
        setTimeout(() => this.connect(), this.reconnectInterval);
    }
    
    onMessage(event) {
        try {
            const payload = JSON.parse(event.data);
            if(payload.topic === "Telemetry" || payload.topic === "System Health") {
                this.tr.processTelemetry(payload.data);
            } else if (payload.topic === "Notification") {
                this.nm.addNotification(payload.data.message);
            }
        } catch (e) {
            console.error("Failed to parse WS message", e);
        }
    }
    
    sendCommand(cmd, payload) {
        if(this.ws) {
            this.ws.send(JSON.stringify({command: cmd, payload: payload}));
        }
    }
}
