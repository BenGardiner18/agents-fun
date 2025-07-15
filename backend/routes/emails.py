from fastapi import APIRouter, HTTPException
from typing import List
from models import Email, EmailCreate, EmailUpdate, MessageResponse
from database import db_manager

router = APIRouter(prefix="/emails", tags=["emails"])

@router.get("/", response_model=List[Email])
def get_emails():
    """Get all emails"""
    rows, cur = db_manager.execute_query("SELECT * FROM emails ORDER BY sent_at DESC")
    
    emails = []
    for row in rows:
        email = db_manager.row_to_dict(row, cur)
        emails.append(Email(**email))
    return emails

@router.get("/{email_id}", response_model=Email)
def get_email(email_id: int):
    """Get a specific email by ID"""
    row, cur = db_manager.execute_single("SELECT * FROM emails WHERE id = %s", (email_id,))
    
    if row is None:
        raise HTTPException(status_code=404, detail="Email not found")
    
    email = db_manager.row_to_dict(row, cur)
    return Email(**email)

@router.post("/", response_model=Email)
def create_email(email: EmailCreate):
    """Create a new email"""
    row, cur = db_manager.execute_insert(
        "INSERT INTO emails (contact_id, subject, body) VALUES (%s, %s, %s) RETURNING *",
        (email.contact_id, email.subject, email.body)
    )
    
    created_email = db_manager.row_to_dict(row, cur)
    return Email(**created_email)

@router.put("/{email_id}", response_model=Email)
def update_email(email_id: int, email: EmailUpdate):
    """Update an existing email"""
    row, cur = db_manager.execute_update(
        "UPDATE emails SET contact_id = %s, subject = %s, body = %s WHERE id = %s RETURNING *",
        (email.contact_id, email.subject, email.body, email_id)
    )
    
    if row is None:
        raise HTTPException(status_code=404, detail="Email not found")
    
    updated_email = db_manager.row_to_dict(row, cur)
    return Email(**updated_email)

@router.delete("/{email_id}", response_model=MessageResponse)
def delete_email(email_id: int):
    """Delete an email"""
    row_count = db_manager.execute_delete("DELETE FROM emails WHERE id = %s", (email_id,))
    
    if row_count == 0:
        raise HTTPException(status_code=404, detail="Email not found")
    
    return MessageResponse(message="Email deleted successfully") 