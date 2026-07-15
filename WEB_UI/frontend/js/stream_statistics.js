class StreamStatistics {
    constructor() {
        this.elFps = document.getElementById('osd-fps');
        this.elLatency = document.getElementById('osd-latency');
        this.elRes = document.getElementById('stat-res');
        this.elBitrate = document.getElementById('stat-bitrate');
        this.elDropped = document.getElementById('stat-dropped');
        
        this.framesReceived = 0;
        this.bytesReceived = 0;
        this.lastTime = performance.now();
        
        setInterval(() => this.updateDisplay(), 1000);
    }
    
    recordFrame(byteLength, width, height, latency) {
        this.framesReceived++;
        this.bytesReceived += byteLength;
        this.elRes.innerText = `${width}x${height}`;
        this.elLatency.innerText = `${latency.toFixed(1)} ms`;
    }
    
    recordDrop() {
        this.elDropped.innerText = parseInt(this.elDropped.innerText) + 1;
    }
    
    updateDisplay() {
        const now = performance.now();
        const delta = (now - this.lastTime) / 1000;
        
        const fps = this.framesReceived / delta;
        const kbps = (this.bytesReceived * 8) / 1000 / delta;
        
        this.elFps.innerText = `${fps.toFixed(1)} FPS`;
        this.elBitrate.innerText = kbps.toFixed(0);
        
        this.framesReceived = 0;
        this.bytesReceived = 0;
        this.lastTime = now;
    }
}
