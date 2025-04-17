import requests
import os

def test_qdrant_health():
    host = os.getenv("QDRANT_HOST", "localhost")
    port = os.getenv("QDRANT_PORT", "6333")
    response = requests.get(f"http://{host}:{port}/collections")
    assert response.status_code == 200