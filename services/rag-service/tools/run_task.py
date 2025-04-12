from app.tasks.embedding import generate_embeddings_task

if __name__ == "__main__":
    res = generate_embeddings_task.delay(["This is a test sentence"])
    print("Task submitted. Waiting for result...")
    print(res.get(timeout=10))
