from sentence_transformers import SentenceTransformer, util
from typing import List, Tuple

model = SentenceTransformer('all-MiniLM-L6-v2')

def get_embedding(text: str):
    # Generate BERT embedding for a single text
    return model.encode(text, convert_to_tensor=True)

def compare_texts(text1: str, text2: str) -> float:
    # Compare two texts and return cosine similarity
    emb1 = get_embedding(text1)
    emb2 = get_embedding(text2)
    score = util.pytorch_cos_sim(emb1, emb2)
    return score.item()

def find_most_similar(input_text: str, candidate_texts: List[str], top_n: int = 3) -> List[Tuple[str, float]]:
    # Return top N most similar texts to input_text from a list
    input_embedding = get_embedding(input_text)
    candidates_embeddings = model.encode(candidate_texts, convert_to_tensor=True)

    similarities = util.pytorch_cos_sim(input_embedding, candidates_embeddings)[0]
    scores = similarities.tolist()

    sorted_scores = sorted(zip(candidate_texts, scores), key=lambda x: x[1], reverse=True)
    return sorted_scores[:top_n]