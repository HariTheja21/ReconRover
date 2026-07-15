class CommandParser:
    def __init__(self, publish):
        self.publish = publish
        
    def parse(self, text: str):
        # Stub parsing
        self.publish("SpeechCommandParsed", {
            "command": text,
            "intent": "unknown",
            "timestamp": 0.0
        })
