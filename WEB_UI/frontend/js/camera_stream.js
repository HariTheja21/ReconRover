document.addEventListener('DOMContentLoaded', () => {
    console.log("Initializing Camera Stream Interface...");
    
    const stats = new StreamStatistics();
    const renderer = new StreamRenderer(stats);
    
    // Mock WebSocket connection logic
    const sendStreamCommand = (cmd) => {
        console.log("Stream Command Issued:", cmd);
    };
    
    const controls = new StreamControls(sendStreamCommand);
    
    // Architectural Verification: Simulate incoming JPEG frames
    setInterval(() => {
        if(controls.isStreaming) {
            // Generate a fake blank JPEG blob for testing renderer pipeline
            const canvas = document.createElement('canvas');
            canvas.width = 640;
            canvas.height = 480;
            const ctx = canvas.getContext('2d');
            ctx.fillStyle = `rgb(${Math.random()*50}, ${Math.random()*50}, ${Math.random()*50})`;
            ctx.fillRect(0, 0, 640, 480);
            
            canvas.toBlob((blob) => {
                renderer.renderFrame(blob, 640, 480, (Date.now() / 1000) - 0.05); // Simulated 50ms latency
            }, 'image/jpeg', 0.8);
        }
    }, 1000 / 15); // Simulate 15 FPS
});
