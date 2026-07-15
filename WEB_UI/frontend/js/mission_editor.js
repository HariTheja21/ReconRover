class MissionEditor {
    constructor() {
        this.waypoints = [];
        this.currentMissionId = null;
        
        this.storage = new MissionStorage();
        this.validator = MissionValidator;
        this.renderer = new MissionRenderer();
        this.executor = new MissionExecutor();
        
        this.map = new MissionMap('map', 
            (lat, lng) => this.addWaypoint(lat, lng),
            (idx, lat, lng) => this.moveWaypoint(idx, lat, lng)
        );

        this.bindEvents();
        this.refreshMissionList();
    }

    bindEvents() {
        document.getElementById('btn-add-wp').addEventListener('click', (e) => {
            this.map.setMode('add');
            e.target.classList.add('active');
            document.getElementById('btn-edit-wp').classList.remove('active');
        });

        document.getElementById('btn-edit-wp').addEventListener('click', (e) => {
            this.map.setMode('edit');
            e.target.classList.add('active');
            document.getElementById('btn-add-wp').classList.remove('active');
        });

        document.getElementById('btn-save').addEventListener('click', () => this.saveCurrentMission());
        document.getElementById('btn-execute').addEventListener('click', () => this.executeCurrentMission());
        document.getElementById('btn-cancel').addEventListener('click', () => this.executor.cancelMission());
        document.getElementById('btn-new-mission').addEventListener('click', () => this.startNewMission());
    }

    addWaypoint(lat, lng) {
        this.waypoints.push({ lat, lng });
        this.updateUI();
    }

    removeWaypoint(index) {
        this.waypoints.splice(index, 1);
        this.updateUI();
    }

    moveWaypoint(index, lat, lng) {
        this.waypoints[index].lat = lat;
        this.waypoints[index].lng = lng;
        this.updateUI();
    }

    updateUI() {
        this.map.renderWaypoints(this.waypoints);
        this.renderer.renderSidebarList(this.waypoints, (idx) => this.removeWaypoint(idx));
    }

    startNewMission() {
        this.currentMissionId = null;
        this.waypoints = [];
        document.getElementById('mission-name').value = '';
        document.getElementById('btn-execute').disabled = true;
        this.updateUI();
    }

    async saveCurrentMission() {
        const name = document.getElementById('mission-name').value;
        const type = document.getElementById('mission-type').value;
        
        const validation = this.validator.validate(name, this.waypoints);
        if (!validation.valid) {
            alert(validation.message);
            return;
        }

        const mission = {
            id: this.currentMissionId,
            name: name,
            type: type,
            waypoints: this.waypoints
        };

        const newId = await this.storage.saveMission(mission);
        this.currentMissionId = newId;
        document.getElementById('btn-execute').disabled = false;
        
        this.refreshMissionList();
    }
    
    async refreshMissionList() {
        const list = document.getElementById('mission-list');
        const header = list.querySelector('.sidebar-header');
        list.innerHTML = '';
        list.appendChild(header);
        
        const missions = await this.storage.listMissions();
        missions.forEach(m => {
            const li = document.createElement('li');
            li.innerHTML = `<a href="#">${m.name} (${m.waypoint_count} WPs)</a>`;
            li.addEventListener('click', () => this.loadMission(m.id));
            list.appendChild(li);
        });
    }
    
    async loadMission(id) {
        const m = await this.storage.loadMission(id);
        if(m) {
            this.currentMissionId = m.id;
            this.waypoints = m.waypoints;
            document.getElementById('mission-name').value = m.name;
            document.getElementById('mission-type').value = m.type;
            document.getElementById('btn-execute').disabled = false;
            this.updateUI();
        }
    }

    async executeCurrentMission() {
        if(this.currentMissionId) {
            document.getElementById('btn-cancel').disabled = false;
            this.executor.executeMission(this.currentMissionId);
        }
    }
}

document.addEventListener('DOMContentLoaded', () => {
    console.log("Initializing Mission Planner...");
    window.missionEditor = new MissionEditor();
});
