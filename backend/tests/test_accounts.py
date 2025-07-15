import pytest
from fastapi import status

def test_create_account(client, sample_account_data):
    """Test creating a new account"""
    response = client.post("/accounts/", json=sample_account_data)
    assert response.status_code == status.HTTP_200_OK
    
    data = response.json()
    assert data["name"] == sample_account_data["name"]
    assert data["industry"] == sample_account_data["industry"]
    assert data["plan"] == sample_account_data["plan"]
    assert data["status"] == sample_account_data["status"]
    assert "id" in data
    assert "created_at" in data

def test_get_accounts_empty(client):
    """Test getting accounts when none exist"""
    response = client.get("/accounts/")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == []

def test_get_accounts_with_data(client, sample_account_data):
    """Test getting accounts with existing data"""
    # Create an account first
    client.post("/accounts/", json=sample_account_data)
    
    response = client.get("/accounts/")
    assert response.status_code == status.HTTP_200_OK
    
    data = response.json()
    assert len(data) == 1
    assert data[0]["name"] == sample_account_data["name"]

def test_get_account_by_id(client, sample_account_data):
    """Test getting a specific account by ID"""
    # Create an account first
    create_response = client.post("/accounts/", json=sample_account_data)
    account_id = create_response.json()["id"]
    
    response = client.get(f"/accounts/{account_id}")
    assert response.status_code == status.HTTP_200_OK
    
    data = response.json()
    assert data["id"] == account_id
    assert data["name"] == sample_account_data["name"]

def test_get_account_not_found(client):
    """Test getting a non-existent account"""
    response = client.get("/accounts/999")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()["detail"] == "Account not found"

def test_update_account(client, sample_account_data):
    """Test updating an existing account"""
    # Create an account first
    create_response = client.post("/accounts/", json=sample_account_data)
    account_id = create_response.json()["id"]
    
    # Update the account
    updated_data = sample_account_data.copy()
    updated_data["name"] = "Updated Company"
    updated_data["status"] = "Inactive"
    
    response = client.put(f"/accounts/{account_id}", json=updated_data)
    assert response.status_code == status.HTTP_200_OK
    
    data = response.json()
    assert data["id"] == account_id
    assert data["name"] == "Updated Company"
    assert data["status"] == "Inactive"

def test_update_account_not_found(client, sample_account_data):
    """Test updating a non-existent account"""
    response = client.put("/accounts/999", json=sample_account_data)
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()["detail"] == "Account not found"

def test_delete_account(client, sample_account_data):
    """Test deleting an existing account"""
    # Create an account first
    create_response = client.post("/accounts/", json=sample_account_data)
    account_id = create_response.json()["id"]
    
    # Delete the account
    response = client.delete(f"/accounts/{account_id}")
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["message"] == "Account deleted successfully"
    
    # Verify it's gone
    get_response = client.get(f"/accounts/{account_id}")
    assert get_response.status_code == status.HTTP_404_NOT_FOUND

def test_delete_account_not_found(client):
    """Test deleting a non-existent account"""
    response = client.delete("/accounts/999")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()["detail"] == "Account not found"

def test_create_account_missing_required_fields(client):
    """Test creating an account without required fields"""
    response = client.post("/accounts/", json={})
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

def test_create_account_with_optional_fields_only(client):
    """Test creating an account with only required fields"""
    minimal_data = {"name": "Minimal Company"}
    response = client.post("/accounts/", json=minimal_data)
    assert response.status_code == status.HTTP_200_OK
    
    data = response.json()
    assert data["name"] == "Minimal Company"
    assert data["industry"] is None
    assert data["plan"] is None
    assert data["status"] is None 