from fastapi import APIRouter, HTTPException
from typing import List
from models import Contact, ContactCreate, ContactUpdate, MessageResponse
from database import db_manager

router = APIRouter(prefix="/contacts", tags=["contacts"])

@router.get("/", response_model=List[Contact])
def get_contacts():
    """Get all contacts"""
    rows, cur = db_manager.execute_query("SELECT * FROM contacts ORDER BY created_at DESC")
    
    contacts = []
    for row in rows:
        contact = db_manager.row_to_dict(row, cur)
        contacts.append(Contact(**contact))
    return contacts

@router.get("/{contact_id}", response_model=Contact)
def get_contact(contact_id: int):
    """Get a specific contact by ID"""
    row, cur = db_manager.execute_single("SELECT * FROM contacts WHERE id = %s", (contact_id,))
    
    if row is None:
        raise HTTPException(status_code=404, detail="Contact not found")
    
    contact = db_manager.row_to_dict(row, cur)
    return Contact(**contact)

@router.post("/", response_model=Contact)
def create_contact(contact: ContactCreate):
    """Create a new contact"""
    row, cur = db_manager.execute_insert(
        "INSERT INTO contacts (account_id, first_name, last_name, email, phone, title, role) VALUES (%s, %s, %s, %s, %s, %s, %s) RETURNING *",
        (contact.account_id, contact.first_name, contact.last_name, contact.email, contact.phone, contact.title, contact.role)
    )
    
    created_contact = db_manager.row_to_dict(row, cur)
    return Contact(**created_contact)

@router.put("/{contact_id}", response_model=Contact)
def update_contact(contact_id: int, contact: ContactUpdate):
    """Update an existing contact"""
    row, cur = db_manager.execute_update(
        "UPDATE contacts SET account_id = %s, first_name = %s, last_name = %s, email = %s, phone = %s, title = %s, role = %s WHERE id = %s RETURNING *",
        (contact.account_id, contact.first_name, contact.last_name, contact.email, contact.phone, contact.title, contact.role, contact_id)
    )
    
    if row is None:
        raise HTTPException(status_code=404, detail="Contact not found")
    
    updated_contact = db_manager.row_to_dict(row, cur)
    return Contact(**updated_contact)

@router.delete("/{contact_id}", response_model=MessageResponse)
def delete_contact(contact_id: int):
    """Delete a contact"""
    row_count = db_manager.execute_delete("DELETE FROM contacts WHERE id = %s", (contact_id,))
    
    if row_count == 0:
        raise HTTPException(status_code=404, detail="Contact not found")
    
    return MessageResponse(message="Contact deleted successfully") 