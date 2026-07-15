class HealthDashboard {
    constructor() {
        this.grid = document.getElementById('health-grid');
        this.cards = {};
        
        const categories = [
            "System", "Runtime", "ESP32", "Sensors", "Camera", 
            "Communication", "Navigation", "SLAM", "Mission", "Ground Station"
        ];
        
        categories.forEach(cat => this.createCard(cat));
    }
    
    createCard(category) {
        const div = document.createElement('div');
        div.className = 'health-card';
        div.innerHTML = `
            <h3>${category}</h3>
            <span class="status-badge offline">OFFLINE</span>
            <span class="health-msg">Waiting for telemetry...</span>
        `;
        this.grid.appendChild(div);
        this.cards[category] = div;
    }
    
    updateHealth(category, status, message) {
        if(this.cards[category]) {
            const badge = this.cards[category].querySelector('.status-badge');
            const msg = this.cards[category].querySelector('.health-msg');
            
            badge.className = `status-badge ${status.toLowerCase()}`;
            badge.innerText = status;
            msg.innerText = message;
        }
    }
}
