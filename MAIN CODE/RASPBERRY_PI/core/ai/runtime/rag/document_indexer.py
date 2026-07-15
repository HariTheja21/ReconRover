class DocumentIndexer:
    def __init__(self, chunker, embedder, vdb, store):
        self.chunker = chunker
        self.embedder = embedder
        self.vdb = vdb
        self.store = store
        
    def index(self, documents: list):
        for doc in documents:
            chunks = self.chunker.chunk(doc["text"])
            for i, chunk in enumerate(chunks):
                chunk_id = f"{doc['id']}_chunk_{i}"
                embedding = self.embedder.get_embeddings(chunk)
                self.store.add_document(chunk_id, {"text": chunk, "source": doc["id"]})
                self.vdb.add([embedding], [{"text": chunk}], [chunk_id])
