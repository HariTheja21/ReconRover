class ActivityFeed {
    constructor() {
        this.feedElement = document.getElementById('activity-feed');
        this.maxItems = 100;
        this.items = [];
    }
    
    addEvent(username, action, details) {
        const d = new Date();
        const timeStr = d.toISOString().split('T')[1].slice(0, 8);
        
        const html = `
            <div class="activity-item">
                <span class="act-time">[${timeStr}]</span>
                <span class="act-user">${username}</span>
                <span class="act-action">${action}</span>
                <span class="act-details">${details}</span>
            </div>
        `;
        
        // Prepend to show newest at top
        this.feedElement.insertAdjacentHTML('afterbegin', html);
        
        // Prune
        while(this.feedElement.children.length > this.maxItems) {
            this.feedElement.removeChild(this.feedElement.lastChild);
        }
    }
}
