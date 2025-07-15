from fastapi import APIRouter, HTTPException
from typing import List
from models import Contact, Email, Call, CallTranscript
from database import db_manager

router = APIRouter(tags=["relationships"])

@router.get("/accounts/{account_id}/contacts", response_model=List[Contact])
def get_account_contacts(account_id: int):
    """Get all contacts for a specific account"""
    rows, cur = db_manager.execute_query(
        "SELECT * FROM contacts WHERE account_id = %s ORDER BY created_at DESC", 
        (account_id,)
    )
    
    contacts = []
    for row in rows:
        contact = db_manager.row_to_dict(row, cur)
        contacts.append(Contact(**contact))
    return contacts

@router.get("/contacts/{contact_id}/emails", response_model=List[Email])
def get_contact_emails(contact_id: int):
    """Get all emails for a specific contact"""
    rows, cur = db_manager.execute_query(
        "SELECT * FROM emails WHERE contact_id = %s ORDER BY sent_at DESC", 
        (contact_id,)
    )
    
    emails = []
    for row in rows:
        email = db_manager.row_to_dict(row, cur)
        emails.append(Email(**email))
    return emails

@router.get("/contacts/{contact_id}/calls", response_model=List[Call])
def get_contact_calls(contact_id: int):
    """Get all calls for a specific contact"""
    rows, cur = db_manager.execute_query(
        "SELECT * FROM calls WHERE contact_id = %s ORDER BY created_at DESC", 
        (contact_id,)
    )
    
    calls = []
    for row in rows:
        call = db_manager.row_to_dict(row, cur)
        calls.append(Call(**call))
    return calls

@router.get("/calls/{call_id}/transcript", response_model=CallTranscript)
def get_call_transcript_by_call(call_id: int):
    """Get the transcript for a specific call"""
    row, cur = db_manager.execute_single(
        "SELECT * FROM call_transcripts WHERE call_id = %s", 
        (call_id,)
    )
    
    if row is None:
        raise HTTPException(status_code=404, detail="Call transcript not found")
    
    transcript = db_manager.row_to_dict(row, cur)
    return CallTranscript(**transcript) 