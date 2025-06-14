from sentence_transformers import SentenceTransformer
from sklearn.cluster import DBSCAN
from collections import defaultdict
from services.summarizer import summarize_controls
from typing import List, Dict

# Load Sentence-BERT model once
model = SentenceTransformer("all-MiniLM-L6-v2")

def batch_harmonize_from_input(controls: List[Dict]) -> List[Dict]:
    """
    Harmonize a batch of controls by:
    1. Converting control descriptions into embeddings
    2. Clustering them using cosine similarity (DBSCAN)
    3. Summarizing each cluster using LLM
    4. Returning unified control per cluster with mapping

    Args:
        controls (List[Dict]): List of controls with keys: framework, control_id, name, description

    Returns:
        List[Dict]: List of unified controls with raw LLM summary and source mappings
    """
    descriptions = [c["description"] for c in controls]
    embeddings = model.encode(descriptions)

    clustering = DBSCAN(eps=0.4, min_samples=2, metric="cosine").fit(embeddings)
    labels = clustering.labels_

    # Group by cluster
    clusters = defaultdict(list)
    for idx, label in enumerate(labels):
        if label != -1:
            clusters[label].append(controls[idx])
    
    # Optional: collect unclustered/outlier controls
    outliers = [controls[idx] for idx, label in enumerate(labels) if label == -1]

    # Summarize each cluster
    unified_results = []
    for cluster_id, group in clusters.items():
        summary = summarize_controls(group)
        unified_results.append({
            "unified_control_id": f"UC-{cluster_id:03}",
            "title": summary["title"],
            "description": summary["description"],
            "implementation_steps": summary["implementation_steps"],
            "mapped_controls": group
        })


    # Optional: attach outliers
    if outliers:
        unified_results.append({
            "unified_control_id": "UC-OUTLIERS",
            "summary": "These controls did not match any cluster.",
            "mapped_controls": outliers
        })

    return unified_results
