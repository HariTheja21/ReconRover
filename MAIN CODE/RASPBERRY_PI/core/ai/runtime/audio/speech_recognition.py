class SpeechRecognition:
    def __init__(self, loader, preprocessor, postprocessor, publish):
        self.loader = loader
        self.preprocessor = preprocessor
        self.postprocessor = postprocessor
        self.publish = publish
        
    def recognize(self, model_name: str, audio_data: bytes) -> str:
        provider = self.loader.get_provider(model_name)
        if not provider:
            return ""
            
        pre = self.preprocessor.preprocess(audio_data)
        raw = provider.transcribe(pre)
        text = self.postprocessor.clean_text(raw)
        
        self.publish("SpeechRecognized", {
            "text": text,
            "confidence": 0.95,
            "timestamp": 0.0
        })
        return text
