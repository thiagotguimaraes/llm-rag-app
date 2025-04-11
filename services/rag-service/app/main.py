from fastapi import FastAPI

app = FastAPI(title="RAG Microservice")

@app.get("/health")
def health_check():
    return {"status": "ok"}
