document.addEventListener('DOMContentLoaded', () => {
    console.log("Initializing Multi-Operator Collaboration Dashboard...");
    
    const session = new SessionManager();
    const identity = session.getIdentity();
    
    // Update Header
    document.getElementById('my-name').innerText = identity.name;
    document.getElementById('my-role').innerText = identity.role;
    
    const roleManager = new RoleManager();
    const presence = new PresenceManager();
    const feed = new ActivityFeed();
    const ui = new CollaborationUI(session, roleManager, feed);
    
    // Simulate initial presence injection (Mocking EventBus WebSockets)
    presence.updatePresence(identity.id, identity.name, identity.role, "ONLINE");
    presence.updatePresence("op_1234", "Commander-Alpha", "Mission Commander", "ONLINE");
    presence.updatePresence("op_5678", "Pilot-Bravo", "Pilot", "IDLE");
    
    feed.addEvent("System", "Session Started", "Connected to EventBus collaboration channel.");
    
    // Simulate an ownership transfer from another operator
    setTimeout(() => {
        ui.updateOwnership("CAMERA", "Pilot-Bravo", "op_5678");
        feed.addEvent("Pilot-Bravo", "Ownership Acquired", "Took control of CAMERA");
    }, 2000);
});
