# Backend: CRM PostgreSQL Setup & FastAPI Server v2.0

This folder contains a **modular, well-tested CRM API** using PostgreSQL and FastAPI with a clean architecture.

## 🏗️ Project Structure

```
backend/
├── api.py                 # Main FastAPI application
├── models.py              # Pydantic models for all entities
├── database.py            # Database connection and utilities
├── conftest.py            # Test configuration and fixtures
├── pytest.ini            # Pytest configuration
├── run_tests.py           # Test runner script
├── routes/                # Modular route definitions
│   ├── __init__.py
│   ├── accounts.py        # Account CRUD operations
│   ├── contacts.py        # Contact CRUD operations
│   ├── emails.py          # Email CRUD operations
│   ├── calls.py           # Call CRUD operations
│   ├── transcripts.py     # Transcript CRUD operations
│   └── relationships.py   # Relationship endpoints
├── tests/                 # Comprehensive test suite
│   ├── __init__.py
│   ├── test_accounts.py   # Account endpoint tests
│   ├── test_relationships.py  # Relationship tests
│   └── test_api.py        # Main API tests
├── crm_schema.sql         # Database schema
└── seed_crm_data.py       # Fake data generator
```

## 🚀 Quick Start

### 1. Start PostgreSQL
```bash
docker run --name crm-postgres -e POSTGRES_PASSWORD=crmsecret -e POSTGRES_USER=crmuser -e POSTGRES_DB=crm -p 5432:5432 -d postgres:16
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Create Database Schema
```bash
psql -h localhost -U crmuser -d crm -f backend/crm_schema.sql
```

### 4. Seed with Fake Data
```bash
python backend/seed_crm_data.py
```

### 5. Start the FastAPI Server
```bash
# Run from the parent directory (agents/)
python start_backend.py
```

**Note**: The server must be started from the parent directory to properly resolve package imports. The old `backend/start_api.py` script has been replaced with `start_backend.py` in the parent directory.

## 🧪 Testing

### Run All Tests
```bash
# Using the test runner (run from parent directory)
python run_tests.py

# Or directly with pytest (run from parent directory)
python -m pytest backend/tests/
```

### Run Specific Tests
```bash
# Test a specific file
python backend/run_tests.py tests/test_accounts.py

# Test a specific function
python backend/run_tests.py tests/test_accounts.py::test_create_account
```

### Test Coverage
Tests automatically generate coverage reports:
- **Terminal**: Shows coverage percentages
- **HTML**: Detailed report in `backend/htmlcov/index.html`

## 📚 API Endpoints

### Core Entities
- **Accounts**: `GET|POST|PUT|DELETE /accounts/`
- **Contacts**: `GET|POST|PUT|DELETE /contacts/`
- **Emails**: `GET|POST|PUT|DELETE /emails/`
- **Calls**: `GET|POST|PUT|DELETE /calls/`
- **Transcripts**: `GET|POST|PUT|DELETE /call-transcripts/`

### Relationships
- `GET /accounts/{id}/contacts` - Get all contacts for an account
- `GET /contacts/{id}/emails` - Get all emails for a contact
- `GET /contacts/{id}/calls` - Get all calls for a contact
- `GET /calls/{id}/transcript` - Get transcript for a call

### System
- `GET /` - API information and version
- `GET /health` - Health check endpoint

## 📖 API Documentation

Once the server is running, visit:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 🔧 Configuration

### Environment Variables
```bash
# Database Configuration
DB_HOST=localhost
DB_PORT=5432
DB_USER=crmuser
DB_PASSWORD=crmsecret
DB_NAME=crm

# Test Database (optional)
TEST_DB_HOST=localhost
TEST_DB_PORT=5432
TEST_DB_USER=crmuser
TEST_DB_PASSWORD=crmsecret
TEST_DB_NAME=crm_test
```

## 🏛️ Architecture

### Modular Design
- **Separation of Concerns**: Models, routes, and database logic are separated
- **Testability**: Each module can be tested independently
- **Maintainability**: Easy to add new features or modify existing ones
- **Scalability**: Clean structure supports future growth

### Database Management
- **Connection Pooling**: Efficient database connections
- **Context Managers**: Automatic resource cleanup
- **Environment Config**: Easy configuration management

### Testing Strategy
- **Unit Tests**: Test individual functions and endpoints
- **Integration Tests**: Test full request/response cycles
- **Relationship Tests**: Test entity relationships and cascading
- **Fixtures**: Reusable test data and setup
- **Coverage**: Comprehensive code coverage reporting

## 🔍 Database Queries

You can also query the database directly:
```bash
psql -h localhost -U crmuser -d crm
```

Example queries:
```sql
-- List all accounts with their contacts
SELECT a.name, c.first_name, c.last_name, c.email
FROM accounts a
LEFT JOIN contacts c ON a.id = c.account_id
ORDER BY a.name;

-- Get call statistics by type
SELECT call_type, COUNT(*) as count, AVG(duration) as avg_duration
FROM calls
GROUP BY call_type
ORDER BY count DESC;

-- Find contacts with recent activity
SELECT c.first_name, c.last_name, 
       COUNT(DISTINCT e.id) as email_count,
       COUNT(DISTINCT ca.id) as call_count
FROM contacts c
LEFT JOIN emails e ON c.id = e.contact_id
LEFT JOIN calls ca ON c.id = ca.contact_id
GROUP BY c.id, c.first_name, c.last_name
ORDER BY email_count + call_count DESC;
```

## 🚦 Development Workflow

1. **Make Changes**: Edit code in the appropriate module
2. **Run Tests**: `python backend/run_tests.py`
3. **Check Coverage**: Open `backend/htmlcov/index.html`
4. **Test API**: Use `/docs` endpoint to test changes
5. **Commit**: Only commit when tests pass

## 🎯 Features

✅ **Modular Architecture** - Clean separation of concerns  
✅ **Comprehensive Testing** - Unit, integration, and relationship tests  
✅ **Environment Configuration** - Easy setup with environment variables  
✅ **Full CRUD Operations** - Complete Create, Read, Update, Delete support  
✅ **Relationship Endpoints** - Navigate between related entities  
✅ **Auto-generated Documentation** - Swagger UI and ReDoc  
✅ **Database Connection Management** - Efficient connection handling  
✅ **Test Coverage Reporting** - HTML and terminal coverage reports  
✅ **Type Safety** - Pydantic models for request/response validation  
✅ **CORS Support** - Ready for frontend integration  
