class SceneMemory:
    def __init__(self):
        self.scenes = []
        
    def snapshot_scene(self, scene_data: dict):
        self.scenes.append(scene_data)
        if len(self.scenes) > 10:
            self.scenes.pop(0)
