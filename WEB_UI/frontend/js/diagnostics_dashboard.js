document.addEventListener('DOMContentLoaded', () => {
    console.log("Initializing Diagnostics Dashboard...");
    
    const logViewer = new LogViewer();
    const healthDash = new HealthDashboard();
    const perfDash = new PerformanceDashboard();
    const reportGen = new ReportGenerator();
    
    // Simulate incoming data for architectural verification
    setInterval(() => {
        const levels = ["INFO", "DEBUG", "WARNING"];
        const sources = ["Navigation", "Camera", "System", "MissionManager"];
        logViewer.appendLog({
            timestamp: Date.now() / 1000,
            level: levels[Math.floor(Math.random() * levels.length)],
            source: sources[Math.floor(Math.random() * sources.length)],
            message: "Routine heartbeat check."
        });
    }, 2000);
    
    setTimeout(() => {
        healthDash.updateHealth("System", "OK", "Running nominally");
        healthDash.updateHealth("Camera", "OK", "Streaming at 30 FPS");
        healthDash.updateHealth("Sensors", "WARNING", "Lidar dusty");
        
        perfDash.updateMetrics({
            cpu_usage: 45.2,
            memory_usage: 60.1,
            temperature: 55.4,
            network_rx: 1500000,
            network_tx: 200000
        });
    }, 1000);
});
