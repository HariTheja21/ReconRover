document.addEventListener('DOMContentLoaded', () => {
    console.log("Initializing Dashboard...");
    
    const themeManager = new ThemeManager();
    const notificationManager = new NotificationManager();
    const widgetManager = new WidgetManager();
    const telemetryRenderer = new TelemetryRenderer(widgetManager);
    
    const wsClient = new WebsocketClient(
        'ws://localhost:8000/ws',
        telemetryRenderer,
        notificationManager,
        widgetManager
    );
    
    // Simulate incoming data for architectural verification
    setInterval(() => {
        const mockData = {
            data: JSON.stringify({
                topic: "Telemetry",
                data: {
                    battery: Math.random() * 20 + 80,
                    cpu: Math.random() * 40 + 10,
                    ram: Math.random() * 10 + 40,
                    mode: "AUTONOMOUS",
                    mission: "WAYPOINT NAV",
                    safety: "SAFE",
                    esp32_status: "CONNECTED",
                    camera_status: "STREAMING"
                }
            })
        };
        wsClient.onMessage(mockData);
    }, 1000);
});
