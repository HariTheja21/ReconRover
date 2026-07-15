class MissionMap {
    constructor(mapId, onWaypointAdded, onWaypointMoved) {
        this.onWaypointAdded = onWaypointAdded;
        this.onWaypointMoved = onWaypointMoved;
        
        // Initialize Leaflet Map
        this.map = L.map(mapId).setView([0, 0], 18);
        
        // Using OpenStreetMap for architectural validation (can be replaced with offline tiles)
        L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
            maxZoom: 22,
            attribution: '© OpenStreetMap'
        }).addTo(this.map);

        this.markers = [];
        this.pathLine = L.polyline([], {color: '#007bff', weight: 3}).addTo(this.map);
        
        this.mode = 'add'; // 'add' or 'edit'

        this.map.on('click', (e) => {
            if (this.mode === 'add') {
                this.onWaypointAdded(e.latlng.lat, e.latlng.lng);
            }
        });
    }

    setMode(mode) {
        this.mode = mode;
        if(mode === 'edit') {
            this.markers.forEach(m => m.dragging.enable());
        } else {
            this.markers.forEach(m => m.dragging.disable());
        }
    }

    renderWaypoints(waypoints) {
        // Clear existing
        this.markers.forEach(m => this.map.removeLayer(m));
        this.markers = [];
        
        const latlngs = [];

        waypoints.forEach((wp, index) => {
            const ll = [wp.lat, wp.lng];
            latlngs.push(ll);
            
            const marker = L.marker(ll, {
                draggable: this.mode === 'edit'
            }).addTo(this.map);
            
            marker.bindTooltip(`WP ${index + 1}`, {permanent: true, direction: 'right'});
            
            marker.on('dragend', (e) => {
                const pos = e.target.getLatLng();
                this.onWaypointMoved(index, pos.lat, pos.lng);
            });
            
            this.markers.push(marker);
        });

        this.pathLine.setLatLngs(latlngs);
        
        if (latlngs.length > 0 && this.markers.length === 1) {
            this.map.panTo(latlngs[0]);
        }
    }
}
