from sentence_transformers import SentenceTransformer
from sklearn.cluster import DBSCAN
from collections import defaultdict
from services.summarizer import summarize_controls
from typing import List, Dict, Optional
import asyncio
from concurrent.futures import ThreadPoolExecutor
import time

# Load Sentence-BERT model once
model = SentenceTransformer("all-MiniLM-L6-v2")

def _analyze_org_context(controls: List[Dict], org_context: Optional[Dict] = None) -> Dict:
    """Analyze organization context and provide insights"""
    if not org_context:
        return {
            "existing_controls_count": 0,
            "industry": None,
            "gaps": [],
            "overlaps": [],
            "recommendations": []
        }
    
    analysis = {
        "existing_controls_count": len(org_context.get("existing_controls", [])),
        "industry": org_context.get("industry"),
        "gaps": [],
        "overlaps": [],
        "recommendations": []
    }
    
    # Compare with existing controls if provided
    if org_context.get("existing_controls"):
        existing_controls = org_context["existing_controls"]
        new_control_descriptions = [c["description"] for c in controls]
        
        # Simple keyword-based overlap detection
        for existing in existing_controls:
            for new_control in controls:
                if any(keyword in new_control["description"].lower() 
                      for keyword in existing.lower().split()):
                    analysis["overlaps"].append({
                        "existing": existing,
                        "new_control": new_control["name"],
                        "framework": new_control["framework"]
                    })
    
    # Industry-specific recommendations
    industry = org_context.get("industry", "").lower()
    if industry in ["finance", "banking"]:
        analysis["recommendations"].append("Focus on regulatory compliance controls (PCI, SOX)")
    elif industry in ["healthcare", "medical"]:
        analysis["recommendations"].append("Prioritize HIPAA and patient data protection controls")
    elif industry in ["technology", "software"]:
        analysis["recommendations"].append("Emphasize secure development and API security controls")
    
    return analysis

def _generate_contextualized_prompt(controls: List[Dict], org_context: Optional[Dict] = None) -> str:
    """Generate a context-aware prompt for LLM summarization"""
    base_prompt = f"""Summarize these security controls into a unified format:

Controls:
{chr(10).join([f"- {c['framework']}: {c['name']} - {c['description'][:200]}{'...' if len(c['description']) > 200 else ''}" for c in controls])}"""

    if org_context:
        industry = org_context.get("industry", "")
        existing_count = len(org_context.get("existing_controls", []))
        
        context_info = f"""

Organization Context:
- Industry: {industry}
- Existing controls: {existing_count}
- Risk profile: {org_context.get('risk_profile', 'Standard')}

Please tailor the implementation steps to be relevant for {industry} industry and consider existing control landscape.
"""
        base_prompt += context_info
    
    base_prompt += """

Return ONLY valid JSON:
{
  "title": "Unified control title",
  "description": "2-3 sentence summary",
  "implementation_steps": [
    {"step": "Step 1", "description": "Action"},
    {"step": "Step 2", "description": "Action"}
  ]
}"""
    
    return base_prompt

def _generate_fast_summary(controls: List[Dict], org_context: Optional[Dict] = None) -> Dict:
    """Generate a fast summary without LLM for speed (PREVIEW MODE ONLY)
    
    This is a basic heuristic-based summary for quick previews.
    For production use, always use normal mode with LLM for quality descriptions.
    """
    if not controls:
        return {"title": "No Controls", "description": "", "implementation_steps": []}
    
    # Simple heuristics for fast summary
    frameworks = list(set(c['framework'] for c in controls))
    names = [c['name'] for c in controls]
    
    # Use first control's name as base, add count
    base_name = names[0] if names else "Control"
    title = f"{base_name} ({len(controls)} controls)"
    
    # Simple description - NOTE: This is basic, not semantic
    description = f"Group of {len(controls)} similar controls from {', '.join(frameworks)} frameworks"
    
    # Add industry context if available
    if org_context and org_context.get("industry"):
        description += f" - Relevant for {org_context['industry']} industry"
    
    return {
        "title": title,
        "description": description,
        "implementation_steps": [],
        "note": "Fast mode: Basic grouping only. Use normal mode for quality descriptions."
    }

