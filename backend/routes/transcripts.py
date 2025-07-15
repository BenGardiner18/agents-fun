from fastapi import APIRouter, HTTPException
from typing import List
from models import CallTranscript, CallTranscriptCreate, CallTranscriptUpdate, MessageResponse
from database import db_manager

router = APIRouter(prefix="/call-transcripts", tags=["call-transcripts"])

@router.get("/", response_model=List[CallTranscript])
def get_call_transcripts():
    """Get all call transcripts"""
    rows, cur = db_manager.execute_query("SELECT * FROM call_transcripts ORDER BY created_at DESC")
    
    transcripts = []
    for row in rows:
        transcript = db_manager.row_to_dict(row, cur)
        transcripts.append(CallTranscript(**transcript))
    return transcripts

@router.get("/{transcript_id}", response_model=CallTranscript)
def get_call_transcript(transcript_id: int):
    """Get a specific call transcript by ID"""
    row, cur = db_manager.execute_single("SELECT * FROM call_transcripts WHERE id = %s", (transcript_id,))
    
    if row is None:
        raise HTTPException(status_code=404, detail="Call transcript not found")
    
    transcript = db_manager.row_to_dict(row, cur)
    return CallTranscript(**transcript)

@router.post("/", response_model=CallTranscript)
def create_call_transcript(transcript: CallTranscriptCreate):
    """Create a new call transcript"""
    row, cur = db_manager.execute_insert(
        "INSERT INTO call_transcripts (call_id, transcript) VALUES (%s, %s) RETURNING *",
        (transcript.call_id, transcript.transcript)
    )
    
    created_transcript = db_manager.row_to_dict(row, cur)
    return CallTranscript(**created_transcript)

@router.put("/{transcript_id}", response_model=CallTranscript)
def update_call_transcript(transcript_id: int, transcript: CallTranscriptUpdate):
    """Update an existing call transcript"""
    row, cur = db_manager.execute_update(
        "UPDATE call_transcripts SET call_id = %s, transcript = %s WHERE id = %s RETURNING *",
        (transcript.call_id, transcript.transcript, transcript_id)
    )
    
    if row is None:
        raise HTTPException(status_code=404, detail="Call transcript not found")
    
    updated_transcript = db_manager.row_to_dict(row, cur)
    return CallTranscript(**updated_transcript)

@router.delete("/{transcript_id}", response_model=MessageResponse)
def delete_call_transcript(transcript_id: int):
    """Delete a call transcript"""
    row_count = db_manager.execute_delete("DELETE FROM call_transcripts WHERE id = %s", (transcript_id,))
    
    if row_count == 0:
        raise HTTPException(status_code=404, detail="Call transcript not found")
    
    return MessageResponse(message="Call transcript deleted successfully") 