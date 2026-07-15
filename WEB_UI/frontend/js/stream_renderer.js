class StreamRenderer {
    constructor(stats) {
        this.canvas = document.getElementById('video-canvas');
        this.ctx = this.canvas.getContext('2d');
        this.stats = stats;
    }
    
    renderFrame(blob, width, height, txTimestamp) {
        const img = new Image();
        img.onload = () => {
            if(this.canvas.width !== width || this.canvas.height !== height) {
                this.canvas.width = width;
                this.canvas.height = height;
            }
            this.ctx.drawImage(img, 0, 0, width, height);
            
            // Calc approximate latency
            const rxTimestamp = Date.now() / 1000;
            const latencyMs = (rxTimestamp - txTimestamp) * 1000;
            
            this.stats.recordFrame(blob.size, width, height, latencyMs);
            URL.revokeObjectURL(img.src);
        };
        img.onerror = () => {
            this.stats.recordDrop();
            URL.revokeObjectURL(img.src);
        };
        img.src = URL.createObjectURL(blob);
    }
}
