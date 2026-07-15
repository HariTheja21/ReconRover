import asyncio
from typing import Dict, List

class DependencyChecker:
    def __init__(self):
        self.started_modules = set()

    def mark_started(self, module: str) -> None:
        self.started_modules.add(module)

    def check_dependencies(self, module: str, dependencies: List[str]) -> bool:
        for dep in dependencies:
            if dep not in self.started_modules:
                return False
        return True
