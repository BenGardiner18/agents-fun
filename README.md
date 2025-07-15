# Multi-Agent CRM System

A comprehensive system combining a multi-agent AI framework with a FastAPI CRM backend, organized in a modular structure.

## 🏗️ Project Structure

```
agents/
├── my_agents/                 # AI Agent System
│   ├── main.py               # Streamlit web app
│   ├── requirements.txt      # Agent-specific dependencies
│   ├── agents.py             # Agent definitions
│   ├── triage.py             # Triage agent logic
│   ├── runner.py             # Agent execution runner
│   ├── tools.py              # Agent tools and functions
│   └── usecases.py           # Use case definitions
├── backend/                   # CRM Backend API
│   ├── api.py                # FastAPI application
│   ├── requirements.txt      # Backend-specific dependencies
│   ├── start_backend.py      # Backend startup script
│   ├── models.py             # Pydantic models
│   ├── database.py           # Database utilities
│   ├── routes/               # API route modules
│   └── tests/                # Test suite
├── run_agents.py             # Launch agent system
├── run_backend.py            # Launch CRM backend
├── run_tests.py              # Test runner
├── requirements.txt          # Complete development dependencies
├── .env                      # Environment variables
└── README.md                 # This file
```

## 🚀 Quick Start

### Prerequisites

1. **Python 3.9+**
2. **PostgreSQL** (for CRM backend)
3. **OpenAI API Key** (for agents)

### Installation

1. **Clone and setup:**
   ```bash
   cd agents
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

2. **Environment setup:**
   ```bash
   # Create .env file with:
   echo "OPENAI_API_KEY=your_openai_api_key_here" > .env
   ```

### Running the System

#### 🤖 Agent System (Streamlit App)

```bash
# Option 1: Use the launcher script
python run_agents.py

# Option 2: Direct streamlit command
streamlit run my_agents/main.py
```

Access at: **http://localhost:8501**

#### 🏢 CRM Backend (FastAPI)

```bash
# Option 1: Use the launcher script
python run_backend.py

# Option 2: Direct backend command
python backend/start_backend.py
```

Access at: **http://localhost:8000**
- API Docs: **http://localhost:8000/docs**
- Alternative Docs: **http://localhost:8000/redoc**

#### 🧪 Run Tests

```bash
python run_tests.py
```

## 📦 Component-Specific Setup

### Agent System Only

```bash
cd my_agents
pip install -r requirements.txt
streamlit run main.py
```

### CRM Backend Only

```bash
cd backend
pip install -r requirements.txt

# Setup PostgreSQL database
docker run --name crm-postgres -e POSTGRES_PASSWORD=crmsecret -e POSTGRES_USER=crmuser -e POSTGRES_DB=crm -p 5432:5432 -d postgres:16
psql -h localhost -U crmuser -d crm -f crm_schema.sql
python seed_crm_data.py

# Start backend
python start_backend.py
```

## 🛠️ Features

### Multi-Agent System
- **Triage Agent**: Routes queries to appropriate specialized agents
- **Knowledge Agent**: Handles general knowledge questions
- **Math Agent**: Solves mathematical problems
- **Streamlit Interface**: Interactive web interface
- **Agent Visualization**: Visual representation of agent flow

### CRM Backend
- **Modular FastAPI Architecture**
- **PostgreSQL Database**
- **Full CRUD Operations** for accounts, contacts, emails, calls
- **Relationship Endpoints**
- **Comprehensive Testing**
- **Auto-generated API Documentation**

## 📋 Environment Variables

```bash
# Required
OPENAI_API_KEY=your_openai_api_key_here

# Optional (CRM Backend)
DB_HOST=localhost
DB_PORT=5432
DB_USER=crmuser
DB_PASSWORD=crmsecret
DB_NAME=crm
```

## 🔧 Development

### Adding New Agents

1. Create agent in `my_agents/agents.py`
2. Add to triage logic in `my_agents/triage.py`
3. Update use cases in `my_agents/usecases.py`

### Adding New API Endpoints

1. Create route file in `backend/routes/`
2. Add models in `backend/models.py`
3. Include router in `backend/api.py`
4. Add tests in `backend/tests/`

### Testing

- **Full test suite**: `python run_tests.py`
- **Backend only**: `python -m pytest backend/tests/`
- **Coverage report**: Generated in `htmlcov/index.html`

## 📚 API Documentation

Once running, visit:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 🤝 Contributing

1. Install development dependencies: `pip install -r requirements.txt`
2. Run tests: `python run_tests.py`
3. Follow the modular structure for new features
4. Add tests for new functionality

## 📄 License

This project is part of a multi-agent system demonstration.
