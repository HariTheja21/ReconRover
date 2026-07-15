class ThemeManager {
    constructor() {
        this.btn = document.getElementById('theme-toggle');
        this.body = document.body;
        
        this.btn.addEventListener('click', () => this.toggleTheme());
    }
    
    toggleTheme() {
        this.body.classList.toggle('dark-mode');
    }
}
