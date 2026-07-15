import asyncio
from typing import Callable, Any

class SemanticEngine:
    def __init__(self, db, lm, loc, obj_mem, room_c, scene_m, linker, kg, optimizer, query, stats, publish: Callable):
        self.db = db
        self.lm = lm
        self.loc = loc
        self.obj_mem = obj_mem
        self.room_c = room_c
        self.scene_m = scene_m
        self.linker = linker
        self.kg = kg
        self.opt = optimizer
        self.query = query
        self.stats = stats
        self.publish = publish
        
    async def process_scene_update(self, scene_data: dict):
        self.scene_m.snapshot_scene(scene_data)
        
        entities = scene_data.get("entities", [])
        classes_in_zone = []
        
        for e in entities:
            e_id = self.linker.link(e, self.obj_mem.in_memory_cache)
            cls_name = e.get("class", "unknown")
            x, y, z = e.get("x", 0.0), e.get("y", 0.0), e.get("z", 0.0)
            
            self.obj_mem.update_object(e_id, cls_name, x, y, z)
            classes_in_zone.append(cls_name)
            self.kg.add_node(e_id, {"type": "object", "class": cls_name})
            
            self.stats.total_objects += 1
            
        room_type, conf = self.room_c.classify(classes_in_zone)
        if conf > 0.7:
            self.publish("RoomClassified", {
                "room_id": self.loc.get_zone(),
                "classification": room_type,
                "confidence": conf,
                "timestamp": asyncio.get_event_loop().time()
            })
            self.stats.rooms_classified += 1
            
        n_nodes, n_edges = self.kg.get_stats()
        self.stats.graph_nodes = n_nodes
        self.stats.graph_edges = n_edges
        
        self.publish("SemanticMapUpdated", {
            "new_entities": len(entities),
            "total_entities": self.stats.total_objects,
            "timestamp": asyncio.get_event_loop().time()
        })
        
    async def create_landmark(self, name: str, x: float, y: float, z: float):
        l_id = self.lm.create_landmark(name, x, y, z)
        self.stats.total_landmarks += 1
        self.kg.add_node(l_id, {"type": "landmark", "name": name})
        self.publish("LandmarkCreated", {
            "landmark_id": l_id,
            "name": name,
            "x": x, "y": y, "z": z,
            "timestamp": asyncio.get_event_loop().time()
        })
