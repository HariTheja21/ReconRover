class Navigation {
    constructor(loader) {
        this.loader = loader;
        this.navContainer = document.getElementById('main-nav');
        this.buttons = this.navContainer.querySelectorAll('.nav-btn');
        
        // Map target IDs to their respective HTML files created in Phase 6.0 - 6.8
        this.routes = {
            'dashboard': 'index_telemetry.html',
            'teleop': 'controls.html',
            'camera': 'camera.html',
            'mission': 'missions.html',
            'config': 'configuration.html',
            'diagnostics': 'diagnostics.html',
            'collab': 'collaboration.html',
            'security': 'security.html'
        };
        
        this.bindEvents();
    }
    
    bindEvents() {
        this.buttons.forEach(btn => {
            btn.addEventListener('click', (e) => {
                const target = e.target.getAttribute('data-target');
                this.navigate(target, e.target);
            });
        });
    }
    
    navigate(target, clickedButton) {
        // Update active state
        this.buttons.forEach(b => b.classList.remove('active'));
        if(clickedButton) {
            clickedButton.classList.add('active');
        } else {
            const btn = this.navContainer.querySelector(`[data-target="${target}"]`);
            if(btn) btn.classList.add('active');
        }
        
        // Load the module
        const url = this.routes[target];
        if(url) {
            this.loader.loadModule(url);
        } else {
            console.error("Unknown route:", target);
        }
    }
}