def batch_harmonize_from_input(controls: List[Dict], fast_mode: bool = False, org_context: Optional[Dict] = None) -> List[Dict]:
    """
    Harmonize a batch of controls by:
    1. Embedding control descriptions
    2. Clustering them using DBSCAN (semantic similarity)
    3. Summarizing each cluster with LLM (semantic meaning) - PARALLEL
    4. Summarizing unclustered controls with LLM (semantic meaning)
    5. Analyzing organization context and providing insights

    Args:
        controls (List[Dict]): List of controls with keys: framework, control_id, name, description
        fast_mode (bool): If True, skip LLM summarization for maximum speed (PREVIEW MODE ONLY)
                         
                         MODE SELECTION:
                         - fast_mode=False (DEFAULT): Use LLM for quality descriptions and implementation steps
                         - fast_mode=True: Basic grouping only, for quick previews or when LLM unavailable
        org_context (Dict): Organization context including:
                           - industry: str (e.g., "finance", "healthcare")
                           - existing_controls: List[str] (list of existing control descriptions)
                           - risk_profile: str (e.g., "high", "medium", "low")
                           - compliance_frameworks: List[str] (e.g., ["PCI", "SOX"])

    Returns:
        List[Dict]: List of unified controls with summaries and source mappings
    """
    start_time = time.time()
    
    # Step 1: Analyze organization context
    org_analysis = _analyze_org_context(controls, org_context)
    print(f"Context analysis completed in {time.time() - start_time:.2f}s")
    
    # Step 2: Embedding (fast)
    descriptions = [c["description"] for c in controls]
    embeddings = model.encode(descriptions)
    print(f"Embedding completed in {time.time() - start_time:.2f}s")

    # Step 3: Clustering (fast)
    clustering = DBSCAN(eps=0.4, min_samples=2, metric="cosine").fit(embeddings)
    labels = clustering.labels_
    print(f"Clustering completed in {time.time() - start_time:.2f}s")

    # Group controls by cluster label
    clusters = defaultdict(list)
    for idx, label in enumerate(labels):
        if label != -1:
            clusters[label].append(controls[idx])

    # Collect outlier controls (label -1)
    outliers = [controls[idx] for idx, label in enumerate(labels) if label == -1]

    # Step 4: Summarization (LLM or Fast Mode)
    unified_results = []
    
    if fast_mode:
        # FAST MODE: No LLM calls, instant results
        for cluster_id, group in clusters.items():
            summary = _generate_fast_summary(group, org_context)
            unified_results.append({
                "unified_control_id": f"UC-{cluster_id:03}",
                "title": summary["title"],
                "description": summary["description"],
                "implementation_steps": summary["implementation_steps"],
                "mapped_controls": group,
                "is_clustered": True,
                "fast_mode": True,
                "org_context_applied": org_context is not None
            })
        
        # Handle outliers in fast mode
        if outliers:
            outlier_summary = _generate_fast_summary(outliers, org_context)
            unified_results.append({
                "unified_control_id": "UC-999",
                "title": outlier_summary["title"],
                "description": outlier_summary["description"],
                "implementation_steps": outlier_summary["implementation_steps"],
                "mapped_controls": outliers,
                "is_clustered": False,
                "fast_mode": True,
                "org_context_applied": org_context is not None
            })
    else:
        # NORMAL MODE: Parallel LLM processing with context
        if clusters:
            # Ensure max_workers is at least 1 to avoid ThreadPoolExecutor error
            max_workers = max(1, min(len(clusters), 4))
            with ThreadPoolExecutor(max_workers=max_workers) as executor:
                # Submit all cluster summarization tasks with context
                future_to_cluster = {
                    executor.submit(summarize_controls, group, org_context): cluster_id 
                    for cluster_id, group in clusters.items()
                }
                
                # Collect results as they complete
                for future in future_to_cluster:
                    cluster_id = future_to_cluster[future]
                    try:
                        summary = future.result()
                        unified_results.append({
                            "unified_control_id": f"UC-{cluster_id:03}",
                            "title": summary["title"],
                            "description": summary["description"],
                            "implementation_steps": summary["implementation_steps"],
                            "mapped_controls": clusters[cluster_id],
                            "is_clustered": True,
                            "fast_mode": False,
                            "org_context_applied": org_context is not None
                        })
                    except Exception as e:
                        print(f"Error processing cluster {cluster_id}: {e}")
                        # Fallback: create basic summary without LLM
                        unified_results.append({
                            "unified_control_id": f"UC-{cluster_id:03}",
                            "title": f"Cluster {cluster_id} Controls",
                            "description": f"Group of {len(clusters[cluster_id])} similar controls",
                            "implementation_steps": [],
                            "mapped_controls": clusters[cluster_id],
                            "is_clustered": True,
                            "fast_mode": False,
                            "org_context_applied": org_context is not None
                        })
        else:
            # No clusters found - all controls are outliers
            print("No clusters found - all controls are unique/outliers")

        # Handle unclustered controls
        if outliers:
            outlier_summary = summarize_controls(outliers, org_context)
            unified_results.append({
                "unified_control_id": "UC-999",
                "title": outlier_summary["title"] or "Other Controls: Unique or Unclustered",
                "description": outlier_summary["description"] or (
                    "These controls did not match any cluster, but remain valuable and are summarized here for review."
                ),
                "implementation_steps": outlier_summary["implementation_steps"] or [],
                "mapped_controls": outliers,
                "is_clustered": False,
                "fast_mode": False,
                "org_context_applied": org_context is not None
            })

    print(f"Total harmonization completed in {time.time() - start_time:.2f}s")
    
    # Return results with organization context analysis
    return {
        "unified_controls": unified_results,
        "organization_analysis": org_analysis,
        "total_clusters": len(unified_results),
        "processing_time": time.time() - start_time
    }
