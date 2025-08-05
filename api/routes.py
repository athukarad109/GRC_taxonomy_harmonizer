from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel
from typing import List, Optional
from services.matcher import match_control
from services.summarizer import summarize_controls
from services.batch import batch_harmonize_from_input
from services.config import config
from services.embedding import get_cache_stats, clear_cache
from services.framework_recommender import generate_framework_recommendation
import time

router = APIRouter()

# Request model for single control
class ControlInput(BaseModel):
    description: str
    top_n: int = 3

# Request model for batch control input
class ControlObject(BaseModel):
    framework: str
    control_id: str
    name: str
    description: str

# Request model for batch harmonization with performance options
class BatchHarmonizeRequest(BaseModel):
    controls: List[ControlObject]
    fast_mode: Optional[bool] = None
    org_context: Optional[dict] = None

# Request model for framework recommendations
class OrganizationData(BaseModel):
    # Core organization information
    business_sector: str  # Primary business sector/industry
    company_size: str  # "startup", "small", "medium", "large", "enterprise"
    revenue_bracket: Optional[str] = None  # "$100K+", "$1M+", "$10M+", "$100M+", "$1B+"
    
    # Geographic information
    business_locations: Optional[List[str]] = None  # ["US", "EU", "Asia", "Global"]
    customer_locations: Optional[List[str]] = None  # ["US", "EU", "Asia", "Global"]
    
    # Data and infrastructure
    data_types: Optional[List[str]] = None  # ["PII", "PHI", "Payment Card Data", "Financial", "Intellectual Property"]
    infrastructure: Optional[str] = None  # "on-premise", "cloud", "hybrid"
    customer_type: Optional[str] = None  # "B2B", "B2C", "B2G"
    
    # Existing compliance and risk
    existing_frameworks: Optional[List[str]] = None  # ["PCI DSS", "SOC 2", "HIPAA", "GDPR", "ISO 27001", "NIST 800-53", "CIS Controls", "COBIT"]
    risk_profile: str = "medium"  # "low", "medium", "high", "critical"
    
    # Implementation constraints
    budget_constraints: Optional[str] = None  # "low", "medium", "high"
    implementation_timeline: Optional[str] = None  # "immediate", "3months", "6months", "1year"
    technical_maturity: Optional[str] = None  # "basic", "intermediate", "advanced"

# Endpoint: Harmonize one control by finding similar ones
@router.post("/harmonize")
def harmonize_control(input_data: ControlInput):
    start_time = time.time()
    try:
        similar_controls = match_control(input_data.description, top_n=input_data.top_n)
        if not similar_controls:
            raise HTTPException(status_code=404, detail="No similar controls found")

        summary = summarize_controls(similar_controls)
        processing_time = time.time() - start_time
        
        return {
            "unified_result": summary,
            "matched_controls": similar_controls,
            "performance": {
                "processing_time_seconds": round(processing_time, 3),
                "controls_processed": 1
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Endpoint: Batch harmonize an array of controls with performance options
@router.post("/batch-harmonize")
def batch_harmonize(request: BatchHarmonizeRequest):
    start_time = time.time()
    try:
        # Use fast_mode from request or default from config
        fast_mode = request.fast_mode if request.fast_mode is not None else config.default_fast_mode
        
        control_dicts = [control.dict() for control in request.controls]
        result = batch_harmonize_from_input(control_dicts, fast_mode=fast_mode, org_context=request.org_context)
        
        processing_time = time.time() - start_time
        
        return {
            "unified_controls": result["unified_controls"],
            "total_clusters": result["total_clusters"],
            "organization_analysis": result["organization_analysis"],
            "performance": {
                "processing_time_seconds": round(processing_time, 3),
                "controls_processed": len(request.controls),
                "fast_mode": fast_mode,
                "clusters_generated": result["total_clusters"],
                "org_context_applied": request.org_context is not None
            },
            "org_context": request.org_context
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Endpoint: Get system configuration and performance stats
@router.get("/config")
def get_config():
    """Get current system configuration and performance statistics"""
    try:
        cache_stats = get_cache_stats()
        return {
            "configuration": config.to_dict(),
            "cache_stats": cache_stats,
            "system_info": {
                "embedding_model": "all-MiniLM-L6-v2",
                "clustering_algorithm": "DBSCAN"
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Endpoint: Clear embedding cache
@router.post("/clear-cache")
def clear_embedding_cache():
    """Clear the embedding cache to free memory"""
    try:
        clear_cache()
        return {"message": "Cache cleared successfully", "cache_stats": get_cache_stats()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Endpoint: Health check with performance info
@router.get("/health")
def health_check():
    """Health check endpoint with basic performance metrics"""
    try:
        cache_stats = get_cache_stats()
        return {
            "status": "healthy",
            "cache_size": cache_stats["cache_size"],
            "config": {
                "fast_mode_default": config.default_fast_mode,
                "parallel_processing": config.enable_parallel,
                "max_workers": config.max_workers
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Endpoint: Generate framework recommendations based on organization data
@router.post("/framework-recommendation")
def get_framework_recommendation(org_data: OrganizationData):
    """Generate comprehensive framework recommendations based on organization characteristics"""
    start_time = time.time()
    try:
        recommendation = generate_framework_recommendation(org_data.dict())
        processing_time = time.time() - start_time
        
        return {
            "recommendation": recommendation,
            "performance": {
                "processing_time_seconds": round(processing_time, 3),
                "organization_analyzed": True
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
