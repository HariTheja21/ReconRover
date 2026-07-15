class ToolResult:
    @staticmethod
    def success(data: dict) -> dict:
        return {"status": "success", "data": data}
        
    @staticmethod
    def error(message: str) -> dict:
        return {"status": "error", "message": message}
