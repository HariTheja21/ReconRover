class TextToSpeech:
    def __init__(self, loader, publish):
        self.loader = loader
        self.publish = publish
        
    def speak(self, text: str, model_name: str = "piper") -> bool:
        provider = self.loader.get_provider(model_name)
        if not provider:
            return False
            
        audio_data = provider.synthesize(text)
        
        self.publish("TextToSpeechCompleted", {
            "text": text,
            "duration_sec": 1.5,
            "timestamp": 0.0
        })
        return True
