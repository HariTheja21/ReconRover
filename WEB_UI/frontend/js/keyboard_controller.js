class KeyboardController {
    constructor(commandSender) {
        this.sender = commandSender;
        this.active = false;
        
        document.addEventListener('keydown', (e) => this.handleKeyDown(e));
        document.addEventListener('keyup', (e) => this.handleKeyUp(e));
        
        this.keys = { w: false, a: false, s: false, d: false };
        this.interval = null;
    }
    
    activate() {
        this.active = true;
        this.interval = setInterval(() => this.loop(), 100);
    }
    
    deactivate() {
        this.active = false;
        if(this.interval) clearInterval(this.interval);
        this.sender.send("STOP");
    }
    
    handleKeyDown(e) {
        if(!this.active) return;
        const key = e.key.toLowerCase();
        if(this.keys.hasOwnProperty(key)) this.keys[key] = true;
    }
    
    handleKeyUp(e) {
        if(!this.active) return;
        const key = e.key.toLowerCase();
        if(this.keys.hasOwnProperty(key)) {
            this.keys[key] = false;
            if(!this.keys.w && !this.keys.s && !this.keys.a && !this.keys.d) {
                this.sender.send("STOP");
            }
        }
    }
    
    loop() {
        if(!this.active) return;
        
        if(this.keys.w && !this.keys.a && !this.keys.d) this.sender.send("DRIVE_FORWARD", {throttle: 50});
        else if(this.keys.s && !this.keys.a && !this.keys.d) this.sender.send("DRIVE_REVERSE", {throttle: 50});
        else if(this.keys.a) this.sender.send("TURN_LEFT", {throttle: 50});
        else if(this.keys.d) this.sender.send("TURN_RIGHT", {throttle: 50});
    }
}
