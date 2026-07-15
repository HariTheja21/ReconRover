class MissionContext:
    def __init__(self):
        self.mission_id = None
        self.parameters = {}
        self.global_context = {}
        
    def init_mission(self, m_id: str, params: dict):
        self.mission_id = m_id
        self.parameters = params
        
    def update_context(self, key: str, value: any):
        self.global_context[key] = value
