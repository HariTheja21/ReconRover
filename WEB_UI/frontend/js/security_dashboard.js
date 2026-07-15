document.addEventListener('DOMContentLoaded', () => {
    console.log("Initializing Security & Access Control Dashboard...");
    
    const session = new SessionSecurity();
    const audit = new AuditViewer();
    
    // Bind UI actions
    document.getElementById('btn-refresh-token').addEventListener('click', () => {
        session.refreshToken();
    });
    
    document.getElementById('btn-logout').addEventListener('click', () => {
        session.logout("User requested logout");
    });
    
    // Simulating incoming malicious activity
    setTimeout(() => {
        audit.addLog("unknown", "LOGIN_ATTEMPT", "GroundStation", "FAILED");
    }, 3000);
    setTimeout(() => {
        audit.addLog("unknown", "LOGIN_ATTEMPT", "GroundStation", "FAILED - ACCOUNT LOCKED");
    }, 4000);
});
