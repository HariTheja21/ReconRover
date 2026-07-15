import asyncio
import time
import numpy as np
from typing import List, Dict, Any
from .object_detector import ObjectDetector
from .object_tracker import ObjectTracker
from .confidence_filter import ConfidenceFilter
from .detection_filter import DetectionFilter
from .class_mapper import ClassMapper
from .bounding_box_manager import BoundingBoxManager
from .vision_overlay import VisionOverlay

class VisionPipeline:
    def __init__(self, detector: ObjectDetector, tracker: ObjectTracker, conf: ConfidenceFilter,
                 det_filter: DetectionFilter, mapper: ClassMapper, bbox: BoundingBoxManager, overlay: VisionOverlay):
        self.detector = detector
        self.tracker = tracker
        self.conf_filter = conf
        self.det_filter = det_filter
        self.mapper = mapper
        self.bbox_manager = bbox
        self.overlay = overlay
        
    async def process_frame(self, frame: np.ndarray) -> tuple[np.ndarray, List[Dict[str, Any]], float]:
        start_time = time.time()
        
        # 1. Detect
        detections = self.detector.detect(frame)
        
        # 2. Map classes
        for d in detections:
            if "class_name" not in d:
                d["class_name"] = self.mapper.get_class_name(d.get("class_id", -1))
                
        # 3. Filter Confidence
        detections = self.conf_filter.filter(detections)
        
        # 4. Filter Allowed Classes
        detections = self.det_filter.filter(detections)
        
        # 5. Format BBoxes
        detections = self.bbox_manager.format_bboxes(detections)
        
        # 6. Track
        detections = self.tracker.update(detections)
        
        # 7. Overlay
        out_frame = self.overlay.draw_overlays(frame.copy(), detections)
        
        latency = (time.time() - start_time) * 1000
        return out_frame, detections, latency
