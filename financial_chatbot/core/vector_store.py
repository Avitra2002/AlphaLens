# core/vector_store.py
import faiss
import pickle
import os
from typing import List, Dict
from sentence_transformers import SentenceTransformer

class LocalFAISS:
    def __init__(self, db_dir=None, embed_model="all-MiniLM-L6-v2"):
        # Always store in project_root/vector_db if db_dir not provided
        if not db_dir:
            project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            db_dir = os.path.join(project_root, "vector_db")

        self.db_dir = db_dir
        os.makedirs(self.db_dir, exist_ok=True)

        self.embedder = SentenceTransformer(embed_model)
        

    def _get_paths(self, namespace):
        return os.path.join(self.db_dir, f"{namespace}.index"), os.path.join(self.db_dir, f"{namespace}_meta.pkl")

    def exists(self, namespace: str) -> bool:
        index_path, meta_path = self._get_paths(namespace)
        return os.path.exists(index_path) and os.path.exists(meta_path)

    def create(self, namespace: str, chunks: List[Dict]):

        # Create a FAISS index for chunks and save locally.
        # chunks: [{"text": str, "metadata": dict}, ...]
       
        texts = [c["text"] for c in chunks]
        embeddings = self.embedder.encode(texts, convert_to_numpy=True)

        dim = embeddings.shape[1]
        index = faiss.IndexFlatL2(dim)
        index.add(embeddings)

        # Save index & metadata
        index_path, meta_path = self._get_paths(namespace)
        faiss.write_index(index, index_path)
        with open(meta_path, "wb") as f:
            pickle.dump(chunks, f)

    def search(self, namespace: str, query: str, top_k: int = 5) -> List[Dict]:
   
        # Search for most relevant chunks to query.
        index_path, meta_path = self._get_paths(namespace)
        index = faiss.read_index(index_path)
        with open(meta_path, "rb") as f:
            chunks = pickle.load(f)

        query_emb = self.embedder.encode([query], convert_to_numpy=True)
        D, I = index.search(query_emb, top_k)

        return [chunks[i] for i in I[0] if i < len(chunks)]

    def get_chunks_by_section(self, namespace: str, section: str):

        # Retrieve all stored chunks for a specific section from a FAISS index's metadata.
      
        # Check if index exists first
        if not self.exists(namespace):
            return []

        _, meta_path = self._get_paths(namespace)

        # Load the metadata file
        import pickle
        with open(meta_path, "rb") as f:
            chunks = pickle.load(f)

        # Filter by section metadata
        return [c for c in chunks if c["metadata"].get("section") == section]