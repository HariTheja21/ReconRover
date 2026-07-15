class MissionStorage {
    constructor() {
        // In reality, this communicates with the backend via fetch() REST API
        // For architectural validation, we use an in-memory mock store
        this.missions = {};
    }

    async saveMission(mission) {
        if (!mission.id) {
            mission.id = 'mis_' + Date.now().toString(36);
        }
        this.missions[mission.id] = JSON.parse(JSON.stringify(mission));
        console.log("Mock saved to backend:", mission);
        return mission.id;
    }

    async loadMission(id) {
        const m = this.missions[id];
        return m ? JSON.parse(JSON.stringify(m)) : null;
    }

    async listMissions() {
        return Object.values(this.missions).map(m => ({
            id: m.id,
            name: m.name,
            type: m.type,
            waypoint_count: m.waypoints.length
        }));
    }
}
