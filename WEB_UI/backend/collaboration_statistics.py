from dataclasses import dataclass

@dataclass
class CollaborationStatistics:
    total_operators_connected: int = 0
    total_ownership_transfers: int = 0
    total_permission_denials: int = 0
    total_activity_events: int = 0
