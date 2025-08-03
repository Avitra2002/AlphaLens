# core/chunker.py
import tiktoken

def chunk_text(text: str, size: int = 2500, overlap: int = 200, model_name: str = "gpt-3.5-turbo") -> list:
    enc = tiktoken.encoding_for_model(model_name)
    tokens = enc.encode(text)

    chunks = []
    start = 0
    while start < len(tokens):
        end = min(start + size, len(tokens))
        chunk_tokens = tokens[start:end]
        chunk_text = enc.decode(chunk_tokens)
        chunks.append(chunk_text)
        start += size - overlap

    return chunks
