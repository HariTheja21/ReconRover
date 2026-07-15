class StreamSessionManager:
    def __init__(self):
        self.viewers = set()

    def add_viewer(self, client_id: str):
        self.viewers.add(client_id)

    def remove_viewer(self, client_id: str):
        self.viewers.discard(client_id)

    def get_active_count(self) -> int:
        return len(self.viewers)

    def has_viewers(self) -> bool:
        return len(self.viewers) > 0
