class OTADashboard {
    constructor() {
        this.btnDeploy = document.getElementById('btn-deploy-ota');
        this.statusText = document.getElementById('ota-status-text');
        this.progressBar = document.getElementById('ota-progress-bar');
        this.logConsole = document.getElementById('ota-logs');
        
        this.isDeploying = false;
        
        this.bindEvents();
    }
    
    bindEvents() {
        this.btnDeploy.addEventListener('click', () => this.startDeployment());
    }
    
    log(msg) {
        const timestamp = new Date().toISOString().split('T')[1].slice(0,8);
        this.logConsole.innerHTML += `<br>[${timestamp}] ${msg}`;
        this.logConsole.scrollTop = this.logConsole.scrollHeight;
    }
    
    startDeployment() {
        const fileInput = document.getElementById('ota-file');
        if(!fileInput.files.length) {
            alert("Please select a firmware package.");
            return;
        }
        
        if(this.isDeploying) return;
        this.isDeploying = true;
        this.btnDeploy.disabled = true;
        
        this.log("Starting OTA deployment sequence...");
        this.statusText.innerText = "VALIDATING";
        this.progressBar.style.width = "10%";
        
        // Mock deployment process
        setTimeout(() => {
            this.log("Checksum verified. Target hardware validated.");
            this.statusText.innerText = "FLASHING";
            this.progressBar.style.width = "40%";
            
            let progress = 40;
            const flashInterval = setInterval(() => {
                progress += 10;
                this.progressBar.style.width = `${progress}%`;
                this.log(`Flashing block at address 0x080${progress}00...`);
                
                if(progress >= 90) {
                    clearInterval(flashInterval);
                    setTimeout(() => this.finishDeployment(), 1000);
                }
            }, 500);
            
        }, 1500);
    }
    
    finishDeployment() {
        this.progressBar.style.width = "100%";
        this.statusText.innerText = "SUCCESS";
        this.log("OTA Deployment Complete. Device rebooting...");
        
        setTimeout(() => {
            this.isDeploying = false;
            this.btnDeploy.disabled = false;
            this.statusText.innerText = "IDLE";
            this.progressBar.style.width = "0%";
            this.log("> System ready.");
        }, 3000);
    }
}

document.addEventListener('DOMContentLoaded', () => {
    window.otaDashboard = new OTADashboard();
});
