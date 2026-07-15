class StreamControls {
    constructor(wsCallback) {
        this.btnToggle = document.getElementById('btn-toggle-stream');
        this.selectQuality = document.getElementById('select-quality');
        this.btnSnapshot = document.getElementById('btn-snapshot');
        this.statusIndicator = document.getElementById('stream-status');
        
        this.wsCallback = wsCallback; // Function to send commands back
        this.isStreaming = false;
        
        this.btnToggle.addEventListener('click', () => this.toggleStream());
        this.selectQuality.addEventListener('change', () => this.changeQuality());
        this.btnSnapshot.addEventListener('click', () => this.takeSnapshot());
    }
    
    toggleStream() {
        this.isStreaming = !this.isStreaming;
        if(this.isStreaming) {
            this.btnToggle.innerText = "Stop Stream";
            this.btnToggle.style.backgroundColor = "var(--status-error)";
            this.statusIndicator.innerText = "Stream Active";
            this.statusIndicator.className = "status-indicator online";
            this.btnSnapshot.disabled = false;
            this.wsCallback({command: "START_STREAM", quality: this.selectQuality.value});
        } else {
            this.btnToggle.innerText = "Start Stream";
            this.btnToggle.style.backgroundColor = "var(--accent-blue)";
            this.statusIndicator.innerText = "Stream Offline";
            this.statusIndicator.className = "status-indicator offline";
            this.btnSnapshot.disabled = true;
            this.wsCallback({command: "STOP_STREAM"});
        }
    }
    
    changeQuality() {
        if(this.isStreaming) {
            this.wsCallback({command: "CHANGE_QUALITY", quality: this.selectQuality.value});
        }
    }
    
    takeSnapshot() {
        const canvas = document.getElementById('video-canvas');
        const dataURL = canvas.toDataURL('image/jpeg', 1.0);
        const a = document.createElement('a');
        a.href = dataURL;
        a.download = `recon-rover-snapshot-${Date.now()}.jpg`;
        a.click();
    }
}
