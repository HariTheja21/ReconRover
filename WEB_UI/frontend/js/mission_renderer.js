class MissionRenderer {
    constructor() {
        this.listEl = document.getElementById('waypoint-list');
        this.statCount = document.getElementById('stat-wp-count');
        this.statDistance = document.getElementById('stat-distance');
    }

    renderSidebarList(waypoints, onRemove) {
        this.listEl.innerHTML = '';
        this.statCount.innerText = waypoints.length;
        
        let totalDistance = 0;
        
        waypoints.forEach((wp, index) => {
            const li = document.createElement('li');
            li.innerHTML = `
                <span>WP ${index + 1}: ${wp.lat.toFixed(5)}, ${wp.lng.toFixed(5)}</span>
                <button class="btn-remove-wp" data-index="${index}">X</button>
            `;
            this.listEl.appendChild(li);
            
            if(index > 0) {
                // Extremely rough distance calc for validation UI
                const pLat = waypoints[index-1].lat;
                const pLng = waypoints[index-1].lng;
                const dist = Math.sqrt(Math.pow(wp.lat - pLat, 2) + Math.pow(wp.lng - pLng, 2)) * 111000;
                totalDistance += dist;
            }
        });
        
        this.statDistance.innerText = `${totalDistance.toFixed(1)} m`;

        this.listEl.querySelectorAll('.btn-remove-wp').forEach(btn => {
            btn.addEventListener('click', (e) => {
                const idx = parseInt(e.target.getAttribute('data-index'));
                onRemove(idx);
            });
        });
    }
}
