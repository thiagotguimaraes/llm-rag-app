def chunk_text(text: str, chunk_size: int = 500, overlap: int = 50) -> list[str]:
    lines = text.splitlines()
    paragraphs = [line.strip() for line in lines if line.strip()]
    all_text = "\n".join(paragraphs)

    chunks = []
    start = 0
    while start < len(all_text):
        end = start + chunk_size
        chunks.append(all_text[start:end])
        start += chunk_size - overlap

    return chunks
