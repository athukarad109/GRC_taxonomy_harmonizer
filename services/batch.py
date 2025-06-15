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
    1. Embedding control descriptions
    2. Clustering them using DBSCAN (semantic similarity)
    3. Summarizing each cluster with LLM (semantic meaning)
    4. Summarizing unclustered controls with LLM (semantic meaning)

    Args:
        controls (List[Dict]): List of controls with keys: framework, control_id, name, description

    Returns:
        List[Dict]: List of unified controls with summaries and source mappings
    """
    descriptions = [c["description"] for c in controls]
    embeddings = model.encode(descriptions)

    clustering = DBSCAN(eps=0.4, min_samples=2, metric="cosine").fit(embeddings)
    labels = clustering.labels_

    # Group controls by cluster label
    clusters = defaultdict(list)
    for idx, label in enumerate(labels):
        if label != -1:
            clusters[label].append(controls[idx])

    # Collect outlier controls (label -1)
    outliers = [controls[idx] for idx, label in enumerate(labels) if label == -1]

    # Generate summaries for each cluster
    unified_results = []
    for cluster_id, group in clusters.items():
        summary = summarize_controls(group)
        unified_results.append({
            "unified_control_id": f"UC-{cluster_id:03}",
            "title": summary["title"],
            "description": summary["description"],
            "implementation_steps": summary["implementation_steps"],
            "mapped_controls": group,
            "is_clustered": True
        })

    # Handle unclustered controls with LLM summarization
    if outliers:
        outlier_summary = summarize_controls(outliers)

        unified_results.append({
            "unified_control_id": "UC-999",
            "title": outlier_summary["title"] or "Other Controls: Unique or Unclustered",
            "description": outlier_summary["description"] or (
                "These controls did not match any cluster, but remain valuable and are summarized here for review."
            ),
            "implementation_steps": outlier_summary["implementation_steps"] or [],
            "mapped_controls": outliers,
            "is_clustered": False
        })


    return unified_results
