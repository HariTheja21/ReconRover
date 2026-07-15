class GlobalErrorHandler {
    constructor(notifManager) {
        this.notifManager = notifManager;
        this.bindGlobalHandlers();
    }
    
    bindGlobalHandlers() {
        window.addEventListener('error', (event) => {
            console.error("Global Error Caught:", event.error);
            this.notifManager.show(`System Error: ${event.message}`, 'error');
        });
        
        window.addEventListener('unhandledrejection', (event) => {
            console.error("Unhandled Promise Rejection:", event.reason);
            this.notifManager.show(`Async Error: ${event.reason}`, 'error');
        });
    }
}
