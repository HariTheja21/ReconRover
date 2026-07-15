class DependencyManager:
    def __init__(self, pkg_mgr):
        self.pkg_mgr = pkg_mgr
        
    def verify_dependencies(self, reqs: list) -> bool:
        for r in reqs:
            if not self.pkg_mgr.is_installed(r):
                return False
        return True
