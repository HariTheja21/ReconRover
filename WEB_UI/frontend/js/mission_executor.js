class MissionExecutor {
    constructor() {
        this.statusEl = document.getElementById('mission-status');
    }

    async executeMission(missionId) {
        console.log(`Requesting execution for mission: ${missionId}`);
        // Simulate backend WS execution broadcast
        this.statusEl.innerText = "RUNNING";
        this.statusEl.className = "status-indicator online";
        
        // Mock progress
        setTimeout(() => {
            this.statusEl.innerText = "COMPLETED";
            this.statusEl.className = "status-indicator online";
            setTimeout(() => {
                this.statusEl.innerText = "IDLE";
                this.statusEl.className = "status-indicator offline";
            }, 3000);
        }, 5000);
    }

    async cancelMission() {
        console.log("Cancelling mission...");
        this.statusEl.innerText = "CANCELLED";
        this.statusEl.className = "status-indicator offline";
    }
}
