class WidgetManager {
    constructor() {
        // Map DOM elements once for fast updates
        this.elements = {
            battery_val: document.getElementById('val-battery'),
            battery_bar: document.getElementById('bar-battery'),
            cpu_val: document.getElementById('val-cpu'),
            cpu_bar: document.getElementById('bar-cpu'),
            ram_val: document.getElementById('val-ram'),
            ram_bar: document.getElementById('bar-ram'),
            mode_val: document.getElementById('val-mode'),
            mission_val: document.getElementById('val-mission'),
            safety_val: document.getElementById('val-safety'),
            esp32_val: document.getElementById('val-esp32'),
            camera_val: document.getElementById('val-camera'),
            connection: document.getElementById('connection-status')
        };
    }
    
    updateNumericWidget(idPrefix, value, unit) {
        if(this.elements[`${idPrefix}_val`]) {
            this.elements[`${idPrefix}_val`].innerText = `${value.toFixed(1)}${unit}`;
        }
        if(this.elements[`${idPrefix}_bar`]) {
            this.elements[`${idPrefix}_bar`].style.width = `${Math.min(100, Math.max(0, value))}%`;
        }
    }
    
    updateTextWidget(idPrefix, text, colorClass = '') {
        const el = this.elements[`${idPrefix}_val`];
        if (el) {
            el.innerText = text;
            el.className = `widget-value text-status ${colorClass}`;
        }
    }
    
    setConnectionState(isOnline) {
        if(isOnline) {
            this.elements.connection.innerText = "Online";
            this.elements.connection.className = "status-indicator online";
        } else {
            this.elements.connection.innerText = "Offline";
            this.elements.connection.className = "status-indicator offline";
        }
    }
}
