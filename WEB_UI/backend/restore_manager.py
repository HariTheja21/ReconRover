import os
import shutil

class RestoreManager:
    def __init__(self, data_dir: str = "data"):
        self.data_dir = data_dir
        
    def restore_from_backup(self, backup_path: str) -> bool:
        if not os.path.exists(backup_path):
            return False
            
        try:
            if os.path.exists(self.data_dir):
                shutil.rmtree(self.data_dir)
            shutil.copytree(backup_path, self.data_dir)
            return True
        except Exception:
            return False
