from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List
from services.matcher import match_control
from services.summarizer import summarize_controls
from services.batch import batch_harmonize_from_input

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

# Endpoint: Harmonize one control by finding similar ones
@router.post("/harmonize")
def harmonize_control(input_data: ControlInput):
    try:
        similar_controls = match_control(input_data.description, top_n=input_data.top_n)
        if not similar_controls:
            raise HTTPException(status_code=404, detail="No similar controls found")

        summary = summarize_controls(similar_controls)
        return {
            "unified_result": summary["raw_summary"],
            "matched_controls": similar_controls
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Endpoint: Batch harmonize an array of controls
@router.post("/batch-harmonize")
def batch_harmonize(controls: List[ControlObject]):
    try:
        control_dicts = [control.dict() for control in controls]
        unified_controls = batch_harmonize_from_input(control_dicts)
        return {
            "unified_controls": unified_controls,
            "total_clusters": len(unified_controls)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
