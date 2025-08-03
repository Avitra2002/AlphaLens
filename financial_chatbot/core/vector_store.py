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

    # def search(self, namespace: str, query: str, top_k: int = 5) -> List[Dict]:
   
    #     # Search for most relevant chunks to query.
    #     index_path, meta_path = self._get_paths(namespace)
    #     index = faiss.read_index(index_path)
    #     with open(meta_path, "rb") as f:
    #         chunks = pickle.load(f)

    #     query_emb = self.embedder.encode([query], convert_to_numpy=True)
    #     D, I = index.search(query_emb, top_k)

    #     return [chunks[i] for i in I[0] if i < len(chunks)]

    def search(
        self,
        namespace: str,
        query: str,
        top_k: int = 5,
        filter_sections: List[str] = None
    ) -> List[Dict]:
        index_path, meta_path = self._get_paths(namespace)
        index = faiss.read_index(index_path)
        with open(meta_path, "rb") as f:
            chunks = pickle.load(f)

        query_emb = self.embedder.encode([query], convert_to_numpy=True)
        D, I = index.search(query_emb, top_k * 3)  # Retrieve more to allow filtering

        results = []
        for i in I[0]:
            if i < len(chunks):
                chunk = chunks[i]
                if not filter_sections or chunk["metadata"].get("section") in filter_sections:
                    results.append(chunk)
                if len(results) >= top_k:
                    break

        return results

    def add_chunks(self, namespace: str, chunks: list):
        #Add new chunks to an existing FAISS index.
        texts = [c["text"] for c in chunks]
        embeddings = self.embedder.encode(texts, convert_to_numpy=True)

        # Load FAISS index
        index = self._load_faiss_index(namespace)
        index.add(embeddings)

        # Update metadata — keep full chunk structure
        _, meta_path = self._get_paths(namespace)
        with open(meta_path, "rb") as f:
            existing_chunks = pickle.load(f)

        existing_chunks.extend(chunks)  # ✅ store full dict objects
        with open(meta_path, "wb") as f:
            pickle.dump(existing_chunks, f)

        # Save updated FAISS index
        self._save_faiss_index(namespace, index)
    
    def list_sections(self, namespace: str):
       #Return a list of unique section IDs stored in this namespace.
        if not self.exists(namespace):
            return []
        _, metadata_path = self._get_paths(namespace)
        with open(metadata_path, "rb") as f:
            chunks = pickle.load(f)
        # Each chunk is a dict with {"text": str, "metadata": {...}}
        return list({str(c.get("metadata", {}).get("section")) for c in chunks if c.get("metadata", {}).get("section")})



    def _load_faiss_index(self, namespace: str):
        #load existing faiss index
        index_path, _ = self._get_paths(namespace)
        if not os.path.exists(index_path):
            raise FileNotFoundError(f"No FAISS index found for namespace {namespace}")
        return faiss.read_index(index_path)
    
    def _save_faiss_index(self, namespace: str, index):
        
        index_path, _ = self._get_paths(namespace)
        faiss.write_index(index, index_path)

    def get_chunks_by_section(self, namespace: str, section: str):
      
        if not self.exists(namespace):
            return []

        _, meta_path = self._get_paths(namespace)

        with open(meta_path, "rb") as f:
            chunks = pickle.load(f)

        # Filter by section metadata
        return [c for c in chunks if c["metadata"].get("section") == section]