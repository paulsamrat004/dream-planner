from pathlib import Path
import joblib
import numpy as np
from config import DOCS_DIR, RAG_INDEX_FILE

class LocalRAG:
    def __init__(self, index_path=RAG_INDEX_FILE):
        self.index_path = Path(index_path)
        if self.index_path.exists():
            self.bundle = joblib.load(self.index_path)
        else:
            self.build()

    def build(self):
        docs = []
        for path in sorted(Path(DOCS_DIR).glob("*.txt")):
            text = path.read_text(encoding="utf-8")
            # Small chunks keep retrieval focused.
            paragraphs = [p.strip() for p in text.split("\n\n") if p.strip()]
            for i, p in enumerate(paragraphs):
                docs.append({"source": path.name, "chunk_id": i, "text": p})

        try:
            from sentence_transformers import SentenceTransformer
            import faiss
            model_name = "all-MiniLM-L6-v2"
            encoder = SentenceTransformer(model_name)
            vectors = encoder.encode([d["text"] for d in docs], normalize_embeddings=True)
            vectors = np.asarray(vectors, dtype="float32")
            index = faiss.IndexFlatIP(vectors.shape[1])
            index.add(vectors)
            self.bundle = {
                "backend": "faiss",
                "model_name": model_name,
                "index": index,
                "docs": docs,
            }
        except Exception:
            from sklearn.feature_extraction.text import TfidfVectorizer
            from sklearn.metrics.pairwise import cosine_similarity
            vectorizer = TfidfVectorizer(stop_words="english")
            matrix = vectorizer.fit_transform([d["text"] for d in docs])
            self.bundle = {
                "backend": "tfidf",
                "vectorizer": vectorizer,
                "matrix": matrix,
                "docs": docs,
            }
        self.index_path.parent.mkdir(exist_ok=True)
        joblib.dump(self.bundle, self.index_path)

    def search(self, query: str, k: int = 3, min_score: float = 0.12):
        if not query or not query.strip():
            return []
        docs = self.bundle["docs"]
        if self.bundle["backend"] == "faiss":
            from sentence_transformers import SentenceTransformer
            encoder = SentenceTransformer(self.bundle["model_name"])
            q = encoder.encode([query], normalize_embeddings=True).astype("float32")
            scores, ids = self.bundle["index"].search(q, min(k, len(docs)))
            results = []
            for score, idx in zip(scores[0], ids[0]):
                if idx >= 0 and float(score) >= min_score:
                    item = dict(docs[int(idx)])
                    item["score"] = float(score)
                    results.append(item)
            return results
        else:
            from sklearn.metrics.pairwise import cosine_similarity
            qv = self.bundle["vectorizer"].transform([query])
            scores = cosine_similarity(qv, self.bundle["matrix"]).ravel()
            ids = np.argsort(scores)[::-1][:k]
            return [
                {**docs[int(i)], "score": float(scores[int(i)])}
                for i in ids if float(scores[int(i)]) >= min_score
            ]

def retrieve(query: str, k: int = 3):
    return LocalRAG().search(query, k=k)
