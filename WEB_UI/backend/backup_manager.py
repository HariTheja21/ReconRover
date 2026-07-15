import os
import shutil
import time

class BackupManager:
    def __init__(self, data_dir: str = "data"):
        self.data_dir = data_dir
        self.backup_dir = "backups"
        if not os.path.exists(self.backup_dir):
            os.makedirs(self.backup_dir, exist_ok=True)
            
    def create_backup(self) -> str:
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        backup_path = os.path.join(self.backup_dir, f"system_backup_{timestamp}")
        try:
            if os.path.exists(self.data_dir):
                shutil.copytree(self.data_dir, backup_path)
            return backup_path
        except Exception as e:
            return f"Backup Failed: {str(e)}"
