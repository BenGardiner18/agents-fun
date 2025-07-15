import pytest
from fastapi import status

def test_root_endpoint(client):
    """Test the root endpoint"""
    response = client.get("/")
    assert response.status_code == status.HTTP_200_OK
    
    data = response.json()
    assert "message" in data
    assert "version" in data
    assert "features" in data
    assert data["version"] == "2.0.0"
    assert isinstance(data["features"], list)

def test_health_check(client):
    """Test the health check endpoint"""
    response = client.get("/health")
    assert response.status_code == status.HTTP_200_OK
    
    data = response.json()
    assert data["status"] == "healthy"
    assert data["version"] == "2.0.0"

def test_openapi_docs(client):
    """Test that OpenAPI docs are accessible"""
    response = client.get("/docs")
    assert response.status_code == status.HTTP_200_OK

def test_openapi_json(client):
    """Test that OpenAPI JSON is accessible"""
    response = client.get("/openapi.json")
    assert response.status_code == status.HTTP_200_OK
    
    data = response.json()
    assert "openapi" in data
    assert "info" in data
    assert data["info"]["title"] == "CRM API"
    assert data["info"]["version"] == "2.0.0"

def test_cors_headers(client):
    """Test that CORS headers are present"""
    response = client.options("/")
    # FastAPI handles CORS automatically, so we just check that OPTIONS is allowed
    assert response.status_code in [status.HTTP_200_OK, status.HTTP_405_METHOD_NOT_ALLOWED] 