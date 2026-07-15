class RoomClassifier:
    def __init__(self):
        pass
        
    def classify(self, objects_in_zone: list) -> tuple[str, float]:
        # Stub: If see a bed, it's a bedroom
        if "bed" in objects_in_zone:
            return "bedroom", 0.9
        if "sofa" in objects_in_zone:
            return "living_room", 0.8
        return "hallway", 0.5
