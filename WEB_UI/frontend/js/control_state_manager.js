class ControlStateManager {
    constructor(sender, keyboard, gamepad, virtual) {
        this.sender = sender;
        this.keyboard = keyboard;
        this.gamepad = gamepad;
        this.virtual = virtual;
        
        this.btnKeyboard = document.getElementById('mode-keyboard');
        this.btnGamepad = document.getElementById('mode-gamepad');
        this.btnVirtual = document.getElementById('mode-virtual');
        
        this.btnKeyboard.addEventListener('click', () => this.setMode('keyboard'));
        this.btnGamepad.addEventListener('click', () => this.setMode('gamepad'));
        this.btnVirtual.addEventListener('click', () => this.setMode('virtual'));
        
        // Default
        this.setMode('keyboard');
    }
    
    setMode(mode) {
        this.keyboard.deactivate();
        this.gamepad.deactivate();
        this.virtual.deactivate();
        
        this.btnKeyboard.classList.remove('active');
        this.btnGamepad.classList.remove('active');
        this.btnVirtual.classList.remove('active');
        
        if (mode === 'keyboard') {
            this.keyboard.activate();
            this.btnKeyboard.classList.add('active');
        } else if (mode === 'gamepad') {
            this.gamepad.activate();
            this.btnGamepad.classList.add('active');
        } else if (mode === 'virtual') {
            this.virtual.activate();
            this.btnVirtual.classList.add('active');
        }
    }
}
