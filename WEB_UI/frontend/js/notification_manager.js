class NotificationManager {
    constructor() {
        this.container = document.getElementById('notification-container');
    }
    
    show(message, type = 'info', duration = 5000) {
        const notif = document.createElement('div');
        notif.className = `notification notif-${type}`;
        notif.innerText = message;
        
        this.container.appendChild(notif);
        
        if (duration > 0) {
            setTimeout(() => {
                notif.style.opacity = '0';
                notif.style.transform = 'translateX(100%)';
                notif.style.transition = 'all 0.3s ease-in';
                setTimeout(() => {
                    if (this.container.contains(notif)) {
                        this.container.removeChild(notif);
                    }
                }, 300);
            }, duration);
        }
    }
}
