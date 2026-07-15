from typing import List, Dict, Any
import time

class TranscriptManager:
    def __init__(self):
        self.session_id = str(time.time())
        self.transcripts: List[Dict[str, Any]] = []
        
    def add_utterance(self, text: str, speaker_id: str = "user"):
        self.transcripts.append({
            "speaker": speaker_id,
            "text": text,
            "timestamp": time.time()
        })
        
    def get_recent(self, n=5) -> List[Dict[str, Any]]:
        return self.transcripts[-n:]
