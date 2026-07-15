class LogViewer {
    constructor() {
        this.tbody = document.getElementById('log-body');
        this.container = document.querySelector('.log-container');
        this.autoScroll = document.getElementById('chk-autoscroll');
        
        this.filters = new LogFilters(() => this.reapplyFilters());
        this.allLogs = [];
        this.maxLogs = 1000;
        
        document.getElementById('btn-clear-logs').addEventListener('click', () => {
            this.allLogs = [];
            this.tbody.innerHTML = '';
        });
    }
    
    appendLog(log) {
        this.allLogs.push(log);
        if(this.allLogs.length > this.maxLogs) {
            this.allLogs.shift();
            if(this.tbody.firstChild) {
                this.tbody.removeChild(this.tbody.firstChild);
            }
        }
        
        if(this.filters.matches(log)) {
            this.renderRow(log);
            this.scrollToBottom();
        }
    }
    
    renderRow(log) {
        const tr = document.createElement('tr');
        tr.className = `log-row ${log.level.toLowerCase()}`;
        
        const d = new Date(log.timestamp * 1000);
        const ts = d.toISOString().split('T')[1].slice(0, 12);
        
        tr.innerHTML = `
            <td>${ts}</td>
            <td>${log.level}</td>
            <td>${log.source}</td>
            <td>${log.message}</td>
        `;
        
        this.tbody.appendChild(tr);
    }
    
    reapplyFilters() {
        this.tbody.innerHTML = '';
        this.allLogs.forEach(log => {
            if(this.filters.matches(log)) {
                this.renderRow(log);
            }
        });
    }
    
    scrollToBottom() {
        if(this.autoScroll.checked) {
            this.container.scrollTop = this.container.scrollHeight;
        }
    }
}
