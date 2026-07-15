class DocumentStore:
    def __init__(self):
        self.documents = {}
        
    def add_document(self, doc_id: str, content: dict):
        self.documents[doc_id] = content
        
    def get_document(self, doc_id: str) -> dict:
        return self.documents.get(doc_id)
