class GamepadController {
    constructor(commandSender) {
        this.sender = commandSender;
        this.active = false;
        this.interval = null;
    }
    
    activate() {
        this.active = true;
        this.interval = requestAnimationFrame(() => this.loop());
    }
    
    deactivate() {
        this.active = false;
        if(this.interval) cancelAnimationFrame(this.interval);
        this.sender.send("STOP");
    }
    
    loop() {
        if(!this.active) return;
        
        const gamepads = navigator.getGamepads ? navigator.getGamepads() : [];
        const gp = gamepads[0];
        
        if (gp) {
            // Very simplified gamepad mapping for verification
            const axesY = gp.axes[1]; // Left stick Y
            const axesX = gp.axes[2]; // Right stick X
            
            if(axesY < -0.2) this.sender.send("DRIVE_FORWARD", {throttle: Math.abs(axesY) * 100});
            else if(axesY > 0.2) this.sender.send("DRIVE_REVERSE", {throttle: axesY * 100});
            else if(axesX < -0.2) this.sender.send("TURN_LEFT", {throttle: Math.abs(axesX) * 100});
            else if(axesX > 0.2) this.sender.send("TURN_RIGHT", {throttle: axesX * 100});
            else this.sender.send("STOP");
        }
        
        this.interval = requestAnimationFrame(() => this.loop());
    }
}
