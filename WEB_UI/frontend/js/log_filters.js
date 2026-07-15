class LogFilters {
    constructor(onFilterChange) {
        this.searchInput = document.getElementById('log-search');
        this.levelFilter = document.getElementById('log-level-filter');
        this.onFilterChange = onFilterChange;
        
        this.bindEvents();
    }
    
    bindEvents() {
        this.searchInput.addEventListener('input', () => this.trigger());
        this.levelFilter.addEventListener('change', () => this.trigger());
    }
    
    trigger() {
        this.onFilterChange(this.searchInput.value, this.levelFilter.value);
    }
    
    matches(log) {
        const term = this.searchInput.value.toLowerCase();
        const level = this.levelFilter.value;
        
        if(level !== "ALL" && log.level !== level) return false;
        if(term && !log.message.toLowerCase().includes(term)) return false;
        
        return true;
    }
}
