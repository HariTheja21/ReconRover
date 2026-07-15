class ConfigurationEditor {
    constructor() {
        this.validator = ConfigurationValidator;
        this.backup = new ConfigurationBackup();
        this.profiles = new ConfigurationProfiles();
        
        this.bindEvents();
    }
    
    bindEvents() {
        document.getElementById('btn-save-config').addEventListener('click', () => this.saveConfiguration());
        document.getElementById('btn-backup').addEventListener('click', () => this.createBackup());
        document.getElementById('btn-restore').addEventListener('click', () => this.restoreDefaults());
    }
    
    gatherFormData() {
        return {
            motion: {
                max_velocity: parseFloat(document.getElementById('cfg-max-vel').value),
                max_acceleration: parseFloat(document.getElementById('cfg-max-accel').value)
            },
            safety: {
                obstacle_distance: parseFloat(document.getElementById('cfg-obs-dist').value),
                battery_critical: parseFloat(document.getElementById('cfg-bat-crit').value)
            },
            comm: {
                heartbeat_ms: parseInt(document.getElementById('cfg-heartbeat').value)
            },
            camera: {
                fps: parseInt(document.getElementById('cfg-cam-fps').value),
                resolution: document.getElementById('cfg-cam-res').value
            }
        };
    }
    
    saveConfiguration() {
        const config = this.gatherFormData();
        const validation = this.validator.validate(config);
        
        if(!validation.valid) {
            alert("Configuration Error: " + validation.message);
            return;
        }
        
        console.log("Saving new configuration payload:", config);
        // Dispatch to backend via WebSocket or REST
        alert("Configuration Applied Successfully (Simulated)");
    }
    
    async createBackup() {
        const config = this.gatherFormData();
        const bid = await this.backup.createBackup(config);
        alert(`Backup created: ${bid}`);
    }
    
    restoreDefaults() {
        if(confirm("Are you sure you want to restore default settings?")) {
            // Hardcoded defaults for demonstration
            document.getElementById('cfg-max-vel').value = "1.0";
            document.getElementById('cfg-max-accel').value = "0.5";
            document.getElementById('cfg-obs-dist').value = "0.5";
            document.getElementById('cfg-bat-crit').value = "10.5";
            document.getElementById('cfg-heartbeat').value = "1000";
            document.getElementById('cfg-cam-fps').value = "30";
            document.getElementById('cfg-cam-res').value = "640x480";
        }
    }
}

document.addEventListener('DOMContentLoaded', () => {
    window.configEditor = new ConfigurationEditor();
});
