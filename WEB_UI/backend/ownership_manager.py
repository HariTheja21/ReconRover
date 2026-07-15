import time
from typing import Dict, Tuple, Callable
from .collaboration_events import OwnershipTransferEvent
from .operator_manager import OperatorManager
from .permission_manager import PermissionManager

class OwnershipManager:
    def __init__(self, operator_manager: OperatorManager, permission_manager: PermissionManager, publish_callback: Callable):
        self.op_manager = operator_manager
        self.perm_manager = permission_manager
        self.publish = publish_callback
        
        # Maps resource (e.g. "DRIVE", "MISSION") to current owner operator_id
        self.owners: Dict[str, str] = {
            "DRIVE": None,
            "MISSION": None,
            "CAMERA": None
        }

    def request_ownership(self, operator_id: str, resource: str) -> Tuple[bool, str]:
        op = self.op_manager.get_operator(operator_id)
        if not op:
            return False, "Operator not found"
            
        if not self.perm_manager.has_permission(op["role"], resource):
            return False, f"Role {op['role']} does not have permission for {resource}"
            
        current_owner = self.owners.get(resource)
        if current_owner == operator_id:
            return True, "Already owner"
            
        # In a real system, you might implement negotiation/force-override logic based on admin roles.
        # Here we allow Administrator to override, or if resource is free.
        if current_owner and op["role"] != "Administrator":
             return False, f"Resource {resource} is currently owned by {current_owner}"
             
        self.owners[resource] = operator_id
        
        event = OwnershipTransferEvent(
            resource=resource,
            previous_owner=current_owner,
            new_owner=operator_id,
            timestamp=time.time()
        )
        self.publish("OwnershipTransferEvent", event)
        return True, "Ownership granted"

    def release_ownership(self, operator_id: str, resource: str) -> bool:
        if self.owners.get(resource) == operator_id:
            self.owners[resource] = None
            event = OwnershipTransferEvent(
                resource=resource,
                previous_owner=operator_id,
                new_owner=None,
                timestamp=time.time()
            )
            self.publish("OwnershipTransferEvent", event)
            return True
        return False

    def release_all_for_operator(self, operator_id: str):
        for resource, owner in self.owners.items():
            if owner == operator_id:
                self.release_ownership(operator_id, resource)
