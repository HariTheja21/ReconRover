class TelemetryRenderer {
    constructor(widgetManager) {
        this.wm = widgetManager;
    }
    
    processTelemetry(data) {
        // Render System Health
        if (data.cpu !== undefined) this.wm.updateNumericWidget('cpu', data.cpu, '%');
        if (data.ram !== undefined) this.wm.updateNumericWidget('ram', data.ram, '%');
        if (data.battery !== undefined) this.wm.updateNumericWidget('battery', data.battery, '%');
        
        // Render Statuses
        if (data.mode) this.wm.updateTextWidget('mode', data.mode);
        if (data.mission) this.wm.updateTextWidget('mission', data.mission);
        if (data.safety) {
            const color = data.safety === 'SAFE' ? 'ok' : 'error';
            this.wm.updateTextWidget('safety', data.safety, color);
        }
        if (data.esp32_status) this.wm.updateTextWidget('esp32', data.esp32_status);
        if (data.camera_status) this.wm.updateTextWidget('camera', data.camera_status);
    }
}
