class DeviceManager:
    def __init__(self, gpu, cpu, mem):
        self.gpu = gpu
        self.cpu = cpu
        self.mem = mem
        
    def get_system_profile(self) -> dict:
        return {
            "gpu": self.gpu.detect(),
            "cpu": self.cpu.detect(),
            "memory": self.mem.detect()
        }
