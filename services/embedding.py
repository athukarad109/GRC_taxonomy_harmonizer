from sentence_transformers import SentenceTransformer, util
from typing import List, Tuple
import hashlib
import pickle
import os

# Global cache for embeddings
_embedding_cache = {}

model = SentenceTransformer('all-MiniLM-L6-v2')

def _get_cache_key(text: str) -> str:
    """Generate cache key for text"""
    return hashlib.md5(text.encode()).hexdigest()

def get_embedding(text: str, use_cache: bool = True):
    """Generate BERT embedding for a single text with optional caching"""
    if use_cache:
        cache_key = _get_cache_key(text)
        if cache_key in _embedding_cache:
            return _embedding_cache[cache_key]
    
    embedding = model.encode(text, convert_to_tensor=True)
    
    if use_cache:
        _embedding_cache[cache_key] = embedding
    
    return embedding

def compare_texts(text1: str, text2: str, use_cache: bool = True) -> float:
    """Compare two texts and return cosine similarity"""
    emb1 = get_embedding(text1, use_cache)
    emb2 = get_embedding(text2, use_cache)
    score = util.pytorch_cos_sim(emb1, emb2)
    return score.item()

def find_most_similar(input_text: str, candidate_texts: List[str], top_n: int = 3, use_cache: bool = True) -> List[Tuple[str, float]]:
    """Return top N most similar texts to input_text from a list"""
    input_embedding = get_embedding(input_text, use_cache)
    candidates_embeddings = model.encode(candidate_texts, convert_to_tensor=True)

    similarities = util.pytorch_cos_sim(input_embedding, candidates_embeddings)[0]
    scores = similarities.tolist()

    sorted_scores = sorted(zip(candidate_texts, scores), key=lambda x: x[1], reverse=True)
    return sorted_scores[:top_n]

def clear_cache():
    """Clear the embedding cache"""
    global _embedding_cache
    _embedding_cache.clear()

def get_cache_stats():
    """Get cache statistics"""
    return {
        "cache_size": len(_embedding_cache),
        "cache_keys": list(_embedding_cache.keys())[:5]  # First 5 keys for debugging
    }