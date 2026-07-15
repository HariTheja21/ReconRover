class MicrophoneManager:
    def __init__(self):
        self.is_recording = False
        
    def start_stream(self):
        self.is_recording = True
        
    def stop_stream(self):
        self.is_recording = False
