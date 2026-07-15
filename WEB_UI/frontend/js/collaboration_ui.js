class CollaborationUI {
    constructor(session, roleManager, feed) {
        this.session = session;
        this.roleManager = roleManager;
        this.feed = feed;
        
        this.owners = {
            "DRIVE": null,
            "MISSION": null,
            "CAMERA": null
        };
        
        this.bindEvents();
    }
    
    bindEvents() {
        const res = ["drive", "mission", "camera"];
        res.forEach(r => {
            document.getElementById(`btn-req-${r}`).addEventListener('click', () => this.requestOwnership(r.toUpperCase()));
            document.getElementById(`btn-rel-${r}`).addEventListener('click', () => this.releaseOwnership(r.toUpperCase()));
        });
    }
    
    updateOwnership(resource, newOwnerName, newOwnerId) {
        this.owners[resource] = newOwnerId;
        const display = newOwnerName ? newOwnerName : "None";
        document.getElementById(`owner-${resource.toLowerCase()}`).innerText = display;
    }
    
    requestOwnership(resource) {
        const identity = this.session.getIdentity();
        
        if(!this.roleManager.hasPermission(identity.role, resource)) {
            alert(`Your role (${identity.role}) does not have permission to request ${resource}.`);
            return;
        }
        
        if(this.owners[resource] && this.owners[resource] !== identity.id && identity.role !== "Administrator") {
             alert(`Resource currently owned by someone else. You cannot override.`);
             return;
        }
        
        // Mock backend confirmation
        this.updateOwnership(resource, identity.name, identity.id);
        this.feed.addEvent(identity.name, "Ownership Acquired", `Took control of ${resource}`);
    }
    
    releaseOwnership(resource) {
        const identity = this.session.getIdentity();
        if(this.owners[resource] === identity.id) {
            this.updateOwnership(resource, null, null);
            this.feed.addEvent(identity.name, "Ownership Released", `Released control of ${resource}`);
        } else {
            alert("You do not own this resource.");
        }
    }
}
