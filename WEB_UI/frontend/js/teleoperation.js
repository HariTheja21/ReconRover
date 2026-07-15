document.addEventListener('DOMContentLoaded', () => {
    console.log("Initializing Teleoperation Interface...");
    
    const sender = new CommandSender();
    
    const keyboard = new KeyboardController(sender);
    const gamepad = new GamepadController(sender);
    const virtual = new VirtualJoystick(sender);
    
    const stateManager = new ControlStateManager(sender, keyboard, gamepad, virtual);
    
    // Emergency Stop
    document.getElementById('btn-estop').addEventListener('click', () => {
        sender.send("EMERGENCY_STOP");
        console.warn("EMERGENCY STOP ISSUED");
    });
    
    // Simulate connection for testing
    setTimeout(() => {
        document.getElementById('connection-status').innerText = 'Online';
        document.getElementById('connection-status').className = 'status-indicator online';
    }, 500);
});
