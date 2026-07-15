class CommandSender {
    constructor() {
        // Mock websocket for architecture phase
        this.connected = true;
    }

    send(command, payload = {}) {
        if (!this.connected) return;
        
        // In real life, JSON.stringify and send over WS
        const packet = {
            topic: "Control",
            data: {
                command: command,
                payload: payload
            }
        };
        
        // Debug output to UI
        const cmdEl = document.getElementById('out-command');
        const thrEl = document.getElementById('out-throttle');
        if(cmdEl) cmdEl.innerText = command;
        if(thrEl) thrEl.innerText = payload.throttle || 0;
        
        // console.log("Transmitting: ", packet);
    }
}
