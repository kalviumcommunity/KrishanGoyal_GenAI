"""FAISS-based embedding / retrieval layer.

Stores:
 - FAISS index for vector similarity (cosine via inner product on normalized vectors)
 - Parallel lists for texts and metadata (persisted as JSONL)

Subject filtering is performed post-retrieval by expanding the candidate pool if necessary.
"""
from typing import List, Dict, Optional
from pathlib import Path
import json
import os
import faiss  # type: ignore
import numpy as np
from sentence_transformers import SentenceTransformer
from .config import settings

PERSIST_DIR = Path(settings.persist_directory)
PERSIST_DIR.mkdir(parents=True, exist_ok=True)

INDEX_PATH = PERSIST_DIR / "index.faiss"
METADATA_PATH = PERSIST_DIR / "metadata.jsonl"
TEXTS_PATH = PERSIST_DIR / "texts.jsonl"
STATE_PATH = PERSIST_DIR / "state.json"

_model = SentenceTransformer(settings.embedding_model)

# Runtime containers
_index = None  # faiss.Index
_metadata: List[Dict] = []
_texts: List[str] = []
_next_id: int = 0


def _normalize(vectors: np.ndarray) -> np.ndarray:
    norms = np.linalg.norm(vectors, axis=1, keepdims=True) + 1e-12
    return vectors / norms


def _create_index(d: int):
    return faiss.IndexFlatIP(d)


def _load_state():
    global _index, _metadata, _texts, _next_id
    if INDEX_PATH.exists():
        _index = faiss.read_index(str(INDEX_PATH))
    else:
        _index = None
    if METADATA_PATH.exists():
        with METADATA_PATH.open("r", encoding="utf-8") as f:
            _metadata = [json.loads(line) for line in f]
    if TEXTS_PATH.exists():
        with TEXTS_PATH.open("r", encoding="utf-8") as f:
            _texts = [json.loads(line)["text"] for line in f]
    if STATE_PATH.exists():
        with STATE_PATH.open("r", encoding="utf-8") as f:
            data = json.load(f)
            _next_id = data.get("next_id", len(_texts))
    else:
        _next_id = len(_texts)


def _save_state():
    if _index is not None:
        faiss.write_index(_index, str(INDEX_PATH))
    # Metadata JSONL
    with METADATA_PATH.open("w", encoding="utf-8") as f:
        for m in _metadata:
            f.write(json.dumps(m, ensure_ascii=False) + "\n")
    with TEXTS_PATH.open("w", encoding="utf-8") as f:
        for t in _texts:
            f.write(json.dumps({"text": t}, ensure_ascii=False) + "\n")
    with STATE_PATH.open("w", encoding="utf-8") as f:
        json.dump({"next_id": _next_id}, f)


def _ensure_loaded():
    if not hasattr(_ensure_loaded, "_loaded"):
        _load_state()
        setattr(_ensure_loaded, "_loaded", True)


def add_texts(chunks: List[str], metadata: List[Dict]):
    """Add new text chunks & metadata to FAISS index."""
    _ensure_loaded()
    global _index, _next_id
    if not chunks:
        return
    embeddings = _model.encode(chunks, show_progress_bar=False)
    embeddings = _normalize(np.array(embeddings, dtype="float32"))
    d = embeddings.shape[1]
    if _index is None:
        _index = _create_index(d)
    elif _index.d != d:
        raise ValueError(f"Embedding dimension mismatch: existing {_index.d} vs new {d}")
    _index.add(embeddings)
    # Append metadata & texts with ids
    for m, t in zip(metadata, chunks):
        m = dict(m)  # copy
        m["id"] = _next_id
        _metadata.append(m)
        _texts.append(t)
        _next_id += 1
    _save_state()


def similarity_search(query: str, k: int = 4, subject: Optional[str] = None):
    if not query:
        return []
    
    _ensure_loaded()
    if _index is None or _index.ntotal == 0:
        return []
    q_emb = _model.encode([query])
    q_emb = _normalize(np.array(q_emb, dtype="float32"))

    # Retrieve an expanded candidate pool to allow subject filtering
    candidate_pool = min(max(k * 10, 50), _index.ntotal)
    scores, idxs = _index.search(q_emb, candidate_pool)
    scores = scores[0]
    idxs = idxs[0]

    results = []
    for score, i in zip(scores, idxs):
        if i < 0:
            continue
        meta = _metadata[i]
        if subject and meta.get("subject") != subject:
            continue
        results.append({
            "text": _texts[i],
            "metadata": meta,
            "distance": float(1 - score)  # cosine distance approx (since score ~ cosine similarity)
        })
        if len(results) >= k:
            break

    # If filtering removed too many, fall back (ignore subject) to fill
    if len(results) < k and subject:
        for score, i in zip(scores, idxs):
            if i < 0:
                continue
            meta = _metadata[i]
            # Skip if already included
            if any(r["metadata"]["id"] == meta["id"] for r in results):
                continue
            results.append({
                "text": _texts[i],
                "metadata": meta,
                "distance": float(1 - score)
            })
            if len(results) >= k:
                break
    return results


def reset_index():
    """Delete all persisted index data and reset in-memory structures."""
    global _index, _metadata, _texts, _next_id
    for p in [INDEX_PATH, METADATA_PATH, TEXTS_PATH, STATE_PATH]:
        if p.exists():
            try:
                p.unlink()
            except OSError:
                pass
    _index = None
    _metadata = []
    _texts = []
    _next_id = 0
    # Mark loader as not loaded so future operations rebuild state
    if hasattr(_ensure_loaded, "_loaded"):
        delattr(_ensure_loaded, "_loaded")



