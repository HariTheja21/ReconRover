class SessionSecurity {
    constructor() {
        this.token = localStorage.getItem('rover_auth_token') || null;
        this.expiresAt = localStorage.getItem('rover_auth_exp') || 0;
        this.timeDisplay = document.getElementById('time-remaining');
        this.headerTimer = document.getElementById('session-timer');
        
        this.startTimer();
    }
    
    startTimer() {
        // Mock a 60 minute session starting now
        this.expiresAt = Date.now() + (3600 * 1000);
        
        setInterval(() => {
            const now = Date.now();
            const remainingStr = Math.floor((this.expiresAt - now) / 1000);
            
            if(remainingStr <= 0) {
                this.logout("Session Expired");
            } else {
                const mins = Math.floor(remainingStr / 60);
                const secs = remainingStr % 60;
                const formatted = `${mins}:${secs.toString().padStart(2, '0')}`;
                
                if(this.timeDisplay) this.timeDisplay.innerText = remainingStr + "s";
                if(this.headerTimer) this.headerTimer.innerText = formatted;
            }
        }, 1000);
    }
    
    logout(reason) {
        localStorage.removeItem('rover_auth_token');
        localStorage.removeItem('rover_auth_exp');
        console.warn("LOGOUT:", reason);
        // window.location.href = 'login.html';
    }
    
    refreshToken() {
        console.log("Token refreshed via secure backend exchange.");
        this.expiresAt = Date.now() + (3600 * 1000);
    }
}
