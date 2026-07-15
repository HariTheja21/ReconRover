class PerformanceDashboard {
    constructor() {
        this.elCpu = document.getElementById('perf-cpu');
        this.elMem = document.getElementById('perf-mem');
        this.elTemp = document.getElementById('perf-temp');
        this.elRx = document.getElementById('perf-rx');
    }
    
    updateMetrics(metrics) {
        this.elCpu.innerText = metrics.cpu_usage.toFixed(1);
        this.elMem.innerText = metrics.memory_usage.toFixed(1);
        this.elTemp.innerText = metrics.temperature.toFixed(1);
        this.elRx.innerText = (metrics.network_rx / 1024).toFixed(0);
    }
}
