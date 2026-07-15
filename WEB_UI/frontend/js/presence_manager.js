class PresenceManager {
    constructor() {
        this.listElement = document.getElementById('operator-list');
        this.operators = {};
    }
    
    updatePresence(operatorId, username, role, status) {
        this.operators[operatorId] = { username, role, status };
        this.render();
    }
    
    render() {
        this.listElement.innerHTML = '';
        for (const [id, op] of Object.entries(this.operators)) {
            const li = document.createElement('li');
            li.className = 'operator-item';
            
            let statusClass = 'status-offline';
            if(op.status === 'ONLINE') statusClass = 'status-online';
            if(op.status === 'IDLE') statusClass = 'status-idle';
            
            li.innerHTML = `
                <div class="status-dot ${statusClass}"></div>
                <div class="operator-info">
                    <span class="operator-name">${op.username}</span>
                    <span class="operator-role">${op.role}</span>
                </div>
            `;
            this.listElement.appendChild(li);
        }
    }
}
