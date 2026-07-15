import sys

class DependencyChecker:
    def __init__(self):
        self.required_python = (3, 12)
        
    def check_all(self) -> bool:
        return self._check_python_version()

    def _check_python_version(self) -> bool:
        if sys.version_info < self.required_python:
            print(f"CRITICAL: Python {self.required_python[0]}.{self.required_python[1]} or higher is required.")
            return False
        return True
