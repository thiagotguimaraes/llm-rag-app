from sentence_transformers import SentenceTransformer
from typing import List

class EmbeddingService:
    _instance = None
    
    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls)
            cls._instance.model = SentenceTransformer(kwargs.get("model_name", "all-MiniLM-L6-v2"))
        return cls._instance

    def embed(self, texts: List[str]) -> List[List[float]]:
        return self.model.encode(texts, convert_to_numpy=True).tolist()

embedding_service = EmbeddingService()