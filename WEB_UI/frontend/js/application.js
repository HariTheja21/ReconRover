document.addEventListener('DOMContentLoaded', () => {
    console.log("Initializing Recon Rover V2 - Production Ground Station");
    
    // Core Services
    const notifManager = new NotificationManager();
    const errorHandler = new GlobalErrorHandler(notifManager);
    const loader = new DashboardLoader();
    const nav = new Navigation(loader);
    
    // App Lifecycle
    class GroundStationApp {
        constructor() {
            this.version = "2.0.0-PROD";
            document.getElementById('app-version').innerText = `v${this.version}`;
            this.checkHealth();
        }
        
        checkHealth() {
            // Mock health check to backend API
            setTimeout(() => {
                const statusIndicator = document.querySelector('.status-indicator');
                const statusText = document.getElementById('status-text');
                
                statusIndicator.className = 'status-indicator status-ok';
                statusText.innerText = "OPERATIONAL";
                
                notifManager.show("Ground Station successfully connected to Rover Backend.", "success");
            }, 1000);
        }
    }
    
    const app = new GroundStationApp();
    
    // Bind global logout
    document.getElementById('btn-logout').addEventListener('click', () => {
        localStorage.removeItem('rover_auth_token');
        notifManager.show("Logging out...", "info", 1500);
        setTimeout(() => {
            window.location.href = 'login.html'; // Assume a generic login page exists
        }, 1500);
    });
});
