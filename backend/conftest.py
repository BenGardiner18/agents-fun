import pytest
import psycopg2
from fastapi.testclient import TestClient
from api import app
from database import DatabaseManager
import os

# Test database configuration
TEST_DB_CONFIG = {
    "host": os.getenv("TEST_DB_HOST", "localhost"),
    "port": int(os.getenv("TEST_DB_PORT", "5432")),
    "user": os.getenv("TEST_DB_USER", "crmuser"),
    "password": os.getenv("TEST_DB_PASSWORD", "crmsecret"),
    "dbname": os.getenv("TEST_DB_NAME", "crm_test")
}

@pytest.fixture(scope="session")
def test_db():
    """Create test database and tables"""
    # Create test database if it doesn't exist
    admin_config = TEST_DB_CONFIG.copy()
    admin_config["dbname"] = "postgres"
    
    conn = psycopg2.connect(**admin_config)
    conn.autocommit = True
    cur = conn.cursor()
    
    # Drop and create test database
    cur.execute(f"DROP DATABASE IF EXISTS {TEST_DB_CONFIG['dbname']}")
    cur.execute(f"CREATE DATABASE {TEST_DB_CONFIG['dbname']}")
    
    conn.close()
    
    # Connect to test database and create tables
    test_conn = psycopg2.connect(**TEST_DB_CONFIG)
    test_conn.autocommit = True
    test_cur = test_conn.cursor()
    
    # Create tables
    test_cur.execute("""
        CREATE TABLE accounts (
            id SERIAL PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            industry VARCHAR(100),
            plan VARCHAR(50),
            status VARCHAR(50),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    test_cur.execute("""
        CREATE TABLE contacts (
            id SERIAL PRIMARY KEY,
            account_id INTEGER REFERENCES accounts(id) ON DELETE CASCADE,
            first_name VARCHAR(100) NOT NULL,
            last_name VARCHAR(100) NOT NULL,
            email VARCHAR(255) UNIQUE NOT NULL,
            phone VARCHAR(50),
            title VARCHAR(100),
            role VARCHAR(100),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    test_cur.execute("""
        CREATE TABLE emails (
            id SERIAL PRIMARY KEY,
            contact_id INTEGER REFERENCES contacts(id) ON DELETE CASCADE,
            subject VARCHAR(255) NOT NULL,
            body TEXT,
            sent_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    test_cur.execute("""
        CREATE TABLE calls (
            id SERIAL PRIMARY KEY,
            contact_id INTEGER REFERENCES contacts(id) ON DELETE CASCADE,
            call_type VARCHAR(50) NOT NULL,
            duration INTEGER,
            outcome VARCHAR(255),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    test_cur.execute("""
        CREATE TABLE call_transcripts (
            id SERIAL PRIMARY KEY,
            call_id INTEGER REFERENCES calls(id) ON DELETE CASCADE,
            transcript TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    test_conn.close()
    
    yield TEST_DB_CONFIG
    
    # Cleanup: drop test database
    conn = psycopg2.connect(**admin_config)
    conn.autocommit = True
    cur = conn.cursor()
    cur.execute(f"DROP DATABASE IF EXISTS {TEST_DB_CONFIG['dbname']}")
    conn.close()

@pytest.fixture
def test_db_manager(test_db):
    """Create a test database manager"""
    return DatabaseManager(test_db)

@pytest.fixture
def client(test_db_manager):
    """Create test client with test database"""
    # Override the database manager in the app
    from database import db_manager
    original_config = db_manager.config
    db_manager.config = test_db_manager.config
    
    with TestClient(app) as test_client:
        yield test_client
    
    # Restore original config
    db_manager.config = original_config

@pytest.fixture
def sample_account_data():
    """Sample account data for testing"""
    return {
        "name": "Test Company",
        "industry": "Software",
        "plan": "Enterprise",
        "status": "Active"
    }

@pytest.fixture
def sample_contact_data():
    """Sample contact data for testing"""
    return {
        "account_id": 1,
        "first_name": "John",
        "last_name": "Doe",
        "email": "john.doe@test.com",
        "phone": "555-1234",
        "title": "CEO",
        "role": "Decision Maker"
    }

@pytest.fixture
def sample_email_data():
    """Sample email data for testing"""
    return {
        "contact_id": 1,
        "subject": "Test Email",
        "body": "This is a test email body"
    }

@pytest.fixture
def sample_call_data():
    """Sample call data for testing"""
    return {
        "contact_id": 1,
        "call_type": "discovery",
        "duration": 30,
        "outcome": "Interested"
    }

@pytest.fixture
def sample_transcript_data():
    """Sample transcript data for testing"""
    return {
        "call_id": 1,
        "transcript": "This is a sample call transcript"
    }

@pytest.fixture(autouse=True)
def clean_db(test_db_manager):
    """Clean database before each test"""
    yield
    # Clean up after each test
    with test_db_manager.get_cursor() as cur:
        cur.execute("TRUNCATE call_transcripts, calls, emails, contacts, accounts RESTART IDENTITY CASCADE") 