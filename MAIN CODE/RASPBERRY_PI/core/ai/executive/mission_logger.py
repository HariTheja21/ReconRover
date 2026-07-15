import logging

logger = logging.getLogger(__name__)

class MissionLogger:
    def __init__(self):
        pass
        
    def log(self, mission_id: str, event: str):
        logger.info(f"[Mission {mission_id}] {event}")
