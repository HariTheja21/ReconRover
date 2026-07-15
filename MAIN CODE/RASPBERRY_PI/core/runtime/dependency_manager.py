"""
Dependency Manager Module
Recon Rover V2 - Phase 3.0
"""

class DependencyManager:
    """Maintains the DAG and determines strict startup ordering."""
    
    def __init__(self):
        self.modules = {} # name -> instance
        self.dependencies = {} # name -> list of names it depends on
        self._startup_order = []
        
    def register(self, module_name: str, instance: any, depends_on: list = None):
        self.modules[module_name] = instance
        self.dependencies[module_name] = depends_on or []
        
    def resolve_order(self) -> list:
        """Topological sort of the DAG."""
        visited = set()
        temp_mark = set()
        order = []
        
        def visit(node):
            if node in temp_mark:
                raise RuntimeError(f"Cyclic dependency detected at {node}")
            if node not in visited:
                temp_mark.add(node)
                for dep in self.dependencies.get(node, []):
                    visit(dep)
                temp_mark.remove(node)
                visited.add(node)
                order.append(node)
                
        for m in self.modules.keys():
            if m not in visited:
                visit(m)
                
        self._startup_order = order
        return order
