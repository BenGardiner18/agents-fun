import pytest
from fastapi import status

def test_get_account_contacts(client, sample_account_data, sample_contact_data):
    """Test getting all contacts for an account"""
    # Create an account
    account_response = client.post("/accounts/", json=sample_account_data)
    account_id = account_response.json()["id"]
    
    # Create a contact for the account
    contact_data = sample_contact_data.copy()
    contact_data["account_id"] = account_id
    client.post("/contacts/", json=contact_data)
    
    # Get contacts for the account
    response = client.get(f"/accounts/{account_id}/contacts")
    assert response.status_code == status.HTTP_200_OK
    
    data = response.json()
    assert len(data) == 1
    assert data[0]["account_id"] == account_id
    assert data[0]["first_name"] == sample_contact_data["first_name"]

def test_get_account_contacts_empty(client, sample_account_data):
    """Test getting contacts for an account with no contacts"""
    # Create an account
    account_response = client.post("/accounts/", json=sample_account_data)
    account_id = account_response.json()["id"]
    
    # Get contacts for the account
    response = client.get(f"/accounts/{account_id}/contacts")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == []

def test_get_contact_emails(client, sample_account_data, sample_contact_data, sample_email_data):
    """Test getting all emails for a contact"""
    # Create an account
    account_response = client.post("/accounts/", json=sample_account_data)
    account_id = account_response.json()["id"]
    
    # Create a contact
    contact_data = sample_contact_data.copy()
    contact_data["account_id"] = account_id
    contact_response = client.post("/contacts/", json=contact_data)
    contact_id = contact_response.json()["id"]
    
    # Create an email for the contact
    email_data = sample_email_data.copy()
    email_data["contact_id"] = contact_id
    client.post("/emails/", json=email_data)
    
    # Get emails for the contact
    response = client.get(f"/contacts/{contact_id}/emails")
    assert response.status_code == status.HTTP_200_OK
    
    data = response.json()
    assert len(data) == 1
    assert data[0]["contact_id"] == contact_id
    assert data[0]["subject"] == sample_email_data["subject"]

def test_get_contact_calls(client, sample_account_data, sample_contact_data, sample_call_data):
    """Test getting all calls for a contact"""
    # Create an account
    account_response = client.post("/accounts/", json=sample_account_data)
    account_id = account_response.json()["id"]
    
    # Create a contact
    contact_data = sample_contact_data.copy()
    contact_data["account_id"] = account_id
    contact_response = client.post("/contacts/", json=contact_data)
    contact_id = contact_response.json()["id"]
    
    # Create a call for the contact
    call_data = sample_call_data.copy()
    call_data["contact_id"] = contact_id
    client.post("/calls/", json=call_data)
    
    # Get calls for the contact
    response = client.get(f"/contacts/{contact_id}/calls")
    assert response.status_code == status.HTTP_200_OK
    
    data = response.json()
    assert len(data) == 1
    assert data[0]["contact_id"] == contact_id
    assert data[0]["call_type"] == sample_call_data["call_type"]

def test_get_call_transcript(client, sample_account_data, sample_contact_data, sample_call_data, sample_transcript_data):
    """Test getting transcript for a call"""
    # Create an account
    account_response = client.post("/accounts/", json=sample_account_data)
    account_id = account_response.json()["id"]
    
    # Create a contact
    contact_data = sample_contact_data.copy()
    contact_data["account_id"] = account_id
    contact_response = client.post("/contacts/", json=contact_data)
    contact_id = contact_response.json()["id"]
    
    # Create a call
    call_data = sample_call_data.copy()
    call_data["contact_id"] = contact_id
    call_response = client.post("/calls/", json=call_data)
    call_id = call_response.json()["id"]
    
    # Create a transcript for the call
    transcript_data = sample_transcript_data.copy()
    transcript_data["call_id"] = call_id
    client.post("/call-transcripts/", json=transcript_data)
    
    # Get transcript for the call
    response = client.get(f"/calls/{call_id}/transcript")
    assert response.status_code == status.HTTP_200_OK
    
    data = response.json()
    assert data["call_id"] == call_id
    assert data["transcript"] == sample_transcript_data["transcript"]

def test_get_call_transcript_not_found(client, sample_account_data, sample_contact_data, sample_call_data):
    """Test getting transcript for a call that doesn't have one"""
    # Create an account
    account_response = client.post("/accounts/", json=sample_account_data)
    account_id = account_response.json()["id"]
    
    # Create a contact
    contact_data = sample_contact_data.copy()
    contact_data["account_id"] = account_id
    contact_response = client.post("/contacts/", json=contact_data)
    contact_id = contact_response.json()["id"]
    
    # Create a call without transcript
    call_data = sample_call_data.copy()
    call_data["contact_id"] = contact_id
    call_response = client.post("/calls/", json=call_data)
    call_id = call_response.json()["id"]
    
    # Try to get transcript for the call
    response = client.get(f"/calls/{call_id}/transcript")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()["detail"] == "Call transcript not found"

def test_cascade_delete_account_contacts(client, sample_account_data, sample_contact_data):
    """Test that deleting an account also deletes its contacts"""
    # Create an account
    account_response = client.post("/accounts/", json=sample_account_data)
    account_id = account_response.json()["id"]
    
    # Create a contact for the account
    contact_data = sample_contact_data.copy()
    contact_data["account_id"] = account_id
    contact_response = client.post("/contacts/", json=contact_data)
    contact_id = contact_response.json()["id"]
    
    # Delete the account
    client.delete(f"/accounts/{account_id}")
    
    # Verify the contact is also deleted
    response = client.get(f"/contacts/{contact_id}")
    assert response.status_code == status.HTTP_404_NOT_FOUND 