class AuditViewer {
    constructor() {
        this.tableBody = document.getElementById('audit-table-body');
        this.logs = [];
        this.loadMockData();
    }
    
    loadMockData() {
        this.addLog("admin", "LOGIN_ATTEMPT", "GroundStation", "SUCCESS");
        this.addLog("pilot_1", "LOGIN_ATTEMPT", "GroundStation", "FAILED");
        this.addLog("pilot_1", "LOGIN_ATTEMPT", "GroundStation", "FAILED");
        this.addLog("admin", "AUTHORIZATION_CHECK", "OTA", "GRANTED");
        this.addLog("observer_1", "AUTHORIZATION_CHECK", "DRIVE", "DENIED");
    }
    
    addLog(actor, action, target, result) {
        const d = new Date();
        const timeStr = d.toISOString().split('T')[1].slice(0, 8);
        
        const resultClass = (result === "SUCCESS" || result === "GRANTED") ? "status-ok" : "status-error";
        
        const tr = document.createElement('tr');
        tr.innerHTML = `
            <td>${timeStr}</td>
            <td>${actor}</td>
            <td>${action}</td>
            <td>${target}</td>
            <td class="${resultClass}">${result}</td>
        `;
        
        this.tableBody.prepend(tr);
    }
}
