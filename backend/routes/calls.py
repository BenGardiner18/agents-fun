from fastapi import APIRouter, HTTPException
from typing import List
from models import Call, CallCreate, CallUpdate, MessageResponse
from database import db_manager

router = APIRouter(prefix="/calls", tags=["calls"])

@router.get("/", response_model=List[Call])
def get_calls():
    """Get all calls"""
    rows, cur = db_manager.execute_query("SELECT * FROM calls ORDER BY created_at DESC")
    
    calls = []
    for row in rows:
        call = db_manager.row_to_dict(row, cur)
        calls.append(Call(**call))
    return calls

@router.get("/{call_id}", response_model=Call)
def get_call(call_id: int):
    """Get a specific call by ID"""
    row, cur = db_manager.execute_single("SELECT * FROM calls WHERE id = %s", (call_id,))
    
    if row is None:
        raise HTTPException(status_code=404, detail="Call not found")
    
    call = db_manager.row_to_dict(row, cur)
    return Call(**call)

@router.post("/", response_model=Call)
def create_call(call: CallCreate):
    """Create a new call"""
    row, cur = db_manager.execute_insert(
        "INSERT INTO calls (contact_id, call_type, duration, outcome) VALUES (%s, %s, %s, %s) RETURNING *",
        (call.contact_id, call.call_type, call.duration, call.outcome)
    )
    
    created_call = db_manager.row_to_dict(row, cur)
    return Call(**created_call)

@router.put("/{call_id}", response_model=Call)
def update_call(call_id: int, call: CallUpdate):
    """Update an existing call"""
    row, cur = db_manager.execute_update(
        "UPDATE calls SET contact_id = %s, call_type = %s, duration = %s, outcome = %s WHERE id = %s RETURNING *",
        (call.contact_id, call.call_type, call.duration, call.outcome, call_id)
    )
    
    if row is None:
        raise HTTPException(status_code=404, detail="Call not found")
    
    updated_call = db_manager.row_to_dict(row, cur)
    return Call(**updated_call)

@router.delete("/{call_id}", response_model=MessageResponse)
def delete_call(call_id: int):
    """Delete a call"""
    row_count = db_manager.execute_delete("DELETE FROM calls WHERE id = %s", (call_id,))
    
    if row_count == 0:
        raise HTTPException(status_code=404, detail="Call not found")
    
    return MessageResponse(message="Call deleted successfully") 