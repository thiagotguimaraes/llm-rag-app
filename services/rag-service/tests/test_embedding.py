from app.services.embedding import EmbeddingService

def test_embed_sentence():
    embedder = EmbeddingService()
    result = embedder.embed(["Hello world"])
    
    assert isinstance(result, list)
    assert isinstance(result[0], list)
    assert len(result[0]) > 0  # Should be a vector
