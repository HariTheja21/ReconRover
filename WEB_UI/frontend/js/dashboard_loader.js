class DashboardLoader {
    constructor() {
        this.iframe = document.getElementById('dashboard-frame');
    }
    
    loadModule(url) {
        // In a real application, you might want a loading spinner here
        console.log(`Loading subsystem: ${url}`);
        this.iframe.src = url;
    }
}
